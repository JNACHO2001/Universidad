# Arquitectura del Sistema - SIGR

## Estilo arquitectónico
Arquitectura **Hexagonal** (Puertos y Adaptadores).

## Capas por módulo
- **dominio/**: Entidades, objetos de valor, reglas de negocio puras.
- **aplicacion/**: Casos de uso, puertos de entrada/salida.
- **infraestructura/**: Adaptadores (REST, persistencia, mensajería).

## Módulos
1. Autenticación
2. Menú
3. Pedidos
4. Reservas
5. Caja y Reportes
