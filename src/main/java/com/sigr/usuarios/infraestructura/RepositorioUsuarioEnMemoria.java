package com.sigr.usuarios.infraestructura;

import com.sigr.usuarios.dominio.RepositorioUsuario;
import com.sigr.usuarios.dominio.Usuario;
import org.springframework.stereotype.Repository;

import java.util.HashMap;
import java.util.Map;
import java.util.Optional;

@Repository
public class RepositorioUsuarioEnMemoria implements RepositorioUsuario {

    private final Map<String, Usuario> almacen = new HashMap<>();

    @Override
    public void guardar(Usuario usuario) {
        almacen.put(usuario.getId(), usuario);
    }

    @Override
    public Optional<Usuario> buscarPorId(String id) {
        return Optional.ofNullable(almacen.get(id));
    }

    @Override
    public Optional<Usuario> buscarPorEmail(String email) {
        return almacen.values().stream()
                .filter(u -> u.getEmail().equals(email))
                .findFirst();
    }

    @Override
    public void eliminar(String id) {
        almacen.remove(id);
    }

    @Override
    public boolean existePorEmail(String email) {
        return almacen.values().stream()
                .anyMatch(u -> u.getEmail().equals(email));
    }
}
