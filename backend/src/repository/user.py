import json 
import os
from models.user import User


class UserReposotory:

    def __init__(self,archivo ="usuarios.json"):
        self.archivo = archivo

    def _leer_archivo(self):
        if not os.path.exists(self.archivo):
            return [
            ]
        

        with open(self.archivo,"r", encoding="utf-8") as f:
            return json.load(f)
        


    def _escribir_archivo(self,datos):
        with open(self.archivo,"w",encoding="utf-8") as f:
            json.dump(datos, f,indent=4, ensure_ascii=False)



    def guardar(self, user:User):
        datos = self._leer_archivo()
        datos.append(user.to_dict())
        self._escribir_archivo(datos)






    def obtener_todos(self):
        datos = self._leer_archivo()
        if not datos:
            return []
        return [User.from_dict(d) for d in datos]
    
    def buscar_por_correo(self,correo :str):
        usuarios =self.obtener_todos()

        for u in usuarios:
            if correo == u.correo:
                return u

        return None
    
    def actualizar(self, correo_original: str, usuario: User):
        datos = self._leer_archivo()
        for i, d in enumerate(datos):
            if d["correo"] == correo_original:
                datos[i] = usuario.to_dict()
                break
        self._escribir_archivo(datos)
        return usuario
    
    def eliminar(self, correo: str):
        datos = self._leer_archivo()
        for i, d in enumerate(datos):
            if d["correo"] == correo:
                usuario_eliminado = datos.pop(i)
                self._escribir_archivo(datos)
                return usuario_eliminado
        return None
        








        
        

    


    