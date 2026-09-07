from functools import reduce
import re

# ============================================================
# LISTAS (listas paralelas)
# ============================================================

# ESTUDIANTES
codigos_estudiantes = [100,101,102,103,104,105,106,107,108,109]
nombres_estudiantes = ["Mora Lassalle","Matías Cura","Marcos Silva Sapia","Nicolás Patiño Pizarro","Vera Spina","Lyndsy Camara","Lara Hoffman","Juliana Sofia Gamas","Juan Pérez","Tomas Fernández"]
edades_estudiantes = [21,22,23,20,24,21,22,20,22,25]
ages_cursada = [2,2,3,1,3,1,1,1,2,4]
correos_estudiantes = ["mora.lassalle@mail.com","matias.cura@mail.com","marcos.silva@mail.com","nicolas.patino@mail.com","vera.spina@mail.com","lyndsy.camara@mail.com","lara.hoffman@mail.com","juliana.gamas@mail.com","juan.perez@mail.com","tomas.fernandez@mail.com"]

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

# ============================================================
# FUNCIONES DE USO GENERAL: BUSQUEDA
# ============================================================

# FUNCION DE BUSQUEDA SECUENCIAL
def buscar_en_listas_secuencial(lista, dato):
    indice = 0
    while indice < len(lista):
        if lista[indice] == dato:
            return indice
        indice = indice + 1
    return -1

# FUNCION DE BUSQUEDA BINARIA
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

# ============================================================
# FUNCIONES DE USO GENERAL: ORDENAMIENTO
# ============================================================

# FUNCION DE ORDENAMIENTO POR SELECCION (edad)
def ordenar_estudiantes_por_edad(codigos, nombres, edades, ages, correos):
    for i in range(len(edades)):
        min_idx = i
        for j in range(i + 1, len(edades)):
            if edades[j] < edades[min_idx]:
                min_idx = j
        edades[i], edades[min_idx] = edades[min_idx], edades[i]
        codigos[i], codigos[min_idx] = codigos[min_idx], codigos[i]
        nombres[i], nombres[min_idx] = nombres[min_idx], nombres[i]
        ages[i], ages[min_idx] = ages[min_idx], ages[i]
        correos[i], correos[min_idx] = correos[min_idx], correos[i]
    print("Estudiantes ordenados por edad.")

# FUNCION AUXILIAR: ordena por codigo (selección) para habilitar busqueda binaria en modificacion
def ordenar_estudiantes_por_codigo(codigos, nombres, edades, ages, correos):
    for i in range(len(codigos)):
        min_idx = i
        for j in range(i + 1, len(codigos)):
            if codigos[j] < codigos[min_idx]:
                min_idx = j
        codigos[i], codigos[min_idx] = codigos[min_idx], codigos[i]
        nombres[i], nombres[min_idx] = nombres[min_idx], nombres[i]
        edades[i], edades[min_idx] = edades[min_idx], edades[i]
        ages[i], ages[min_idx] = ages[min_idx], ages[i]
        correos[i], correos[min_idx] = correos[min_idx], correos[i]

# FUNCION DE ORDENAMIENTO POR BURBUJA (nota), con corte anticipado
def ordenar_calificaciones_por_nota(codigos_calif, est_calif, mat_calif, notas, condiciones):
    n = len(notas)
    for i in range(n):
        # Si en una pasada completa no hay intercambios, la lista ya esta ordenada
        # y se corta el bucle externo antes de tiempo.
        hubo_intercambio = False
        for j in range(0, n - i - 1):
            if notas[j] > notas[j + 1]:
                notas[j], notas[j + 1] = notas[j + 1], notas[j]
                codigos_calif[j], codigos_calif[j + 1] = codigos_calif[j + 1], codigos_calif[j]
                est_calif[j], est_calif[j + 1] = est_calif[j + 1], est_calif[j]
                mat_calif[j], mat_calif[j + 1] = mat_calif[j + 1], mat_calif[j]
                condiciones[j], condiciones[j + 1] = condiciones[j + 1], condiciones[j]
                hubo_intercambio = True
        if not hubo_intercambio:
            break
    print("Calificaciones ordenadas por nota.")

