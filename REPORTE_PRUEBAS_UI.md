# Reporte de Pruebas Automatizadas

## Información General

| Campo | Valor |
|---|---|
| **Fecha y hora de ejecución** | 2026-05-11 00:31 – 00:40 UTC |
| **URL probada** | http://localhost:5173/ |
| **API backend** | http://127.0.0.1:8000 |
| **Herramienta utilizada** | Playwright (MCP) |
| **Navegador utilizado** | Google Chrome 147.0.0.0 |
| **Total de pruebas ejecutadas** | 10 |
| **Pruebas exitosas** | 7 |
| **Pruebas fallidas** | 3 |

---

## Resumen Ejecutivo

| # | Módulo | Caso de Prueba | Método HTTP | Endpoint | Código HTTP | Resultado | Observaciones |
|---|---|---|---|---|---|---|---|
| 1 | Usuarios | Consultar todos los usuarios | GET | /usuarios | 200 | ✅ PASÓ | Datos devueltos correctamente |
| 2 | Usuarios | Crear usuario con datos válidos | POST | /usuarios | 200 | ✅ PASÓ | Usuario creado. Debería retornar 201 |
| 3 | Usuarios | Crear usuario con campos vacíos | POST | /usuarios | 400 | ✅ PASÓ | Backend valida y rechaza |
| 4 | Usuarios | Crear usuario con correo duplicado | POST | /usuarios | 400 | ✅ PASÓ | Backend detecta duplicado |
| 5 | Usuarios | Editar usuario con datos válidos | PUT | /usuarios/:correo | 200 | ✅ PASÓ | Actualización correcta |
| 6 | Usuarios | Editar usuario con campos vacíos | PUT | /usuarios/:correo | 200 | ❌ FALLÓ | **BUG:** Backend acepta nombre/apellido vacíos |
| 7 | Usuarios | Cancelar edición | — | — | — | ✅ PASÓ | Formulario vuelve a modo registro |
| 8 | Usuarios | Eliminar usuario | DELETE | /usuarios/:correo | 200 | ✅ PASÓ | Eliminación correcta |
| 9 | UI | Toggle visibilidad contraseña | — | — | — | ❌ FALLÓ | **BUG:** Input no cambia de tipo password a text |
| 10 | Usuarios | Crear usuario con correo sin formato | POST | /usuarios | — | ⚠️ PARCIAL | Frontend bloquea, backend no valida formato |

---

## Detalle de Pruebas

---

### Prueba 1 — Consultar registros (GET)

- **Objetivo:** Verificar que la tabla de usuarios se carga correctamente al iniciar la aplicación.
- **Pasos ejecutados:**
  1. Navegar a `http://localhost:5173/`
  2. Observar la tabla "User Directory"
  3. Capturar la petición GET al backend
- **Datos utilizados:** Ninguno (solo lectura)
- **Resultado esperado:** Tabla con registros existentes cargada y petición GET con 200 OK
- **Resultado obtenido:** Tabla mostró 2 usuarios preexistentes (`fercho taru` y `juan fermin`). GET retornó 200 OK con JSON `{"mensaje":"datos obtenidos correctamente","data":[...]}`
- **Código HTTP:** `200 OK`
- **Estado final:** ✅ PASÓ

> **Nota de seguridad:** La respuesta incluye las contraseñas en texto plano: `"contraseña":"5456112"` y `"contraseña":"123456"`. Esto es una vulnerabilidad crítica de seguridad.

---

### Prueba 2 — Crear usuario con datos válidos (POST)

- **Objetivo:** Verificar que el formulario de registro crea un usuario correctamente.
- **Pasos ejecutados:**
  1. Rellenar el campo Nombre con `Carlos`
  2. Rellenar el campo Apellido con `Martinez`
  3. Rellenar el campo Correo con `carlos.martinez@empresa.com`
  4. Rellenar el campo Contraseña con `Segura123!`
  5. Hacer clic en "Registrar usuario"
- **Datos utilizados:** `{ nombre: "Carlos", apellido: "Martinez", correo: "carlos.martinez@empresa.com", contraseña: "Segura123!" }`
- **Resultado esperado:** Usuario creado, mensaje de éxito en UI, tabla actualizada con el nuevo registro
- **Resultado obtenido:** Mensaje `"Usuario creado correctamente"` mostrado en UI. Tabla actualizada con la fila de Carlos Martinez. POST retornó 200 con `{"mensaje":"Usuario creado correctamente","correo":"carlos.martinez@empresa.com"}`
- **Código HTTP:** `200 OK`
- **Estado final:** ✅ PASÓ

