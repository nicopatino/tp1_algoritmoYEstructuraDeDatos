# ============================================================
# SISTEMA DE GESTION ACADEMICA - SEGUNDA PARTE
# MENU PRINCIPAL Y CONSULTAS (Persona 3: Marcos Silva Sapia)
#
# Reemplaza al "submenu 4" de la Parte 1 (demos de diccionarios,
# tuplas y conjuntos) por consultas reales sobre los datos del sistema.
# ============================================================

from base_comun import (cargar_datos_iniciales, login, pedir_opcion, pedir_entero,
                        condicion_a_texto, es_aprobada)
from persistencia import (ARCHIVO_DATOS, guardar_datos_json, cargar_datos_json, respaldar_archivo,
                          detectar_calificaciones_huerfanas, registrar_operacion, leer_log, resumir_log)
from persona_1_estudiantes import submenu_estudiantes
from materias import submenu_materias
from calificaciones import submenu_calificaciones as submenu_calificaciones_modulo


def obtener_campos_calificacion(calificacion):
    """Obtener (estudiante, materia, nota, condición) desde un dict o una tupla."""
    if isinstance(calificacion, dict):
        return (
            calificacion["estudiante"],
            calificacion["materia"],
            calificacion["nota"],
            calificacion["condicion"],
        )
    if isinstance(calificacion, (tuple, list)) and len(calificacion) == 5:
        return calificacion[1], calificacion[2], calificacion[3], calificacion[4]
    raise ValueError("El registro de calificación no tiene un formato reconocido.")


# ------------------------------------------------------------
# CONSULTAS (funciones de calculo: devuelven datos, no imprimen)
# ------------------------------------------------------------

def analitico_estudiante(codigo, estudiantes, materias, calificaciones):
    """Devuelve la tupla (nombre, filas, promedio) de un estudiante.
    Cada fila es una tupla (materia, nota, condicion). Lanza ValueError si no existe."""
    if codigo not in estudiantes:
        raise ValueError(f"No existe un estudiante con código {codigo}")
    filas = []
    for calificacion in calificaciones.values():
        codigo_estudiante, codigo_materia, nota, condicion = obtener_campos_calificacion(calificacion)
        if codigo_estudiante == codigo:
            # get() con valor por defecto: si la materia fue borrada no se rompe con KeyError
            nombre_materia = materias.get(codigo_materia, {}).get("nombre", "Desconocida")
            filas.append((nombre_materia, nota, condicion_a_texto(condicion)))
    promedio = 0
    if len(filas) > 0:
        promedio = round(sum(list(map(lambda fila: fila[1], filas))) / len(filas), 2)
    return (estudiantes[codigo]["nombre"], filas, promedio)


def ranking_estudiantes(estudiantes, calificaciones):
    """Devuelve una lista de tuplas (codigo, nombre, promedio, cantidad_notas)
    ordenada de mayor a menor promedio. Solo incluye estudiantes con notas."""
    acumulado = {}   # diccionario contador: codigo -> [suma_notas, cantidad_notas]
    for calificacion in calificaciones.values():
        codigo, codigo_materia, nota, condicion = obtener_campos_calificacion(calificacion)
        if codigo in estudiantes:
            if codigo not in acumulado:
                acumulado[codigo] = [0, 0]
            acumulado[codigo][0] += nota
            acumulado[codigo][1] += 1
    ranking = []
    for codigo in acumulado:
        suma, cantidad = acumulado[codigo]
        ranking.append((codigo, estudiantes[codigo]["nombre"], round(suma / cantidad, 2), cantidad))
    return sorted(ranking, key=lambda fila: fila[2], reverse=True)