# FUNCION DE ORDENAMIENTO POR INSERCION (cuatrimestre)
def ordenar_materias_por_cuatrimestre(codigos, nombres, cuatrimestre, carga_horaria):
    for i in range(1, len(cuatrimestre)):
        clave_cuatrimestre = cuatrimestre[i]
        clave_codigo = codigos[i]
        clave_nombre = nombres[i]
        clave_carga = carga_horaria[i]
        j = i - 1
        while j >= 0 and clave_cuatrimestre < cuatrimestre[j]:
            cuatrimestre[j + 1] = cuatrimestre[j]
            codigos[j + 1] = codigos[j]
            nombres[j + 1] = nombres[j]
            carga_horaria[j + 1] = carga_horaria[j]
            j = j - 1
        cuatrimestre[j + 1] = clave_cuatrimestre
        codigos[j + 1] = clave_codigo
        nombres[j + 1] = clave_nombre
        carga_horaria[j + 1] = clave_carga
    print("Materias ordenadas por cuatrimestre.")

# ============================================================
# FUNCIONES DE USO GENERAL: VALIDACION DE ENTRADAS
# ============================================================

# FUNCION AUXILIAR: pide un numero entero al usuario, repite si no es un numero
def pedir_entero(mensaje):
    while True:
        entrada = input(mensaje)
        es_numero = True
        if len(entrada) == 0:
            es_numero = False
        else:
            inicio = 0
            if entrada[0] == "-":
                inicio = 1
            if inicio == len(entrada):
                es_numero = False
            else:
                for c in entrada[inicio:]:
                    if c < "0" or c > "9":
                        es_numero = False
        if es_numero:
            return int(entrada)
        print("Entrada invalida. Por favor ingrese un numero entero.")

# FUNCION DE VALIDACION DE CORREO CON EXPRESIONES REGULARES
# Patron: texto@texto.dominio (sin espacios, con un solo @ y un punto en el dominio)
def validar_email(correo):
    patron = r"^[\w\.]+@[\w]+\.[a-z]{2,}$"
    if re.match(patron, correo):
        return True
    return False

# FUNCION AUXILIAR: pide un correo valido al usuario, repite si no cumple el formato
def pedir_email(mensaje):
    while True:
        correo = input(mensaje)
        if validar_email(correo):
            return correo
        print("Correo invalido. Formato esperado: usuario@dominio.com")

# FUNCION DE EXTRACCION DE DATOS CON EXPRESIONES REGULARES
# Extrae el dominio (lo que sigue despues del @) de un correo ya validado
def extraer_dominio(correo):
    resultado = re.search(r"@([A-Za-z0-9.-]+)", correo)
    if resultado:
        return resultado.group(1)
    return "desconocido"

# ============================================================
# FUNCIONES ESTUDIANTES
# ============================================================

def alta_estudiantes(codigo, nombre, edad, age, correo):
    nuevo_codigo = pedir_entero("Ingrese el codigo del estudiante nuevo: ")
    while nuevo_codigo in codigo:
        nuevo_codigo = pedir_entero("El codigo ya esta asignado a otro estudiante, porfavor ingrese otro número: ")
    codigo.append(nuevo_codigo)
    nuevo_nombre = input("Ingrese el nombre del estudiante nuevo: ")
    nombre.append(nuevo_nombre)
    nuevo_edad = pedir_entero("Ingrese la edad del estudiante nuevo: ")
    while nuevo_edad < 17 or nuevo_edad > 99:
        nuevo_edad = pedir_entero("Edad invalida, ingrese nuevamente la edad (17-99): ")
    edad.append(nuevo_edad)
    nuevo_age = pedir_entero("Ingrese el año de cursada del estudiante nuevo: ")
    while nuevo_age < 1 or nuevo_age > 9:
        nuevo_age = pedir_entero("Año de cursada invalido, ingrese nuevamente (1-9): ")
    age.append(nuevo_age)
    nuevo_correo = pedir_email("Ingrese el correo electronico del estudiante nuevo: ")
    correo.append(nuevo_correo)
    print("El estudiante", nuevo_nombre, nuevo_codigo, "a sido dado de alta correctamente")

def baja_estudiantes(codigos, nombres, edades, ages, correos, calificaciones):
    codigo = pedir_entero("Ingrese el código del estudiante a eliminar: ")
    if codigo in codigos:
        pos = buscar_en_listas_secuencial(codigos, codigo)
        pos_calificacion = buscar_en_listas_secuencial(calificaciones, codigo)
        if pos_calificacion != -1:
            print("No se puede eliminar porque tiene calificaciones asociadas")
        else:
            codigos.pop(pos)
            nombres.pop(pos)
            edades.pop(pos)
            ages.pop(pos)
            correos.pop(pos)
            print("Estudiante eliminado correctamente.")
    else:
        print("Código de estudiante no encontrado.")

