"""Funciones para cargar el modelo y clasificar textos."""

from pathlib import Path

import joblib


BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_FILE = BASE_DIR / "model" / "clasificador.pkl"



def cargar_modelo():  # noqa: D401
    """Carga el modelo entrenado desde disco."""
    if not MODEL_FILE.exists():
        raise FileNotFoundError(
            "No existe el modelo entrenado. Primero selecciona la opción de entrenar."
        )

    return joblib.load(MODEL_FILE)



def clasificar_texto(texto):  # noqa: D401
    """Clasifica un texto y devuelve la etiqueta y las probabilidades."""
    modelo = cargar_modelo()

    etiqueta = modelo.predict([texto])[0]

    # Probabilidades por clase.
    probabilidades = modelo.predict_proba([texto])[0]
    clases = modelo.classes_

    resultados = sorted(
        zip(clases, probabilidades),
        key=lambda x: x[1],
        reverse=True,
    )

    return etiqueta, resultados