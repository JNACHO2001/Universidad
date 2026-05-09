from pydantic import BaseModel


class CreateUserRequest(BaseModel):
    nombre: str
    apellido: str
    correo: str
    contraseña: str


