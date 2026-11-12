# Importa re para comprobar el formato de los correos con una expresion regular.
import re


# Expresion regular sencilla para comprobar el formato del correo.
# Exige texto antes de @ y un dominio con al menos un punto.
PATRON_CORREO = r"^[A-Za-z0-9_.+-]+@[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)+$"


def correo_en_uso(estudiantes, correo):
    # Recorre los datos de cada estudiante guardado.
    # Se recorren los estudiantes para evitar correos repetidos.
    for datos in estudiantes.values():
        # Compara sin distinguir mayusculas de minusculas.
        if datos["correo"].lower() == correo.lower():
            # Informa que el correo ya pertenece a un estudiante.
            return True
    # Si termino el recorrido, el correo no esta registrado.
    return False


def alta_estudiante(estudiantes, codigo, nombre, edad, anio, correo):
    # Se validan los datos antes de guardar el nuevo estudiante.
    # Evita sobrescribir un estudiante con el mismo codigo.
    if codigo in estudiantes:
        raise ValueError("El codigo ya existe.")
    # Verifica los rangos permitidos para codigo, edad y año.
    if not 100 <= codigo <= 999 or not 17 <= edad <= 99 or not 1 <= anio <= 9:
        raise ValueError("El codigo, la edad o el año no son validos.")
    # El nombre debe incluir por lo menos nombre y apellido.
    if len(nombre.split()) < 2:
        raise ValueError("Ingrese nombre y apellido.")
    # Comprueba que el correo tenga el formato esperado.
    if not re.match(PATRON_CORREO, correo):
        raise ValueError("El correo no es valido.")
    # No permite usar el correo de otro estudiante.
    if correo_en_uso(estudiantes, correo):
        raise ValueError("El correo ya esta en uso.")

    # Guarda los datos del estudiante usando su codigo como clave.
    estudiantes[codigo] = {
        # Guarda el nombre completo.
        "nombre": nombre,
        # Guarda la edad.
        "edad": edad,
        # Guarda el año de cursada.
        "anio": anio,
        # Guarda el correo electronico.
        "correo": correo,
    }
    # Se devuelve el codigo y el nombre del estudiante agregado.
    return codigo, nombre


def baja_estudiante(estudiantes, calificaciones, codigo, borrar_calificaciones):
    # Comprueba que el estudiante exista antes de eliminarlo.
    if codigo not in estudiantes:
        raise KeyError("El estudiante no existe.")

    # Se juntan las calificaciones para poder borrarlas sin modificar el diccionario al recorrerlo.
    codigos_borrar = []
    # Recorre todas las calificaciones registradas.
    for codigo_calif, datos in calificaciones.items():
        # Guarda el codigo de cada calificacion del estudiante indicado.
        if datos["cod_est"] == codigo:
            codigos_borrar.append(codigo_calif)

    # Si hay calificaciones asociadas, solo se permite la baja si se pidio borrarlas.
    if codigos_borrar and not borrar_calificaciones:
        raise ValueError("El estudiante tiene calificaciones asociadas.")

    # Inicializa el contador de calificaciones que se eliminaran.
    cantidad_borrada = 0
    # Elimina las calificaciones asociadas previamente encontradas.
    for codigo_calif in codigos_borrar:
        del calificaciones[codigo_calif]
        # Suma una al contador por cada calificacion eliminada.
        cantidad_borrada += 1

    # Conserva el nombre para devolverlo despues de eliminar al estudiante.
    nombre = estudiantes[codigo]["nombre"]
    # Elimina al estudiante del diccionario.
    del estudiantes[codigo]
    # Se informa el nombre y la cantidad de calificaciones que se eliminaron.
    return nombre, cantidad_borrada


