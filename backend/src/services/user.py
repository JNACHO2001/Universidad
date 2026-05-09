from repository.user import UserReposotory
from models.user import User


class UserService:

    def __init__(self):
        self.repo = UserReposotory()
        



    def crearUsuario(self, user:User):
        if not user.nombre or not user.apellido:
            raise ValueError("Los campos  no deben estar vacios ")
        
        if not user.correo:
            raise ValueError("el campo no pude estar vacio")
        
        if not user.contraseña or len(user.contraseña) < 6:
            raise ValueError("no nay contraseña o debe ser mas de 6 caracteres ")
        

        existe = self.repo.buscar_por_correo(user.correo)
        if   existe:
            raise ValueError("el correo ya esta en la base de datos")
        
       
        self.repo.guardar(user)
        print ("el usuario ha sido creado")    
        return user
    

    def actualizarUsuario(self, correo: str, datosnuevos):
        existe = self.repo.buscar_por_correo(correo)
        if not existe:
            raise ValueError("no se encontro el usuario")
        return self.repo.actualizar(correo, User.from_dict(datosnuevos))
    
    def eliminarUsuario(self, correo: str):
        existe = self.repo.buscar_por_correo(correo)
        if not existe:
            raise ValueError("no se encontro el usuario")
        return self.repo.eliminar(correo)
    

    def mostrarUsuarios(self):
        usuarios =self.repo.obtener_todos()
        if not usuarios:
            raise ValueError("no hay datos",usuarios)
        return usuarios

            

        
        

    








