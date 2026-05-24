package com.sigr.usuarios.infraestructura;

import com.sigr.usuarios.aplicacion.*;
import com.sigr.usuarios.dominio.Rol;
import com.sigr.usuarios.dominio.Usuario;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/api/usuarios")
public class ControladorUsuario {

    private final ServicioUsuario servicio;

    public ControladorUsuario(ServicioUsuario servicio) {
        this.servicio = servicio;
    }

    @PostMapping
    public ResponseEntity<Map<String, String>> crear(@RequestBody CrearRequest req) {
        String id = servicio.crear(new CrearUsuarioComando(req.nombre(), req.email(), req.contrasena(), Rol.valueOf(req.rol())));
        return ResponseEntity.status(HttpStatus.CREATED).body(Map.of("id", id));
    }

    @PutMapping("/{id}")
    public ResponseEntity<Void> actualizar(@PathVariable String id, @RequestBody ActualizarRequest req) {
        Rol rol = req.rol() != null ? Rol.valueOf(req.rol()) : null;
        servicio.actualizar(new ActualizarUsuarioComando(id, req.nombre(), req.email(), req.contrasena(), rol));
        return ResponseEntity.noContent().build();
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> eliminar(@PathVariable String id) {
        servicio.eliminar(id);
        return ResponseEntity.noContent().build();
    }

    @GetMapping("/{id}")
    public ResponseEntity<UsuarioResponse> buscar(@PathVariable String id) {
        Usuario u = servicio.buscar(id);
        return ResponseEntity.ok(new UsuarioResponse(u.getId(), u.getNombre(), u.getEmail(), u.getRol().name()));
    }

    @ExceptionHandler(UsuarioNoEncontradoException.class)
    public ResponseEntity<Map<String, String>> manejarNoEncontrado(UsuarioNoEncontradoException ex) {
        return ResponseEntity.status(HttpStatus.NOT_FOUND).body(Map.of("error", ex.getMessage()));
    }

    @ExceptionHandler(EmailDuplicadoException.class)
    public ResponseEntity<Map<String, String>> manejarEmailDuplicado(EmailDuplicadoException ex) {
        return ResponseEntity.status(HttpStatus.CONFLICT).body(Map.of("error", ex.getMessage()));
    }

    record CrearRequest(String nombre, String email, String contrasena, String rol) {}
    record ActualizarRequest(String nombre, String email, String contrasena, String rol) {}
    record UsuarioResponse(String id, String nombre, String email, String rol) {}
}
