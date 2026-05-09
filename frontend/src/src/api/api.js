const api = "http://127.0.0.1:8000"

export const obtenerUsuarios = async () => {
  const respuesta = await fetch(`${api}/usuarios`)
  if (!respuesta.ok) throw new Error("No se encontraron usuarios")
  const json = await respuesta.json()
  return json.data ?? []
}