# Usa busqueda binaria: primero ordena por codigo, busca, luego el orden queda por codigo
def modificacion_estudiantes(codigos, nombres, edades, ages, correos):
    codigo = pedir_entero("Ingrese el código del estudiante que desea modificar: ")
    if codigo in codigos:
        ordenar_estudiantes_por_codigo(codigos, nombres, edades, ages, correos)
        pos = buscar_en_listas_binaria(codigos, codigo)
        nombres[pos] = input("Ingrese nuevo nombre: ")
        edad = pedir_entero("Ingrese nueva edad: ")
        while edad < 17 or edad > 99:
            edad = pedir_entero("Edad invalida. Ingrese nueva edad: ")
        edades[pos] = edad
        anio = pedir_entero("Ingrese nuevo año de cursada: ")
        while anio < 1 or anio > 9:
            anio = pedir_entero("Año invalido. Ingrese nuevo año de cursada: ")
        ages[pos] = anio
        correos[pos] = pedir_email("Ingrese nuevo correo electronico: ")
        print("Estudiante modificado correctamente.")
    else:
        print("El estudiante no existe.")

def listado_estudiantes(codigos, nombres, edades, ages, correos):
    for i in range(len(codigos)):
        print("Codigo:", codigos[i], "-Nombre:", nombres[i], "-Edad:", edades[i], "- Año:", ages[i],
              "- Correo:", correos[i], "- Dominio:", extraer_dominio(correos[i]))

# ============================================================
# FUNCIONES MATERIAS
# ============================================================

def alta_materias(codigo, nombre, cuatrimestre, carga_horaria):
    nuevo_codigo = pedir_entero("Ingrese el codigo de la materia nueva: ")
    while nuevo_codigo in codigo:
        nuevo_codigo = pedir_entero("El codigo ya esta asignado a otra materia, porfavor ingrese otro número: ")
    codigo.append(nuevo_codigo)
    nuevo_nombre = input("Ingrese el nombre de la materia nueva: ")
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
    print("La materia", nuevo_nombre, nuevo_codigo, "a sido dada de alta correctamente")

# Si la materia tiene calificaciones asociadas, ofrece eliminarlas en cascada (con confirmacion)
def baja_materias(codigos, nombres, cuatrimestre, carga_horaria, codigos_calif, est_calif, mat_calif, notas, condiciones):
    codigo = pedir_entero("Ingrese el código de la materia a eliminar: ")
    if codigo not in codigos:
        print("Código de materia no encontrado.")
        return
    pos = buscar_en_listas_secuencial(codigos, codigo)
    if buscar_en_listas_secuencial(mat_calif, codigo) != -1:
        print("No se puede eliminar porque tiene calificaciones asociadas")
        vaciar_calificaciones(codigos_calif, est_calif, mat_calif, notas, condiciones)
        if buscar_en_listas_secuencial(mat_calif, codigo) != -1:
            return
    codigos.pop(pos)
    nombres.pop(pos)
    cuatrimestre.pop(pos)
    carga_horaria.pop(pos)
    print("Materia dada de baja correctamente.")

def modificacion_materias(codigos, nombres, cuatrimestre, carga_horaria):
    codigo = pedir_entero("Ingrese el código de la materia que desea modificar: ")
    if codigo in codigos:
        pos = buscar_en_listas_secuencial(codigos, codigo)
        nombres[pos] = input("Ingrese nuevo nombre de la materia: ")
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

def listado_materias(codigos, nombres, cuatrimestre, carga_horaria):
    for i in range(len(codigos)):
        print("Codigo:", codigos[i], "-Nombre:", nombres[i], "-Cuatrimestre:", cuatrimestre[i],
              "-Carga horaria:", carga_horaria[i])

# ============================================================
# FUNCIONES CALIFICACIONES
# ============================================================

