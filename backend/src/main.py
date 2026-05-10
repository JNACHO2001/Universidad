from fastapi import FastAPI
from routes.user import router as user_router
from fastapi.middleware.cors import CORSMiddleware

# Instancia principal de la aplicación FastAPI
app = FastAPI()

# Orígenes permitidos para hacer peticiones al backend
# Solo el frontend de Vite corriendo en localhost:5173 puede consumir la API
origenes = [
    "http://localhost:5173"
]

# Middleware CORS: sin esto el navegador bloquearía las peticiones del frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=origenes,
    allow_credentials=True,
    allow_methods=["*"],   # permite GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],
)

# Registra todas las rutas de usuarios bajo el prefijo /usuarios
app.include_router(user_router)
