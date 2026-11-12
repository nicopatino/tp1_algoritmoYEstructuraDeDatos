# ============================================================
# SISTEMA DE GESTION ACADEMICA - SEGUNDA PARTE
# BASE COMUN (Persona 3: Marcos Silva Sapia)
#
# Funciones compartidas por todo el sistema:
#   - datos iniciales en diccionarios
#   - constantes del sistema (tuplas)
#   - validaciones que lanzan ValueError
#   - ingreso de datos generico (pedir_dato)
#   - login (registra cada intento en el log de texto)
# Este archivo NO imprime nada al importarse: solo define cosas.
# ============================================================

import re
from persistencia import registrar_operacion

# ------------------------------------------------------------
# CONSTANTES DEL SISTEMA (TUPLAS)
# Se usan tuplas porque son datos fijos: ningun modulo deberia
# poder modificarlos durante la ejecucion. Cada rango es (minimo, maximo).
# ------------------------------------------------------------
RANGO_CODIGO_ESTUDIANTE = (100, 999)
RANGO_CODIGO_MATERIA = (200, 999)
RANGO_EDAD = (17, 99)
RANGO_ANIO_CURSADA = (1, 9)
RANGO_CUATRIMESTRE = (1, 2)
RANGO_CARGA_HORARIA = (1, 20)
RANGO_NOTA = (1, 10)
NOTA_APROBACION = 6

# Posicion 0 = condicion 1, posicion 1 = condicion 2, posicion 2 = condicion 3
CONDICIONES = ("regular", "promocionado", "desaprobado")

# Nombres de los campos de cada registro (el orden coincide con las listas de la Parte 1)
CAMPOS_ESTUDIANTE = ("nombre", "edad", "anio", "correo")
CAMPOS_MATERIA = ("nombre", "cuatrimestre", "carga_horaria")
CAMPOS_CALIFICACION = ("estudiante", "materia", "nota", "condicion")

# Expresion regular de correo (la misma de la Parte 1, vista en la Clase VI)
PATRON_CORREO = r"^[A-Za-z0-9_.+-]+@[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)+$"

# Diccionario usuario -> contraseña: permite sumar usuarios sin tocar login()
USUARIOS = {"admin": "admin"}
INTENTOS_MAXIMOS = 3


# ------------------------------------------------------------
# DATOS INICIALES: de listas paralelas (Parte 1) a diccionarios
# ------------------------------------------------------------

def armar_diccionario(codigos, campos, columnas):
    """Convierte listas paralelas en un diccionario {codigo: {campo: valor}}.
    Lanza ValueError si hay codigos repetidos o listas de distinto largo."""
    # Conjunto: si al sacar repetidos el largo cambia, habia codigos duplicados
    if len(set(codigos)) != len(codigos):
        raise ValueError("Hay codigos repetidos en los datos iniciales")
    for columna in columnas:
        if len(columna) != len(codigos):
            raise ValueError("Las listas paralelas no tienen la misma cantidad de elementos")
    diccionario = {}
    for i in range(len(codigos)):
        registro = {}
        for j in range(len(campos)):
            registro[campos[j]] = columnas[j][i]
        diccionario[codigos[i]] = registro
    return diccionario