def alta_calificaciones(codigos_calif, est_calif, mat_calif, notas, condiciones, codigos_estudiantes, codigos_materias):
    nuevo_codigo = pedir_entero("Ingrese el código de la calificación nueva: ")
    while nuevo_codigo in codigos_calif:
        nuevo_codigo = pedir_entero("El código ya existe, ingrese otro: ")
    codigos_calif.append(nuevo_codigo)
    codigo_est = pedir_entero("Ingrese el código del estudiante: ")
    while codigo_est not in codigos_estudiantes:
        codigo_est = pedir_entero("Ese estudiante no existe. Ingréselo de nuevo: ")
    est_calif.append(codigo_est)
    codigo_mat = pedir_entero("Ingrese el código de la materia: ")
    while codigo_mat not in codigos_materias:
        codigo_mat = pedir_entero("Esa materia no existe. Ingrésela de nuevo: ")
    mat_calif.append(codigo_mat)
    nota = pedir_entero("Ingrese la nota (1-10): ")
    while nota < 1 or nota > 10:
        nota = pedir_entero("Nota inválida, ingrese un valor entre 1 y 10: ")
    notas.append(nota)
    condicion = pedir_entero("Ingrese la condición (1=regular, 2=promocionado, 3=desaprobado): ")
    while condicion < 1 or condicion > 3:
        condicion = pedir_entero("Condición inválida, ingrese 1, 2 o 3: ")
    condiciones.append(condicion)
    print("La calificación", nuevo_codigo, "fue dada de alta correctamente")

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

def vaciar_calificaciones(codigos_calif, est_calif, mat_calif, notas, condiciones):
    confirmacion = input("Para eliminar la materia se deben eliminar las calificaciones, desea eliminar todas las calificaciones? (si/no): ")
    if confirmacion == "si":
        codigos_calif.clear()
        est_calif.clear()
        mat_calif.clear()
        notas.clear()
        condiciones.clear()
        print("Todas las calificaciones fueron eliminadas.")
    else:
        print("No se eliminaron las calificaciones.")

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
        nota = pedir_entero("Ingrese la nueva nota (1-10): ")
        while nota < 1 or nota > 10:
            nota = pedir_entero("Nota inválida, ingrese un valor entre 1 y 10: ")
        notas[pos] = nota
        condicion = pedir_entero("Ingrese la nueva condición (1=regular, 2=promocionado, 3=desaprobado): ")
        while condicion < 1 or condicion > 3:
            condicion = pedir_entero("Condición inválida, ingrese 1, 2 o 3: ")
        condiciones[pos] = condicion
        print("Calificación modificada correctamente.")
    else:
        print("Código de calificación no encontrado.")

def listado_calificaciones(codigos_calif, est_calif, mat_calif, notas, condiciones):
    for i in range(len(codigos_calif)):
        print("Codigo:", codigos_calif[i], "- Estudiante:", est_calif[i],
              "- Materia:", mat_calif[i], "- Nota:", notas[i], "- Condición:", condiciones[i])

# ============================================================
# LOGIN Y MENUS
# ============================================================

def login():
    usuarios_validos = "admin"
    contrasenas_validas = "admin"
    intentos = 3
    ingreso_correcto = False
    while ingreso_correcto == False and intentos > 0:
        usuario = input("Ingrese su usuario: ")
        contrasena = input("Ingrese su contraseña: ")
        if usuario == usuarios_validos and contrasena == contrasenas_validas:
            print("---Inicio de sesión valido---")
            ingreso_correcto = True
        else:
            intentos = intentos - 1
            print("-Inicio de sesión invalido, te quedan", intentos, "intentos-")
    return ingreso_correcto

def submenu1():
    salida_submenu1 = False
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
            baja_estudiantes(codigos_estudiantes, nombres_estudiantes, edades_estudiantes, ages_cursada, correos_estudiantes, codigos_estudiantes_calif)
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

def submenu2():
    salida_submenu2 = False
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

def submenu3():
    salida_submenu3 = False
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
            informe_matriz_notas()
        elif opcion == 8:
            estadisticas_con_lambda(notas, condiciones, nombres_estudiantes)
        elif opcion == 0:
            salida_submenu3 = True
        else:
            print("Opcion no valida, vuelva a elegir")

def menu_principal():
    salida_menu = False
    while salida_menu == False:
        print("---Bienvenido al menú principal---")
        print("1. Estudiantes")
        print("2. Materias")
        print("3. Calificaciones")
        print("0. Cerrar sesión")
        opcion = pedir_entero("Seleccione una opción: ")
        if opcion == 1:
            submenu1()
        elif opcion == 2:
            submenu2()
        elif opcion == 3:
            submenu3()
        elif opcion == 0:
            print("Cerrando sesión")
            salida_menu = True
        else:
            print("Opcion no valida, porfavor elija nuevamente")

