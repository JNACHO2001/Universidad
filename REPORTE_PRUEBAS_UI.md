# Reporte de Pruebas Automatizadas — User Central Management Console

---

## 1. Información General

| Campo               | Detalle                                             |
|---------------------|-----------------------------------------------------|
| **Aplicación**      | User Central - Management Console                  |
| **URL Frontend**    | http://localhost:5173/                              |
| **URL Backend**     | http://127.0.0.1:8000                               |
| **Framework UI**    | Vue 3 (Vite)                                        |
| **Framework API**   | FastAPI (Python)                                    |
| **Herramienta QA**  | Playwright MCP (JavaScript)                         |
| **Fecha ejecución** | 2026-05-10                                          |
| **Ejecutado por**   | Agente QA Senior — Claude Sonnet 4.6                |
| **Rama**            | testeo-y-calidad/unidad-2-actividad-2               |

---

## 2. Resumen Ejecutivo

| Métrica                        | Valor  |
|-------------------------------|--------|
| Total de casos de prueba       | 15     |
| Casos exitosos (PASS)          | 13     |
| Casos fallidos (FAIL)          | 2      |
| Tasa de éxito                  | 86.7 % |
| Bugs críticos encontrados      | 2      |
| Endpoints evaluados            | 4      |

### Conclusión rápida

La aplicación cubre correctamente el flujo principal de creación, consulta, edición y eliminación de usuarios. Las validaciones del formulario de **creación** funcionan bien tanto a nivel frontend (HTML5) como backend. Sin embargo, se identificaron **2 bugs de severidad alta** relacionados con la falta de validación en el endpoint de actualización (`PUT`) y con el código HTTP incorrecto al consultar una lista vacía (`GET`).

---

## 3. Endpoints Consumidos

| Método   | Endpoint                          | Descripción                      |
|----------|-----------------------------------|----------------------------------|
| `GET`    | `/usuarios`                       | Obtener lista de usuarios        |
| `POST`   | `/usuarios`                       | Crear nuevo usuario              |
| `PUT`    | `/usuarios/{correo}`              | Actualizar usuario por correo    |
| `DELETE` | `/usuarios/{correo}`              | Eliminar usuario por correo      |

---

## 4. Detalle de Pruebas

### TC-01 — Crear usuario con datos válidos

| Campo              | Valor                                  |
|--------------------|----------------------------------------|
| **Tipo**           | Funcional — CRUD Crear                 |
| **Endpoint**       | `POST /usuarios`                       |
| **Datos entrada**  | nombre: Ana, apellido: García, correo: ana.garcia@empresa.com, contraseña: Password123 |
| **HTTP esperado**  | 200                                    |
| **HTTP obtenido**  | 200 OK                                 |
| **Mensaje UI**     | "Usuario creado correctamente"         |
| **Resultado**      | ✅ PASS                                |
| **Observaciones**  | El usuario aparece en la tabla inmediatamente tras la creación. El formulario se limpia automáticamente. |

---

### TC-02 — Crear usuario con correo duplicado

| Campo              | Valor                                  |
|--------------------|----------------------------------------|
| **Tipo**           | Validación — dato inválido             |
| **Endpoint**       | `POST /usuarios`                       |
| **Datos entrada**  | correo: ana.garcia@empresa.com (ya registrado) |
| **HTTP esperado**  | 400                                    |
| **HTTP obtenido**  | 400 Bad Request                        |
| **Mensaje UI**     | "El correo ya está registrado"         |
| **Resultado**      | ✅ PASS                                |
| **Observaciones**  | El backend valida la unicidad del correo y retorna el mensaje correcto. |

---

### TC-03 — Crear usuario con todos los campos vacíos

| Campo              | Valor                                  |
|--------------------|----------------------------------------|
| **Tipo**           | Validación — campos vacíos             |
| **Endpoint**       | `POST /usuarios`                       |
| **Datos entrada**  | todos los campos vacíos                |
| **HTTP esperado**  | 400                                    |
| **HTTP obtenido**  | 400 Bad Request                        |
| **Mensaje UI**     | "Los campos no deben estar vacíos"     |
| **Resultado**      | ✅ PASS                                |
| **Observaciones**  | La validación ocurre en el backend, no en el frontend. El formulario llega al servidor con campos vacíos y este rechaza la petición. |

---

### TC-04 — Crear usuario con correo de formato inválido

