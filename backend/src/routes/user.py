from fastapi import APIRouter, HTTPException
from services.user import UserService
from models.user import User
from dto.response import CreateUserRequest

router = APIRouter(prefix="/usuarios")

servicio = UserService()


@router.post("")
def crear_usuario(data: CreateUserRequest):
    try:
        user = User(data.nombre, data.apellido, data.correo, data.contraseña)
        servicio.crearUsuario(user)
        return {"mensaje": "Usuario creado correctamente", "correo": user.correo}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{correo}")
def actualizar_usuario(correo: str, data: CreateUserRequest):
    try:
        servicio.actualizarUsuario(correo, data.model_dump())
        return {"mensaje": "Usuario actualizado correctamente"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.delete("/{correo}")
def eliminar(correo:str):
    try:
        servicio.eliminarUsuario(correo)
        return {"mensaje": "Usuario eliminado correctamente"}
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    

@router.get("")
def mostrar_Usuarios():
    try:
        datos = servicio.mostrarUsuarios()
        if datos:
            return {"mensaje":"datos obnetidos correctamente ","data":datos}
            
        

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

