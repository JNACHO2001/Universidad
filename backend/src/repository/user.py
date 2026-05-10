import json
import os
from models.user import User


# Capa de acceso a datos: lee y escribe usuarios en un archivo JSON local
class UserReposotory:

    def __init__(self, archivo="usuarios.json"):
        # Nombre del archivo que actúa como base de datos
        self.archivo = archivo

    # Lee el archivo y retorna la lista; si no existe, retorna lista vacía
    def _leer_archivo(self):
        if not os.path.exists(self.archivo):
            return []
        with open(self.archivo, "r", encoding="utf-8") as f:
            return json.load(f)

    # Sobreescribe el archivo con la lista actualizada
    def _escribir_archivo(self, datos):
        with open(self.archivo, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)

    # Agrega un nuevo usuario al final de la lista
    def guardar(self, user: User):
        datos = self._leer_archivo()
        datos.append(user.to_dict())
        self._escribir_archivo(datos)

    # Retorna todos los usuarios convertidos a objetos User
    def obtener_todos(self):
        datos = self._leer_archivo()
        if not datos:
            return []
        return [User.from_dict(d) for d in datos]

    # Busca un usuario por correo; retorna None si no existe
    def buscar_por_correo(self, correo: str):
        for u in self.obtener_todos():
            if correo == u.correo:
                return u
        return None

    # Reemplaza los datos del usuario que coincida con correo_original
    def actualizar(self, correo_original: str, usuario: User):
        datos = self._leer_archivo()
        for i, d in enumerate(datos):
            if d["correo"] == correo_original:
                datos[i] = usuario.to_dict()
                break
        self._escribir_archivo(datos)
        return usuario

    # Elimina el usuario con ese correo y retorna sus datos; retorna None si no existe
    def eliminar(self, correo: str):
        datos = self._leer_archivo()
        for i, d in enumerate(datos):
            if d["correo"] == correo:
                usuario_eliminado = datos.pop(i)
                self._escribir_archivo(datos)
                return usuario_eliminado
        return None