def informe_materia(codigo, estudiantes, materias, calificaciones):
    """Devuelve la tupla (nombre_materia, filas, aprobados, promedio) de una materia.
    Cada fila es una tupla (estudiante, nota, condicion). Lanza ValueError si no existe."""
    if codigo not in materias:
        raise ValueError(f"No existe una materia con código {codigo}")
    filas = []
    aprobados = 0
    for calificacion in calificaciones.values():
        codigo_estudiante, codigo_materia, nota, condicion = obtener_campos_calificacion(calificacion)
        if codigo_materia == codigo:
            nombre_est = estudiantes.get(codigo_estudiante, {}).get("nombre", "Desconocido")
            filas.append((nombre_est, nota, condicion_a_texto(condicion)))
            if es_aprobada(nota):
                aprobados += 1
    promedio = 0
    if len(filas) > 0:
        promedio = round(sum(list(map(lambda fila: fila[1], filas))) / len(filas), 2)
    return (materias[codigo]["nombre"], filas, aprobados, promedio)


# ------------------------------------------------------------
# CONSULTAS (funciones de pantalla: piden el dato y muestran)
# ------------------------------------------------------------

def mostrar_analitico(estudiantes, materias, calificaciones):
    codigo = pedir_entero("Ingrese el código del estudiante: ", "código")
    try:
        nombre, filas, promedio = analitico_estudiante(codigo, estudiantes, materias, calificaciones)
    except ValueError as error:
        print("Error:", error)
        return
    print(f"\n--- ANALÍTICO DE {nombre.upper()} ({codigo}) ---")
    if len(filas) == 0:
        print("El estudiante todavía no tiene calificaciones.")
        return
    for materia, nota, condicion in filas:
        print(f"{materia:22} | Nota: {nota:>2} | {condicion}")
    print("Promedio:", promedio)


def mostrar_ranking(estudiantes, calificaciones):
    ranking = ranking_estudiantes(estudiantes, calificaciones)
    print("\n--- RANKING DE ESTUDIANTES POR PROMEDIO ---")
    if len(ranking) == 0:
        print("No hay calificaciones cargadas.")
        return
    puesto = 1
    for codigo, nombre, promedio, cantidad in ranking:
        print(f"{puesto:>2}. {nombre:25} ({codigo}) | Promedio: {promedio:5} | Notas: {cantidad}")
        puesto += 1


def mostrar_informe_materia(estudiantes, materias, calificaciones):
    codigo = pedir_entero("Ingrese el código de la materia: ", "código")
    try:
        nombre, filas, aprobados, promedio = informe_materia(codigo, estudiantes, materias, calificaciones)
    except ValueError as error:
        print("Error:", error)
        return
    print(f"\n--- INFORME DE {nombre.upper()} ({codigo}) ---")
    if len(filas) == 0:
        print("La materia todavía no tiene calificaciones.")
        return
    for estudiante, nota, condicion in filas:
        print(f"{estudiante:25} | Nota: {nota:>2} | {condicion}")
    print("Aprobados:", aprobados, "de", len(filas), "| Promedio:", promedio)


def mostrar_historial(cantidad=10):
    """Usa la informacion guardada en log_operaciones.txt: muestra las ultimas
    operaciones y cuantas hubo de cada tipo."""
    registros = leer_log()
    print("\n--- HISTORIAL DE OPERACIONES ---")
    if len(registros) == 0:
        print("Todavía no hay operaciones registradas.")
        return
    print(f"Últimas {min(cantidad, len(registros))} de {len(registros)}:")
    for tipo, usuario, detalle in registros[-cantidad:]:
        print(f"  {tipo:15} | {usuario:10} | {detalle}")
    print("Resumen por tipo:")
    resumen = resumir_log(registros)
    for tipo in sorted(resumen):
        print(f"  {tipo:15}: {resumen[tipo]}")


def submenu_consultas(estudiantes, materias, calificaciones):
    salir = False
    while not salir:
        print("\n---Submenú de consultas---")
        print("1. Analítico de un estudiante")
        print("2. Ranking de estudiantes")
        print("3. Informe por materia")
        print("4. Historial de operaciones")
        print("0. Volver atrás")
        opcion = pedir_opcion((1, 2, 3, 4, 0))
        if opcion == 1:
            mostrar_analitico(estudiantes, materias, calificaciones)
        elif opcion == 2:
            mostrar_ranking(estudiantes, calificaciones)
        elif opcion == 3:
            mostrar_informe_materia(estudiantes, materias, calificaciones)
        elif opcion == 4:
            mostrar_historial()
        else:
            salir = True


