from pydantic import BaseModel


# DTO (Data Transfer Object) que define la estructura esperada del cuerpo
# en las peticiones POST y PUT. Pydantic valida automáticamente los tipos
# y retorna un error 422 si falta algún campo.
class CreateUserRequest(BaseModel):
    nombre: str
    apellido: str
    correo: str
    contraseña: str