| Campo              | Valor                                  |
|--------------------|----------------------------------------|
| **Tipo**           | Validación — formato de correo         |
| **Endpoint**       | N/A (bloqueado por validación nativa)  |
| **Datos entrada**  | correo: "correo-invalido"              |
| **HTTP esperado**  | Sin petición                           |
| **HTTP obtenido**  | Sin petición al servidor               |
| **Mensaje UI**     | Tooltip nativo del navegador           |
| **Resultado**      | ✅ PASS                                |
| **Observaciones**  | El campo `<input type="email">` activa la validación HTML5 nativa del navegador, impidiendo el submit. No se realiza ninguna petición HTTP. |

---

### TC-05 — Crear segundo usuario válido

| Campo              | Valor                                  |
|--------------------|----------------------------------------|
| **Tipo**           | Funcional — CRUD Crear                 |
| **Endpoint**       | `POST /usuarios`                       |
| **Datos entrada**  | nombre: Carlos, apellido: Ruiz, correo: carlos.ruiz@empresa.com, contraseña: SecurePass789 |
| **HTTP esperado**  | 200                                    |
| **HTTP obtenido**  | 200 OK                                 |
| **Mensaje UI**     | "Usuario creado correctamente"         |
| **Resultado**      | ✅ PASS                                |
| **Observaciones**  | La tabla muestra dos registros tras la creación. El GET posterior retorna 200. |

---

### TC-06 — Editar usuario existente

| Campo              | Valor                                  |
|--------------------|----------------------------------------|
| **Tipo**           | Funcional — CRUD Editar                |
| **Endpoint**       | `PUT /usuarios/ana.garcia@empresa.com` |
| **Datos entrada**  | nombre: "Ana Lucía", apellido: "García López" |
| **HTTP esperado**  | 200                                    |
| **HTTP obtenido**  | 200 OK                                 |
| **Mensaje UI**     | "Usuario actualizado correctamente"    |
| **Resultado**      | ✅ PASS                                |
| **Observaciones**  | Al hacer clic en el botón "edit" de la tabla, el formulario se pre-rellena con los datos del usuario y el botón cambia a "Actualizar usuario". La tabla refleja los cambios tras la respuesta. |

---

### TC-07 — Cancelar modo edición

| Campo              | Valor                                  |
|--------------------|----------------------------------------|
| **Tipo**           | Funcional — UX                         |
| **Endpoint**       | N/A                                    |
| **Datos entrada**  | Clic en "Cancelar"                     |
| **HTTP esperado**  | Sin petición                           |
| **HTTP obtenido**  | Sin petición                           |
| **Mensaje UI**     | Formulario limpiado, botón vuelve a "Registrar usuario" |
| **Resultado**      | ✅ PASS                                |
| **Observaciones**  | El formulario vuelve al estado inicial sin realizar ninguna petición. |

---

### TC-08 — Eliminar usuario existente

| Campo              | Valor                                         |
|--------------------|-----------------------------------------------|
| **Tipo**           | Funcional — CRUD Eliminar                     |
| **Endpoint**       | `DELETE /usuarios/carlos.ruiz@empresa.com`    |
| **HTTP esperado**  | 200                                           |
| **HTTP obtenido**  | 200 OK                                        |
| **Mensaje UI**     | "Usuario eliminado correctamente"             |
| **Resultado**      | ✅ PASS                                       |
| **Observaciones**  | El registro desaparece de la tabla de forma reactiva (filtrado local) sin recargar toda la lista. No hay diálogo de confirmación antes de eliminar. |

---

### TC-09 — Editar usuario con campos nombre y apellido vacíos (vía UI)

| Campo              | Valor                                         |
|--------------------|-----------------------------------------------|
| **Tipo**           | Validación — campos vacíos en edición         |
| **Endpoint**       | `PUT /usuarios/ana.garcia@empresa.com`        |
| **Datos entrada**  | nombre: "", apellido: "", contraseña: ""      |
| **HTTP esperado**  | 400 (debería validar)                         |
| **HTTP obtenido**  | **200 OK** ❌                                 |
| **Mensaje UI**     | "Usuario actualizado correctamente"           |
| **Resultado**      | ❌ FAIL — **BUG-02**                          |
| **Observaciones**  | El backend acepta la actualización con campos vacíos. La tabla muestra al usuario con nombre y apellido en blanco. El servicio `crearUsuario` valida los campos obligatorios, pero `actualizarUsuario` omite completamente esas validaciones. |

---

### TC-10 — Eliminar usuario inexistente

