

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

### Visión general

El proyecto está dividido en dos aplicaciones independientes que se comunican a través de HTTP:

```
┌──────────────────────────────────────────────────────────────┐
│                      CLIENTE (Browser)                        │
│                                                               │
│   ┌─────────────────────────────────────────────────────┐    │
│   │                    Vue 3 + Vite                      │    │
│   │                                                      │    │
│   │   main.js                                            │    │
│   │     └── App.vue          (componente raíz)           │    │
│   │           └── HelloWorld.vue  (lógica CRUD + UI)     │    │
│   │                 └── api/api.js  (cliente HTTP)        │    │
│   └──────────────────────┬──────────────────────────────┘    │
└─────────────────────────│────────────────────────────────────┘
                           │  fetch() — HTTP/JSON
                           │  localhost:5173  →  localhost:8000
┌─────────────────────────│────────────────────────────────────┐
│                SERVER   │  (FastAPI + Uvicorn)                │
│                          │                                    │
│   main.py ──────────────▼──────────────────────────────┐    │
│   (punto de entrada,     │                               │    │
│    CORS, registro        ▼                               │    │
│    de routers)     routes/user.py                        │    │
│                    (recibe HTTP,                         │    │
│                     llama al servicio)                   │    │
│                          │                               │    │
│                          ▼                               │    │
│                    services/user.py                      │    │
│                    (valida reglas                        │    │
│                     de negocio)                          │    │
│                          │                               │    │
│                          ▼                               │    │
│                    repository/user.py                    │    │
│                    (lee y escribe                        │    │
│                     el archivo JSON)                     │    │
│                          │                               │    │
│                          ▼                               │    │
│                    usuarios.json                         │    │
│                    (base de datos)                       │    │
└──────────────────────────────────────────────────────────────┘
```

---

### Por qué esta arquitectura en capas

El backend sigue el patrón **Layered Architecture** (arquitectura por capas). La idea central es que **cada capa solo conoce a la capa inmediatamente inferior**, nunca salta capas ni se mezcla con responsabilidades ajenas.

Esto resuelve un problema concreto: si todo el código estuviera junto en un solo archivo, cambiar cómo se guardan los datos (por ejemplo, pasar de JSON a una base de datos real) obligaría a tocar también la lógica de validación y las rutas HTTP. Con capas separadas, ese cambio ocurre en un solo lugar.

---

### Descripción de cada capa y archivo

#### `main.py` — Punto de entrada y configuración global

Es el archivo que arranca la aplicación. Sus únicas responsabilidades son:

1. Crear la instancia de FastAPI.
2. Configurar CORS para permitir que el frontend (puerto 5173) hable con el backend (puerto 8000) sin que el navegador lo bloquee.
3. Registrar los routers (grupos de endpoints) que están definidos en otras capas.

No contiene lógica de negocio ni acceso a datos. Si en el futuro se agregan más módulos (productos, pedidos, etc.), solo se registran aquí sus routers, sin tocar nada más.

---

#### `dto/response.py` — Validación de entrada (Data Transfer Object)

Un DTO es el "contrato" que define exactamente qué datos debe enviar el cliente para que una operación sea válida. Usando Pydantic, FastAPI valida automáticamente el cuerpo de cada petición antes de que llegue a cualquier otra parte del código.

**¿Por qué existe esta capa separada?**  
Porque la validación de *formato* (¿vienen todos los campos? ¿son del tipo correcto?) es distinta de la validación de *negocio* (¿ya existe este correo? ¿la contraseña cumple la política?). Mezclarlas genera código difícil de mantener. El DTO solo se preocupa por el formato; las reglas de negocio viven en el servicio.

Si FastAPI detecta que el cliente no cumple el DTO, retorna automáticamente un `422` con el detalle del error, sin que el desarrollador tenga que escribir esa lógica.

---

#### `models/user.py` — Entidad de dominio

Define la estructura interna de un usuario tal como el sistema lo entiende. Es la representación pura del dato, sin lógica de HTTP ni de base de datos.

**¿Por qué existe separado del DTO?**  
El DTO representa lo que *entra* por la red. El modelo representa lo que *vive* dentro del sistema. Pueden diferir: en el futuro el modelo podría tener campos calculados, timestamps o un ID generado internamente que el cliente nunca envía. Tener ambos separados permite evolucionar uno sin afectar el otro.

---

#### `services/user.py` — Lógica de negocio