def modificar_estudiante(estudiantes, codigo, nuevos_datos):
    # Comprueba que exista el estudiante que se quiere modificar.
    if codigo not in estudiantes:
        raise KeyError("El estudiante no existe.")

    # Solo se cambian los campos incluidos en nuevos_datos.
    # Recorre los pares campo y valor recibidos para la modificacion.
    for campo, valor in nuevos_datos.items():
        # Solo admite estos cuatro campos del estudiante.
        if campo not in ("nombre", "edad", "anio", "correo"):
            raise ValueError("Campo no valido.")
        # El nombre debe tener al menos dos palabras.
        if campo == "nombre" and len(valor.split()) < 2:
            raise ValueError("Ingrese nombre y apellido.")
        # Comprueba que la edad este dentro del rango aceptado.
        if campo == "edad" and not 17 <= valor <= 99:
            raise ValueError("La edad debe estar entre 17 y 99.")
        # Comprueba que el año de cursada sea valido.
        if campo == "anio" and not 1 <= valor <= 9:
            raise ValueError("El año debe estar entre 1 y 9.")
        # Si se modifica el correo, valida su formato y unicidad.
        if campo == "correo":
            # Rechaza correos con formato incorrecto.
            if not re.match(PATRON_CORREO, valor):
                raise ValueError("El correo no es valido.")
            # Busca el mismo correo entre los otros estudiantes.
            for otro_codigo, datos in estudiantes.items():
                # Excluye al estudiante actual de la comprobacion.
                if otro_codigo != codigo and datos["correo"].lower() == valor.lower():
                    raise ValueError("El correo ya esta en uso.")
        # Guarda el nuevo valor en el campo correspondiente.
        estudiantes[codigo][campo] = valor

    # Devuelve los datos actualizados del estudiante.
    return estudiantes[codigo]


def listar_estudiantes_ordenados(estudiantes, campo):
    # Se arma una lista nueva para no cambiar el orden del diccionario original.
    lista = []
    # Copia edad, codigo y nombre de cada estudiante en una tupla.
    for codigo, datos in estudiantes.items():
        lista.append((datos["edad"], codigo, datos["nombre"]))

    # Verifica que el criterio de orden sea uno de los permitidos.
    if campo not in ("edad", "codigo", "nombre"):
        raise ValueError("Ordene por edad, codigo o nombre.")

    # Ordenamiento burbuja, como en los algoritmos vistos en clase.
    # En cada pasada compara elementos contiguos y los intercambia si estan desordenados.
    for i in range(len(lista)):
        # La parte final ya queda ordenada en las pasadas anteriores.
        for j in range(len(lista) - 1 - i):
            # Compara las edades cuando ese es el criterio elegido.
            if campo == "edad":
                intercambiar = lista[j][0] > lista[j + 1][0]
            # Compara los codigos cuando ese es el criterio elegido.
            elif campo == "codigo":
                intercambiar = lista[j][1] > lista[j + 1][1]
            # En otro caso compara los nombres sin distinguir mayusculas.
            else:
                intercambiar = lista[j][2].lower() > lista[j + 1][2].lower()
            # Intercambia las tuplas cuando la comparacion indica desorden.
            if intercambiar:
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
    # Devuelve la lista ordenada sin alterar el diccionario original.
    return lista


def buscar_estudiantes_por_nombre(estudiantes, texto):
    # La busqueda ignora mayusculas y minusculas.
    encontrados = []
    # Recorre los estudiantes registrados.
    for codigo, datos in estudiantes.items():
        # Agrega los que contienen el texto buscado en su nombre.
        if texto.lower() in datos["nombre"].lower():
            encontrados.append((codigo, datos["nombre"]))
    # Devuelve los codigos y nombres que coinciden.
    return encontrados


def contar_estudiantes_por_anio(estudiantes):
    # Se acumula cuántos estudiantes hay en cada año de cursada.
    cantidades = {}
    # Recorre los datos de todos los estudiantes.
    for datos in estudiantes.values():
        # Obtiene el año de cursada del estudiante actual.
        anio = datos["anio"]
        # Crea el contador del año la primera vez que aparece.
        if anio not in cantidades:
            cantidades[anio] = 0
        # Suma el estudiante al contador de ese año.
        cantidades[anio] += 1
    # Devuelve el diccionario con las cantidades por año.
    return cantidades