| Campo              | Valor                                         |
|--------------------|-----------------------------------------------|
| **Tipo**           | Manejo de errores — recurso no encontrado     |
| **Endpoint**       | `DELETE /usuarios/noexiste@test.com`          |
| **HTTP esperado**  | 404                                           |
| **HTTP obtenido**  | 404 Not Found                                 |
| **Mensaje API**    | `{"detail": "No se encontró el usuario"}`    |
| **Resultado**      | ✅ PASS                                       |
| **Observaciones**  | Verificado mediante fetch directo desde el contexto de página. |

---

### TC-11 — Editar usuario inexistente

| Campo              | Valor                                         |
|--------------------|-----------------------------------------------|
| **Tipo**           | Manejo de errores — recurso no encontrado     |
| **Endpoint**       | `PUT /usuarios/noexiste@test.com`             |
| **HTTP esperado**  | 404                                           |
| **HTTP obtenido**  | 404 Not Found                                 |
| **Mensaje API**    | `{"detail": "No se encontró el usuario"}`    |
| **Resultado**      | ✅ PASS                                       |
| **Observaciones**  | Verificado mediante fetch directo. |

---

### TC-12 — Crear usuario con contraseña menor a 6 caracteres

| Campo              | Valor                                         |
|--------------------|-----------------------------------------------|
| **Tipo**           | Validación — longitud de contraseña           |
| **Endpoint**       | `POST /usuarios`                              |
| **Datos entrada**  | contraseña: "123"                             |
| **HTTP esperado**  | 400                                           |
| **HTTP obtenido**  | 400 Bad Request                               |
| **Mensaje API**    | `{"detail": "La contraseña debe tener al menos 6 caracteres"}` |
| **Resultado**      | ✅ PASS                                       |
| **Observaciones**  | Validación correcta a nivel de servicio. No hay validación equivalente en el frontend. |

---

### TC-13 — Crear usuario con correo vacío (solo correo)

| Campo              | Valor                                         |
|--------------------|-----------------------------------------------|
| **Tipo**           | Validación — campo correo vacío               |
| **Endpoint**       | `POST /usuarios`                              |
| **Datos entrada**  | correo: "", resto de campos con valores válidos |
| **HTTP esperado**  | 400                                           |
| **HTTP obtenido**  | 400 Bad Request                               |
| **Mensaje API**    | `{"detail": "El campo correo no puede estar vacío"}` |
| **Resultado**      | ✅ PASS                                       |
| **Observaciones**  | La validación diferenciada del correo funciona correctamente. |

---

### TC-14 — Actualizar usuario con todos los campos vacíos (vía API directa)

| Campo              | Valor                                         |
|--------------------|-----------------------------------------------|
| **Tipo**           | Validación — campos vacíos en PUT             |
| **Endpoint**       | `PUT /usuarios/ana.garcia@empresa.com`        |
| **Datos entrada**  | nombre: "", apellido: "", contraseña: ""      |
| **HTTP esperado**  | 400                                           |
| **HTTP obtenido**  | **200 OK** ❌                                 |
| **Mensaje API**    | `{"mensaje": "Usuario actualizado correctamente"}` |
| **Resultado**      | ❌ FAIL — **BUG-02 confirmado**               |
| **Observaciones**  | Confirma que el bug existe a nivel de API, no solo en la UI. El método `actualizarUsuario` en `services/user.py` no aplica ninguna de las validaciones presentes en `crearUsuario`. |

---

### TC-15 — Consultar lista de usuarios (GET)

| Campo              | Valor                                         |
|--------------------|-----------------------------------------------|
| **Tipo**           | Funcional — CRUD Consultar                    |
| **Endpoint**       | `GET /usuarios`                               |
| **HTTP esperado**  | 200                                           |
| **HTTP obtenido**  | 200 OK                                        |
| **Mensaje API**    | `{"mensaje": "datos obtenidos correctamente", "data": [...]}` |
| **Resultado**      | ✅ PASS (cuando hay usuarios)                 |
| **Observaciones**  | Cuando la lista está vacía, el backend retorna **404** en lugar de 200 con array vacío — ver BUG-01. |

---

## 5. Bugs Encontrados

### BUG-01 — GET /usuarios retorna 404 cuando no hay usuarios registrados

