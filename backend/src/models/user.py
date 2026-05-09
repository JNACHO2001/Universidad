


class User:
    def __init__(self,nombre,apellido,correo,contraseña):
        self.nombre  = nombre
        self.apellido  = apellido
        self.correo  = correo
        self.contraseña  = contraseña






    def to_dict(self):
        return {
            "nombre":self.nombre,
            "apellido":self.apellido,
            "correo": self.correo,
            "contraseña":self.contraseña


        }
    


    @staticmethod
    def from_dict(data):
        return User(
            data["nombre"],
            data["apellido"],
            data["correo"],
            data["contraseña"],


        )