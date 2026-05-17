# DOLMEN · Clasificador de Textos de Alumbrado Público

> Sistema de clasificación automática de textos basado en Machine Learning que determina si un documento es **relevante o no relevante** para la empresa **DOLMEN**, prestadora de servicios de alumbrado público.

---

## 📋 Descripción

Este proyecto implementa un modelo de clasificación de texto en español utilizando un pipeline de:

1. **TF-IDF** (Term Frequency - Inverse Document Frequency) para convertir los textos en vectores numéricos.
2. **Multinomial Naive Bayes** como algoritmo de clasificación eficiente para texto.

El modelo aprende a reconocer si un texto pertenece al ámbito operacional de DOLMEN (contratos, facturas, informes técnicos, mantenimientos de luminarias, etc.) o si es un texto ajeno a la empresa.

---

## 🗂️ Estructura del proyecto

```
Universidad/
│
├── main.py              # Punto de entrada: menú interactivo por consola
├── entrenamiento.py     # Lógica de entrenamiento, evaluación y guardado del modelo
├── prediccion.py        # Carga del modelo y clasificación de textos nuevos
├── requirements.txt     # Dependencias del proyecto
│
├── datos/
│   └── documentos.csv   # Dataset de ejemplos etiquetados (relevante / no_relevante)
│
└── model/               # Carpeta generada automáticamente al entrenar
    └── clasificador.pkl # Modelo entrenado y serializado
```

---

## ⚙️ Requisitos

- Python 3.9 o superior
- Las dependencias listadas en `requirements.txt`

### Instalación de dependencias

```bash
pip install -r requirements.txt
```

**Dependencias:**

| Librería | Versión mínima | Uso |
|---|---|---|
| `pandas` | 2.0.0 | Lectura y manejo del dataset CSV |
| `scikit-learn` | 1.4.0 | TF-IDF, Naive Bayes, métricas |
| `joblib` | 1.3.0 | Guardar y cargar el modelo entrenado |

---

## 🚀 Uso

Ejecuta el programa principal desde la raíz del proyecto:

```bash
python main.py
```

Se mostrará el siguiente menú:

```
==================================================
 DOLMEN • CLASIFICADOR DE TEXTOS DE ALUMBRADO PÚBLICO
==================================================
1. Entrenar modelo
2. Clasificar texto
3. Salir
==================================================
```

### Opción 1 — Entrenar modelo

Lee el dataset `datos/documentos.csv`, entrena el modelo y lo guarda en `model/clasificador.pkl`. Se muestran métricas de evaluación (accuracy, precision, recall, F1).

> ⚠️ **Debe ejecutarse al menos una vez antes de clasificar.**

### Opción 2 — Clasificar texto

Solicita al usuario que ingrese un texto libre. El modelo predice si es:

- ✅ `relevante` — El texto está relacionado con DOLMEN y el alumbrado público.
- ❌ `no_relevante` — El texto no tiene relación con la empresa.

También muestra el porcentaje de confianza de cada clase.

**Ejemplo de salida:**

```
 Ingrese el texto del documento:
> DOLMEN realizará mantenimiento de luminarias en el sector norte

 Tipo de documento detectado: relevante

 Probabilidades:
- relevante      92.45%
- no_relevante    7.55%
```

---

## 📊 Dataset

El archivo `datos/documentos.csv` contiene **40 ejemplos** etiquetados:

| Clase | Cantidad | Ejemplos de contenido |
|---|---|---|
| `relevante` | 20 | Contratos con DOLMEN, facturas de luminarias, informes técnicos, mantenimientos, instalaciones de postes LED |
| `no_relevante` | 20 | Textos de salud, educación, acueducto, deportes, inmuebles, aseo urbano |

### Formato del CSV

```csv
texto,etiqueta
"DOLMEN realizará el mantenimiento preventivo de luminarias...",relevante
"El restaurante El Rincón ofrece platos típicos...",no_relevante
```

Para **agregar más ejemplos**, simplemente añade filas al CSV con el mismo formato y reentrena el modelo (opción 1).

---

## 🧠 Cómo funciona el modelo

```
Texto de entrada
      │
      ▼
┌─────────────┐
│   TF-IDF    │  Convierte palabras en vectores numéricos.
│ Vectorizer  │  Palabras clave del alumbrado tienen mayor peso.
└─────────────┘
      │
      ▼
┌─────────────┐
│  Naive      │  Calcula la probabilidad de que el texto
│  Bayes      │  pertenezca a cada clase.
└─────────────┘
      │
      ▼
 relevante / no_relevante  +  % de confianza
```

---

## 📈 Métricas de evaluación

Al entrenar, el sistema muestra automáticamente:

- **Accuracy**: porcentaje total de predicciones correctas.
- **Precision**: de los textos clasificados como relevantes, ¿cuántos realmente lo son?
- **Recall**: de todos los textos relevantes, ¿cuántos fueron correctamente identificados?
- **F1-score**: balance entre precision y recall.

---

## 👨‍💼 Contexto empresarial

**DOLMEN** es una empresa prestadora de servicios de **alumbrado público** que gestiona:

- Instalación y mantenimiento de luminarias y postes
- Modernización a tecnología LED de bajo consumo
- Monitoreo remoto mediante sistemas SCADA
- Operación de alumbrado en zonas urbanas, viales y rurales
- Generación de informes técnicos y energéticos para municipios

Este clasificador permite **filtrar automáticamente** documentos y textos que son pertinentes para la operación de la empresa, optimizando la gestión documental.

---

## 🛠️ Posibles mejoras futuras

- [ ] Agregar más ejemplos al dataset (mínimo 50 por clase para mayor precisión)
- [ ] Incorporar stopwords en español para mejorar el vectorizador TF-IDF
- [ ] Implementar interfaz web con Flask o FastAPI
- [ ] Exportar reportes en PDF con los resultados de clasificación
- [ ] Agregar soporte para clasificar archivos `.txt` y `.pdf` directamente
