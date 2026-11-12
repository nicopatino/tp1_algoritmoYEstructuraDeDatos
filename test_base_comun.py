# ============================================================
# PRUEBAS UNITARIAS - BASE COMUN Y CONSULTAS (Persona 3)
# Se ejecutan solas, sin abrir el menu:  python test_base_comun.py
# Cada prueba muestra: funcion probada, datos, resultado esperado,
# resultado obtenido y si fue APROBADA o FALLIDA.
# ============================================================

from base_comun import (convertir_entero, validar_rango, validar_nombre, validar_correo,
                        validar_opcion, cargar_datos_iniciales, RANGO_NOTA)
from menu_principal import analitico_estudiante


def ejecutar_prueba(numero, tipo, funcion, datos, esperado, ejecutar):
    """ejecutar es una funcion sin parametros (lambda) que llama a la funcion probada.
    Si la funcion lanza ValueError, el resultado obtenido es el mensaje del error;
    si lanza FileNotFoundError, el resultado es el nombre de la excepcion."""
    try:
        obtenido = ejecutar()
    except ValueError as error:
        obtenido = "ValueError: " + str(error)
    except FileNotFoundError:
        obtenido = "FileNotFoundError"
    aprobada = obtenido == esperado
    print(f"Prueba {numero} [{tipo}]")
    print("  Función:  ", funcion)
    print("  Datos:    ", datos)
    print("  Esperado: ", esperado)
    print("  Obtenido: ", obtenido)
    print("  Resultado:", "APROBADA" if aprobada else "FALLIDA")
    print()
    return aprobada


def correr_pruebas():
    estudiantes, materias, calificaciones = cargar_datos_iniciales()
    resultados = []

    # ---------- 4 CASOS VALIDOS ----------
    resultados.append(ejecutar_prueba(1, "válido", "convertir_entero", '("25", "edad")',
                                      25, lambda: convertir_entero("25", "edad")))
    resultados.append(ejecutar_prueba(2, "válido", "validar_correo", '"marcos.silva@alumno.edu.ar"',
                                      "marcos.silva@alumno.edu.ar",
                                      lambda: validar_correo("marcos.silva@alumno.edu.ar")))
    resultados.append(ejecutar_prueba(3, "válido", "validar_nombre", '"  Juan   Pérez " (espacios de más)',
                                      "Juan Pérez", lambda: validar_nombre("  Juan   Pérez ")))
    resultados.append(ejecutar_prueba(4, "válido", "cargar_datos_iniciales", "listas de la Parte 1",
                                      (10, 10, 10, "Marcos Silva Sapia"),
                                      lambda: (len(estudiantes), len(materias), len(calificaciones),
                                               estudiantes[102]["nombre"])))

    # ---------- 3 CASOS INVALIDOS ----------
    resultados.append(ejecutar_prueba(5, "inválido", "convertir_entero", '("abc", "nota")',
                                      "ValueError: El campo nota debe ser un número entero",
                                      lambda: convertir_entero("abc", "nota")))
    resultados.append(ejecutar_prueba(6, "inválido", "validar_correo", '"marcos@gmail" (sin dominio)',
                                      "ValueError: Correo inválido. Ejemplos válidos: usuario@gmail.com, usuario@alumno.edu.ar",
                                      lambda: validar_correo("marcos@gmail")))
    resultados.append(ejecutar_prueba(7, "inválido", "validar_opcion", '("9", (1, 2, 3, 4, 0))',
                                      "ValueError: Opción inexistente. Opciones válidas: 1, 2, 3, 4, 0",
                                      lambda: validar_opcion("9", (1, 2, 3, 4, 0))))

    # ---------- 2 CASOS LIMITE ----------
    resultados.append(ejecutar_prueba(8, "límite", "validar_rango", "(10, RANGO_NOTA=(1, 10), 'nota')",
                                      10, lambda: validar_rango(10, RANGO_NOTA, "nota")))
    resultados.append(ejecutar_prueba(9, "límite", "convertir_entero", '("   ", "código") (solo espacios)',
                                      "ValueError: El campo código es obligatorio",
                                      lambda: convertir_entero("   ", "código")))

    # ---------- 1 CASO RELEVANTE PARA EL SISTEMA ----------
    resultados.append(ejecutar_prueba(10, "relevante", "analitico_estudiante",
                                      "(102, datos iniciales) -> analítico de Marcos",
                                      ("Marcos Silva Sapia", [("Diseño Web", 6, "regular")], 6.0),
                                      lambda: analitico_estudiante(102, estudiantes, materias, calificaciones)))

    aprobadas = resultados.count(True)
    print(f"RESUMEN: {aprobadas} de {len(resultados)} pruebas aprobadas")


if __name__ == "__main__":
    correr_pruebas()