> **Observación:** El estándar REST recomienda `201 Created` para creación de recursos, no `200 OK`.

---

### Prueba 3 — Crear usuario con campos vacíos (POST)

- **Objetivo:** Verificar que el backend rechaza el registro cuando todos los campos están vacíos.
- **Pasos ejecutados:**
  1. No ingresar ningún dato en el formulario
  2. Hacer clic en "Registrar usuario"
- **Datos utilizados:** `{ nombre: "", apellido: "", correo: "", contraseña: "" }`
- **Resultado esperado:** Backend retorna error 400, UI muestra mensaje de error
- **Resultado obtenido:** Backend retornó 400 con `{"detail":"Los campos no deben estar vacíos"}`. UI mostró el mensaje de error.
- **Código HTTP:** `400 Bad Request`
- **Estado final:** ✅ PASÓ

---

### Prueba 4 — Crear usuario con correo duplicado (POST)

- **Objetivo:** Verificar que el sistema impide registrar dos usuarios con el mismo correo.
- **Pasos ejecutados:**
  1. Ingresar datos válidos usando el correo `carlos.martinez@empresa.com` (ya registrado)
  2. Hacer clic en "Registrar usuario"
- **Datos utilizados:** `{ nombre: "Carlos", apellido: "Duplicado", correo: "carlos.martinez@empresa.com", contraseña: "Pass123!" }`
- **Resultado esperado:** Backend retorna error 400, UI muestra mensaje de error
- **Resultado obtenido:** Backend retornó 400 con `{"detail":"El correo ya está registrado"}`. UI mostró el mensaje de error.
- **Código HTTP:** `400 Bad Request`
- **Estado final:** ✅ PASÓ

---

### Prueba 5 — Editar usuario con datos válidos (PUT)

- **Objetivo:** Verificar que el formulario de edición actualiza correctamente un usuario.
- **Pasos ejecutados:**
  1. Hacer clic en botón "edit" del usuario `Carlos Martinez`
  2. Verificar que el formulario carga los datos actuales del usuario
  3. Modificar el campo Apellido a `Martinez-Actualizado`
  4. Hacer clic en "Actualizar usuario"
- **Datos utilizados:** `{ nombre: "Carlos", apellido: "Martinez-Actualizado", correo: "carlos.martinez@empresa.com", contraseña: "Segura123!" }`
- **Resultado esperado:** Usuario actualizado, mensaje de éxito, tabla refleja el cambio
- **Resultado obtenido:** Formulario cargó datos preexistentes correctamente. PUT a `/usuarios/carlos.martinez@empresa.com` retornó 200 con `{"mensaje":"Usuario actualizado correctamente"}`. Tabla actualizó el apellido.
- **Código HTTP:** `200 OK`
- **Estado final:** ✅ PASÓ

---

### Prueba 6 — Editar usuario con campos vacíos (PUT) — BUG

- **Objetivo:** Verificar que el backend rechaza la actualización cuando nombre y apellido están vacíos.
- **Pasos ejecutados:**
  1. Hacer clic en botón "edit" del usuario `Carlos Martinez-Actualizado`
  2. Borrar el campo Nombre (dejarlo vacío)
  3. Borrar el campo Apellido (dejarlo vacío)
  4. Hacer clic en "Actualizar usuario"
- **Datos utilizados:** `{ nombre: "", apellido: "", correo: "carlos.martinez@empresa.com", contraseña: "Segura123!" }`
- **Resultado esperado:** Backend retorna error 400 con mensaje de validación
- **Resultado obtenido:** Backend retornó **200 OK** con `{"mensaje":"Usuario actualizado correctamente"}`. El usuario quedó con nombre y apellido vacíos en la base de datos, mostrando celdas vacías en la tabla.
- **Código HTTP:** `200 OK` _(incorrecto — debería ser 400)_
- **Estado final:** ❌ FALLÓ

---

### Prueba 7 — Cancelar edición

- **Objetivo:** Verificar que el botón "Cancelar" descarta los cambios y restaura el formulario al modo de registro.
- **Pasos ejecutados:**
  1. Hacer clic en botón "edit" de cualquier usuario
  2. Hacer clic en el botón "Cancelar"
