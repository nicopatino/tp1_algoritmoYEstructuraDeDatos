"""Pruebas de la integración del submenú y la baja de estudiantes."""

from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import patch

from menu_principal import menu_principal
from persona_1_estudiantes import baja_estudiante


def ejecutar_prueba(numero, descripcion, esperado, ejecutar):
    obtenido = ejecutar()
    aprobada = obtenido == esperado
    print(f"Prueba {numero}: {descripcion}")
    print("  Esperado:", esperado)
    print("  Obtenido:", obtenido)
    print("  Resultado:", "APROBADA" if aprobada else "FALLIDA")
    print()
    return aprobada


def baja_diccionario():
    estudiantes = {100: {"nombre": "Ana Perez"}}
    calificaciones = {
        1: {"estudiante": 100, "materia": 200, "nota": 8, "condicion": 2},
        2: {"estudiante": 101, "materia": 200, "nota": 7, "condicion": 1},
    }
    resultado = baja_estudiante(estudiantes, calificaciones, 100, True)
    return resultado, estudiantes, calificaciones


def baja_tupla():
    estudiantes = {100: {"nombre": "Ana Perez"}}
    calificaciones = {
        1: (1, 100, 200, 8, 2),
        2: (2, 101, 200, 7, 1),
    }
    resultado = baja_estudiante(estudiantes, calificaciones, 100, True)
    return resultado, estudiantes, calificaciones


def baja_requiere_confirmacion():
    estudiantes = {100: {"nombre": "Ana Perez"}}
    calificaciones = {
        1: {"estudiante": 100, "materia": 200, "nota": 8, "condicion": 2},
    }
    try:
        baja_estudiante(estudiantes, calificaciones, 100, False)
    except ValueError as error:
        return str(error), 100 in estudiantes, len(calificaciones)
    return "No se lanzo ValueError", 100 in estudiantes, len(calificaciones)


def submenu_integrado():
    estudiantes = {}
    materias = {}
    calificaciones = {}
    salida = StringIO()
    with patch("menu_principal.pedir_opcion", side_effect=[1, 0]), \
            patch("menu_principal.guardar_datos_json", return_value=False), \
            patch("menu_principal.registrar_operacion"), \
            patch("builtins.input", return_value="0"), \
            redirect_stdout(salida):
        menu_principal(estudiantes, materias, calificaciones, "admin")
    return "--- ESTUDIANTES ---" in salida.getvalue()


def otros_submenus_conservan_parametros():
    estudiantes = {100: {"nombre": "Ana Perez"}}
    materias = {200: {"nombre": "Algoritmos"}}
    calificaciones = {}
    with patch("menu_principal.pedir_opcion", side_effect=[2, 3, 0]), \
            patch("menu_principal.submenu_materias") as submenu_materias, \
            patch("menu_principal.submenu_calificaciones") as submenu_calificaciones, \
            patch("menu_principal.guardar_datos_json", return_value=False), \
            patch("menu_principal.registrar_operacion"), \
            redirect_stdout(StringIO()):
        menu_principal(estudiantes, materias, calificaciones, "admin")
    return (
        submenu_materias.call_args.args == (estudiantes, materias, calificaciones)
        and submenu_calificaciones.call_args.args == (estudiantes, materias, calificaciones)
    )


def correr_pruebas():
    resultados = [
        ejecutar_prueba(
            1, "Baja elimina la calificación en formato diccionario",
            (("Ana Perez", 1), {}, {2: {"estudiante": 101, "materia": 200, "nota": 7, "condicion": 1}}),
            baja_diccionario,
        ),
        ejecutar_prueba(
            2, "Baja elimina la calificación en tupla de cinco elementos",
            (("Ana Perez", 1), {}, {2: (2, 101, 200, 7, 1)}),
            baja_tupla,
        ),
        ejecutar_prueba(
            3, "Baja requiere confirmación si hay calificaciones",
            ("El estudiante tiene calificaciones asociadas.", True, 1),
            baja_requiere_confirmacion,
        ),
        ejecutar_prueba(
            4, "El menú principal abre el submenú real de Estudiantes",
            True,
            submenu_integrado,
        ),
        ejecutar_prueba(
            5, "Materias y Calificaciones conservan sus tres parámetros",
            True,
            otros_submenus_conservan_parametros,
        ),
    ]
    aprobadas = resultados.count(True)
    print(f"RESUMEN: {aprobadas} de {len(resultados)} pruebas aprobadas")
    return aprobadas == len(resultados)


if __name__ == "__main__":
    if not correr_pruebas():
        raise SystemExit(1)
