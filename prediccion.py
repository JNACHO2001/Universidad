"""Funciones para cargar el modelo y clasificar textos."""
# Este archivo se encarga de dos cosas:
# 1. Cargar desde disco el modelo que fue entrenado y guardado.
# 2. Usar ese modelo para predecir la categoría de un texto nuevo.

from pathlib import Path
# Importa Path para manejar rutas de archivos de forma compatible
# con Windows, Mac y Linux (evita problemas con "/" vs "\").

import joblib
# Librería para cargar objetos de Python desde archivos .pkl en disco.
# Es más eficiente que pickle para objetos grandes como modelos de ML.


BASE_DIR = Path(__file__).resolve().parent
# __file__ = ruta absoluta de este archivo (prediccion.py).
# .resolve() convierte la ruta relativa en absoluta.
# .parent sube un nivel → llega a la carpeta raíz del proyecto (Universidad/).
# BUG CORREGIDO: antes era .parent.parent, que subía DOS niveles (demasiado).

MODEL_FILE = BASE_DIR / "model" / "clasificador.pkl"
# Construye la ruta completa al archivo del modelo guardado.
# El operador "/" de Path concatena directorios de forma segura.
# Resultado: .../Universidad/model/clasificador.pkl


def cargar_modelo():  # noqa: D401
    """Carga el modelo entrenado desde disco."""
    if not MODEL_FILE.exists():
        # Verifica si el archivo .pkl existe antes de intentar abrirlo.
        raise FileNotFoundError(
            "No existe el modelo entrenado. Primero selecciona la opción de entrenar."
        )
        # Si no existe, lanza un error con un mensaje claro para el usuario.

    return joblib.load(MODEL_FILE)
    # Deserializa (carga) el pipeline completo desde el archivo .pkl.
    # Devuelve el pipeline con TF-IDF + Naive Bayes listos para predecir.


def clasificar_texto(texto):  # noqa: D401
    """Clasifica un texto y devuelve la etiqueta y las probabilidades."""
    modelo = cargar_modelo()
    # Carga el pipeline entrenado desde disco llamando a la función de arriba.

    etiqueta = modelo.predict([texto])[0]
    # modelo.predict() recibe una lista de textos y devuelve una lista de etiquetas.
    # [texto] → envuelve el string en una lista (scikit-learn lo requiere así).
    # [0] → extrae el primer (y único) elemento de la lista de resultados.
    # Resultado: el nombre de la categoría predicha (ej. "contrato").

    # Probabilidades por clase.
    probabilidades = modelo.predict_proba([texto])[0]
    # predict_proba() devuelve la probabilidad de pertenecer a CADA clase.
    # [texto] → igual que arriba, debe ser una lista.
    # [0] → extrae el array de probabilidades del primer texto.
    # Resultado: array como [0.05, 0.80, 0.10, 0.05] (una prob. por clase).

    clases = modelo.classes_
    # modelo.classes_ es un atributo del clasificador entrenado.
    # Contiene los nombres de todas las categorías en el mismo orden
    # que las probabilidades de predict_proba().
    # Ejemplo: ["contrato", "factura", "informe", "memo"]

    resultados = sorted(
        zip(clases, probabilidades),
        # zip() combina las dos listas elemento a elemento:
        # [("contrato", 0.05), ("factura", 0.80), ("informe", 0.10), ...]
        key=lambda x: x[1],
        # Ordena por el segundo elemento de cada tupla (la probabilidad).
        reverse=True,
        # reverse=True → de mayor a menor probabilidad.
        # Así la clase más probable aparece primero en la lista.
    )

    return etiqueta, resultados
    # Devuelve dos valores a quien llame esta función:
    # - etiqueta: el nombre de la clase ganadora (string).
    # - resultados: lista de tuplas (clase, probabilidad) ordenada de mayor a menor.