- **Datos utilizados:** Ninguno
- **Resultado esperado:** Formulario vuelve al modo "Registrar usuario" sin guardar cambios, botón "Registrar usuario" reaparece
- **Resultado obtenido:** El formulario se limpió y volvió al modo registro correctamente. No se realizó ninguna petición HTTP al backend.
- **Código HTTP:** Ninguno
- **Estado final:** ✅ PASÓ

---

### Prueba 8 — Eliminar usuario (DELETE)

- **Objetivo:** Verificar que el botón "delete" elimina un usuario correctamente.
- **Pasos ejecutados:**
  1. Hacer clic en el botón "delete" del usuario con correo `carlos.martinez@empresa.com`
  2. Verificar la respuesta y el estado de la tabla
- **Datos utilizados:** Correo `carlos.martinez@empresa.com` (extraído del registro)
- **Resultado esperado:** Usuario eliminado, mensaje de confirmación, fila desaparece de la tabla
- **Resultado obtenido:** DELETE a `/usuarios/carlos.martinez@empresa.com` retornó 200 con `{"mensaje":"Usuario eliminado correctamente"}`. La fila desapareció de la tabla. Tabla quedó con 2 registros.
- **Código HTTP:** `200 OK`
- **Estado final:** ✅ PASÓ

> **Observación:** No hay diálogo de confirmación antes de eliminar. Un clic accidental borra el registro permanentemente.

---

### Prueba 9 — Toggle visibilidad de contraseña — BUG

- **Objetivo:** Verificar que el botón de ojo ("visibility") alterna el campo de contraseña entre tipo `password` y `text`.
- **Pasos ejecutados:**
  1. Escribir `MiClave123` en el campo Contraseña
  2. Verificar que el tipo del input es `password` (valor oculto)
  3. Hacer clic en el botón "visibility"
  4. Verificar que el tipo del input cambió a `text` (valor visible)
- **Datos utilizados:** Contraseña: `MiClave123`
- **Resultado esperado:** Después del clic, el input cambia de `type="password"` a `type="text"` mostrando la contraseña en texto plano
- **Resultado obtenido:** El tipo del input permaneció en `password` antes y después del clic. La contraseña no se hace visible. El botón recibe el estado `[active]` pero no ejecuta el cambio de tipo.
- **Código HTTP:** N/A
- **Estado final:** ❌ FALLÓ

---

### Prueba 10 — Crear usuario con correo sin formato válido

- **Objetivo:** Verificar el comportamiento del sistema ante un correo sin el símbolo `@`.
- **Pasos ejecutados:**
  1. Completar el formulario con correo `correo-sin-arroba`
  2. Hacer clic en "Registrar usuario"
- **Datos utilizados:** `{ nombre: "Test", apellido: "Invalido", correo: "correo-sin-arroba", contraseña: "Pass123" }`
- **Resultado esperado:** El sistema rechaza el correo inválido con un mensaje de error
- **Resultado obtenido:** El navegador bloqueó el envío gracias al atributo HTML5 `type="email"` en el input. No se realizó ninguna petición HTTP al backend. **Sin embargo, la validación solo existe en el frontend.**
- **Código HTTP:** Ninguno (bloqueado por validación HTML5)
- **Estado final:** ⚠️ PARCIAL — Validación solo en cliente, no en servidor

> **Evidencia de vulnerabilidad backend:** Uno de los usuarios preexistentes (`juan fermin`) tiene el correo `joseesapelgmail.com` (sin `@`), lo que confirma que el endpoint POST no valida el formato del correo a nivel de backend.

---

## Código de las Pruebas Automatizadas

