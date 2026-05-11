

## Tabla de contenido

- [Descripción general](#descripción-general)
- [Arquitectura del proyecto](#arquitectura-del-proyecto)
- [Tecnologías utilizadas](#tecnologías-utilizadas)
- [Estructura de carpetas](#estructura-de-carpetas)
- [Requisitos previos](#requisitos-previos)
- [Instalación y configuración](#instalación-y-configuración)
  - [Backend](#backend)
  - [Frontend](#frontend)
- [Uso](#uso)
- [API Reference](#api-reference)
- [Modelo de datos](#modelo-de-datos)
- [Variables de entorno y configuración](#variables-de-entorno-y-configuración)


---

## Descripción general

**User Central** es una aplicación CRUD completa que permite crear, consultar, actualizar y eliminar usuarios a través de una interfaz web moderna. El proyecto sigue una arquitectura en capas en el backend (Routes → Services → Repository → Models) y un diseño basado en componentes en el frontend.

Fue desarrollado con fines académicos para explorar patrones de diseño REST, separación de responsabilidades y comunicación cliente-servidor.

---

## Arquitectura del proyecto

```
┌─────────────────────────────────────────────────────────┐
│                     CLIENTE (Browser)                    │
│                                                          │
│   ┌───────────────────────────────────────────────────┐  │
│   │                  Vue 3 + Vite                     │  │
│   │  App.vue → HelloWorld.vue  ←→  api.js (fetch)    │  │
│   └───────────────────┬───────────────────────────────┘  │
└───────────────────────│─────────────────────────────────┘
                        │ HTTP / JSON  (localhost:5173 → 8000)
┌───────────────────────│─────────────────────────────────┐
│                SERVER (FastAPI + Uvicorn)                │
│                                                          │
│   ┌──────────┐   ┌──────────┐   ┌────────────┐          │
│   │  Routes  │ → │ Services │ → │ Repository │          │
│   │ /usuarios│   │ Validación│  │ JSON file  │          │
│   └──────────┘   └──────────┘   └─────┬──────┘          │
│                                        │                 │
│                               ┌────────▼───────┐        │
│                               │  usuarios.json │        │
│                               └────────────────┘        │
└─────────────────────────────────────────────────────────┘
```

### Capas del backend

| Capa | Archivo | Responsabilidad |
|------|---------|-----------------|
| Routes | `routes/user.py` | Recibir peticiones HTTP y retornar respuestas |
| Services | `services/user.py` | Lógica de negocio y validaciones de dominio |
| Repository | `repository/user.py` | Lectura y escritura en el archivo JSON |
| Models | `models/user.py` | Definición de la entidad `User` |
| DTO | `dto/response.py` | Validación de datos de entrada con Pydantic |

---

## Tecnologías utilizadas

### Backend

| Herramienta | Versión | Rol |
|-------------|---------|-----|
| Python | 3.10+ | Lenguaje principal |
| FastAPI | 0.115.12 | Framework web asincrónico |
| Uvicorn | 0.34.0 | Servidor ASGI |
| Pydantic | (incluido con FastAPI) | Validación de DTOs |

### Frontend

| Herramienta | Versión | Rol |
|-------------|---------|-----|
| Vue | 3.5.32 | Framework reactivo UI |
| Vite | 8.0.10 | Build tool y dev server |
| @vitejs/plugin-vue | 6.0.6 | Soporte de SFCs `.vue` en Vite |
| Material Symbols | CDN | Iconografía |
| Google Fonts (Inter) | CDN | Tipografía |

### Almacenamiento

| Herramienta | Rol |
|-------------|-----|
| JSON local (`usuarios.json`) | Persistencia de datos sin base de datos externa |

---

## Estructura de carpetas

```
Universidad/
├── backend/
│   └── src/
│       ├── dto/
│       │   └── response.py          # DTOs con validación Pydantic
│       ├── models/
│       │   └── user.py              # Entidad User
│       ├── repository/
│       │   └── user.py              # Acceso a datos (R/W sobre JSON)
│       ├── routes/
│       │   └── user.py              # Endpoints HTTP
│       ├── services/
│       │   └── user.py              # Lógica de negocio
│       ├── main.py                  # Punto de entrada FastAPI
│       ├── requirements.txt         # Dependencias Python
│       └── usuarios.json            # Base de datos JSON
│
├── frontend/
│   └── src/
│       ├── public/
│       │   └── favicon.svg
│       ├── src/
│       │   ├── api/
│       │   │   └── api.js           # Cliente HTTP hacia el backend
│       │   ├── assets/
│       │   │   └── HelloWorld.css   # Estilos del componente principal
│       │   ├── components/
│       │   │   └── HelloWorld.vue   # Componente CRUD de usuarios
│       │   ├── App.vue              # Componente raíz
│       │   ├── main.js              # Punto de entrada Vue
│       │   └── style.css            # Estilos globales
│       ├── index.html
│       ├── package.json
│       └── vite.config.js
│
└── README.md
```

---

## Requisitos previos

- **Python** 3.10 o superior
- **Node.js** 18 o superior (incluye `npm`)
- **Git**

---

## Instalación y configuración

### Backend

```bash
# 1. Ir al directorio del backend
cd backend/src

# 2. Crear el entorno virtual
python -m venv .venv

# 3. Activar el entorno virtual
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
# macOS / Linux
source .venv/bin/activate

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Iniciar el servidor
uvicorn main:app --reload
```

El servidor queda disponible en: `http://127.0.0.1:8000`  
Documentación interactiva (Swagger): `http://127.0.0.1:8000/docs`

---

### Frontend

```bash
# 1. Ir al directorio del frontend
cd frontend/src

# 2. Instalar dependencias
npm install

# 3. Iniciar el servidor de desarrollo
npm run dev
```

La aplicación queda disponible en: `http://localhost:5173`

#### Scripts disponibles

| Comando | Descripción |
|---------|-------------|
| `npm run dev` | Servidor de desarrollo con Hot Module Replacement |

---

## Uso

1. Con ambos servidores corriendo, abre `http://localhost:5173` en el navegador.
2. **Crear usuario**: completa el formulario (nombre, apellido, correo, contraseña) y haz clic en *Registrar usuario*.
3. **Editar usuario**: haz clic en el icono de editar en la fila del usuario deseado, modifica los campos y haz clic en *Actualizar usuario*.
4. **Eliminar usuario**: haz clic en el icono de eliminar en la fila correspondiente.
5. Los mensajes de éxito y error se muestran en la parte superior del formulario.

---

## API Reference

**Base URL**: `http://127.0.0.1:8000`

### Usuarios

#### Crear usuario

```http
POST /usuarios
Content-Type: application/json

{
  "nombre": "string",
  "apellido": "string",
  "correo": "string",
  "contraseña": "string"   // mínimo 6 caracteres
}
```

| Código | Descripción |
|--------|-------------|
| `200` | Usuario creado exitosamente |
| `400` | Campos vacíos, contraseña muy corta o correo duplicado |
| `422` | Error de validación de tipos (Pydantic) |

---

#### Obtener todos los usuarios

```http
GET /usuarios
```

**Respuesta exitosa**

```json
{
  "mensaje": "Usuarios encontrados",
  "data": [
    {
      "nombre": "string",
      "apellido": "string",
      "correo": "string",
      "contraseña": "string"
    }
  ]
}
```

---

#### Actualizar usuario

```http
PUT /usuarios/{correo}
Content-Type: application/json

{
  "nombre": "string",
  "apellido": "string",
  "correo": "string",
  "contraseña": "string"
}
```

| Código | Descripción |
|--------|-------------|
| `200` | Usuario actualizado exitosamente |
| `400` | Validación fallida |
| `404` | Usuario no encontrado |

---

#### Eliminar usuario

```http
DELETE /usuarios/{correo}
```

| Código | Descripción |
|--------|-------------|
| `200` | Usuario eliminado exitosamente |
| `404` | Usuario no encontrado |

---

## Modelo de datos

### Entidad `User`

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| `nombre` | `str` | Requerido, no vacío | Nombre del usuario |
| `apellido` | `str` | Requerido, no vacío | Apellido del usuario |
| `correo` | `str` | Requerido, único | Correo electrónico (clave primaria) |
| `contraseña` | `str` | Mínimo 6 caracteres | Contraseña de acceso |

### Ejemplo en `usuarios.json`

```json
[
  {
    "nombre": "Juan",
    "apellido": "Pérez",
    "correo": "juan.perez@ejemplo.com",
    "contraseña": "segura123"
  }
]
```

---

## Variables de entorno y configuración

### Backend — CORS

El servidor permite solicitudes únicamente desde el origen configurado en `main.py`:

```python
origins = ["http://localhost:5173"]
```

Para cambiar el origen permitido (por ejemplo en producción), edita dicha lista en `backend/src/main.py`.

### Frontend — URL del backend

La URL base del backend está definida en `frontend/src/src/api/api.js`. Si el backend corre en un puerto o host diferente, actualiza la constante correspondiente en ese archivo.

---



