package com.sigr.usuarios.aplicacion;

import com.sigr.usuarios.dominio.Rol;

public record ActualizarUsuarioComando(String id, String nombre, String email, String contrasena, Rol rol) {}
