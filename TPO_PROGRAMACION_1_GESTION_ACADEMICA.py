# LISTAS
from functools import reduce
import re

# ESTUDIANTES
codigos_estudiantes = [100,101,102,103,104,105,106,107,108,109]

nombres_estudiantes = [ "Mora Lassalle","Matías Cura","Marcos Silva Sapia","Nicolás Patiño Pizarro","Vera Spina","Lyndsy Camara","Lara Hoffman","Juliana Sofia Gamas","Juan Pérez","Tomas Fernández"]

edades_estudiantes = [21,22,23,20,24,21,22,20,22,25]

ages_cursada = [2,2,3,1,3,1,1,1,2,4]

correos_estudiantes = ["mora.lassalle@gmail.com","matias.cura@gmail.com","marcos.silva@alumno.edu.ar",
                       "nicolas.patino@gmail.com","vera.spina@gmail.com","lyndsy.camara@gmail.com",
                       "lara.hoffman@gmail.com","juliana.gamas@alumno.edu.ar","juan.perez@gmail.com",
                       "tomas.fernandez@gmail.com"]


# MATERIAS
codigos_materias = [200,201,202,203,204,205,206,207,208,209]

nombres_materias = ["Inglés","Programación","Estadística","Cálculo I","Diseño Web","Sistemas Operativos","Álgebra","Física I","Algoritmos","Economía"]

cuatrimestres = [1,1,1,1,2,2,2,2,2,1]

cargas_horarias = [4,4,4,4,4,4,4,4,4,4]


# CALIFICACIONES
codigos_calificaciones = [1,2,3,4,5,6,7,8,9,10]

codigos_estudiantes_calif = [100,101,102,103,104,105,106,107,108,109]

codigos_materias_calif = [202,201,204,200,206,208,207,205,203,209]

notas = [8,3,6,7,6,5,9,2,4,9]

condiciones = [2,3,1,1,1,1,2,3,1,2]

#FUNCIONES DE USO GENERAL
#FUNCION DE BUSQUEDA EN LISTA
def buscar_en_listas_secuencial(lista, dato):
    indice = 0
    while indice < len(lista):
        if lista[indice] == dato:
            return indice
        indice = indice + 1
    return -1

#FUNCION DE BUSQUEDA BINARIA
# PRECONDICION: la lista debe estar ordenada de menor a mayor
def buscar_en_listas_binaria(lista, dato):
    izquierda = 0
    derecha = len(lista) - 1
    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2
        if lista[medio] == dato:
            return medio
        elif lista[medio] < dato:
            izquierda = medio + 1
        else:
            derecha = medio - 1
    return -1

#FUNCION DE ORDENAMIENTO POR SELECCION
def ordenar_estudiantes_por_edad(codigos, nombres, edades, ages, correos):
    for i in range(len(edades)):
        min_idx = i
        for j in range(i+1, len(edades)):
            if edades[j] < edades[min_idx]:
                min_idx = j
        edades[i], edades[min_idx] = edades[min_idx], edades[i]
        codigos[i], codigos[min_idx] = codigos[min_idx], codigos[i]
        nombres[i], nombres[min_idx] = nombres[min_idx], nombres[i]
        ages[i], ages[min_idx] = ages[min_idx], ages[i]
        correos[i], correos[min_idx] = correos[min_idx], correos[i]
    print("Estudiantes ordenados por edad.")

#FUNCION AUXILIAR: ordena codigos_estudiantes por codigo (para habilitar busqueda binaria en modificacion)
def ordenar_estudiantes_por_codigo(codigos, nombres, edades, ages, correos):
    for i in range(len(codigos)):
        min_idx = i
        for j in range(i+1, len(codigos)):
            if codigos[j] < codigos[min_idx]:
                min_idx = j
        codigos[i], codigos[min_idx] = codigos[min_idx], codigos[i]
        nombres[i], nombres[min_idx] = nombres[min_idx], nombres[i]
        edades[i], edades[min_idx] = edades[min_idx], edades[i]
        ages[i], ages[min_idx] = ages[min_idx], ages[i]
        correos[i], correos[min_idx] = correos[min_idx], correos[i]

#FUNCION DE ORDENAMIENTO POR BURBUJA
def ordenar_calificaciones_por_nota(codigos_calif, est_calif, mat_calif, notas, condiciones):
    n = len(notas)
    for i in range(n):
        # OPTIMIZACION (corte anticipado / "bandera de intercambio"):
        # si en una pasada completa no se hizo NINGUN intercambio, la lista ya esta
        # ordenada y no hace falta seguir pasando -> cortamos el bucle externo antes.
        hubo_intercambio = False
        for j in range(0, n-i-1):
            if notas[j] > notas[j+1]:
                notas[j], notas[j+1] = notas[j+1], notas[j]
                codigos_calif[j], codigos_calif[j+1] = codigos_calif[j+1], codigos_calif[j]
                est_calif[j], est_calif[j+1] = est_calif[j+1], est_calif[j]
                mat_calif[j], mat_calif[j+1] = mat_calif[j+1], mat_calif[j]
                condiciones[j], condiciones[j+1] = condiciones[j+1], condiciones[j]
                hubo_intercambio = True
        if not hubo_intercambio:
            break
    print("Calificaciones ordenadas por nota.")

#FUNCION DE ORDENAMIENTO POR INSERCION
def ordenar_materias_por_cuatrimestre(codigos, nombres, cuatrimestre, carga_horaria):
    for i in range(1, len(cuatrimestre)):
        clave_cuatrimestre = cuatrimestre[i]
        clave_codigo = codigos[i]
        clave_nombre = nombres[i]
        clave_carga = carga_horaria[i]
        j = i - 1
        while j >= 0 and clave_cuatrimestre < cuatrimestre[j]:
            cuatrimestre[j+1] = cuatrimestre[j]
            codigos[j+1] = codigos[j]
            nombres[j+1] = nombres[j]
            carga_horaria[j+1] = carga_horaria[j]
            j = j - 1
        cuatrimestre[j+1] = clave_cuatrimestre
        codigos[j+1] = clave_codigo
        nombres[j+1] = clave_nombre
        carga_horaria[j+1] = clave_carga
    print("Materias ordenadas por cuatrimestre.")

