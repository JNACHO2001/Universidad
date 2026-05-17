"""
Entrena un modelo de clasificación de texto en español.

Pipeline:
1. TF-IDF: Convierte texto en vectores numéricos.
2. Multinomial Naive Bayes: Algoritmo de clasificación eficiente para texto.
"""
# Este archivo contiene toda la lógica para cargar datos, crear el modelo,
# entrenarlo, evaluarlo y guardarlo en disco para usarlo después.


from pathlib import Path
# Importa Path para manejar rutas de archivos de forma compatible
# con Windows, Mac y Linux (evita problemas con "/" vs "\").

import joblib
# Librería para guardar y cargar objetos de Python en disco.
# Es más eficiente que pickle para objetos grandes como modelos de ML.

import pandas as pd
# Pandas es la librería estándar para manejar datos tabulares (como CSV).
# Se abrevia como "pd" por convención.

from sklearn.feature_extraction.text import TfidfVectorizer
# TF-IDF (Term Frequency - Inverse Document Frequency):
# Convierte textos en vectores numéricos.
# Palabras que aparecen mucho en UN documento pero poco en el resto
# reciben un peso mayor (son más "importantes" para ese documento).

from sklearn.metrics import accuracy_score, classification_report
# accuracy_score: calcula el porcentaje de predicciones correctas.
# classification_report: genera una tabla con precisión, recall y F1 por clase.

from sklearn.model_selection import train_test_split
# Divide automáticamente los datos en dos grupos:
# - Entrenamiento (70%): para que el modelo aprenda.
# - Prueba (30%): para evaluar qué tan bien generalizó.

from sklearn.naive_bayes import MultinomialNB
# Multinomial Naive Bayes: algoritmo de clasificación muy eficiente para texto.
# Funciona bien con conteos de palabras y vectores TF-IDF.
# "Naive" porque asume que las palabras son independientes entre sí.

from sklearn.pipeline import Pipeline
# Pipeline encadena pasos de procesamiento.
# Aquí: primero transforma el texto con TF-IDF, luego clasifica con Naive Bayes.
# Ventaja: en predicción, basta llamar a pipeline.predict() y hace todo automáticamente.

# --- Rutas del proyecto ---
BASE_DIR = Path(__file__).resolve().parent
# __file__ = ruta absoluta de este archivo (entrenamiento.py).
# .resolve() convierte la ruta relativa en absoluta.
# .parent sube un nivel → llega a la carpeta raíz del proyecto (Universidad/).
# BUG CORREGIDO: antes era .parent.parent, que subía DOS niveles (demasiado).

DATA_FILE = BASE_DIR / "datos" / "documentos.csv"
# Construye la ruta al archivo CSV con los datos de entrenamiento.
# El operador "/" de Path concatena directorios de forma segura entre sistemas operativos.
# Resultado: .../Universidad/datos/documentos.csv

MODEL_DIR = BASE_DIR / "model"
# Carpeta donde se guardará el modelo entrenado.
# Resultado: .../Universidad/model/

MODEL_FILE = MODEL_DIR / "clasificador.pkl"
# Ruta completa del archivo del modelo guardado.
# .pkl es la extensión estándar para archivos serializados con joblib/pickle.


def cargar_datos():  # noqa: D401
    """Carga el dataset desde CSV."""
    if not DATA_FILE.exists():
        # Verifica si el archivo CSV existe antes de intentar abrirlo.
        raise FileNotFoundError(f"No se encontró el archivo: {DATA_FILE}")
        # Si no existe, lanza un error descriptivo con la ruta exacta que buscó.

    df = pd.read_csv(DATA_FILE)
    # Lee el archivo CSV y lo convierte en un DataFrame de pandas.
    # Un DataFrame es como una tabla de Excel en Python.

    if "texto" not in df.columns or "etiqueta" not in df.columns:
        # Verifica que el CSV tenga exactamente las columnas requeridas:
        # - "texto": el contenido del documento.
        # - "etiqueta": la categoría/clase del documento.
        raise ValueError("El CSV debe tener las columnas 'texto' y 'etiqueta'.")
        # Si faltan columnas, lanza un error antes de continuar.

    return df
    # Devuelve el DataFrame con todos los datos listos para usar.


