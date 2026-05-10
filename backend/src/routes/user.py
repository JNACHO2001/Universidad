from fastapi import APIRouter, HTTPException
from services.user import UserService
from models.user import User
from dto.response import CreateUserRequest

# Todas las rutas de este archivo tienen el prefijo /usuarios
router = APIRouter(prefix="/usuarios")

servicio = UserService()


# POST /usuarios — crea un nuevo usuario
# Retorna 400 si los datos son inválidos o el correo ya existe
@router.post("")
def crear_usuario(data: CreateUserRequest):
    try:
        user = User(data.nombre, data.apellido, data.correo, data.contraseña)
        servicio.crearUsuario(user)
        return {"mensaje": "Usuario creado correctamente", "correo": user.correo}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# PUT /usuarios/{correo} — actualiza los datos de un usuario existente
# Retorna 404 si el correo no se encuentra
@router.put("/{correo}")
def actualizar_usuario(correo: str, data: CreateUserRequest):
    try:
        servicio.actualizarUsuario(correo, data.model_dump())
        return {"mensaje": "Usuario actualizado correctamente"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# DELETE /usuarios/{correo} — elimina un usuario por su correo
# Retorna 404 si el correo no se encuentra
@router.delete("/{correo}")
def eliminar(correo: str):
    try:
        servicio.eliminarUsuario(correo)
        return {"mensaje": "Usuario eliminado correctamente"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# GET /usuarios — retorna la lista completa de usuarios
# Retorna 404 si no hay ningún usuario registrado
@router.get("")
def mostrar_Usuarios():
    try:
        datos = servicio.mostrarUsuarios()
        return {"mensaje": "datos obtenidos correctamente", "data": datos or []}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
