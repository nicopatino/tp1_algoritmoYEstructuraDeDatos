"""Pruebas de la integración del submenú y la baja de estudiantes."""

import menu_principal
import persona_1_estudiantes
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


def ejecutar_menu(opciones, estudiantes, materias, calificaciones, submenus=None):
    opciones = iter(opciones)
    funciones_originales = {}
    for nombre in ("pedir_opcion", "guardar_datos_json", "registrar_operacion",
                   "submenu_materias", "submenu_calificaciones"):
        funciones_originales[nombre] = getattr(menu_principal, nombre)

    atributos_originales = []
    for modulo, nombre in ((menu_principal, "print"),
                           (persona_1_estudiantes, "print"),
                           (persona_1_estudiantes, "input")):
        atributos_originales.append((modulo, nombre, nombre in vars(modulo),
                                     vars(modulo).get(nombre)))

    menu_principal.pedir_opcion = lambda *args, **kwargs: next(opciones)
    menu_principal.guardar_datos_json = lambda *args, **kwargs: False
    menu_principal.registrar_operacion = lambda *args, **kwargs: None
    menu_principal.submenu_materias = (submenus or {}).get(
        "materias", funciones_originales["submenu_materias"])
    menu_principal.submenu_calificaciones = (submenus or {}).get(
        "calificaciones", funciones_originales["submenu_calificaciones"])
    menu_principal.print = lambda *args, **kwargs: None
    persona_1_estudiantes.print = lambda *args, **kwargs: None
    entradas_estudiante = []
    persona_1_estudiantes.input = lambda *args, **kwargs: (
        entradas_estudiante.append(args) or "0"
    )

    try:
        menu_principal.menu_principal(estudiantes, materias, calificaciones, "admin")
    finally:
        for nombre, funcion in funciones_originales.items():
            setattr(menu_principal, nombre, funcion)
        for modulo, nombre, existia, valor in atributos_originales:
            if existia:
                setattr(modulo, nombre, valor)
            else:
                delattr(modulo, nombre)
    return entradas_estudiante


def submenu_integrado():
    entradas = ejecutar_menu([1, 0], {}, {}, {})
    return len(entradas) == 1


def otros_submenus_conservan_parametros():
    estudiantes = {100: {"nombre": "Ana Perez"}}
    materias = {200: {"nombre": "Algoritmos"}}
    calificaciones = {}
    llamadas = []

    def registrar_llamada(nombre):
        return lambda *argumentos: llamadas.append((nombre, argumentos))

    ejecutar_menu(
        [2, 3, 0], estudiantes, materias, calificaciones,
        {
            "materias": registrar_llamada("materias"),
            "calificaciones": registrar_llamada("calificaciones"),
        },
    )
    return llamadas == [
        ("materias", (estudiantes, materias, calificaciones)),
        ("calificaciones", (estudiantes, materias, calificaciones)),
    ]


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