# FUNCION AUXILIAR: pide un numero entero al usuario, repite si no es un numero
def pedir_entero(mensaje):
    # Manejo de excepciones: controla entradas que no se pueden convertir a entero.
    while True:
        entrada = input(mensaje)

        try:
            numero = int(entrada)
        except ValueError:
            print("Entrada invalida. Por favor ingrese un numero entero.")
        else:
            return numero

# FUNCION AUXILIAR: pide un nombre completo (nombre + apellido, y opcionalmente
# segundo nombre) y valida que:
# - solo tenga letras y espacios
# - tenga al menos 2 palabras (nombre y apellido)
# - cada palabra tenga al menos 2 letras
# - cada palabra empiece con mayuscula
def pedir_nombre(mensaje):
    while True:
        nombre = input(mensaje).strip()
        while "  " in nombre:
            nombre = nombre.replace("  ", " ")
        palabras = nombre.split(" ")
        solo_letras_y_espacios = len(nombre) > 0 and all(c.isalpha() or c == " " for c in nombre)
        al_menos_2_palabras = len(palabras) >= 2
        cada_palabra_valida = all(len(palabra) >= 2 for palabra in palabras)
        cada_palabra_mayuscula = all(palabra[0].isupper() for palabra in palabras if len(palabra) > 0)
        if solo_letras_y_espacios and al_menos_2_palabras and cada_palabra_valida and cada_palabra_mayuscula:
            return nombre
        elif not solo_letras_y_espacios:
            print("Nombre invalido. Debe contener solo letras y espacios (sin numeros ni simbolos).")
        elif not al_menos_2_palabras:
            print("Nombre invalido. Debe ingresar al menos nombre y apellido.")
        elif not cada_palabra_valida:
            print("Nombre invalido. Cada parte del nombre (nombre, segundo nombre, apellido) debe tener al menos 2 letras.")
        else:
            print("Nombre invalido. Cada parte del nombre debe empezar con mayuscula (ej: Juan Perez).")

# FUNCION AUXILIAR: pide un correo electronico y valida su formato
# Acepta dominios con uno o mas niveles (gmail.com, universidad.edu.ar, empresa.com.ar, etc.)
PATRON_CORREO = r'^[A-Za-z0-9_.+-]+@[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)+$'
def pedir_correo(mensaje):
    while True:
        correo = input(mensaje).strip()
        if re.match(PATRON_CORREO, correo):
            return correo
        print("Correo invalido. Ejemplos validos: usuario@gmail.com, usuario@universidad.edu.ar")

# FUNCION AUXILIAR: pide nota y condicion y valida que sean consistentes entre si
# (nota >= 6 implica aprobado; nota < 6 implica desaprobado)
def pedir_nota_y_condicion():
    while True:
        nota = pedir_entero("Ingrese la nota (1-10): ")
        while nota < 1 or nota > 10:
            nota = pedir_entero("Nota invalida, ingrese un valor entre 1 y 10: ")
        condicion = pedir_entero("Ingrese la condición (1=regular, 2=promocionado, 3=desaprobado): ")
        while condicion < 1 or condicion > 3:
            condicion = pedir_entero("Condición invalida, ingrese 1, 2 o 3: ")
        aprobo_por_condicion = condicion in (1, 2)
        aprobo_por_nota = nota >= 6
        if aprobo_por_condicion == aprobo_por_nota:
            return nota, condicion
        if aprobo_por_condicion:
            print("Inconsistencia: la condición es aprobado/promocionado pero la nota es menor a 6. Vuelva a cargar nota y condición.")
        else:
            print("Inconsistencia: la condición es desaprobado pero la nota es mayor o igual a 6. Vuelva a cargar nota y condición.")

#FUNCIONES ESTUDIANTES
#FUNCION DE ALTA ESTUDIANTES
def alta_estudiantes(codigo, nombre, edad, age, correo):
    nuevo_codigo = pedir_entero("Ingrese el codigo del estudiante nuevo (100-999): ")
    while nuevo_codigo < 100 or nuevo_codigo > 999:
        nuevo_codigo = pedir_entero("Codigo invalido, debe estar entre 100 y 999: ")
    bandera1 = False
    while bandera1 != True:
        if nuevo_codigo in codigo:
            nuevo_codigo = pedir_entero("El codigo ya esta asignado a otro estudiante, porfavor ingrese otro número: ")
            while nuevo_codigo < 100 or nuevo_codigo > 999:
                nuevo_codigo = pedir_entero("Codigo invalido, debe estar entre 100 y 999: ")
        else:
            codigo.append(nuevo_codigo)
            bandera1 = True
    nuevo_nombre = pedir_nombre("Ingrese el nombre del estudiante nuevo: ")
    nombre.append(nuevo_nombre)
    nuevo_edad = pedir_entero("Ingrese la edad del estudiante nuevo: ")
    while nuevo_edad < 17 or nuevo_edad > 99:
        nuevo_edad = pedir_entero("Edad invalida, ingrese nuevamente la edad (17-99): ")
    edad.append(nuevo_edad)
    nuevo_age = pedir_entero("Ingrese el año de cursada del estudiante nuevo: ")
    while nuevo_age < 1  or nuevo_age > 9:
        nuevo_age = pedir_entero("Año de cursada invalido, ingrese nuevamente (1-9): ")
    age.append(nuevo_age)
    nuevo_correo = pedir_correo("Ingrese el correo electronico del estudiante nuevo: ")
    correo.append(nuevo_correo)
    print("El estudiante",nuevo_nombre,nuevo_codigo,"ha sido dado de alta correctamente")

