"""
Entrena un modelo de clasificación de texto en español.

Pipeline:
1. TF-IDF: Convierte texto en vectores numéricos.
2. Multinomial Naive Bayes: Algoritmo de clasificación eficiente para texto.
"""


from pathlib import Path

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

# Rutas del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "documentos.csv"
MODEL_DIR = BASE_DIR / "model"
MODEL_FILE = MODEL_DIR / "clasificador.pkl"

def cargar_datos():  # noqa: D401
    """Carga el dataset desde CSV."""
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {DATA_FILE}")

    df = pd.read_csv(DATA_FILE)

    if "texto" not in df.columns or "etiqueta" not in df.columns:
        raise ValueError("El CSV debe tener las columnas 'texto' y 'etiqueta'.")

    return df


def crear_pipeline():  # noqa: D401
    """Crea el pipeline de procesamiento y clasificación."""
    return Pipeline([
        (
            "tfidf",
            TfidfVectorizer(
                lowercase=True,
                stop_words=None,  # Para español podrías agregar stopwords más adelante.
                ngram_range=(1, 2),  # Usa palabras individuales y pares de palabras.
            ),
        ),
        ("classifier", MultinomialNB()),
    ])


def entrenar_modelo():  # noqa: D401
    """Entrena, evalúa y guarda el modelo."""
    print(" Cargando datos...")
    df = cargar_datos()

    X = df["texto"]
    y = df["etiqueta"]

    # Divide los datos en entrenamiento y prueba.
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.3,
        random_state=42,
        stratify=y,
    )


    print(" Creando pipeline...")
    pipeline = crear_pipeline()

    print(" Entrenando modelo...")
    pipeline.fit(X_train, y_train)

    print(" Evaluando modelo...")
    y_pred = pipeline.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    print(f"\n Accuracy: {accuracy:.2%}\n")

    print(" Reporte de clasificación:")
    print(classification_report(y_test, y_pred, zero_division=0))

    print(" Guardando modelo...")
    MODEL_DIR.mkdir(exist_ok=True)
    joblib.dump(pipeline, MODEL_FILE)

    print(f" Modelo guardado en: {MODEL_FILE}")


if __name__ == "__main__":  # pragma: no cover
    entrenar_modelo()