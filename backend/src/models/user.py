# Modelo de dominio que representa a un usuario en el sistema
class User:

    def __init__(self, nombre, apellido, correo, contraseña):
        self.nombre = nombre
        self.apellido = apellido
        self.correo = correo
        self.contraseña = contraseña

    # Convierte el objeto a diccionario para guardarlo en el JSON
    def to_dict(self):
        return {
            "nombre": self.nombre,
            "apellido": self.apellido,
            "correo": self.correo,
            "contraseña": self.contraseña,
        }

    # Reconstruye un objeto User desde un diccionario leído del JSON
    @staticmethod
    def from_dict(data):
        return User(
            data["nombre"],
            data["apellido"],
            data["correo"],
            data["contraseña"],
        )
