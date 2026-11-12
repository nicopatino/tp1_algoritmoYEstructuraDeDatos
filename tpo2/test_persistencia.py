# ============================================================
# PRUEBAS UNITARIAS - PERSISTENCIA (Persona 3)
# Se ejecutan solas:  python test_persistencia.py
# Usan archivos propios (prueba_*.json / prueba_*.txt) para no tocar
# los datos reales del sistema. Se recrean en cada ejecucion.
# ============================================================

from base_comun import cargar_datos_iniciales
from persistencia import (guardar_datos_json, cargar_datos_json, detectar_calificaciones_huerfanas,
                          leer_log, resumir_log)
from test_base_comun import ejecutar_prueba


def escribir_texto(ruta, contenido):
    """Auxiliar de las pruebas: crea un archivo con un contenido fijo."""
    with open(ruta, "w", encoding="utf-8") as archivo:
        archivo.write(contenido)


def guardar_y_recuperar():
    """Simula cerrar y volver a abrir el programa: guarda, vuelve a leer del disco
    y verifica que los codigos vuelvan como enteros y los datos sean los mismos."""
    estudiantes, materias, calificaciones = cargar_datos_iniciales()
    calificaciones[11] = {"estudiante": 102, "materia": 201, "nota": 9, "condicion": 2}
    guardar_datos_json(estudiantes, materias, calificaciones, "prueba_datos.json")
    est2, mat2, cal2 = cargar_datos_json("prueba_datos.json")
    return (11 in cal2, cal2[11]["nota"], est2[102]["nombre"], cal2 == calificaciones)


def correr_pruebas():
    resultados = []

    # Archivos de prueba
    escribir_texto("prueba_danado.json", '{"estudiantes": {"100": ')
    escribir_texto("prueba_incompleto.json", '{"estudiantes": {}, "calificaciones": {}}')
    escribir_texto("prueba_log.txt", "LOGIN_OK | admin | ingreso correcto\n"
                                     "linea rota sin separadores\n"
                                     "LOGIN_FALLIDO | juan | quedan 2 intentos\n"
                                     "LOGIN_OK | admin | ingreso correcto\n")

    # VALIDO / RELEVANTE: ciclo completo guardar -> cerrar -> abrir -> recuperar
    resultados.append(ejecutar_prueba(1, "válido", "guardar_datos_json + cargar_datos_json",
                                      "datos iniciales + calificación 11 nueva",
                                      (True, 9, "Marcos Silva Sapia", True), guardar_y_recuperar))

    # INVALIDO: primera ejecucion, el archivo no existe
    resultados.append(ejecutar_prueba(2, "inválido", "cargar_datos_json", '"no_existe.json"',
                                      "FileNotFoundError", lambda: cargar_datos_json("no_existe.json")))

    # INVALIDO: archivo cortado a la mitad
    resultados.append(ejecutar_prueba(3, "inválido", "cargar_datos_json", "JSON cortado a la mitad",
                                      "ValueError: El archivo prueba_danado.json está dañado (no es un JSON válido)",
                                      lambda: cargar_datos_json("prueba_danado.json")))

    # LIMITE: JSON valido pero sin la seccion "materias"
    resultados.append(ejecutar_prueba(4, "límite", "cargar_datos_json", "JSON sin sección materias",
                                      "ValueError: Al archivo prueba_incompleto.json le faltan secciones: materias",
                                      lambda: cargar_datos_json("prueba_incompleto.json")))

    # LIMITE: log con una linea mal formada en el medio
    resultados.append(ejecutar_prueba(5, "límite", "leer_log + resumir_log",
                                      "log de 4 líneas, una sin separadores",
                                      {"LOGIN_OK": 2, "LOGIN_FALLIDO": 1},
                                      lambda: resumir_log(leer_log("prueba_log.txt"))))

    # RELEVANTE: calificacion que apunta a un estudiante borrado
    resultados.append(ejecutar_prueba(6, "relevante", "detectar_calificaciones_huerfanas",
                                      "calificación 12 con estudiante 555 inexistente",
                                      {12},
                                      lambda: detectar_calificaciones_huerfanas(
                                          {100: {}}, {200: {}},
                                          {1: {"estudiante": 100, "materia": 200},
                                           12: {"estudiante": 555, "materia": 200}})))

    aprobadas = resultados.count(True)
    print(f"RESUMEN: {aprobadas} de {len(resultados)} pruebas aprobadas")


if __name__ == "__main__":
    correr_pruebas()
