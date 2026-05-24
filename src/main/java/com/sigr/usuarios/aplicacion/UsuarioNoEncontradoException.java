package com.sigr.usuarios.aplicacion;

public class UsuarioNoEncontradoException extends RuntimeException {
    public UsuarioNoEncontradoException(String id) {
        super("Usuario no encontrado: " + id);
    }
}