def crear_pipeline():  # noqa: D401
    """Crea el pipeline de procesamiento y clasificación."""
    return Pipeline([
        # Pipeline recibe una lista de pasos en orden. Cada paso es una tupla (nombre, objeto).
        (
            "tfidf",
            # Nombre interno del paso (puede ser cualquier string).
            TfidfVectorizer(
                lowercase=True,
                # Convierte todo el texto a minúsculas antes de procesar.
                # Así "Contrato" y "contrato" se tratan igual.

                stop_words=None,
                # No elimina palabras comunes (como "el", "la", "de").
                # Para español sería útil agregar stopwords en el futuro.

                ngram_range=(1, 2),
                # Analiza palabras individuales (unigramas) Y pares de palabras (bigramas).
                # Ejemplo: "contrato laboral" se analiza como unidad además de "contrato" y "laboral" por separado.
                # Esto mejora la precisión al capturar frases importantes.
            ),
        ),
        ("classifier", MultinomialNB()),
        # Segundo paso: el clasificador Naive Bayes.
        # Recibe los vectores TF-IDF del paso anterior y aprende a clasificarlos.
    ])


def entrenar_modelo():  # noqa: D401
    """Entrena, evalúa y guarda el modelo."""
    print(" Cargando datos...")
    df = cargar_datos()
    # Llama a la función de arriba para obtener el DataFrame con los datos.

    X = df["texto"]
    # X = las características (features): los textos de los documentos.
    # Convencionalmente se llama X en Machine Learning.

    y = df["etiqueta"]
    # y = las etiquetas (labels): las categorías de cada documento.
    # Convencionalmente se llama y en Machine Learning (lo que queremos predecir).

    # Divide los datos en entrenamiento y prueba.
    X_train, X_test, y_train, y_test = train_test_split(
        X,           # Textos de entrada.
        y,           # Etiquetas correspondientes.
        test_size=0.3,
        # El 30% de los datos se reserva para prueba, el 70% para entrenar.
        # Con 40 ejemplos y 2 clases esto da ~12 muestras de prueba → suficiente.
        random_state=42,
        # Semilla para el generador de números aleatorios.
        # Con el mismo valor, la división siempre será igual → resultados reproducibles.
        stratify=y,
        # Garantiza que ambas clases (relevante / no_relevante) estén representadas
        # proporcionalmente en entrenamiento y prueba.
        # Reactivado porque ahora el dataset tiene suficientes ejemplos por clase.
    )

    print(" Creando pipeline...")
    pipeline = crear_pipeline()
    # Crea el pipeline con TF-IDF + Naive Bayes listos para usar.

    print(" Entrenando modelo...")
    pipeline.fit(X_train, y_train)
    # .fit() es el método de entrenamiento en scikit-learn.
    # Primero transforma X_train con TF-IDF, luego entrena Naive Bayes con los vectores.

    print(" Evaluando modelo...")
    y_pred = pipeline.predict(X_test)
    # .predict() usa el modelo entrenado para predecir las etiquetas de los datos de prueba.
    # y_pred contiene las predicciones; y_test tiene las etiquetas reales.

    accuracy = accuracy_score(y_test, y_pred)
    # Compara las predicciones (y_pred) con las reales (y_test).
    # Devuelve un número entre 0 y 1 (ej: 0.85 = 85% de aciertos).

    print(f"\n Accuracy: {accuracy:.2%}\n")
    # :.2% formatea el decimal como porcentaje con 2 cifras decimales.
    # Ejemplo: 0.8523 → "85.23%"

    print(" Reporte de clasificación:")
    print(classification_report(y_test, y_pred, zero_division=0))
    # Imprime una tabla detallada con métricas por cada categoría:
    # - Precision: de los que predije como X, ¿cuántos realmente son X?
    # - Recall: de todos los que son X, ¿cuántos identifiqué correctamente?
    # - F1-score: promedio armónico entre precision y recall.
    # zero_division=0: si una clase no tiene predicciones, muestra 0 en vez de advertencia.

    print(" Guardando modelo...")
    MODEL_DIR.mkdir(exist_ok=True)
    # Crea la carpeta "model/" si no existe.
    # exist_ok=True evita un error si la carpeta ya existía.

    joblib.dump(pipeline, MODEL_FILE)
    # Serializa (guarda) el pipeline completo en un archivo .pkl en disco.
    # Incluye tanto el vectorizador TF-IDF como el clasificador entrenado.

    print(f" Modelo guardado en: {MODEL_FILE}")
    # Confirma al usuario dónde quedó guardado el modelo.


if __name__ == "__main__":  # pragma: no cover
    # Esta condición se cumple solo cuando se ejecuta este archivo directamente:
    # "python entrenamiento.py"
    # Si otro archivo importa entrenar_modelo(), este bloque NO se ejecuta.
    # "pragma: no cover" le dice a las herramientas de cobertura que ignoren esta línea.
    entrenar_modelo()
    # Ejecuta directamente el entrenamiento sin pasar por el menú de main.py.