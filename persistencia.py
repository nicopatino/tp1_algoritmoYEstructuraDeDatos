# ============================================================
# SISTEMA DE GESTION ACADEMICA - SEGUNDA PARTE
# PERSISTENCIA (Persona 3: Marcos Silva Sapia)
#
#   - datos_sistema.json   : estudiantes, materias y calificaciones.
#                            Se guarda al salir de cada submenu y al
#                            cerrar sesion; se recupera al iniciar.
#   - log_operaciones.txt  : una linea por operacion (login, guardado,
#                            cierre). Se lee desde Consultas -> Historial.
#
# Este modulo no importa nada del resto del sistema (evita importaciones
# circulares): solo usa json, que se ve en la materia.
# ============================================================

import json

# Tuplas de configuracion: nombres fijos que no deben cambiar en ejecucion
ARCHIVO_DATOS = "datos_sistema.json"
ARCHIVO_LOG = "log_operaciones.txt"
SECCIONES_DATOS = ("estudiantes", "materias", "calificaciones")
SEPARADOR_LOG = " | "


# ------------------------------------------------------------
# ARCHIVO JSON
# ------------------------------------------------------------

def guardar_datos_json(estudiantes, materias, calificaciones, ruta=ARCHIVO_DATOS):
    """Guarda los 3 diccionarios en un unico archivo JSON.
    Devuelve True si se pudo guardar, False si hubo un problema con el archivo."""
    datos = {"estudiantes": estudiantes, "materias": materias, "calificaciones": calificaciones}
    try:
        with open(ruta, "w", encoding="utf-8") as archivo:
            # indent: el archivo queda legible; ensure_ascii=False: guarda tildes y ñ tal cual
            json.dump(datos, archivo, indent=4, ensure_ascii=False)
        return True
    except OSError as error:
        # Disco lleno, sin permisos, carpeta inexistente, etc.
        print("Error: no se pudieron guardar los datos en", ruta, "->", error)
        return False


def convertir_claves_a_entero(diccionario, seccion):
    """JSON solo admite claves de texto: al guardar, el codigo 100 queda como "100".
    Esta funcion vuelve a convertir las claves a entero al recuperar los datos."""
    if type(diccionario) != dict:
        raise ValueError(f"La sección '{seccion}' del archivo no tiene el formato esperado")
    convertido = {}
    for clave, valor in diccionario.items():
        try:
            convertido[int(clave)] = valor
        except ValueError:
            raise ValueError(f"La sección '{seccion}' tiene un código inválido: '{clave}'")
    return convertido


def reconstruir_calificaciones(calificaciones):
    """Reconstruye como tuplas las actas de cinco campos guardadas como arreglos JSON.
    Los registros históricos que son diccionarios se conservan sin cambios."""
    reconstruidas = {}
    for codigo, calificacion in calificaciones.items():
        if isinstance(calificacion, (list, tuple)) and len(calificacion) == 5:
            reconstruidas[codigo] = tuple(calificacion)
        else:
            reconstruidas[codigo] = calificacion
    return reconstruidas


def cargar_datos_json(ruta=ARCHIVO_DATOS):
    """Lee el JSON y devuelve la tupla (estudiantes, materias, calificaciones).
    - Lanza FileNotFoundError si el archivo todavia no existe (primera ejecucion).
    - Lanza ValueError si el archivo esta dañado o le falta alguna seccion."""
    with open(ruta, "r", encoding="utf-8") as archivo:
        try:
            datos = json.load(archivo)
        except json.JSONDecodeError:
            raise ValueError(f"El archivo {ruta} está dañado (no es un JSON válido)")
    if type(datos) != dict:
        raise ValueError(f"El archivo {ruta} no tiene el formato esperado")
    # Conjuntos: diferencia entre las secciones esperadas y las que trae el archivo
    faltantes = set(SECCIONES_DATOS) - set(datos.keys())
    if len(faltantes) > 0:
        raise ValueError(f"Al archivo {ruta} le faltan secciones: {', '.join(sorted(faltantes))}")
    estudiantes = convertir_claves_a_entero(datos["estudiantes"], "estudiantes")
    materias = convertir_claves_a_entero(datos["materias"], "materias")
    calificaciones = convertir_claves_a_entero(datos["calificaciones"], "calificaciones")
    calificaciones = reconstruir_calificaciones(calificaciones)
    return (estudiantes, materias, calificaciones)


def respaldar_archivo(ruta):
    """Copia el contenido de un archivo dañado a ruta + '.bak' antes de que se
    sobrescriba, para no perder la informacion. Devuelve el nombre del respaldo."""
    ruta_respaldo = ruta + ".bak"
    try:
        with open(ruta, "r", encoding="utf-8", errors="replace") as original:
            contenido = original.read()
        with open(ruta_respaldo, "w", encoding="utf-8") as respaldo:
            respaldo.write(contenido)
        return ruta_respaldo
    except OSError:
        return ""


def detectar_calificaciones_huerfanas(estudiantes, materias, calificaciones):
    """Devuelve el conjunto de codigos de calificaciones que apuntan a un estudiante
    o a una materia que ya no existe. Acepta tuplas nuevas y diccionarios históricos."""
    huerfanas = set()
    for codigo, calificacion in calificaciones.items():
        if isinstance(calificacion, (tuple, list)):
            if len(calificacion) != 5:
                huerfanas.add(codigo)
                continue
            codigo_estudiante = calificacion[1]
            codigo_materia = calificacion[2]
        elif isinstance(calificacion, dict):
            codigo_estudiante = calificacion.get("estudiante")
            codigo_materia = calificacion.get("materia")
        else:
            huerfanas.add(codigo)
            continue
        if codigo_estudiante not in estudiantes or codigo_materia not in materias:
            huerfanas.add(codigo)
    return huerfanas


# ------------------------------------------------------------
# ARCHIVO DE TEXTO: LOG DE OPERACIONES
# Cada linea: TIPO | usuario | detalle
# ------------------------------------------------------------

def registrar_operacion(tipo, usuario, detalle, ruta=ARCHIVO_LOG):
    """Agrega una linea al final del log (modo 'a': no borra lo anterior).
    Si el log no se puede escribir se avisa, pero el sistema sigue funcionando."""
    # Se sacan los separadores del texto para que la linea no se rompa al leerla
    linea = SEPARADOR_LOG.join([tipo, usuario.replace("|", "/"), detalle.replace("|", "/")])
    try:
        with open(ruta, "a", encoding="utf-8") as archivo:
            archivo.write(linea + "\n")
    except OSError:
        print("Aviso: no se pudo escribir en el log de operaciones.")


def leer_log(ruta=ARCHIVO_LOG):
    """Devuelve una lista de tuplas (tipo, usuario, detalle), una por linea del log.
    Si el archivo no existe todavia, devuelve una lista vacia.
    Las lineas mal formadas se ignoran en vez de cortar el programa."""
    registros = []
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                partes = linea.strip().split(SEPARADOR_LOG)
                if len(partes) == 3:
                    registros.append((partes[0], partes[1], partes[2]))
    except FileNotFoundError:
        return []
    return registros


def resumir_log(registros):
    """Diccionario contador: tipo de operacion -> cantidad de veces que aparece."""
    resumen = {}
    for tipo, usuario, detalle in registros:
        resumen[tipo] = resumen.get(tipo, 0) + 1
    return resumen