#FUNCION DE BAJA ESTUDIANTES
# Si el estudiante tiene calificaciones asociadas, se ofrece eliminar UNICAMENTE
# las calificaciones de ESE estudiante (no todas las calificaciones del sistema).
def baja_estudiantes(codigos, nombres, edades, ages, correos, codigos_calif, est_calif, mat_calif, notas, condiciones):
    codigo = pedir_entero("Ingrese el código del estudiante a eliminar: ")
    if codigo in codigos:
        pos = buscar_en_listas_secuencial(codigos, codigo)
        indices_asociados = [i for i in range(len(est_calif)) if est_calif[i] == codigo]
        if len(indices_asociados) > 0:
            print("No se puede eliminar porque tiene calificaciones asociadas")
            respuesta = input("Para eliminar el estudiante se deben eliminar sus calificaciones, ¿desea eliminar las calificaciones de este estudiante? (si/no): ").strip().lower()
            if respuesta != "si":
                print("Operación cancelada. El estudiante no fue eliminado.")
                return
            for i in sorted(indices_asociados, reverse=True):
                codigos_calif.pop(i)
                est_calif.pop(i)
                mat_calif.pop(i)
                notas.pop(i)
                condiciones.pop(i)
            print("Se eliminaron las calificaciones del estudiante.")
        codigos.pop(pos)
        nombres.pop(pos)
        edades.pop(pos)
        ages.pop(pos)
        correos.pop(pos)
        print("Estudiante eliminado correctamente.")
    else:
        print("Código de estudiante no encontrado.")

#FUNCION DE MODIFICACION ESTUDIANTES
# Usa busqueda binaria: primero ordena por codigo, busca, luego restaura el orden original por codigo
def modificacion_estudiantes(codigos, nombres, edades, ages, correos):
    codigo = pedir_entero("Ingrese el código del estudiante que desea modificar: ")
    if codigo in codigos:
        # Ordenar por codigo antes de usar busqueda binaria
        ordenar_estudiantes_por_codigo(codigos, nombres, edades, ages, correos)
        pos = buscar_en_listas_binaria(codigos, codigo)
        nombres[pos] = pedir_nombre("Ingrese nuevo nombre: ")
        edad = pedir_entero("Ingrese nueva edad: ")
        while edad < 17 or edad > 99:
            edad = pedir_entero("Edad invalida. Ingrese nueva edad: ")
        edades[pos] = edad
        anio = pedir_entero("Ingrese nuevo año de cursada: ")
        while anio < 1 or anio > 9:
            anio = pedir_entero("Año invalido. Ingrese nuevo año de cursada: ")
        ages[pos] = anio
        correos[pos] = pedir_correo("Ingrese nuevo correo electronico: ")
        print("Estudiante modificado correctamente.")
    else:
        print("El estudiante no existe.")

#FUNCION DE LISTADO DE ESTUDIANTES
def listado_estudiantes(codigos, nombres, edades, ages, correos):
    for i in range(len(codigos)):
        print("Codigo:", codigos[i], "-Nombre:", nombres[i], "-Edad:", edades[i], "- Año:", ages[i], "- Correo:", correos[i])


#FUNCIONES MATERIAS
#FUNCION DE ALTA MATERIAS
def alta_materias(codigo, nombre, cuatrimestre, carga_horaria):
    nuevo_codigo = pedir_entero("Ingrese el codigo de la materia nueva (200-999): ")
    while nuevo_codigo < 200 or nuevo_codigo > 999:
        nuevo_codigo = pedir_entero("Codigo invalido, debe estar entre 200 y 999: ")
    bandera1 = False
    while bandera1 != True:
        if nuevo_codigo in codigo:
            nuevo_codigo = pedir_entero("El codigo ya esta asignado a otra materia, porfavor ingrese otro número: ")
        else:
            codigo.append(nuevo_codigo)
            bandera1 = True
    nuevo_nombre = pedir_nombre("Ingrese el nombre de la materia nueva: ")
    nombre.append(nuevo_nombre)
    nuevo_cuatri = pedir_entero("Ingrese el cuatrimestre nuevo: ")
    while nuevo_cuatri < 1 or nuevo_cuatri > 2:
        print("Cuatrimestre invalido")
        nuevo_cuatri = pedir_entero("Ingrese cuatrimestre 1 o 2: ")
    cuatrimestre.append(nuevo_cuatri)
    nuevo_carga = pedir_entero("Ingrese la carga horaria de la materia: ")
    while nuevo_carga < 1 or nuevo_carga > 20:
        print("Carga horaria invalida")
        nuevo_carga = pedir_entero("Ingrese carga horaria: ")
    carga_horaria.append(nuevo_carga)
    print("La materia",nuevo_nombre,nuevo_codigo," ha sido dada de alta correctamente")

#FUNCION DE BAJA MATERIAS
# Si la materia tiene calificaciones asociadas, se ofrece eliminar UNICAMENTE
# las calificaciones de ESA materia (no todas las calificaciones del sistema).
def baja_materias(codigos, nombres, cuatrimestre, carga_horaria, codigos_calif, est_calif, mat_calif, notas, condiciones):
    codigo = pedir_entero("Ingrese el código de la materia a eliminar: ")
    if codigo in codigos:
        pos = buscar_en_listas_secuencial(codigos, codigo)
        indices_asociados = [i for i in range(len(mat_calif)) if mat_calif[i] == codigo]
        if len(indices_asociados) > 0:
            print("No se puede eliminar porque tiene calificaciones asociadas")
            respuesta = input("Para eliminar la materia se deben eliminar sus calificaciones, ¿desea eliminar las calificaciones de esta materia? (si/no): ").strip().lower()
            if respuesta != "si":
                print("Operación cancelada. La materia no fue eliminada.")
                return
            for i in sorted(indices_asociados, reverse=True):
                codigos_calif.pop(i)
                est_calif.pop(i)
                mat_calif.pop(i)
                notas.pop(i)
                condiciones.pop(i)
            print("Se eliminaron las calificaciones de la materia.")
        codigos.pop(pos)
        nombres.pop(pos)
        cuatrimestre.pop(pos)
        carga_horaria.pop(pos)
        print("Materia dada de baja correctamente.")
    else:
        print("Código de materia no encontrado.")

