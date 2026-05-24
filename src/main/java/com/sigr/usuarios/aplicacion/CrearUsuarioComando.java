package com.sigr.usuarios.aplicacion;

import com.sigr.usuarios.dominio.Rol;

public record CrearUsuarioComando(String nombre, String email, String contrasena, Rol rol) {}
