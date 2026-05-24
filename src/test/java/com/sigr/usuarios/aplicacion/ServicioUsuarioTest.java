package com.sigr.usuarios.aplicacion;

/**
 * Tests unitarios de ServicioUsuario.
 *
 * Estrategia de prueba:
 *   - Se usa Mockito para simular el repositorio, de modo que los tests
 *     no dependan de base de datos ni de ninguna infraestructura externa.
 *   - Cada test sigue la estructura DADO / CUANDO / ENTONCES:
 *       DADO    → condición inicial del sistema antes de la acción
 *       CUANDO  → acción que se ejecuta sobre el servicio
 *       ENTONCES→ resultado esperado (valor retornado, excepción lanzada,
 *                 o método del repositorio que debió o no debió llamarse)
 *
 * Cobertura:
 *   crear()     → 3 tests (flujo feliz, email duplicado, datos inválidos)
 *   actualizar()→ 4 tests (flujo feliz, ID inexistente, email duplicado, mismo email)
 *   eliminar()  → 2 tests (flujo feliz, ID inexistente)
 *   buscar()    → 2 tests (flujo feliz, ID inexistente)
 */

import com.sigr.usuarios.dominio.RepositorioUsuario;
import com.sigr.usuarios.dominio.Rol;
import com.sigr.usuarios.dominio.Usuario;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.ArgumentCaptor;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.Optional;

import static org.assertj.core.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.BDDMockito.*;

// Activa Mockito: permite usar @Mock sin levantar Spring ni base de datos
@ExtendWith(MockitoExtension.class)
@DisplayName("ServicioUsuario")
class ServicioUsuarioTest {

    // Repositorio simulado: reemplaza la implementación real para que
    // los tests no dependan de ningún almacenamiento externo
    @Mock
    private RepositorioUsuario repositorio;

    private ServicioUsuario servicio;

    // Se ejecuta antes de cada test: crea una instancia limpia del servicio
    // inyectando el repositorio simulado
    @BeforeEach
    void setUp() {
        servicio = new ServicioUsuario(repositorio);
    }

    // ================================================================
    // CREAR USUARIO
    // ================================================================
    @Nested
    @DisplayName("crear()")
    class Crear {

        @Test
        @DisplayName("datos válidos → genera ID y guarda el usuario")
        void crear_guardaUsuarioYRetornaId() {
            // DADO: que el email no está registrado en el sistema
            given(repositorio.existePorEmail("ana@mail.com")).willReturn(false);

            // CUANDO: se solicita crear un usuario con nombre, email, contraseña y rol válidos
            String id = servicio.crear(new CrearUsuarioComando("Ana", "ana@mail.com", "clave123", Rol.CLIENTE));

            // ENTONCES: debe retornar un ID generado (no vacío)
            //           y debe haber llamado a guardar() con los datos correctos
            assertThat(id).isNotBlank();
            ArgumentCaptor<Usuario> captor = ArgumentCaptor.forClass(Usuario.class);
            then(repositorio).should().guardar(captor.capture());
            assertThat(captor.getValue().getNombre()).isEqualTo("Ana");
            assertThat(captor.getValue().getRol()).isEqualTo(Rol.CLIENTE);
        }

        @Test
        @DisplayName("email duplicado → lanza EmailDuplicadoException y no guarda")
        void crear_lanzaExcepcionSiEmailDuplicado() {
            // DADO: que ya existe un usuario con ese email en el sistema
            given(repositorio.existePorEmail("ana@mail.com")).willReturn(true);

            // CUANDO: se intenta crear otro usuario con el mismo email
            // ENTONCES: debe lanzar EmailDuplicadoException con el email en el mensaje
            //           y NO debe llamar a guardar() para no crear registros duplicados
            assertThatThrownBy(() ->
                servicio.crear(new CrearUsuarioComando("Ana", "ana@mail.com", "clave123", Rol.CLIENTE))
            ).isInstanceOf(EmailDuplicadoException.class)
             .hasMessageContaining("ana@mail.com");

            then(repositorio).should(never()).guardar(any());
        }

        @Test
        @DisplayName("nombre vacío → lanza IllegalArgumentException")
        void crear_lanzaExcepcionSiNombreEsVacio() {
            // DADO: que el email no está duplicado (el error viene del nombre, no del repositorio)
            given(repositorio.existePorEmail("ana@mail.com")).willReturn(false);

            // CUANDO: se intenta crear un usuario con nombre vacío
            // ENTONCES: la entidad Usuario debe rechazarlo antes de guardar
            assertThatThrownBy(() ->
                servicio.crear(new CrearUsuarioComando("", "ana@mail.com", "clave123", Rol.CLIENTE))
            ).isInstanceOf(IllegalArgumentException.class)
             .hasMessageContaining("nombre");
        }