#FUNCION DE MODIFICACIONES MATERIAS
def modificacion_materias(codigos, nombres, cuatrimestre, carga_horaria):
    codigo = pedir_entero("Ingrese el código de la materia que desea modificar: ")
    if codigo in codigos:
        pos = buscar_en_listas_secuencial(codigos, codigo)
        nombres[pos] = pedir_nombre("Ingrese nuevo nombre de la materia: ")
        nuevo_cuatri = pedir_entero("Ingrese el nuevo cuatrimestre: ")
        while nuevo_cuatri < 1 or nuevo_cuatri > 2:
            nuevo_cuatri = pedir_entero("Cuatrimestre invalido. Ingrese nuevamente: ")
        cuatrimestre[pos] = nuevo_cuatri
        carga = pedir_entero("Ingrese carga horaria: ")
        while carga < 1 or carga > 20:
            carga = pedir_entero("Carga horaria invalida. Ingrese nuevamente: ")
        carga_horaria[pos] = carga
        print("Materia modificada correctamente")
    else:
        print("La materia no existe")

#FUNCIONES DE LISTADO DE MATERIAS
def listado_materias(codigos, nombres, cuatrimestre, carga_horaria):
    for i in range(len(codigos)):
        print("Codigo:", codigos[i], "-Nombre:", nombres[i], "-Cuatrimestre:", cuatrimestre[i], "-Carga horaria:", carga_horaria[i])


#FUNCIONES CALIFICACIONES

#FUNCION DE ALTA CALIFICACIONES
def alta_calificaciones(codigos_calif, est_calif, mat_calif, notas, condiciones, codigos_estudiantes, codigos_materias):
    nuevo_codigo = pedir_entero("Ingrese el código de la calificación nueva: ")

    bandera = False
    while bandera != True:
        if nuevo_codigo in codigos_calif:
            nuevo_codigo = pedir_entero("El código ya existe, ingrese otro: ")
        else:
            codigos_calif.append(nuevo_codigo)
            bandera = True

    codigo_est = pedir_entero("Ingrese el código del estudiante: ")

    while codigo_est not in codigos_estudiantes:
        codigo_est = pedir_entero("Ese estudiante no existe. Ingréselo de nuevo: ")

    codigo_mat = pedir_entero("Ingrese el código de la materia: ")

    while codigo_mat not in codigos_materias:
        codigo_mat = pedir_entero("Esa materia no existe. Ingrésela de nuevo: ")

    # No permite dos calificaciones para el mismo estudiante y materia.
    while any(est_calif[i] == codigo_est and mat_calif[i] == codigo_mat
              for i in range(len(est_calif))):

        print("Ese estudiante ya tiene una calificación para esa materia.")

        codigo_est = pedir_entero("Ingrese otro código de estudiante: ")

        while codigo_est not in codigos_estudiantes:
            codigo_est = pedir_entero("Ese estudiante no existe. Ingréselo de nuevo: ")

    # Recién ahora agregamos los datos
    est_calif.append(codigo_est)
    mat_calif.append(codigo_mat)

    nota, condicion = pedir_nota_y_condicion()

    notas.append(nota)
    condiciones.append(condicion)

    print("La calificación", nuevo_codigo, "fue dada de alta correctamente")

#FUNCION DE BAJA CALIFICACIONES
def baja_calificaciones(codigos_calif, est_calif, mat_calif, notas, condiciones):
    codigo = pedir_entero("Ingrese el código de la calificación a eliminar: ")
    if codigo in codigos_calif:
        pos = buscar_en_listas_secuencial(codigos_calif, codigo)
        codigos_calif.pop(pos)
        est_calif.pop(pos)
        mat_calif.pop(pos)
        notas.pop(pos)
        condiciones.pop(pos)
        print("Calificación eliminada correctamente.")
    else:
        print("Código de calificación no encontrado.")

#FUNCION DE MODIFICACION CALIFICACIONES
def modificacion_calificaciones(codigos_calif, est_calif, mat_calif, notas, condiciones, codigos_estudiantes, codigos_materias):
    codigo = pedir_entero("Ingrese el código de la calificación que desea modificar: ")
    if codigo in codigos_calif:
        pos = buscar_en_listas_secuencial(codigos_calif, codigo)
        codigo_est = pedir_entero("Ingrese el nuevo código del estudiante: ")
        while codigo_est not in codigos_estudiantes:
            codigo_est = pedir_entero("Ese estudiante no existe. Ingréselo de nuevo: ")
        est_calif[pos] = codigo_est
        codigo_mat = pedir_entero("Ingrese el nuevo código de la materia: ")
        while codigo_mat not in codigos_materias:
            codigo_mat = pedir_entero("Esa materia no existe. Ingrésela de nuevo: ")
        mat_calif[pos] = codigo_mat
        nota, condicion = pedir_nota_y_condicion()
        notas[pos] = nota
        condiciones[pos] = condicion
        print("Calificación modificada correctamente.")
    else:
        print("Código de calificación no encontrado.")

#FUNCION DE LISTADO CALIFICACIONES
def listado_calificaciones(codigos_calif, est_calif, mat_calif, notas, condiciones):
    for i in range(len(codigos_calif)):
        print("Codigo:", codigos_calif[i], "- Estudiante:", est_calif[i],
              "- Materia:", mat_calif[i], "- Nota:", notas[i], "- Condición:", condiciones[i])


# FUNCIONES DE MATRIZ Y ESTADISTICAS CON LAMBDA

def mostrar_matriz_notas():
    print("\n--- MATRIZ DE NOTAS (ESTUDIANTES X MATERIAS) ---")

    # Encabezado con codigos de materias
    print("Estudiante |", " | ".join(str(codigo) for codigo in codigos_materias))
    print("-" * (14 + len(codigos_materias) * 6))

    for codigo_est in codigos_estudiantes:
        fila = []
        for codigo_mat in codigos_materias:
            nota_encontrada = "-"
            for i in range(len(codigos_estudiantes_calif)):
                if (codigos_estudiantes_calif[i] == codigo_est
                        and codigos_materias_calif[i] == codigo_mat):
                    nota_encontrada = notas[i]
                    break
            fila.append(str(nota_encontrada))
        print(f"{codigo_est:9} |", " | ".join(fila))