```javascript
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext();
  const page = await context.newPage();
  const BASE_URL = 'http://localhost:5173';
  const API_URL = 'http://127.0.0.1:8000';

  const results = [];
  const log = (test, status, http, obs) => results.push({ test, status, http, obs });

  // ─── PRUEBA 1: Consultar registros ──────────────────────────────────────────
  await page.goto(BASE_URL);
  await page.waitForResponse(r => r.url().includes('/usuarios') && r.request().method() === 'GET');
  const rows = await page.locator('table tbody tr').count();
  log('Consultar registros', rows > 0 ? 'PASÓ' : 'FALLÓ', 200, `${rows} usuario(s) encontrado(s)`);

  // ─── PRUEBA 2: Crear usuario con datos válidos ───────────────────────────────
  await page.getByRole('textbox', { name: 'Nombre' }).fill('Carlos');
  await page.getByRole('textbox', { name: 'Apellido' }).fill('Martinez');
  await page.getByRole('textbox', { name: 'Correo' }).fill('carlos.martinez@empresa.com');
  await page.getByRole('textbox', { name: 'Contraseña' }).fill('Segura123!');
  const [postRes] = await Promise.all([
    page.waitForResponse(r => r.url().includes('/usuarios') && r.request().method() === 'POST'),
    page.getByRole('button', { name: 'Registrar usuario' }).click()
  ]);
  const postBody = await postRes.json();
  log('Crear usuario (datos válidos)', postRes.status() === 200 ? 'PASÓ' : 'FALLÓ', postRes.status(), postBody.mensaje);

  // ─── PRUEBA 3: Crear usuario con campos vacíos ───────────────────────────────
  const [emptyRes] = await Promise.all([
    page.waitForResponse(r => r.url().includes('/usuarios') && r.request().method() === 'POST'),
    page.getByRole('button', { name: 'Registrar usuario' }).click()
  ]);
  const emptyBody = await emptyRes.json();
  log('Crear usuario (campos vacíos)', emptyRes.status() === 400 ? 'PASÓ' : 'FALLÓ', emptyRes.status(), emptyBody.detail);

  // ─── PRUEBA 4: Crear usuario con correo duplicado ────────────────────────────
  await page.getByRole('textbox', { name: 'Nombre' }).fill('Carlos');
  await page.getByRole('textbox', { name: 'Apellido' }).fill('Duplicado');
  await page.getByRole('textbox', { name: 'Correo' }).fill('carlos.martinez@empresa.com');
  await page.getByRole('textbox', { name: 'Contraseña' }).fill('Pass123!');
  const [dupRes] = await Promise.all([
    page.waitForResponse(r => r.url().includes('/usuarios') && r.request().method() === 'POST'),
    page.getByRole('button', { name: 'Registrar usuario' }).click()
  ]);
  const dupBody = await dupRes.json();
  log('Crear usuario (correo duplicado)', dupRes.status() === 400 ? 'PASÓ' : 'FALLÓ', dupRes.status(), dupBody.detail);

  // ─── PRUEBA 5: Editar usuario con datos válidos ──────────────────────────────
  await page.getByRole('button', { name: 'edit' }).nth(2).click();
  await page.getByRole('textbox', { name: 'Apellido' }).fill('Martinez-Actualizado');
  const [putRes] = await Promise.all([
    page.waitForResponse(r => r.url().includes('/usuarios/') && r.request().method() === 'PUT'),
    page.getByRole('button', { name: 'Actualizar usuario' }).click()
  ]);
  const putBody = await putRes.json();
  log('Editar usuario (datos válidos)', putRes.status() === 200 ? 'PASÓ' : 'FALLÓ', putRes.status(), putBody.mensaje);

  // ─── PRUEBA 6: Editar usuario con campos vacíos (BUG) ───────────────────────
  await page.getByRole('button', { name: 'edit' }).nth(2).click();
  await page.getByRole('textbox', { name: 'Nombre' }).fill('');
  await page.getByRole('textbox', { name: 'Apellido' }).fill('');
  const [putEmptyRes] = await Promise.all([
    page.waitForResponse(r => r.url().includes('/usuarios/') && r.request().method() === 'PUT'),
    page.getByRole('button', { name: 'Actualizar usuario' }).click()
  ]);
  const putEmptyBody = await putEmptyRes.json();
  log('Editar usuario (campos vacíos)', putEmptyRes.status() === 400 ? 'PASÓ' : 'FALLÓ',
    putEmptyRes.status(), `BUG: ${putEmptyBody.mensaje} — debería ser 400`);

  // ─── PRUEBA 7: Cancelar edición ──────────────────────────────────────────────
  await page.getByRole('button', { name: 'edit' }).nth(2).click();
  await page.getByRole('button', { name: 'Cancelar' }).click();
  const isRegisterMode = await page.getByRole('button', { name: 'Registrar usuario' }).isVisible();
  log('Cancelar edición', isRegisterMode ? 'PASÓ' : 'FALLÓ', 'N/A', 'Formulario vuelve a modo registro');

  // ─── PRUEBA 8: Eliminar usuario ──────────────────────────────────────────────
  const [deleteRes] = await Promise.all([
    page.waitForResponse(r => r.url().includes('/usuarios/') && r.request().method() === 'DELETE'),
    page.getByRole('button', { name: 'delete' }).nth(2).click()
  ]);
  const deleteBody = await deleteRes.json();
  log('Eliminar usuario', deleteRes.status() === 200 ? 'PASÓ' : 'FALLÓ', deleteRes.status(), deleteBody.mensaje);

  // ─── PRUEBA 9: Toggle visibilidad contraseña (BUG) ──────────────────────────
  await page.getByRole('textbox', { name: 'Contraseña' }).fill('MiClave123');
  const typeBefore = await page.evaluate(() =>
    document.querySelector('input[placeholder="••••••••"]')?.type
  );
  await page.getByRole('button', { name: 'visibility' }).click();
  const typeAfter = await page.evaluate(() =>
    document.querySelector('input[placeholder="••••••••"]')?.type
  );
  log('Toggle visibilidad contraseña', typeAfter === 'text' ? 'PASÓ' : 'FALLÓ', 'N/A',
    `BUG: tipo antes=${typeBefore}, después=${typeAfter} (debería ser 'text')`);

  // ─── PRUEBA 10: Correo inválido (validación HTML5 frontend) ─────────────────
  await page.getByRole('textbox', { name: 'Nombre' }).fill('Test');
  await page.getByRole('textbox', { name: 'Apellido' }).fill('Invalido');
  await page.getByRole('textbox', { name: 'Correo' }).fill('correo-sin-arroba');
  await page.getByRole('textbox', { name: 'Contraseña' }).fill('Pass123');
  const requestSent = await new Promise(resolve => {
    let sent = false;
    page.on('request', req => { if (req.method() === 'POST') sent = true; });
    page.getByRole('button', { name: 'Registrar usuario' }).click().then(() => {
      setTimeout(() => resolve(sent), 1000);
    });
  });
  log('Correo inválido (sin @)', !requestSent ? 'PARCIAL' : 'FALLÓ', 'N/A',
    'Frontend bloquea, backend no valida formato de correo');

  // ─── REPORTE CONSOLA ─────────────────────────────────────────────────────────
  console.table(results);
  await browser.close();
})();
```