| Campo              | Valor                                         |
|--------------------|-----------------------------------------------|
| **Severidad**      | Alta                                          |
| **Archivo**        | `backend/src/services/user.py` línea 44       |
| **Endpoint**       | `GET /usuarios`                               |
| **HTTP obtenido**  | 404 Not Found                                 |
| **HTTP esperado**  | 200 OK con `{"data": []}`                     |
| **Descripción**    | El servicio lanza `ValueError("No hay usuarios registrados")` cuando la lista está vacía, lo que la ruta convierte en un `HTTPException(status_code=404)`. Un recurso de colección vacío debería responder 200 con array vacío, no 404. |
| **Impacto**        | Al iniciar la aplicación sin usuarios, la consola del navegador muestra un error y la UI no distingue entre "sin datos" y "servidor caído". |
| **Reproducción**   | Vaciar `usuarios.json` → `GET http://127.0.0.1:8000/usuarios` → 404 |

**Corrección sugerida** en `services/user.py`:
```python
def mostrarUsuarios(self):
    return self.repo.obtener_todos()  # devuelve [] si está vacío
```
Y en `routes/user.py`, eliminar el bloque `try/except` de `mostrar_Usuarios`.

---

### BUG-02 — PUT /usuarios/{correo} acepta campos vacíos sin validar

| Campo              | Valor                                         |
|--------------------|-----------------------------------------------|
| **Severidad**      | Alta                                          |
| **Archivo**        | `backend/src/services/user.py` línea 29       |
| **Endpoint**       | `PUT /usuarios/{correo}`                      |
| **HTTP obtenido**  | 200 OK (incorrecto)                           |
| **HTTP esperado**  | 400 Bad Request                               |
| **Descripción**    | El método `actualizarUsuario` solo verifica que el usuario exista, pero no aplica las mismas validaciones de `crearUsuario` (campos vacíos, longitud de contraseña). Es posible guardar un usuario con nombre, apellido y contraseña en blanco. |
| **Impacto**        | Corrupción de datos. La tabla muestra filas con celdas vacías. La contraseña puede quedar en blanco permitiendo acceso sin credenciales. |
| **Reproducción**   | Crear un usuario → clic en "edit" → borrar nombre/apellido → "Actualizar usuario" → 200 OK, datos corruptos. |

**Corrección sugerida** en `services/user.py`:
```python
def actualizarUsuario(self, correo: str, datosnuevos):
    if not self.repo.buscar_por_correo(correo):
        raise ValueError("No se encontró el usuario")

    nuevo = User.from_dict(datosnuevos)
    if not nuevo.nombre or not nuevo.apellido:
        raise ValueError("Los campos no deben estar vacíos")
    if not nuevo.contraseña or len(nuevo.contraseña) < 6:
        raise ValueError("La contraseña debe tener al menos 6 caracteres")

    return self.repo.actualizar(correo, nuevo)
```

---

## 6. Código Fuente de las Pruebas Automatizadas

El siguiente código representa las pruebas ejecutadas mediante Playwright MCP durante esta sesión.

