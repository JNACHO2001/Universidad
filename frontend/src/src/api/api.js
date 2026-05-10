const api = "http://127.0.0.1:8000";

export const crearUsuario = async (usuario) => {
  const respuesta = await fetch(`${api}/usuarios`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(usuario),
  });
  if (!respuesta.ok) {
    throw new Error("No se pudo crear el usuario");
  }

  const data = await respuesta.json();
  return data;
};

export const editarUsuario = async (correo,usuarioActualizado) => {
  const respuesta = await fetch(`${api}/usuarios/${correo}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(usuarioActualizado),
  });

  if (!respuesta.ok) {
    throw new Error("error al actulizar usuario")
    
    
  }

  const data = await respuesta.json();
  return data;
  
}

export const obtenerUsuarios = async () => {
  const respuesta = await fetch(`${api}/usuarios`);
  if (!respuesta.ok) throw new Error("No se encontraron usuarios");
  const json = await respuesta.json();
  return json.data ?? [];
};
export const eliminarUsuario = async (correo) => {
  const respuesta = await fetch(`${api}/usuarios/${correo}`, {
    method: "DELETE",
  });

  if (!respuesta.ok) {
    throw new Error("No se encontro el usuario");
  }

  const data = await respuesta.json();
  return data;
};