# ============================================================
# MATRICES Y ESTADISTICAS
# ============================================================

# map + lambda + zip: arma la matriz [codigo_calif, codigo_materia, condicion] sin loop manual
def listas_a_matriz(lista1, lista2, lista3):
    matriz = list(map(lambda fila: [fila[0], fila[1], fila[2]], zip(lista1, lista2, lista3)))
    return matriz

def conservar_unicos(matriz):
    unicos = []
    for fila in matriz:
        if buscar_en_listas_secuencial(unicos, fila[1]) == -1:
            unicos.append(fila[1])
    return unicos

# Recorre las calificaciones UNA SOLA VEZ (no una pasada completa por cada materia) y
# acumula aprobados/desaprobados de todas las materias en simultaneo.
def armar_matriz_estadisticas(materias_unicas):
    aprobados = [0] * len(materias_unicas)
    desaprobados = [0] * len(materias_unicas)
    for i in range(len(codigos_materias_calif)):
        pos = buscar_en_listas_secuencial(materias_unicas, codigos_materias_calif[i])
        if pos != -1:
            if condiciones[i] != 3:
                aprobados[pos] += 1
            else:
                desaprobados[pos] += 1
    matriz = list(map(lambda idx: [materias_unicas[idx], aprobados[idx], desaprobados[idx]], range(len(materias_unicas))))
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
        porcentaje = (aprob * 100 / total) if total > 0 else 0
        print(f"{nombre:20} | {aprob:^5} | {desap:^5} | {porcentaje:6.2f}%")

# FUNCION QUE IMPRIME LA MATRIZ DE NOTAS CON ENCABEZADOS
def imprimir_matriz_notas(matriz, nombres_est, nombres_mat):
    print("Materias:", nombres_mat)
    for i in range(len(matriz)):
        print("Estudiante:", nombres_est[i])
        for j in range(len(matriz[i])):
            print("   ", nombres_mat[j], "-", matriz[i][j])

# Arma una matriz (lista bidimensional) de notas: filas=estudiantes, columnas=materias
def armar_matriz_notas(codigos_est, codigos_mat, est_calif, mat_calif, notas):
    matriz = []
    for i in range(len(codigos_est)):
        fila = []
        for j in range(len(codigos_mat)):
            nota_encontrada = "-"
            for k in range(len(est_calif)):
                if est_calif[k] == codigos_est[i] and mat_calif[k] == codigos_mat[j]:
                    nota_encontrada = notas[k]
            fila.append(nota_encontrada)
        matriz.append(fila)
    return matriz

def informe_matriz_notas():
    matriz = armar_matriz_notas(codigos_estudiantes, codigos_materias, codigos_estudiantes_calif, codigos_materias_calif, notas)
    print("\n--- MATRIZ DE NOTAS (Estudiantes x Materias) ---")
    imprimir_matriz_notas(matriz, nombres_estudiantes, nombres_materias)

# Demostracion explicita de map / filter / reduce con funciones lambda sobre las notas
def estadisticas_con_lambda(notas, condiciones, nombres_estudiantes):
    if len(notas) == 0:
        print("No hay calificaciones cargadas.")
        return
    notas_sobre_100 = list(map(lambda n: n * 10, notas))
    indices_aprobados = list(filter(lambda i: condiciones[i] != 3, range(len(condiciones))))
    notas_aprobados = list(map(lambda i: notas[i], indices_aprobados))
    suma_total = reduce(lambda acumulado, n: acumulado + n, notas, 0)
    promedio_general = suma_total / len(notas)
    print("\n--- ESTADISTICAS CON FUNCIONES LAMBDA ---")
    print("Notas originales:", notas)
    print("Notas escaladas sobre 100 (map):", notas_sobre_100)
    print("Notas de aprobados (filter):", notas_aprobados)
    print("Promedio general de notas (reduce):", promedio_general)

# ============================================================
# INICIO DE PROGRAMA
# ============================================================
    
print("---Sistema de calificaciones---")
print("    --Inicio de sesión--       ")
inicio_de_sesion = login()
    if inicio_de_sesion == True:
        menu_principal()
    else:
        print("Por seguridad se bloqueo el acceso")