---

## Errores Encontrados

### BUG-01 — PUT /usuarios acepta nombre y apellido vacíos (CRÍTICO)

- **Endpoint:** `PUT http://127.0.0.1:8000/usuarios/:correo`
- **Comportamiento actual:** El backend retorna `200 OK` y guarda el usuario con `nombre: ""` y `apellido: ""`.
- **Comportamiento esperado:** Retornar `400 Bad Request` con mensaje `"Los campos no deben estar vacíos"`.
- **Impacto:** Corrupción de datos. Usuarios quedan con nombre y apellido en blanco en la base de datos.
- **Causa probable:** El endpoint PUT no reutiliza la misma lógica de validación de campos vacíos que el endpoint POST.

---

### BUG-02 — Toggle de visibilidad de contraseña no funciona (MEDIO)

- **Componente:** Botón `visibility` en el campo Contraseña.
- **Comportamiento actual:** El input mantiene `type="password"` después de hacer clic. La contraseña no se muestra.
- **Comportamiento esperado:** Al hacer clic, el input alterna entre `type="password"` y `type="text"`.
- **Causa probable:** El manejador del evento `onClick` del botón no está actualizando correctamente el estado React que controla el tipo del input, o hay un bug en la condición del estado booleano `showPassword`.

---

### BUG-03 — Backend no valida formato de correo electrónico (ALTO)

- **Endpoints afectados:** `POST /usuarios`, `PUT /usuarios/:correo`
- **Comportamiento actual:** El backend acepta correos con formato inválido (sin `@`). Evidencia: el usuario `juan fermin` tiene correo `joseesapelgmail.com` en la base de datos.
- **Comportamiento esperado:** Rechazar correos que no cumplan el formato `nombre@dominio.tld`.
- **Causa probable:** Sin validación de formato en el backend. Solo existe la validación `type="email"` del HTML5, que puede ser omitida mediante peticiones directas a la API.

---

### BUG-04 — POST /usuarios retorna 200 en lugar de 201 (BAJO)