def submenu_estudiantes(estudiantes, calificaciones):
    # El menu se repite hasta que se elige volver.
    while True:
        # Muestra el titulo y las operaciones disponibles.
        print("\n--- ESTUDIANTES ---")
        # Opcion para registrar un estudiante.
        print("1. Alta")
        # Opcion para eliminar un estudiante.
        print("2. Baja")
        # Opcion para cambiar datos de un estudiante.
        print("3. Modificar")
        # Opcion para listar estudiantes ordenados.
        print("4. Listar ordenados")
        # Opcion para buscar estudiantes por nombre.
        print("5. Buscar por nombre")
        # Opcion para contar estudiantes en cada año.
        print("6. Contar por año")
        # Opcion para comprobar si un correo ya se usa.
        print("7. Buscar correo")
        # Opcion para volver al menu anterior.
        print("0. Volver")
        # Lee la opcion elegida por el usuario.
        opcion = input("Opcion: ")

        # Captura errores de datos para que el menu no se cierre.
        try:
            # Solicita los datos y registra el nuevo estudiante.
            if opcion == "1":
                codigo = int(input("Codigo: "))
                nombre = input("Nombre y apellido: ")
                edad = int(input("Edad: "))
                anio = int(input("Año de cursada: "))
                correo = input("Correo: ")
                print(alta_estudiante(estudiantes, codigo, nombre, edad, anio, correo))
            # Pide el codigo y confirma si deben quitarse tambien sus calificaciones.
            elif opcion == "2":
                codigo = int(input("Codigo: "))
                borrar = input("Borrar tambien sus calificaciones? (si/no): ").lower() == "si"
                print(baja_estudiante(estudiantes, calificaciones, codigo, borrar))
            # Pide un codigo y solo los nuevos campos que se quieran cambiar.
            elif opcion == "3":
                codigo = int(input("Codigo: "))
                # Este diccionario contendra unicamente los campos ingresados.
                datos = {}
                # Recorre los campos que pueden modificarse.
                for campo in ("nombre", "edad", "anio", "correo"):
                    valor = input("Nuevo " + campo + " (vacio para dejar igual): ")
                    # Omite los campos que se dejaron vacios.
                    if valor:
                        # Convierte los campos numericos de texto a enteros.
                        if campo in ("edad", "anio"):
                            valor = int(valor)
                        # Agrega el nuevo valor a la modificacion.
                        datos[campo] = valor
                print(modificar_estudiante(estudiantes, codigo, datos))
            # Pide el criterio y muestra los estudiantes ordenados.
            elif opcion == "4":
                campo = input("Ordenar por edad, codigo o nombre: ").lower()
                for estudiante in listar_estudiantes_ordenados(estudiantes, campo):
                    print(estudiante)
            # Busca el texto ingresado dentro de los nombres.
            elif opcion == "5":
                texto = input("Nombre a buscar: ")
                print(buscar_estudiantes_por_nombre(estudiantes, texto))
            # Muestra la cantidad de estudiantes por año.
            elif opcion == "6":
                print(contar_estudiantes_por_anio(estudiantes))
            # Comprueba si el correo ingresado ya esta registrado.
            elif opcion == "7":
                correo = input("Correo: ")
                print(correo_en_uso(estudiantes, correo))
            # Termina el submenu y vuelve a la pantalla anterior.
            elif opcion == "0":
                return
            # Avisa cuando se ingresa una opcion que no existe.
            else:
                print("Opcion no valida.")
        # Informa errores de validacion o codigos de estudiante inexistentes.
        except (ValueError, KeyError) as error:
            print("Error:", error)
