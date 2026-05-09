<script setup>
import { ref, onMounted } from 'vue'
import { obtenerUsuarios } from '../api/api'

const Usuarios = ref([])

onMounted(async () => {
  try {
    Usuarios.value = await obtenerUsuarios()
  } catch (e) {
    console.error(e)
  }
})
</script>

<template>
  <div class="page">

    <!-- Formulario -->
    <section class="register-card">
      <h2>Registrar Usuario</h2>
      <form class="register-form">
        <div class="field">
          <label for="nombre">Nombre</label>
          <input id="nombre" type="text" placeholder="Ej. Alejandro" />
        </div>
        <div class="field">
          <label for="apellido">Apellido</label>
          <input id="apellido" type="text" placeholder="Ej. Rodriguez" />
        </div>
        <div class="field field--full">
          <label for="correo">Correo</label>
          <input id="correo" type="email" placeholder="alejandro@empresa.com" />
        </div>
        <div class="field field--full">
          <label for="password">Contraseña</label>
          <div class="password-wrapper">
            <input id="password" type="password" placeholder="••••••••" />
            <button type="button" class="toggle-password">
              <span class="material-symbols-outlined">visibility</span>
            </button>
          </div>
        </div>
        <div class="field field--full form-actions">
          <button type="submit" class="btn-primary">Registrar</button>
        </div>
      </form>
    </section>

    <!-- Tabla -->
    <section class="directory-card">
      <h2>User Directory</h2>
      <table class="user-table">
        <thead>
          <tr>
            <th>Usuario</th>
            <th>Email</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="Usuario in Usuarios" :key="Usuario.id">
            <td>
              <div class="user-cell">
                {{ Usuario.nombre }}
              </div>
            </td>
            <td>{{ Usuario.correo }}</td>
            <td>
              <button class="btn-edit" title="Editar"><span class="material-symbols-outlined">edit</span></button>
              <button class="btn-delete" title="Eliminar"><span class="material-symbols-outlined">delete</span></button>
            </td>
          </tr>
        </tbody>
      </table>
    </section>

  </div>
</template>