        @Test
        @DisplayName("email sin @ → lanza IllegalArgumentException")
        void crear_lanzaExcepcionSiEmailEsInvalido() {
            // DADO: que el email no está duplicado (el error viene del formato, no del repositorio)
            given(repositorio.existePorEmail("no-es-email")).willReturn(false);

            // CUANDO: se intenta crear un usuario con email sin formato válido
            // ENTONCES: la entidad Usuario debe rechazarlo antes de guardar
            assertThatThrownBy(() ->
                servicio.crear(new CrearUsuarioComando("Ana", "no-es-email", "clave123", Rol.CLIENTE))
            ).isInstanceOf(IllegalArgumentException.class)
             .hasMessageContaining("Email");
        }

        @Test
        @DisplayName("contraseña menor a 6 caracteres → lanza IllegalArgumentException")
        void crear_lanzaExcepcionSiContrasenaEsCorta() {
            // DADO: que el email no está duplicado (el error viene de la contraseña, no del repositorio)
            given(repositorio.existePorEmail("ana@mail.com")).willReturn(false);

            // CUANDO: se intenta crear un usuario con contraseña insegura (menos de 6 chars)
            // ENTONCES: la entidad Usuario debe rechazarlo antes de guardar
            assertThatThrownBy(() ->
                servicio.crear(new CrearUsuarioComando("Ana", "ana@mail.com", "123", Rol.CLIENTE))
            ).isInstanceOf(IllegalArgumentException.class)
             .hasMessageContaining("contraseña");
        }
    }

    // ================================================================
    // ACTUALIZAR USUARIO
    // ================================================================
    @Nested
    @DisplayName("actualizar()")
    class Actualizar {

        @Test
        @DisplayName("datos nuevos válidos → modifica nombre y email del usuario existente")
        void actualizar_modificaNombreYEmail() {
            // DADO: que existe un usuario con id-1 y el nuevo email no está ocupado
            Usuario existente = new Usuario("id-1", "Ana", "ana@mail.com", "clave123", Rol.CLIENTE);
            given(repositorio.buscarPorId("id-1")).willReturn(Optional.of(existente));
            given(repositorio.existePorEmail("nueva@mail.com")).willReturn(false);

            // CUANDO: se actualiza con nuevo nombre y nuevo email
            servicio.actualizar(new ActualizarUsuarioComando("id-1", "Ana Nueva", "nueva@mail.com", null, null));

            // ENTONCES: el objeto usuario debe reflejar los nuevos valores
            //           y debe haberse llamado a guardar() para persistir el cambio
            assertThat(existente.getNombre()).isEqualTo("Ana Nueva");
            assertThat(existente.getEmail()).isEqualTo("nueva@mail.com");
            then(repositorio).should().guardar(existente);
        }

        @Test
        @DisplayName("ID inexistente → lanza UsuarioNoEncontradoException")
        void actualizar_lanzaExcepcionSiUsuarioNoExiste() {
            // DADO: que no existe ningún usuario con ese ID en el repositorio
            given(repositorio.buscarPorId("id-inexistente")).willReturn(Optional.empty());

            // CUANDO: se intenta actualizar un usuario que no existe
            // ENTONCES: debe lanzar UsuarioNoEncontradoException con el ID en el mensaje
            assertThatThrownBy(() ->
                servicio.actualizar(new ActualizarUsuarioComando("id-inexistente", "Nombre", null, null, null))
            ).isInstanceOf(UsuarioNoEncontradoException.class)
             .hasMessageContaining("id-inexistente");
        }

        @Test
        @DisplayName("nuevo email ya usado por otro usuario → lanza EmailDuplicadoException y no guarda")
        void actualizar_lanzaExcepcionSiNuevoEmailYaDuplicado() {
            // DADO: que existe el usuario id-1 pero el nuevo email ya lo usa otro usuario
            Usuario existente = new Usuario("id-1", "Ana", "ana@mail.com", "clave123", Rol.CLIENTE);
            given(repositorio.buscarPorId("id-1")).willReturn(Optional.of(existente));
            given(repositorio.existePorEmail("otro@mail.com")).willReturn(true);

            // CUANDO: se intenta cambiar el email por uno que ya está registrado
            // ENTONCES: debe lanzar EmailDuplicadoException
            //           y NO debe guardar para evitar sobrescribir con datos inválidos
            assertThatThrownBy(() ->
                servicio.actualizar(new ActualizarUsuarioComando("id-1", null, "otro@mail.com", null, null))
            ).isInstanceOf(EmailDuplicadoException.class);

            then(repositorio).should(never()).guardar(any());
        }

