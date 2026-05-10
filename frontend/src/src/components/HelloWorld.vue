<script setup>
import { ref, onMounted } from "vue";
import {
  obtenerUsuarios,
  eliminarUsuario,
  crearUsuario,
  editarUsuario,
} from "../api/api";

const Usuarios = ref([]);
const modoedicion = ref(false);
const mensajeError = ref("");
const mensajeExito = ref("");

const seleccionarUsuario = (datosUsuario) => {
  usuario.value = { ...datosUsuario };
  modoedicion.value = true;
};

const limpiarFormulario = () => {
  usuario.value = {
    nombre: "",
    apellido: "",
    correo: "",
    contraseña: "",
  };

  modoedicion.value = false;
};

const usuario = ref({
  nombre: "",
  apellido: "",
  correo: "",
  contraseña: "",
});

const cargarUsuarios = async () => {
  Usuarios.value = await obtenerUsuarios();
};

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
    mensajeError.value = error.message;
  }
};

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
    <!-- Mensajes -->
    <p v-if="mensajeExito" class="msg msg--exito">{{ mensajeExito }}</p>
    <p v-if="mensajeError" class="msg msg--error">{{ mensajeError }}</p>

    <!-- Formulario -->
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
          <button v-if="modoedicion" type="button" class="btn-cancelar" @click="limpiarFormulario">
            Cancelar
          </button>
          <button type="submit" class="btn-primary">
            {{ modoedicion ? "Actualizar usuario" : "Registrar usuario" }}
          </button>
        </div>
      </form>
    </section>

    <!-- Tabla -->
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
              <button type="button" class="btn-edit" title="Editar" @click="seleccionarUsuario(Usuario)">
                <span class="material-symbols-outlined">edit</span>
              </button>
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
