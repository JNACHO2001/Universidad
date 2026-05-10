// URL base del backend FastAPI corriendo en local
const api = "http://127.0.0.1:8000";

// Lee el campo "detail" que FastAPI incluye en los errores HTTP
// y lo lanza como un Error normal para que el catch del componente lo muestre
const manejarError = async (respuesta) => {
  const json = await respuesta.json().catch(() => ({}));
  throw new Error(json.detail ?? "Error en el servidor");
};

// Crea un nuevo usuario enviando sus datos como JSON al backend
export const crearUsuario = async (usuario) => {
  const respuesta = await fetch(`${api}/usuarios`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(usuario),
  });
  if (!respuesta.ok) await manejarError(respuesta);
  const data = await respuesta.json();
  return data;
};

// Actualiza los datos de un usuario identificado por su correo
export const editarUsuario = async (correo, usuarioActualizado) => {
  const respuesta = await fetch(`${api}/usuarios/${correo}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(usuarioActualizado),
  });
  if (!respuesta.ok) await manejarError(respuesta);
  const data = await respuesta.json();
  return data;
};

// Obtiene la lista de todos los usuarios; retorna arreglo vacío si no hay ninguno
export const obtenerUsuarios = async () => {
  const respuesta = await fetch(`${api}/usuarios`);
  if (!respuesta.ok) await manejarError(respuesta);
  const json = await respuesta.json();
  return json.data ?? [];
};

// Elimina un usuario por su correo
export const eliminarUsuario = async (correo) => {
  const respuesta = await fetch(`${api}/usuarios/${correo}`, {
    method: "DELETE",
  });
  if (!respuesta.ok) await manejarError(respuesta);
  const data = await respuesta.json();
  return data;
};