def estadisticas_lambda():
    print("\n--- ESTADISTICAS CON FUNCIONES LAMBDA ---")

    notas_originales = notas.copy()

    # MAP: escala las notas de 1-10 a una escala de 0-100.
    notas_escaladas = list(map(lambda nota: nota * 10, notas_originales))

    # FILTER: aprobados segun la nota (>= 6).
    notas_aprobados = list(filter(lambda nota: nota >= 6, notas_originales))

    # REDUCE: promedio general.
    suma_notas = reduce(lambda acumulado, nota: acumulado + nota, notas_originales, 0)
    promedio = suma_notas / len(notas_originales) if notas_originales else 0

    print("Notas originales:", notas_originales)
    print("Notas escaladas sobre 100 (map):", notas_escaladas)
    print("Notas de aprobados (filter):", notas_aprobados)
    print("Promedio general de notas (reduce):", promedio)


# ============================================================
# MANEJO DE ERRORES INTEGRADO
# ============================================================
# El manejo de excepciones se aplica dentro de las operaciones reales
# del sistema. Se controlan especialmente ValueError, IndexError,
# KeyError, TypeError y ZeroDivisionError, evitando cierres abruptos.

# Login
print("---Sistema de calificaciones---")
print("    --Inicio de sesión--       ")
# INICIO FUNCION LOGIN
def login():
#Datos
    usuarios_validos = "admin"
    contrasenas_validas = "admin"
    intentos = 3
    ingreso_correcto = False

# Ciclo de validación o no
    while ingreso_correcto == False and intentos > 0:
            usuario = input("Ingrese su usuario: ")
            contrasena = input("Ingrese su contraseña: ")

            if usuario == usuarios_validos and contrasena == contrasenas_validas:
                print("---Inicio de sesión valido---")
                ingreso_correcto = True
            else:
                intentos = intentos - 1
                print("-Inicio de sesión invalido, te quedan", intentos,"intentos-")
    return ingreso_correcto
# FIN FUNCION LOGIN

# INICIO FUNCION SUBMENU ESTUDIANTES
def submenu1():
    salida_submenu1 = False  #Bandera para salir del programa
    while salida_submenu1 == False:
        print("---Submenu de estudiantes ---")
        print("1. Alta")
        print("2. Baja")
        print("3. Modificación")
        print("4. Listado")
        print("5. Listado ordenado por edad")
        print("0. Volver atras")

        opcion = pedir_entero("Elije una opción: ")

        if opcion == 1:
            alta_estudiantes(codigos_estudiantes, nombres_estudiantes, edades_estudiantes, ages_cursada, correos_estudiantes)
        elif opcion == 2:
            baja_estudiantes(codigos_estudiantes, nombres_estudiantes, edades_estudiantes, ages_cursada, correos_estudiantes, codigos_calificaciones, codigos_estudiantes_calif, codigos_materias_calif, notas, condiciones)
        elif opcion == 3:
            modificacion_estudiantes(codigos_estudiantes, nombres_estudiantes, edades_estudiantes, ages_cursada, correos_estudiantes)
        elif opcion == 4:
            listado_estudiantes(codigos_estudiantes, nombres_estudiantes, edades_estudiantes, ages_cursada, correos_estudiantes)
        elif opcion == 5:
            ordenar_estudiantes_por_edad(codigos_estudiantes, nombres_estudiantes, edades_estudiantes, ages_cursada, correos_estudiantes)
            listado_estudiantes(codigos_estudiantes, nombres_estudiantes, edades_estudiantes, ages_cursada, correos_estudiantes)
        elif opcion == 0:
            salida_submenu1 = True
        else:
            print("Opcion no valida, vuelva a elegir")
# FIN FUNCION SUBMENU ESTUDIANTES

# INICIO SUBMENU MATERIAS
def submenu2():
    salida_submenu2 = False  #Bandera para salir del programa
    while salida_submenu2 == False:
        print("---Submenu de materias---")
        print("1. Alta")
        print("2. Baja")
        print("3. Modificación")
        print("4. Listado")
        print("5. Listado ordenado por cuatrimestre")
        print("0. Volver atras")

        opcion = pedir_entero("Elije una opción: ")

        if opcion == 1:
            alta_materias(codigos_materias, nombres_materias, cuatrimestres, cargas_horarias)
        elif opcion == 2:
            baja_materias(codigos_materias, nombres_materias, cuatrimestres, cargas_horarias, codigos_calificaciones, codigos_estudiantes_calif, codigos_materias_calif, notas, condiciones)
        elif opcion == 3:
            modificacion_materias(codigos_materias, nombres_materias, cuatrimestres, cargas_horarias)
        elif opcion == 4:
            listado_materias(codigos_materias, nombres_materias, cuatrimestres, cargas_horarias)
        elif opcion == 5:
            ordenar_materias_por_cuatrimestre(codigos_materias, nombres_materias, cuatrimestres, cargas_horarias)
            listado_materias(codigos_materias, nombres_materias, cuatrimestres, cargas_horarias)
        elif opcion == 0:
            salida_submenu2 = True
        else:
            print("Opcion no valida, vuelva a elegir")
# FIN FUNCION SUBMENU MATERIAS

# INICIO FUNCION SUBMENU CALIFICACIONES
def submenu3():
    salida_submenu3 = False  #Bandera para salir del programa
    while salida_submenu3 == False:
        print("---Submenu de calificaciones---")
        print("1. Alta")
        print("2. Baja")
        print("3. Modificación")
        print("4. Listado")
        print("5. Listado ordenado por nota")
        print("6. Estadística por materia")
        print("7. Matriz de notas (Estudiantes x Materias)")
        print("8. Estadísticas con funciones lambda (map/filter/reduce)")
        print("0. Volver atras")

        opcion = pedir_entero("Elije una opción: ")

        if opcion == 1:
            alta_calificaciones(codigos_calificaciones, codigos_estudiantes_calif, codigos_materias_calif, notas, condiciones, codigos_estudiantes, codigos_materias)
        elif opcion == 2:
            baja_calificaciones(codigos_calificaciones, codigos_estudiantes_calif, codigos_materias_calif, notas, condiciones)
        elif opcion == 3:
            modificacion_calificaciones(codigos_calificaciones, codigos_estudiantes_calif, codigos_materias_calif, notas, condiciones, codigos_estudiantes, codigos_materias)
        elif opcion == 4:
            listado_calificaciones(codigos_calificaciones, codigos_estudiantes_calif, codigos_materias_calif, notas, condiciones)
        elif opcion == 5:
            ordenar_calificaciones_por_nota(codigos_calificaciones, codigos_estudiantes_calif, codigos_materias_calif, notas, condiciones)
            listado_calificaciones(codigos_calificaciones, codigos_estudiantes_calif, codigos_materias_calif, notas, condiciones)
        elif opcion == 6:
            informe_aprobados_por_materia()
        elif opcion == 7:
            mostrar_matriz_notas()
        elif opcion == 8:
            estadisticas_lambda()
        elif opcion == 0:
            salida_submenu3 = True
        else:
            print("Opcion no valida, vuelva a elegir")
