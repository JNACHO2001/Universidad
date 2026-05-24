package com.sigr.usuarios.dominio;

import java.util.Optional;

public interface RepositorioUsuario {
    void guardar(Usuario usuario);
    Optional<Usuario> buscarPorId(String id);
    Optional<Usuario> buscarPorEmail(String email);
    void eliminar(String id);
    boolean existePorEmail(String email);
}