```javascript
// ─────────────────────────────────────────────────────────────────
// pruebas_ui.spec.js  —  User Central Management Console
// Herramienta: Playwright MCP (JavaScript)
// URL Frontend: http://localhost:5173/
// URL Backend:  http://127.0.0.1:8000
// ─────────────────────────────────────────────────────────────────

// TC-01: Crear usuario con datos válidos
await page.goto('http://localhost:5173/');
await page.getByRole('textbox', { name: 'Nombre' }).fill('Ana');
await page.getByRole('textbox', { name: 'Apellido' }).fill('García');
await page.getByRole('textbox', { name: 'Correo' }).fill('ana.garcia@empresa.com');
await page.getByRole('textbox', { name: 'Contraseña' }).fill('Password123');
await page.getByRole('button', { name: 'Registrar usuario' }).click();
// Esperado: POST /usuarios → 200, mensaje "Usuario creado correctamente"

// TC-02: Correo duplicado
await page.getByRole('textbox', { name: 'Nombre' }).fill('Carlos');
await page.getByRole('textbox', { name: 'Apellido' }).fill('Ruiz');
await page.getByRole('textbox', { name: 'Correo' }).fill('ana.garcia@empresa.com');
await page.getByRole('textbox', { name: 'Contraseña' }).fill('OtraPass456');
await page.getByRole('button', { name: 'Registrar usuario' }).click();
// Esperado: POST /usuarios → 400, mensaje "El correo ya está registrado"

// TC-03: Campos vacíos
await page.getByRole('textbox', { name: 'Nombre' }).fill('');
await page.getByRole('textbox', { name: 'Apellido' }).fill('');
await page.getByRole('textbox', { name: 'Correo' }).fill('');
await page.getByRole('textbox', { name: 'Contraseña' }).fill('');
await page.getByRole('button', { name: 'Registrar usuario' }).click();
// Esperado: POST /usuarios → 400, mensaje "Los campos no deben estar vacíos"

// TC-04: Correo con formato inválido (validación HTML5 nativa)
await page.getByRole('textbox', { name: 'Nombre' }).fill('Test');
await page.getByRole('textbox', { name: 'Apellido' }).fill('User');
await page.getByRole('textbox', { name: 'Correo' }).fill('correo-invalido');
await page.getByRole('textbox', { name: 'Contraseña' }).fill('Pass123');
await page.getByRole('button', { name: 'Registrar usuario' }).click();
// Esperado: sin request HTTP — navegador bloquea el submit por type="email"

// TC-05: Crear segundo usuario válido
await page.getByRole('textbox', { name: 'Nombre' }).fill('Carlos');
await page.getByRole('textbox', { name: 'Apellido' }).fill('Ruiz');
await page.getByRole('textbox', { name: 'Correo' }).fill('carlos.ruiz@empresa.com');
await page.getByRole('textbox', { name: 'Contraseña' }).fill('SecurePass789');
await page.getByRole('button', { name: 'Registrar usuario' }).click();
// Esperado: POST /usuarios → 200

// TC-06: Editar usuario existente
await page.getByRole('button', { name: 'edit' }).first().click();
await page.getByRole('textbox', { name: 'Nombre' }).fill('Ana Lucía');
await page.getByRole('textbox', { name: 'Apellido' }).fill('García López');
await page.getByRole('button', { name: 'Actualizar usuario' }).click();
// Esperado: PUT /usuarios/ana.garcia@empresa.com → 200

// TC-07: Cancelar modo edición
await page.getByRole('button', { name: 'edit' }).first().click();
await page.getByRole('button', { name: 'Cancelar' }).click();
// Esperado: sin request, formulario limpiado, modo creación restaurado

// TC-08: Eliminar usuario existente
await page.getByRole('button', { name: 'delete' }).nth(1).click();
// Esperado: DELETE /usuarios/carlos.ruiz@empresa.com → 200

// TC-09: Editar con campos vacíos (detecta BUG-02)
await page.getByRole('button', { name: 'edit' }).click();
await page.getByRole('textbox', { name: 'Nombre' }).fill('');
await page.getByRole('textbox', { name: 'Apellido' }).fill('');
await page.getByRole('button', { name: 'Actualizar usuario' }).click();
// Esperado: 400 — Obtenido: 200 ❌ BUG

// TC-10, TC-11, TC-12, TC-13, TC-14, TC-15: verificaciones vía fetch en página
await page.evaluate(async () => {
  // TC-10: DELETE usuario inexistente
  const r1 = await fetch('http://127.0.0.1:8000/usuarios/noexiste@test.com', { method: 'DELETE' });
  // Esperado: 404 "No se encontró el usuario"

  // TC-11: PUT usuario inexistente
  const r2 = await fetch('http://127.0.0.1:8000/usuarios/noexiste@test.com', {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ nombre: 'X', apellido: 'Y', correo: 'noexiste@test.com', contraseña: 'abc123' })
  });
  // Esperado: 404 "No se encontró el usuario"

  // TC-12: Contraseña corta
  const r3 = await fetch('http://127.0.0.1:8000/usuarios', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ nombre: 'Pedro', apellido: 'Soto', correo: 'pedro@test.com', contraseña: '123' })
  });
  // Esperado: 400 "La contraseña debe tener al menos 6 caracteres"

  // TC-13: Correo vacío
  const r4 = await fetch('http://127.0.0.1:8000/usuarios', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ nombre: 'Pedro', apellido: 'Soto', correo: '', contraseña: 'validpass' })
  });
  // Esperado: 400 "El campo correo no puede estar vacío"

  // TC-14: PUT campos vacíos (confirma BUG-02)
  const r5 = await fetch('http://127.0.0.1:8000/usuarios/ana.garcia@empresa.com', {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ nombre: '', apellido: '', correo: 'ana.garcia@empresa.com', contraseña: '' })
  });
  // Esperado: 400 — Obtenido: 200 ❌ BUG

  // TC-15: GET estado actual
  const r6 = await fetch('http://127.0.0.1:8000/usuarios');
  // Esperado: 200 con array de usuarios
});
```

---

## 7. Tabla Resumen de Resultados