# FIN FUNCION SUBMENU CALIFICACIONES


# ===== NUEVAS ESTRUCTURAS DE DATOS: DICCIONARIOS, TUPLAS Y CONJUNTOS =====

# ---------------- DICCIONARIOS ----------------

def crear_diccionario_estudiantes():
    # Diccionario anidado: codigo -> datos del estudiante.
    # La clave permite acceder rapidamente a toda la informacion del alumno.
    estudiantes = {}

    try:
        for i in range(len(codigos_estudiantes)):
            estudiantes[codigos_estudiantes[i]] = {
                "nombre": nombres_estudiantes[i],
                "edad": edades_estudiantes[i],
                "año": ages_cursada[i],
                "correo": correos_estudiantes[i]
            }
    except IndexError:
        # Si alguna lista paralela tiene distinta cantidad de elementos,
        # se evita que el sistema se cierre.
        print("Error: los datos de estudiantes no tienen la misma cantidad de elementos.")
        return {}

    return estudiantes


def mostrar_diccionario_estudiantes():
    estudiantes = crear_diccionario_estudiantes()

    print("\n--- DICCIONARIO DE ESTUDIANTES ---")
    print("Clave = codigo | Valor = datos del estudiante")

    for codigo, datos in estudiantes.items():
        print(codigo, "->", datos)

    print("\nCantidad de estudiantes:", len(estudiantes))

    # keys() obtiene las claves y values() obtiene los valores.
    print("Claves:", list(estudiantes.keys()))
    print("Valores:", list(estudiantes.values()))


def consultar_estudiante_diccionario():
    estudiantes = crear_diccionario_estudiantes()
    codigo = pedir_entero("Ingrese el codigo del estudiante a consultar: ")

    # get() evita un KeyError si la clave no existe.
    try:
        datos = estudiantes.get(codigo)
        if datos is None:
            print("El estudiante no existe.")
        else:
            print("\n--- DATOS DEL ESTUDIANTE ---")
            for clave, valor in datos.items():
                print(clave, ":", valor)
    except KeyError:
        print("Error: la clave del estudiante no existe en el diccionario.")


def modificar_estudiante_diccionario():
    estudiantes = crear_diccionario_estudiantes()
    codigo = pedir_entero("Ingrese el codigo del estudiante a modificar: ")

    if codigo not in estudiantes:
        print("El estudiante no existe.")
        return

    estudiantes[codigo]["edad"] = pedir_entero("Ingrese la nueva edad: ")
    estudiantes[codigo]["año"] = pedir_entero("Ingrese el nuevo año de cursada: ")

    print("Diccionario modificado:")
    print(estudiantes[codigo])


def ordenar_diccionario_estudiantes():
    estudiantes = crear_diccionario_estudiantes()

    # Los diccionarios mantienen el orden de insercion.
    # Con sorted() podemos crear otro diccionario ordenado por clave.
    estudiantes_ordenados = dict(sorted(estudiantes.items()))

    print("\n--- DICCIONARIO ORDENADO POR CODIGO ---")
    for codigo, datos in estudiantes_ordenados.items():
        print(codigo, "->", datos)


def diccionario_listas_zip():
    # Las diapositivas muestran que un diccionario puede convertirse
    # en listas de claves y valores, y tambien reconstruirse con zip().
    dias = {1: "DO", 2: "LU", 3: "MA", 4: "MI", 5: "JU", 6: "VI", 7: "SA"}

    lista_claves = list(dias.keys())
    lista_valores = list(dias.values())
    nuevo_diccionario = dict(zip(lista_claves, lista_valores))

    print("\n--- DICCIONARIO, KEYS(), VALUES() Y ZIP() ---")
    print("Diccionario:", dias)
    print("Lista de claves:", lista_claves)
    print("Lista de valores:", lista_valores)
    print("Diccionario reconstruido con zip():", nuevo_diccionario)


def submenu_diccionarios():
    salir = False

    while not salir:
        print("\n--- SUBMENU DE DICCIONARIOS ---")
        print("1. Mostrar diccionario de estudiantes")
        print("2. Consultar estudiante con get()")
        print("3. Modificar datos en un diccionario")
        print("4. Ordenar diccionario por clave")
        print("5. Convertir diccionario a listas y usar zip()")
        print("0. Volver atras")

        opcion = pedir_entero("Elija una opcion: ")

        if opcion == 1:
            mostrar_diccionario_estudiantes()
        elif opcion == 2:
            consultar_estudiante_diccionario()
        elif opcion == 3:
            modificar_estudiante_diccionario()
        elif opcion == 4:
            ordenar_diccionario_estudiantes()
        elif opcion == 5:
            diccionario_listas_zip()
        elif opcion == 0:
            salir = True
        else:
            print("Opcion no valida.")


# ---------------- TUPLAS ----------------

