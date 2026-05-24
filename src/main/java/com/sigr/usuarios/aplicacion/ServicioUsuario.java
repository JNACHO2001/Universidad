package com.sigr.usuarios.aplicacion;

import com.sigr.usuarios.dominio.Rol;
import com.sigr.usuarios.dominio.RepositorioUsuario;
import com.sigr.usuarios.dominio.Usuario;
import org.springframework.stereotype.Service;

import java.util.UUID;

@Service
public class ServicioUsuario {

    private final RepositorioUsuario repositorio;

    public ServicioUsuario(RepositorioUsuario repositorio) {
        this.repositorio = repositorio;
    }

    public String crear(CrearUsuarioComando cmd) {
        if (repositorio.existePorEmail(cmd.email())) {
            throw new EmailDuplicadoException(cmd.email());
        }
        String id = UUID.randomUUID().toString();
        Usuario usuario = new Usuario(id, cmd.nombre(), cmd.email(), cmd.contrasena(), cmd.rol());
        repositorio.guardar(usuario);
        return id;
    }

    public void actualizar(ActualizarUsuarioComando cmd) {
        Usuario usuario = repositorio.buscarPorId(cmd.id())
                .orElseThrow(() -> new UsuarioNoEncontradoException(cmd.id()));

        if (cmd.nombre() != null) usuario.actualizarNombre(cmd.nombre());
        if (cmd.email() != null) {
            boolean emailCambiado = !cmd.email().equals(usuario.getEmail());
            if (emailCambiado && repositorio.existePorEmail(cmd.email())) {
                throw new EmailDuplicadoException(cmd.email());
            }
            usuario.actualizarEmail(cmd.email());
        }
        if (cmd.contrasena() != null) usuario.actualizarContrasena(cmd.contrasena());
        if (cmd.rol() != null) usuario.actualizarRol(cmd.rol());

        repositorio.guardar(usuario);
    }

    public void eliminar(String id) {
        if (repositorio.buscarPorId(id).isEmpty()) {
            throw new UsuarioNoEncontradoException(id);
        }
        repositorio.eliminar(id);
    }

    public Usuario buscar(String id) {
        return repositorio.buscarPorId(id)
                .orElseThrow(() -> new UsuarioNoEncontradoException(id));
    }
}