def cargar_datos_iniciales():
    """Devuelve la tupla (estudiantes, materias, calificaciones), cada uno un diccionario.
    Las listas son locales: ya no hay variables globales con los datos."""
    # ESTUDIANTES
    codigos_estudiantes = [100, 101, 102, 103, 104, 105, 106, 107, 108, 109]
    nombres_estudiantes = ["Mora Lassalle", "Matías Cura", "Marcos Silva Sapia", "Nicolás Patiño Pizarro",
                           "Vera Spina", "Lyndsy Camara", "Lara Hoffman", "Juliana Sofia Gamas",
                           "Juan Pérez", "Tomas Fernández"]
    edades_estudiantes = [21, 22, 23, 20, 24, 21, 22, 20, 22, 25]
    anios_cursada = [2, 2, 3, 1, 3, 1, 1, 1, 2, 4]
    correos_estudiantes = ["mora.lassalle@gmail.com", "matias.cura@gmail.com", "marcos.silva@alumno.edu.ar",
                           "nicolas.patino@gmail.com", "vera.spina@gmail.com", "lyndsy.camara@gmail.com",
                           "lara.hoffman@gmail.com", "juliana.gamas@alumno.edu.ar", "juan.perez@gmail.com",
                           "tomas.fernandez@gmail.com"]

    # MATERIAS
    codigos_materias = [200, 201, 202, 203, 204, 205, 206, 207, 208, 209]
    nombres_materias = ["Inglés", "Programación", "Estadística", "Cálculo I", "Diseño Web",
                        "Sistemas Operativos", "Álgebra", "Física I", "Algoritmos", "Economía"]
    cuatrimestres = [1, 1, 1, 1, 2, 2, 2, 2, 2, 1]
    cargas_horarias = [4, 4, 4, 4, 4, 4, 4, 4, 4, 4]

    # CALIFICACIONES
    codigos_calificaciones = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    estudiantes_calif = [100, 101, 102, 103, 104, 105, 106, 107, 108, 109]
    materias_calif = [202, 201, 204, 200, 206, 208, 207, 205, 203, 209]
    notas = [8, 3, 6, 7, 6, 5, 9, 2, 4, 9]
    condiciones = [2, 3, 1, 1, 1, 1, 2, 3, 1, 2]

    estudiantes = armar_diccionario(codigos_estudiantes, CAMPOS_ESTUDIANTE,
                                    (nombres_estudiantes, edades_estudiantes, anios_cursada, correos_estudiantes))
    materias = armar_diccionario(codigos_materias, CAMPOS_MATERIA,
                                 (nombres_materias, cuatrimestres, cargas_horarias))
    calificaciones = armar_diccionario(codigos_calificaciones, CAMPOS_CALIFICACION,
                                       (estudiantes_calif, materias_calif, notas, condiciones))
    return (estudiantes, materias, calificaciones)


# ------------------------------------------------------------
# VALIDACIONES: cada una devuelve el dato limpio o lanza ValueError
# con un mensaje claro para el usuario. No piden datos por teclado,
# por eso se pueden probar con pruebas unitarias.
# ------------------------------------------------------------

def convertir_entero(texto, campo):
    """Convierte un texto a entero. Lanza ValueError si esta vacio o no es un numero."""
    texto = str(texto).strip()
    if texto == "":
        raise ValueError(f"El campo {campo} es obligatorio")
    try:
        return int(texto)
    except ValueError:
        raise ValueError(f"El campo {campo} debe ser un número entero")


def validar_rango(valor, rango, campo):
    """Verifica que valor este dentro de rango = (minimo, maximo), extremos incluidos."""
    minimo, maximo = rango   # desempaquetado de la tupla
    if valor < minimo or valor > maximo:
        raise ValueError(f"El campo {campo} debe estar entre {minimo} y {maximo}")
    return valor


def validar_texto_obligatorio(texto, campo):
    """Saca espacios de los extremos y espacios dobles. Lanza ValueError si queda vacio.
    Sirve para textos que no son nombres de persona (ej: nombre de una materia)."""
    texto = str(texto).strip()
    while "  " in texto:
        texto = texto.replace("  ", " ")
    if texto == "":
        raise ValueError(f"El campo {campo} es obligatorio")
    return texto


def validar_nombre(nombre):
    """Nombre de persona: solo letras y espacios, al menos nombre y apellido,
    cada palabra con 2 letras o mas y empezando con mayuscula."""
    nombre = validar_texto_obligatorio(nombre, "nombre")
    for caracter in nombre:
        if not caracter.isalpha() and caracter != " ":
            raise ValueError("El nombre debe contener solo letras y espacios")
    palabras = nombre.split(" ")
    if len(palabras) < 2:
        raise ValueError("Debe ingresar al menos nombre y apellido")
    for palabra in palabras:
        if len(palabra) < 2:
            raise ValueError("Cada parte del nombre debe tener al menos 2 letras")
        if not palabra[0].isupper():
            raise ValueError("Cada parte del nombre debe empezar con mayúscula (ej: Juan Pérez)")
    return nombre