def crear_tupla_estudiante():
    if len(codigos_estudiantes) == 0:
        print("No hay estudiantes cargados.")
        return

    codigo = pedir_entero("Ingrese el codigo del estudiante: ")
    pos = buscar_en_listas_secuencial(codigos_estudiantes, codigo)

    if pos == -1:
        print("El estudiante no existe.")
        return

    # Tupla: datos fijos y ordenados del estudiante.
    try:
        estudiante = (
            codigos_estudiantes[pos],
            nombres_estudiantes[pos],
            edades_estudiantes[pos],
            ages_cursada[pos],
            correos_estudiantes[pos]
        )
    except IndexError:
        print("Error: no se pudo acceder a los datos del estudiante.")
        return

    print("\n--- TUPLA DEL ESTUDIANTE ---")
    print("Tupla:", estudiante)
    print("Codigo (indice 0):", estudiante[0])
    print("Nombre (indice 1):", estudiante[1])
    print("Edad (indice 2):", estudiante[2])
    print("Año de cursada (indice 3):", estudiante[3])
    print("Correo (indice 4):", estudiante[4])

    # Desempaquetado de tupla.
    codigo_t, nombre_t, edad_t, año_t, correo_t = estudiante
    print("\nDesempaquetado:")
    print(codigo_t, nombre_t, edad_t, año_t, correo_t)

    print("Las tuplas son inmutables: no se pueden agregar, eliminar ni modificar elementos.")


def mostrar_tuplas_materias():
    print("\n--- TUPLAS DE MATERIAS ---")

    for i in range(len(codigos_materias)):
        materia = (
            codigos_materias[i],
            nombres_materias[i],
            cuatrimestres[i],
            cargas_horarias[i]
        )
        print(materia)


def tupla_como_clave():
    # Una tupla puede utilizarse como clave de un diccionario.
    aulas = {
        (1, "Lunes"): "Aula 101",
        (1, "Martes"): "Aula 203",
        (2, "Lunes"): "Aula 305"
    }

    print("\n--- TUPLA COMO CLAVE DE DICCIONARIO ---")
    print(aulas)

    clave = (1, "Lunes")
    print("Buscando", clave, "->", aulas.get(clave))


def submenu_tuplas():
    salir = False

    while not salir:
        print("\n--- SUBMENU DE TUPLAS ---")
        print("1. Crear y recorrer tupla de un estudiante")
        print("2. Mostrar tuplas de materias")
        print("3. Usar una tupla como clave de diccionario")
        print("0. Volver atras")

        opcion = pedir_entero("Elija una opcion: ")

        if opcion == 1:
            crear_tupla_estudiante()
        elif opcion == 2:
            mostrar_tuplas_materias()
        elif opcion == 3:
            tupla_como_clave()
        elif opcion == 0:
            salir = True
        else:
            print("Opcion no valida.")


# ---------------- CONJUNTOS ----------------

def crear_conjuntos_sistema():
    conjunto_estudiantes = set(codigos_estudiantes)
    conjunto_estudiantes_con_nota = set(codigos_estudiantes_calif)

    conjunto_materias = set(codigos_materias)
    conjunto_materias_con_nota = set(codigos_materias_calif)

    return (
        conjunto_estudiantes,
        conjunto_estudiantes_con_nota,
        conjunto_materias,
        conjunto_materias_con_nota
    )


def mostrar_conjuntos():
    estudiantes, estudiantes_nota, materias, materias_nota = crear_conjuntos_sistema()

    print("\n--- CONJUNTOS DEL SISTEMA ---")
    print("Estudiantes:", estudiantes)
    print("Estudiantes con calificacion:", estudiantes_nota)
    print("Materias:", materias)
    print("Materias con calificacion:", materias_nota)


def operaciones_conjuntos():
    estudiantes, estudiantes_nota, materias, materias_nota = crear_conjuntos_sistema()

    print("\n--- OPERACIONES CON CONJUNTOS ---")

    # INTERSECCION: elementos que estan en ambos conjuntos.
    con_calificacion = estudiantes & estudiantes_nota

    # DIFERENCIA: elementos que estan en el primer conjunto pero no en el segundo.
    sin_calificacion = estudiantes - estudiantes_nota

    # UNION: todos los elementos sin repetir.
    todos_los_estudiantes = estudiantes | estudiantes_nota

    # DIFERENCIA SIMETRICA: elementos que estan en uno u otro, pero no en ambos.
    exclusivos = estudiantes ^ estudiantes_nota

    print("Union de estudiantes:", todos_los_estudiantes)
    print("Interseccion (estudiantes con calificacion):", con_calificacion)
    print("Diferencia (estudiantes sin calificacion):", sin_calificacion)
    print("Diferencia simetrica:", exclusivos)

    print("\n--- OPERACIONES CON MATERIAS ---")
    print("Union:", materias | materias_nota)
    print("Interseccion:", materias & materias_nota)
    print("Diferencia (materias sin calificacion):", materias - materias_nota)
    print("Diferencia simetrica:", materias ^ materias_nota)


def buscar_en_conjunto():
    estudiantes, _, _, _ = crear_conjuntos_sistema()

    codigo = pedir_entero("Ingrese el codigo del estudiante a buscar: ")

    if codigo in estudiantes:
        print("El codigo pertenece al conjunto de estudiantes.")
    else:
        print("El codigo no pertenece al conjunto de estudiantes.")


def eliminar_repetidos_con_set():
    # Los conjuntos eliminan automaticamente los elementos repetidos.
    notas_con_repetidos = [8, 3, 6, 7, 6, 5, 9, 2, 4, 9, 8, 6]

    notas_unicas = set(notas_con_repetidos)

    print("\n--- ELIMINAR REPETIDOS CON SET ---")
    print("Lista original:", notas_con_repetidos)
    print("Conjunto sin repetidos:", notas_unicas)


def submenu_conjuntos():
    salir = False

    while not salir:
        print("\n--- SUBMENU DE CONJUNTOS ---")
        print("1. Mostrar conjuntos del sistema")
        print("2. Union, interseccion, diferencia y diferencia simetrica")
        print("3. Buscar elemento con in")
        print("4. Eliminar repetidos con set")
        print("0. Volver atras")

        opcion = pedir_entero("Elija una opcion: ")

        if opcion == 1:
            mostrar_conjuntos()
        elif opcion == 2:
            operaciones_conjuntos()
        elif opcion == 3:
            buscar_en_conjunto()
        elif opcion == 4:
            eliminar_repetidos_con_set()
        elif opcion == 0:
            salir = True
        else:
            print("Opcion no valida.")