- **Endpoint:** `POST http://127.0.0.1:8000/usuarios`
- **Comportamiento actual:** Retorna `200 OK` al crear un recurso nuevo.
- **Comportamiento esperado:** Retornar `201 Created` según el estándar REST.
- **Impacto:** Bajo impacto funcional, pero viola las convenciones REST y puede confundir a consumidores de la API.

---

### BUG-05 — Contraseñas expuestas en texto plano en GET /usuarios (CRÍTICO - SEGURIDAD)

- **Endpoint:** `GET http://127.0.0.1:8000/usuarios`
- **Comportamiento actual:** La respuesta incluye el campo `contraseña` con el valor en texto plano: `"contraseña":"5456112"`.
- **Comportamiento esperado:** Las contraseñas deben almacenarse con hash (bcrypt/argon2) y nunca devolverse en ninguna respuesta de la API.
- **Impacto:** Cualquier persona con acceso a la red puede leer todas las contraseñas. Vulnerabilidad OWASP A02:2021 – Cryptographic Failures.

---

### BUG-06 — Sin confirmación antes de eliminar (MEDIO - UX)

- **Componente:** Botón `delete` en la tabla de usuarios.
- **Comportamiento actual:** Al hacer clic en `delete`, el usuario se elimina inmediatamente sin pedir confirmación.
- **Comportamiento esperado:** Mostrar un diálogo de confirmación (`"¿Está seguro de eliminar este usuario?"`) antes de ejecutar el DELETE.
- **Impacto:** Un clic accidental elimina datos de forma irreversible.

---

## Recomendaciones

1. **Validar campos en endpoint PUT:** Agregar la misma validación de campos vacíos que existe en el POST al endpoint PUT del backend. Ejemplo en FastAPI:
   ```python
   if not usuario.nombre.strip() or not usuario.apellido.strip():
       raise HTTPException(status_code=400, detail="Los campos no deben estar vacíos")
   ```

2. **Corregir toggle de contraseña:** Revisar el estado React del componente. El botón debe alternar un estado `showPassword` (booleano) y el input debe usar `type={showPassword ? 'text' : 'password'}`. Verificar que el `onClick` del botón llame a `setShowPassword(prev => !prev)`.

3. **Validar formato de correo en backend:** Agregar validación con regex o usando la librería `email-validator`. En FastAPI con Pydantic usar `EmailStr`:
   ```python
   from pydantic import EmailStr
   class Usuario(BaseModel):
       correo: EmailStr
   ```

4. **Corregir códigos HTTP REST:** Cambiar la respuesta del POST de `200` a `201 Created` usando `return JSONResponse(status_code=201, content={...})`.

5. **Hashear contraseñas:** Nunca almacenar ni retornar contraseñas en texto plano. Usar `bcrypt` o `passlib`:
   ```python
   from passlib.context import CryptContext
   pwd_context = CryptContext(schemes=["bcrypt"])
   hashed = pwd_context.hash(usuario.contraseña)
   ```
   Además, excluir el campo `contraseña` de todas las respuestas GET.

6. **Agregar confirmación de borrado:** Antes de ejecutar el DELETE, mostrar un diálogo nativo (`window.confirm`) o un modal personalizado que requiera confirmación explícita del usuario.

7. **Agregar validación de contraseña mínima:** Actualmente no hay validación de longitud o complejidad de contraseña. Establecer mínimo 8 caracteres con al menos una letra y un número.

---

## Conclusión

La aplicación **User Central - Management Console** cumple con el flujo básico de operaciones CRUD: registrar, consultar, editar y eliminar usuarios funciona en el camino feliz. Sin embargo, se identificaron **6 defectos** — 2 de ellos críticos en materia de seguridad y consistencia de datos.

El problema más grave es la **exposición de contraseñas en texto plano** (BUG-05), que representa una vulnerabilidad de seguridad severa que debe corregirse antes de cualquier despliegue en producción. El segundo problema prioritario es la **falta de validación en el endpoint PUT** (BUG-01), que permite corromper datos dejando usuarios con campos vacíos.

La ausencia de validación de formato de correo en el backend (BUG-03) también es un riesgo alto, ya que la validación actual solo reside en el frontend y puede saltarse con peticiones directas a la API.

**Evaluación general: La aplicación NO está lista para producción.** Se recomienda corregir los bugs críticos (BUG-01, BUG-03, BUG-05) como mínimo antes de continuar con el desarrollo de nuevas funcionalidades.

---

*Reporte generado automáticamente mediante Playwright (MCP) el 2026-05-11.*