def validar_correo(correo):
    """Valida el formato del correo con expresion regular (usuario@dominio.ext)."""
    correo = validar_texto_obligatorio(correo, "correo")
    if not re.match(PATRON_CORREO, correo):
        raise ValueError("Correo inválido. Ejemplos válidos: usuario@gmail.com, usuario@alumno.edu.ar")
    return correo


def validar_opcion(texto, opciones_validas):
    """Convierte la opcion elegida a entero y verifica que exista en el menu."""
    opcion = convertir_entero(texto, "opción")
    if opcion not in opciones_validas:
        lista_opciones = ", ".join(map(str, opciones_validas))
        raise ValueError(f"Opción inexistente. Opciones válidas: {lista_opciones}")
    return opcion


def condicion_a_texto(codigo_condicion):
    """Traduce la condicion numerica (1, 2 o 3) a su nombre usando la tupla CONDICIONES."""
    validar_rango(codigo_condicion, (1, len(CONDICIONES)), "condición")
    return CONDICIONES[codigo_condicion - 1]


def es_aprobada(nota):
    """Criterio unico de aprobacion para todo el sistema."""
    return nota >= NOTA_APROBACION


# ------------------------------------------------------------
# INGRESO DE DATOS
# pedir_dato es el unico ciclo de "pedir hasta que sea valido".
# Reemplaza los while repetidos de todas las altas y modificaciones.
# ------------------------------------------------------------

def pedir_dato(mensaje, validador):
    """Pide un dato por teclado y lo pasa por validador (una funcion).
    Si el validador lanza ValueError, muestra el motivo y vuelve a pedir."""
    while True:
        texto = input(mensaje)
        try:
            return validador(texto)
        except ValueError as error:
            print("Error:", error)


def pedir_entero(mensaje, campo="valor"):
    """Se mantiene el nombre de la Parte 1 para no romper el codigo que ya lo usa."""
    return pedir_dato(mensaje, lambda texto: convertir_entero(texto, campo))


def pedir_entero_en_rango(mensaje, rango, campo):
    """Pide un entero y verifica que este dentro del rango (tupla de constantes)."""
    return pedir_dato(mensaje, lambda texto: validar_rango(convertir_entero(texto, campo), rango, campo))


def pedir_opcion(opciones_validas, mensaje="Elija una opción: "):
    """Pide una opcion de menu y solo acepta las que existen."""
    return pedir_dato(mensaje, lambda texto: validar_opcion(texto, opciones_validas))


# ------------------------------------------------------------
# LOGIN
# ------------------------------------------------------------

def credenciales_validas(usuario, contrasena, usuarios):
    """True si el usuario existe en el diccionario y la contraseña coincide."""
    return usuario in usuarios and usuarios[usuario] == contrasena


def login(usuarios=USUARIOS, intentos_maximos=INTENTOS_MAXIMOS):
    """Permite hasta intentos_maximos intentos.
    Devuelve el nombre del usuario si el ingreso fue correcto, o "" si se bloqueo.
    Cada intento queda registrado en log_operaciones.txt (auditoria de accesos)."""
    intentos = intentos_maximos
    while intentos > 0:
        usuario = input("Ingrese su usuario: ").strip()
        contrasena = input("Ingrese su contraseña: ")
        if credenciales_validas(usuario, contrasena, usuarios):
            print("---Inicio de sesión válido---")
            registrar_operacion("LOGIN_OK", usuario, "ingreso correcto")
            return usuario
        intentos = intentos - 1
        # Nunca se guarda la contraseña en el log, solo el usuario que se intentó
        registrar_operacion("LOGIN_FALLIDO", usuario, f"quedan {intentos} intentos")
        print("-Inicio de sesión inválido, te quedan", intentos, "intentos-")
    registrar_operacion("BLOQUEO", usuario, "se agotaron los intentos")
    return ""