| ID     | Caso de Prueba                                | Endpoint                                  | HTTP Esperado | HTTP Obtenido | Resultado |
|--------|-----------------------------------------------|-------------------------------------------|---------------|---------------|-----------|
| TC-01  | Crear usuario con datos válidos               | `POST /usuarios`                          | 200           | 200           | ✅ PASS   |
| TC-02  | Crear usuario con correo duplicado            | `POST /usuarios`                          | 400           | 400           | ✅ PASS   |
| TC-03  | Crear usuario con todos los campos vacíos     | `POST /usuarios`                          | 400           | 400           | ✅ PASS   |
| TC-04  | Correo con formato inválido (HTML5)           | N/A                                       | Sin request   | Sin request   | ✅ PASS   |
| TC-05  | Crear segundo usuario válido                  | `POST /usuarios`                          | 200           | 200           | ✅ PASS   |
| TC-06  | Editar usuario existente                      | `PUT /usuarios/ana.garcia@empresa.com`    | 200           | 200           | ✅ PASS   |
| TC-07  | Cancelar modo edición                         | N/A                                       | Sin request   | Sin request   | ✅ PASS   |
| TC-08  | Eliminar usuario existente                    | `DELETE /usuarios/carlos.ruiz@empresa.com`| 200           | 200           | ✅ PASS   |
| TC-09  | Editar usuario con campos vacíos (UI)         | `PUT /usuarios/ana.garcia@empresa.com`    | 400           | **200** ❌    | ❌ FAIL   |
| TC-10  | Eliminar usuario inexistente                  | `DELETE /usuarios/noexiste@test.com`      | 404           | 404           | ✅ PASS   |
| TC-11  | Editar usuario inexistente                    | `PUT /usuarios/noexiste@test.com`         | 404           | 404           | ✅ PASS   |
| TC-12  | Crear usuario con contraseña corta            | `POST /usuarios`                          | 400           | 400           | ✅ PASS   |
| TC-13  | Crear usuario con correo vacío                | `POST /usuarios`                          | 400           | 400           | ✅ PASS   |
| TC-14  | Actualizar usuario con campos vacíos (API)    | `PUT /usuarios/ana.garcia@empresa.com`    | 400           | **200** ❌    | ❌ FAIL   |
| TC-15  | Consultar lista de usuarios                   | `GET /usuarios`                           | 200           | 200           | ✅ PASS   |

---

## 8. Recomendaciones

### R-01 — Añadir validaciones al método `actualizarUsuario` (Prioridad: Alta)
El servicio `services/user.py` debe validar campos obligatorios y longitud de contraseña al actualizar, igual que al crear. Ver corrección sugerida en BUG-02.

### R-02 — Corregir código HTTP en GET /usuarios vacío (Prioridad: Alta)
Una colección vacía no es un error 404. Retornar `200 OK` con `{"data": []}` es semánticamente correcto y evita que la UI trate la ausencia de registros como un fallo del servidor.

### R-03 — Agregar validación en frontend antes de enviar el formulario de edición (Prioridad: Media)
El formulario de creación no valida campos en el cliente antes de enviar al servidor. Para el caso de edición, añadir validación JavaScript que impida el submit con campos vacíos mejora la experiencia de usuario y reduce llamadas innecesarias al backend.

### R-04 — Añadir diálogo de confirmación antes de eliminar (Prioridad: Media)
El botón "delete" elimina el registro inmediatamente sin pedir confirmación. Un `window.confirm()` o modal evita eliminaciones accidentales.

### R-05 — Mostrar mensaje diferenciado cuando la lista está vacía (Prioridad: Baja)
Si no hay usuarios, la tabla debería mostrar un texto como "No hay usuarios registrados aún" en lugar de estar simplemente vacía.

### R-06 — Validar contraseña mínima también en el frontend (Prioridad: Baja)
La validación de `>= 6 caracteres` solo existe en el backend. Añadirla en el cliente mejora la experiencia.

---

## 9. Conclusión

La aplicación **User Central Management Console** implementa correctamente el flujo CRUD básico para la gestión de usuarios. El **86.7 %** de los casos de prueba pasan sin problemas y la interfaz responde de forma apropiada a los escenarios de éxito y a la mayoría de los casos de error.

Se detectaron **2 bugs de severidad alta** que deben corregirse antes de pasar a producción:

1. **BUG-01**: `GET /usuarios` vacío retorna 404 en lugar de 200 — afecta la carga inicial de la app.
2. **BUG-02**: `PUT /usuarios/{correo}` no valida campos obligatorios — permite corrupción de datos de usuario.

Ambas correcciones son simples y están localizadas en `backend/src/services/user.py`.