        @Test
        @DisplayName("mismo email actual → no verifica duplicado y guarda correctamente")
        void actualizar_permiteMantenermismoEmail() {
            // DADO: que el usuario id-1 existe y se envía su mismo email en la actualización
            Usuario existente = new Usuario("id-1", "Ana", "ana@mail.com", "clave123", Rol.CLIENTE);
            given(repositorio.buscarPorId("id-1")).willReturn(Optional.of(existente));

            // CUANDO: se actualiza solo el nombre manteniendo el mismo email
            servicio.actualizar(new ActualizarUsuarioComando("id-1", "Ana Actualizada", "ana@mail.com", null, null));

            // ENTONCES: NO debe consultar existePorEmail (el email no cambió, no hay riesgo)
            //           y debe guardar los cambios correctamente
            then(repositorio).should(never()).existePorEmail(any());
            then(repositorio).should().guardar(existente);
        }
    }

    // ================================================================
    // ELIMINAR USUARIO
    // ================================================================
    @Nested
    @DisplayName("eliminar()")
    class Eliminar {

        @Test
        @DisplayName("ID existente → elimina el usuario del repositorio")
        void eliminar_borraUsuarioExistente() {
            // DADO: que el usuario con id-1 existe en el repositorio
            Usuario existente = new Usuario("id-1", "Ana", "ana@mail.com", "clave123", Rol.CLIENTE);
            given(repositorio.buscarPorId("id-1")).willReturn(Optional.of(existente));

            // CUANDO: se solicita eliminar ese usuario
            servicio.eliminar("id-1");

            // ENTONCES: debe llamar a eliminar() en el repositorio con el ID correcto
            then(repositorio).should().eliminar("id-1");
        }

        @Test
        @DisplayName("ID inexistente → lanza UsuarioNoEncontradoException y no elimina nada")
        void eliminar_lanzaExcepcionSiUsuarioNoExiste() {
            // DADO: que no existe ningún usuario con ese ID
            given(repositorio.buscarPorId("id-inexistente")).willReturn(Optional.empty());

            // CUANDO: se intenta eliminar un usuario que no existe
            // ENTONCES: debe lanzar UsuarioNoEncontradoException
            //           y NO debe llamar a eliminar() para evitar operaciones sobre nada
            assertThatThrownBy(() -> servicio.eliminar("id-inexistente"))
                .isInstanceOf(UsuarioNoEncontradoException.class)
                .hasMessageContaining("id-inexistente");

            then(repositorio).should(never()).eliminar(any());
        }
    }

    // ================================================================
    // BUSCAR USUARIO
    // ================================================================
    @Nested
    @DisplayName("buscar()")
    class Buscar {

        @Test
        @DisplayName("ID existente → retorna el usuario con sus datos correctos")
        void buscar_retornaUsuarioCuandoExiste() {
            // DADO: que existe un usuario con id-1 en el repositorio
            Usuario existente = new Usuario("id-1", "Ana", "ana@mail.com", "clave123", Rol.CLIENTE);
            given(repositorio.buscarPorId("id-1")).willReturn(Optional.of(existente));

            // CUANDO: se busca el usuario por su ID
            Usuario resultado = servicio.buscar("id-1");

            // ENTONCES: debe retornar el usuario con el nombre correcto
            assertThat(resultado.getNombre()).isEqualTo("Ana");
        }

        @Test
        @DisplayName("ID inexistente → lanza UsuarioNoEncontradoException")
        void buscar_lanzaExcepcionSiNoExiste() {
            // DADO: que no existe ningún usuario con ese ID
            given(repositorio.buscarPorId("no-existe")).willReturn(Optional.empty());

            // CUANDO: se intenta buscar un usuario que no existe
            // ENTONCES: debe lanzar UsuarioNoEncontradoException
            assertThatThrownBy(() -> servicio.buscar("no-existe"))
                .isInstanceOf(UsuarioNoEncontradoException.class);
        }
    }
}
