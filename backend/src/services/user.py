from repository.user import UserReposotory
from models.user import User


# Capa de negocio: aplica validaciones antes de delegar al repositorio
class UserService:

    def __init__(self):
        self.repo = UserReposotory()

    # Valida campos obligatorios y que el correo no esté duplicado antes de guardar
    def crearUsuario(self, user: User):
        if not user.nombre or not user.apellido:
            raise ValueError("Los campos no deben estar vacíos")

        if not user.correo:
            raise ValueError("El campo correo no puede estar vacío")

        if not user.contraseña or len(user.contraseña) < 6:
            raise ValueError("La contraseña debe tener al menos 6 caracteres")

        if self.repo.buscar_por_correo(user.correo):
            raise ValueError("El correo ya está registrado")

        self.repo.guardar(user)
        return user

    # Verifica que el usuario exista antes de actualizar
    def actualizarUsuario(self, correo: str, datosnuevos):
        if not self.repo.buscar_por_correo(correo):
            raise ValueError("No se encontró el usuario")
        return self.repo.actualizar(correo, User.from_dict(datosnuevos))

    # Verifica que el usuario exista antes de eliminar
    def eliminarUsuario(self, correo: str):
        if not self.repo.buscar_por_correo(correo):
            raise ValueError("No se encontró el usuario")
        return self.repo.eliminar(correo)

    # Lanza ValueError si la lista está vacía para que la ruta retorne 404
    def mostrarUsuarios(self):
        usuarios = self.repo.obtener_todos()
        if not usuarios:
            raise ValueError("No hay usuarios registrados")
        return usuarios
