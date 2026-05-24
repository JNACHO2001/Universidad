package com.sigr.usuarios.dominio;

import java.util.Objects;

public class Usuario {

    private final String id;
    private String nombre;
    private String email;
    private String contrasena;
    private Rol rol;

    public Usuario(String id, String nombre, String email, String contrasena, Rol rol) {
        if (nombre == null || nombre.isBlank()) throw new IllegalArgumentException("El nombre es obligatorio");
        if (email == null || !email.contains("@")) throw new IllegalArgumentException("Email inválido");
        if (contrasena == null || contrasena.length() < 6) throw new IllegalArgumentException("La contraseña debe tener al menos 6 caracteres");
        this.id = Objects.requireNonNull(id, "El id es obligatorio");
        this.nombre = nombre;
        this.email = email;
        this.contrasena = contrasena;
        this.rol = Objects.requireNonNull(rol, "El rol es obligatorio");
    }

    public void actualizarNombre(String nombre) {
        if (nombre == null || nombre.isBlank()) throw new IllegalArgumentException("El nombre es obligatorio");
        this.nombre = nombre;
    }

    public void actualizarEmail(String email) {
        if (email == null || !email.contains("@")) throw new IllegalArgumentException("Email inválido");
        this.email = email;
    }

    public void actualizarContrasena(String contrasena) {
        if (contrasena == null || contrasena.length() < 6) throw new IllegalArgumentException("La contraseña debe tener al menos 6 caracteres");
        this.contrasena = contrasena;
    }

    public void actualizarRol(Rol rol) {
        this.rol = Objects.requireNonNull(rol, "El rol es obligatorio");
    }

    public String getId() { return id; }
    public String getNombre() { return nombre; }
    public String getEmail() { return email; }
    public String getContrasena() { return contrasena; }
    public Rol getRol() { return rol; }
}