Es el cerebro de la aplicación. Aquí viven las reglas que hacen que este sistema sea un gestor de usuarios y no cualquier otra cosa:

- ¿El correo ya está registrado? → error.
- ¿La contraseña tiene al menos 6 caracteres? → error.
- ¿El usuario a editar existe? → si no, error 404.

**¿Por qué no poner estas validaciones en la ruta o en el repositorio?**  
Porque las reglas de negocio son independientes tanto del protocolo de transporte (HTTP) como del mecanismo de almacenamiento (JSON, base de datos). Si mañana la aplicación expone una CLI o un worker de tareas, el servicio puede reutilizarse sin cambios. Si se cambia de JSON a PostgreSQL, las reglas siguen siendo las mismas y no hay que reescribirlas.

---

#### `repository/user.py` — Acceso a datos

Es la única capa que sabe que los datos están en un archivo JSON. Lee el archivo, lo deserializa, hace la operación (crear, buscar, actualizar, eliminar) y lo vuelve a escribir.

**¿Por qué aislar esto?**  
Porque el almacenamiento es un detalle de implementación. Si en el futuro se decide usar una base de datos real, solo se reescribe este archivo. El servicio y las rutas no se enteran del cambio porque el repositorio les sigue entregando los mismos objetos `User`. Este principio se llama **inversión de dependencias**: las capas superiores dependen de una interfaz (qué hace el repositorio), no de cómo lo hace.

---

#### `routes/user.py` — Endpoints HTTP

Define los cuatro endpoints del recurso `/usuarios` (GET, POST, PUT, DELETE). Su trabajo es:

1. Recibir la petición HTTP.
2. Llamar al servicio correspondiente con los datos ya validados por el DTO.
3. Devolver la respuesta HTTP con el código de estado correcto.

La ruta no valida reglas de negocio ni toca datos directamente. Solo traduce entre el mundo HTTP y el mundo de la lógica de la aplicación. Esto la hace fácil de probar y de reemplazar (si se cambia FastAPI por otro framework, solo se reescribe esta capa).

---

### Flujo completo de una petición

A continuación se muestra el recorrido de una petición **POST /usuarios** desde el navegador hasta el archivo JSON y de regreso:

```
Navegador
  │
  │  POST /usuarios  { nombre, apellido, correo, contraseña }
  ▼
routes/user.py
  │  FastAPI valida el body contra CreateUserRequest (DTO)
  │  Si el formato es inválido → responde 422 automáticamente
  │  Si es válido → llama a user_service.crear_usuario(data)
  ▼
services/user.py
  │  ¿Correo ya existe?     → lanza HTTPException 400
  │  ¿Contraseña < 6 chars? → lanza HTTPException 400
  │  ¿Campos vacíos?        → lanza HTTPException 400
  │  Todo OK → llama a user_repository.guardar(user)
  ▼
repository/user.py
  │  Lee usuarios.json
  │  Agrega el nuevo usuario al array
  │  Escribe usuarios.json actualizado
  ▼
usuarios.json  (dato persistido)
  │
  └── respuesta sube por las capas → { "mensaje": "Usuario creado", "correo": "..." }
  ▼
Navegador recibe 200 OK y muestra mensaje de éxito
```

---

### Frontend: estructura de componentes

El frontend sigue el principio de **separación entre lógica de comunicación y lógica de presentación**:

| Archivo | Responsabilidad |
|---------|-----------------|
| `main.js` | Monta la aplicación Vue en el DOM. No contiene lógica propia. |
| `App.vue` | Componente raíz mínimo. Solo importa y renderiza `HelloWorld.vue`. Existir como capa separada permite agregar en el futuro un sistema de rutas (Vue Router) sin modificar los componentes de negocio. |
| `components/HelloWorld.vue` | Contiene todo el estado reactivo (lista de usuarios, formulario, modo edición, mensajes de error/éxito) y los métodos CRUD. Es el único componente con lógica de negocio del frontend. |
| `api/api.js` | Cliente HTTP aislado. Todas las llamadas `fetch()` al backend viven aquí. Si la URL del backend cambia, o si se quiere reemplazar `fetch` por `axios`, el cambio ocurre en un solo lugar sin tocar el componente. |

**¿Por qué separar `api.js` del componente?**  
Porque la forma de comunicarse con el servidor es un detalle técnico, no lógica de UI. Un componente no debería saber si los datos vienen de un fetch, de un WebSocket o de un mock. Mantenerlos separados hace que ambos sean más fáciles de probar y reutilizar.

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



