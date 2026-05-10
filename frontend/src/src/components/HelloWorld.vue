<script setup>
import { ref, onMounted } from "vue";
import {
  obtenerUsuarios,
  eliminarUsuario,
  crearUsuario,
  editarUsuario,
} from "../api/api";

// Lista reactiva de usuarios que alimenta la tabla
const Usuarios = ref([]);

// Controla si el formulario está en modo edición o creación
const modoedicion = ref(false);

// Mensajes de feedback visibles al usuario tras cada operación
const mensajeError = ref("");
const mensajeExito = ref("");

// Copia los datos del usuario seleccionado al formulario y activa modo edición
const seleccionarUsuario = (datosUsuario) => {
  usuario.value = { ...datosUsuario };
  modoedicion.value = true;
};

// Vacía el formulario y vuelve al modo creación
const limpiarFormulario = () => {
  usuario.value = {
    nombre: "",
    apellido: "",
    correo: "",
    contraseña: "",
  };
  modoedicion.value = false;
};

// Modelo del formulario enlazado con v-model
const usuario = ref({
  nombre: "",
  apellido: "",
  correo: "",
  contraseña: "",
});

// Recarga la tabla desde el backend
const cargarUsuarios = async () => {
  Usuarios.value = await obtenerUsuarios();
};

// Crea o actualiza un usuario según el modo activo, luego limpia el formulario
const guardarUsuario = async () => {
  mensajeError.value = "";
  mensajeExito.value = "";
  try {
    if (modoedicion.value) {
      await editarUsuario(usuario.value.correo, usuario.value);
      await cargarUsuarios();
      mensajeExito.value = "Usuario actualizado correctamente";
    } else {
      await crearUsuario(usuario.value);
      await cargarUsuarios();
      mensajeExito.value = "Usuario creado correctamente";
    }
    limpiarFormulario();
  } catch (error) {
    // El mensaje viene del backend via manejarError en api.js
    mensajeError.value = error.message;
  }
};

// Elimina el usuario y lo quita de la lista local sin recargar toda la tabla
const eliminar = async (correo) => {
  mensajeError.value = "";
  mensajeExito.value = "";
  try {
    await eliminarUsuario(correo);
    Usuarios.value = Usuarios.value.filter((u) => u.correo !== correo);
    mensajeExito.value = "Usuario eliminado correctamente";
  } catch (error) {
    mensajeError.value = error.message;
  }
};

// Carga los usuarios al montar el componente por primera vez
onMounted(async () => {
  try {
    Usuarios.value = await obtenerUsuarios();
  } catch (e) {
    console.error(e);
  }
});
</script>

<template>
  <div class="page">
    <!-- Mensajes de feedback -->
    <p v-if="mensajeExito" class="msg msg--exito">{{ mensajeExito }}</p>
    <p v-if="mensajeError" class="msg msg--error">{{ mensajeError }}</p>

    <!-- Formulario: sirve tanto para crear como para editar según modoedicion -->
    <section class="register-card">
      <h2>Registrar Usuario</h2>
      <form class="register-form" @submit.prevent="guardarUsuario">
        <div class="field">
          <label for="nombre">Nombre</label>
          <input
            id="nombre"
            type="text"
            placeholder="Ej. Alejandro"
            v-model="usuario.nombre"
          />
        </div>
        <div class="field">
          <label for="apellido">Apellido</label>
          <input
            id="apellido"
            type="text"
            placeholder="Ej. Rodriguez"
            v-model="usuario.apellido"
          />
        </div>
        <div class="field field--full">
          <label for="correo">Correo</label>
          <input
            id="correo"
            type="email"
            placeholder="alejandro@empresa.com"
            v-model="usuario.correo"
          />
        </div>
        <div class="field field--full">
          <label for="password">Contraseña</label>
          <div class="password-wrapper">
            <input
              id="password"
              type="password"
              placeholder="••••••••"
              v-model="usuario.contraseña"
            />
            <button type="button" class="toggle-password">
              <span class="material-symbols-outlined">visibility</span>
            </button>
          </div>
        </div>
        <div class="field field--full form-actions">
          <!-- Solo aparece en modo edición para cancelar sin guardar -->
          <button v-if="modoedicion" type="button" class="btn-cancelar" @click="limpiarFormulario">
            Cancelar
          </button>
          <!-- El texto cambia según el modo activo -->
          <button type="submit" class="btn-primary">
            {{ modoedicion ? "Actualizar usuario" : "Registrar usuario" }}
          </button>
        </div>
      </form>
    </section>

    <!-- Tabla de usuarios con acciones de editar y eliminar -->
    <section class="directory-card">
      <h2>User Directory</h2>
      <table class="user-table">
        <thead>
          <tr>
            <th>Nombre</th>
            <th>Apellido</th>
            <th>Correo</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="Usuario in Usuarios" :key="Usuario.correo">
            <td>
              <div class="user-cell">
                {{ Usuario.nombre }}
              </div>
            </td>
            <td>{{ Usuario.apellido }}</td>
            <td>{{ Usuario.correo }}</td>
            <td>
              <!-- Carga el usuario en el formulario para editar -->
              <button type="button" class="btn-edit" title="Editar" @click="seleccionarUsuario(Usuario)">
                <span class="material-symbols-outlined">edit</span>
              </button>
              <!-- Elimina directamente sin confirmación -->
              <button
                type="button"
                class="btn-delete"
                title="Eliminar"
                @click="eliminar(Usuario.correo)"
              >
                <span class="material-symbols-outlined">delete</span>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </section>
  </div>
</template>