# ------------------------------------------------------------
# MENU PRINCIPAL
# Solo coordina: no tiene logica de negocio. Los datos viajan por parametro.
# ------------------------------------------------------------

def menu_principal(estudiantes, materias, calificaciones, usuario):
    salir = False
    while not salir:
        print("\n---Bienvenido al menú principal---")
        print("1. Estudiantes")
        print("2. Materias")
        print("3. Calificaciones")
        print("4. Consultas")
        print("0. Cerrar sesión")
        # pedir_opcion ya rechaza opciones inexistentes: no hace falta el "else: opcion no valida"
        opcion = pedir_opcion((1, 2, 3, 4, 0), "Seleccione una opción: ")
        if opcion == 1:
            submenu_estudiantes(estudiantes, calificaciones)
        elif opcion == 2:
            submenu_materias(estudiantes, materias, calificaciones)
        elif opcion == 3:
            submenu_calificaciones_modulo(estudiantes, materias, calificaciones)
        elif opcion == 4:
            submenu_consultas(estudiantes, materias, calificaciones)
        else:
            salir = True
        # Guardado: al volver de un submenu que puede modificar datos (1, 2, 3) y al
        # cerrar sesion (0). Las consultas solo leen, no hace falta guardar.
        if opcion != 4:
            if guardar_datos_json(estudiantes, materias, calificaciones):
                print(f"(Datos guardados en {ARCHIVO_DATOS})")
                registrar_operacion("GUARDADO", usuario, f"opción {opcion} del menú principal")
    registrar_operacion("CIERRE_SESION", usuario, "salida normal")
    print("Cerrando sesión")


def iniciar_datos():
    """Recupera los datos guardados en la ejecucion anterior.
    Devuelve la tupla (estudiantes, materias, calificaciones)."""
    try:
        estudiantes, materias, calificaciones = cargar_datos_json()
        print(f"Datos recuperados de {ARCHIVO_DATOS}: {len(estudiantes)} estudiantes, "
              f"{len(materias)} materias, {len(calificaciones)} calificaciones.")
    except FileNotFoundError:
        # Primera ejecucion: todavia no hay archivo, se arranca con los datos de la Parte 1
        print(f"No se encontró {ARCHIVO_DATOS}: se cargan los datos iniciales.")
        estudiantes, materias, calificaciones = cargar_datos_iniciales()
        guardar_datos_json(estudiantes, materias, calificaciones)
    except ValueError as error:
        # Archivo dañado: se respalda antes de sobrescribirlo y se usan los datos iniciales
        print("Error:", error)
        respaldo = respaldar_archivo(ARCHIVO_DATOS)
        if respaldo != "":
            print(f"Se guardó una copia del archivo dañado en {respaldo}.")
        print("Se cargan los datos iniciales.")
        estudiantes, materias, calificaciones = cargar_datos_iniciales()
    # Integridad: avisa si hay calificaciones que apuntan a estudiantes o materias inexistentes
    huerfanas = detectar_calificaciones_huerfanas(estudiantes, materias, calificaciones)
    if len(huerfanas) > 0:
        print("Aviso: estas calificaciones refieren a estudiantes o materias inexistentes:",
              sorted(huerfanas))
    return (estudiantes, materias, calificaciones)


def main():
    print("---Sistema de Gestión Académica---")
    estudiantes, materias, calificaciones = iniciar_datos()
    print("    --Inicio de sesión--")
    usuario = login()
    if usuario != "":
        menu_principal(estudiantes, materias, calificaciones, usuario)
    else:
        print("Por seguridad se bloqueó el acceso")


if __name__ == "__main__":
    main()
