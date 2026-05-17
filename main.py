"""Aplicación principal por consola."""
# Este archivo es el punto de entrada del programa.
# Se encarga de mostrar el menú y coordinar las acciones del usuario.

from prediccion import clasificar_texto
# Importa la función clasificar_texto desde el archivo prediccion.py
# Así main.py puede clasificar textos sin repetir ese código aquí.

from entrenamiento import entrenar_modelo
# Importa la función entrenar_modelo desde el archivo entrenamiento.py
# Separa responsabilidades: main solo coordina, no entrena directamente.


def mostrar_menu():  # noqa: D401
    """Muestra el menú principal."""
    print("\n" + "=" * 50)
    # \n es un salto de línea para separar visualmente cada iteración del menú.
    # "=" * 50 repite el carácter "=" 50 veces → crea una línea decorativa.

    print(" DOLMEN • CLASIFICADOR DE TEXTOS DE ALUMBRADO PÚBLICO")
    # Título del programa que refleja la empresa (DOLMEN) y su propósito:
    # determinar si un texto es relevante o no para la empresa.

    print("=" * 50)
    # Segunda línea decorativa que cierra el encabezado.

    print("1. Entrenar modelo")
    print("2. Clasificar texto")
    print("3. Salir")
    # Las tres opciones disponibles para el usuario.

    print("=" * 50)
    # Línea final decorativa que cierra el recuadro del menú.


def opcion_entrenar():  # noqa: D401
    """Ejecuta el entrenamiento."""
    # Esta función se llama cuando el usuario selecciona la opción "1".
    try:
        entrenar_modelo()
        # Llama a la función importada de entrenamiento.py.
        # Si todo funciona, entrenará el modelo y lo guardará en disco.
    except Exception as error:
        # Captura cualquier error que ocurra durante el entrenamiento
        # (por ejemplo: archivo CSV no encontrado, datos inválidos, etc.)
        print(f"❌ Error durante el entrenamiento: {error}")
        # Muestra el error al usuario sin romper/cerrar el programa.


def opcion_clasificar():  # noqa: D401
    """Solicita un texto y lo clasifica."""
    # Esta función se llama cuando el usuario selecciona la opción "2".
    print("\n Ingrese el texto del documento:")
    # Instrucción al usuario para que sepa qué debe escribir.

    texto = input("> ").strip()
    # input("> ") muestra el símbolo ">" y espera que el usuario escriba algo.
    # .strip() elimina espacios en blanco al inicio y al final del texto ingresado.

    if not texto:
        # Si el usuario presionó Enter sin escribir nada, "texto" estará vacío.
        print(" Debe ingresar un texto.")
        return
        # "return" termina la función aquí, sin intentar clasificar texto vacío.

    try:
        etiqueta, resultados = clasificar_texto(texto)
        # Llama a clasificar_texto (de prediccion.py) y desempaca los 2 valores:
        # - etiqueta: la categoría predicha (ej. "contrato", "factura", etc.)
        # - resultados: lista de (clase, probabilidad) ordenada de mayor a menor.

        print(f"\n Tipo de documento detectado: {etiqueta}\n")
        # Muestra la categoría ganadora, la más probable.

        print(" Probabilidades:")
        # Encabezado para la tabla de probabilidades.

        for clase, probabilidad in resultados:
            # Itera sobre cada par (nombre de clase, probabilidad) de la lista.
            print(f"- {clase:<15} {probabilidad:.2%}")
            # clase:<15 → alinea el texto a la izquierda en un campo de 15 caracteres.
            # probabilidad:.2% → convierte el número decimal a porcentaje con 2 decimales.
            # Ejemplo: 0.8523 → "85.23%"

    except Exception as error:
        # Captura errores al clasificar (ej. modelo no entrenado todavía).
        print(f" Error al clasificar: {error}")


def main():  # noqa: D401
    """Punto de entrada de la aplicación."""
    while True:
        # Bucle infinito que mantiene el menú activo hasta que el usuario elige salir.
        mostrar_menu()
        # Imprime el menú en pantalla en cada iteración del bucle.

        opcion = input("Seleccione una opción: ").strip()
        # Pide al usuario que ingrese una opción.
        # .strip() elimina espacios accidentales antes/después del número.

        if opcion == "1":
            opcion_entrenar()
            # Si el usuario escribe "1", llama a la función de entrenamiento.
        elif opcion == "2":
            opcion_clasificar()
            # Si el usuario escribe "2", llama a la función de clasificación.
        elif opcion == "3":
            print(" Hasta luego.")
            # Mensaje de despedida al usuario.
            break
            # "break" interrumpe el bucle while True y termina el programa.
            # BUG CORREGIDO: antes faltaba este break, el programa nunca salía.


if __name__ == "__main__":
    # Esta condición verifica si el script se está ejecutando directamente
    # (con "python main.py") y NO está siendo importado por otro archivo.
    # BUG CORREGIDO: antes main() estaba dentro del elif, fuera del guard.
    main()
    # Llama a la función principal para arrancar el programa.