# ---------------- MENU GENERAL DE NUEVAS ESTRUCTURAS ----------------

def submenu4():
    salir = False

    while not salir:
        print("\n--- ESTRUCTURAS DE DATOS NUEVAS ---")
        print("1. Diccionarios")
        print("2. Tuplas")
        print("3. Conjuntos")
        print("0. Volver atras")

        opcion = pedir_entero("Elija una opcion: ")

        if opcion == 1:
            submenu_diccionarios()
        elif opcion == 2:
            submenu_tuplas()
        elif opcion == 3:
            submenu_conjuntos()
        elif opcion == 0:
            salir = True
        else:
            print("Opcion no valida.")

# INICIO FUNCION MENU PRINCIPAL
def menu_principal():
    salida_menu = False  #Bandera para salir del programa
    while salida_menu == False:
        print("---Bienvenido al menú principal---")
        print("1. Estudiantes")
        print("2. Materias")
        print("3. Calificaciones")
        print("4. Diccionarios, Tuplas y Conjuntos")
        print("0. Cerrar sesión")

        opcion = pedir_entero("Seleccione una opción: ")

        if opcion == 1:
            submenu1()
        elif opcion == 2:
            submenu2()
        elif opcion == 3:
            submenu3()
        elif opcion == 4:
            submenu4()
        elif opcion == 0:
            print("Cerrando sesión")
            salida_menu = True
        else:
            print("Opcion no valida, porfavor elija nuevamente")
# FIN FUNCION MENU PRINCIPAL

# ===== MATRIZ Y ESTADISTICAS =====

def listas_a_matriz(lista1, lista2, lista3):
    # OPTIMIZACION / requisito de catedra: se arma la matriz con map + lambda en vez de un
    # bucle for manual. zip() empareja los 3 elementos de cada posicion i, y map aplica la
    # lambda a cada tupla para convertirla en la fila [lista1[i], lista2[i], lista3[i]].
    matriz = list(map(lambda fila: [fila[0], fila[1], fila[2]], zip(lista1, lista2, lista3)))
    return matriz

def conservar_unicos(matriz):
    # Recorre la matriz de calificaciones y arma la lista de materias unicas, conservando
    # el orden de aparicion (no se usa dict/set para no salirse de listas simples).
    unicos = []
    for fila in matriz:
        if buscar_en_listas_secuencial(unicos, fila[1]) == -1:
            unicos.append(fila[1])
    return unicos

def obtener_aprobados_materia(materias, notas, materia):
    # Se considera aprobada una calificacion cuando la nota es mayor o igual a 6.
    indices_aprobados = filter(
        lambda i: materias[i] == materia and notas[i] >= 6,
        range(len(materias))
    )
    return reduce(lambda acumulado, _indice: acumulado + 1, indices_aprobados, 0)

def obtener_desaprobados_materia(materias, notas, materia):
    # Se considera desaprobada una calificacion cuando la nota es menor a 6.
    indices_desaprobados = filter(
        lambda i: materias[i] == materia and notas[i] < 6,
        range(len(materias))
    )
    return reduce(lambda acumulado, _indice: acumulado + 1, indices_desaprobados, 0)

def armar_matriz_estadisticas(materias_unicas):
    # Recorre las calificaciones una sola vez y cuenta aprobados/desaprobados
    # segun la nota (>= 6 aprobado, < 6 desaprobado).
    aprobados = [0] * len(materias_unicas)
    desaprobados = [0] * len(materias_unicas)

    try:
        for i in range(len(codigos_materias_calif)):
            pos = buscar_en_listas_secuencial(materias_unicas, codigos_materias_calif[i])
            if pos != -1:
                if notas[i] >= 6:
                    aprobados[pos] += 1
                else:
                    desaprobados[pos] += 1
    except IndexError:
        print("Error: las listas de calificaciones no tienen datos consistentes.")
        return []

    matriz = list(map(
        lambda idx: [materias_unicas[idx], aprobados[idx], desaprobados[idx]],
        range(len(materias_unicas))
    ))
    return matriz

def obtener_nombre_materia(codigo):
    pos = buscar_en_listas_secuencial(codigos_materias, codigo)
    if pos != -1:
        return nombres_materias[pos]
    return "Desconocida"

def informe_aprobados_por_materia():
    matriz = listas_a_matriz(codigos_calificaciones, codigos_materias_calif, condiciones)
    materias_unicas = conservar_unicos(matriz)
    matriz_est = armar_matriz_estadisticas(materias_unicas)

    print("\n--- ESTADISTICA POR MATERIA ---")
    print("Materia             | Aprob | Desap | % Aprob")

    for fila in matriz_est:
        nombre = obtener_nombre_materia(fila[0])
        aprob = fila[1]
        desap = fila[2]
        total = aprob + desap

        try:
            porcentaje = (aprob * 100 / total) if total > 0 else 0
        except ZeroDivisionError:
            # Protección adicional: nunca dividir por cero.
            porcentaje = 0
        except TypeError:
            print("Error: los datos de aprobados/desaprobados no son numericos.")
            porcentaje = 0

        print(f"{nombre:20} | {aprob:^5} | {desap:^5} | {porcentaje:6.2f}%")

# NOTA SOBRE OTROS ERRORES DE LA CLASE XI:
# - NameError normalmente indica una variable o funcion mal escrita/no definida.
#   No se oculta con un except general porque es un error de programacion que
#   conviene detectar y corregir.
# - FileNotFoundError se aplica cuando el programa trabaja con archivos.
#   Este sistema no abre archivos durante su funcionamiento normal, por lo que
#   no se agrega una operacion artificial solo para provocar ese error.
# - TypeError se controla en las operaciones donde realmente puede aparecer.
#
# Se evita usar "except:" de forma general, porque la diapositiva advierte que
# esconder errores importantes dificulta detectar problemas y puede generar
# programas poco confiables.

# INICIO DE PROGRAMA
if __name__ == "__main__":
    inicio_de_sesion = login()

    if inicio_de_sesion == True:
        menu_principal()
    else:
        print("Por seguridad se bloqueo el acceso")
