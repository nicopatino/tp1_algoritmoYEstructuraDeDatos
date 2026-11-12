"""Operaciones y submenú para la gestión de calificaciones."""

import csv

from base_comun import (
	CONDICIONES,
	NOTA_APROBACION,
	RANGO_CODIGO_ESTUDIANTE,
	RANGO_CODIGO_MATERIA,
	RANGO_NOTA,
	convertir_entero,
	condicion_a_texto,
	es_aprobada,
	pedir_dato,
	pedir_entero_en_rango,
	pedir_opcion,
	validar_rango,
)


def validar_codigo_calificacion(codigo):
	"""Convertir y validar un código de calificación entero positivo."""
	codigo = convertir_entero(codigo, "código de calificación")
	if codigo < 1:
		raise ValueError("El código de calificación debe ser mayor que cero.")
	return codigo


def validar_calificacion(nota, condicion):
	"""Validar nota 1-10 y coherencia entre nota aprobada y condición."""
	nota = validar_rango(convertir_entero(nota, "nota"), RANGO_NOTA, "nota")
	condicion = validar_rango(
		convertir_entero(condicion, "condición"),
		(1, len(CONDICIONES)),
		"condición",
	)
	if (nota >= NOTA_APROBACION) != (condicion in (1, 2)):
		raise ValueError(
			"La condición debe ser regular/promocionado para notas desde 6, "
			"y desaprobado para notas menores a 6."
		)
	return nota, condicion


def convertir_acta(codigo, registro):
	"""Convertir un acta de formato tuple/list o dict histórico a una tupla."""
	codigo = validar_codigo_calificacion(codigo)
	if isinstance(registro, dict):
		try:
			acta = (
				codigo,
				convertir_entero(registro["estudiante"], "código de estudiante"),
				convertir_entero(registro["materia"], "código de materia"),
				convertir_entero(registro["nota"], "nota"),
				convertir_entero(registro["condicion"], "condición"),
			)
		except KeyError as error:
			raise ValueError("El registro de calificación no tiene todos sus campos.") from error
	else:
		if not isinstance(registro, (tuple, list)) or len(registro) != 5:
			raise ValueError("Cada acta debe contener cinco campos.")
		acta = tuple(convertir_entero(valor, "campo del acta") for valor in registro)
		if acta[0] != codigo:
			raise ValueError("El código del acta no coincide con la clave del diccionario.")
	validar_codigo_calificacion(acta[0])
	validar_rango(acta[1], RANGO_CODIGO_ESTUDIANTE, "código de estudiante")
	validar_rango(acta[2], RANGO_CODIGO_MATERIA, "código de materia")
	validar_rango(acta[3], RANGO_NOTA, "nota")
	validar_rango(acta[4], (1, len(CONDICIONES)), "condición")
	return acta


def normalizar_calificaciones(calificaciones):
	"""Reemplazar registros históricos dict/list por tuplas en el diccionario recibido."""
	actas = []
	for codigo, registro in calificaciones.items():
		acta = convertir_acta(codigo, registro)
		actas.append(acta)
	pares = set()
	for acta in actas:
		par = (acta[1], acta[2])
		if par in pares:
			raise ValueError("Hay calificaciones duplicadas para el mismo estudiante y materia.")
		pares.add(par)
	for acta in actas:
		calificaciones[acta[0]] = acta
	return calificaciones


def obtener_actas(calificaciones):
	"""Devolver las calificaciones como lista de tuplas, sin mutar el diccionario."""
	return [convertir_acta(codigo, registro) for codigo, registro in calificaciones.items()]


def buscar_calificacion(calificaciones, codigo):
	"""Buscar un acta por código y devolverla como tupla; lanzar KeyError si falta."""
	codigo = validar_codigo_calificacion(codigo)
	registro = calificaciones.get(codigo)
	if registro is None:
		raise KeyError("No existe una calificación con código {}.".format(codigo))
	return convertir_acta(codigo, registro)


def validar_referencias(codigo_estudiante, codigo_materia, estudiantes, materias):
	"""Validar que existan el estudiante y la materia referenciados por el acta."""
	codigo_estudiante = convertir_entero(codigo_estudiante, "código de estudiante")
	codigo_materia = convertir_entero(codigo_materia, "código de materia")
	validar_rango(codigo_estudiante, RANGO_CODIGO_ESTUDIANTE, "código de estudiante")
	validar_rango(codigo_materia, RANGO_CODIGO_MATERIA, "código de materia")
	if estudiantes.get(codigo_estudiante) is None:
		raise KeyError("No existe el estudiante con código {}.".format(codigo_estudiante))
	if materias.get(codigo_materia) is None:
		raise KeyError("No existe la materia con código {}.".format(codigo_materia))
	return codigo_estudiante, codigo_materia


def crear_calificacion(calificaciones, codigo, codigo_estudiante, codigo_materia,
					   nota, condicion, estudiantes, materias):
	"""Validar y guardar un acta como tupla, evitando códigos y pares duplicados."""
	codigo = validar_codigo_calificacion(codigo)
	if codigo in calificaciones:
		raise ValueError("Ya existe una calificación con código {}.".format(codigo))
	codigo_estudiante, codigo_materia = validar_referencias(
		codigo_estudiante, codigo_materia, estudiantes, materias
	)
	nota, condicion = validar_calificacion(nota, condicion)
	for acta in obtener_actas(calificaciones):
		if acta[1] == codigo_estudiante and acta[2] == codigo_materia:
			raise ValueError("El estudiante ya tiene una calificación para esa materia.")
	calificaciones[codigo] = (codigo, codigo_estudiante, codigo_materia, nota, condicion)
	return calificaciones[codigo]


def eliminar_calificacion(calificaciones, codigo):
	"""Eliminar una calificación existente o lanzar KeyError si no existe."""
	codigo = validar_codigo_calificacion(codigo)
	if codigo not in calificaciones:
		raise KeyError("No existe una calificación con código {}.".format(codigo))
	del calificaciones[codigo]


def modificar_calificacion(calificaciones, codigo, codigo_estudiante, codigo_materia,
						   nota, condicion, estudiantes, materias):
	"""Modificar un acta existente y guardarla como una nueva tupla inmutable."""
	codigo = validar_codigo_calificacion(codigo)
	buscar_calificacion(calificaciones, codigo)
	codigo_estudiante, codigo_materia = validar_referencias(
		codigo_estudiante, codigo_materia, estudiantes, materias
	)
	nota, condicion = validar_calificacion(nota, condicion)
	for otra_acta in obtener_actas(calificaciones):
		if otra_acta[0] != codigo and otra_acta[1] == codigo_estudiante and otra_acta[2] == codigo_materia:
			raise ValueError("El estudiante ya tiene una calificación para esa materia.")
	calificaciones[codigo] = (codigo, codigo_estudiante, codigo_materia, nota, condicion)
	return calificaciones[codigo]


def ordenar_calificaciones_por_nota(calificaciones, descendente=False):
	"""Devolver las actas ordenadas por nota y luego por código."""
	return sorted(
		obtener_actas(calificaciones),
		key=lambda acta: (acta[3], acta[0]),
		reverse=descendente,
	)


def calcular_promedio(calificaciones, codigo_estudiante=None, codigo_materia=None):
	"""Calcular promedio general o filtrado; lanzar ZeroDivisionError si no hay notas."""
	actas = obtener_actas(calificaciones)
	if codigo_estudiante is not None:
		codigo_estudiante = convertir_entero(codigo_estudiante, "código de estudiante")
	if codigo_materia is not None:
		codigo_materia = convertir_entero(codigo_materia, "código de materia")
	notas = [
		acta[3] for acta in actas
		if (codigo_estudiante is None or acta[1] == codigo_estudiante)
		and (codigo_materia is None or acta[2] == codigo_materia)
	]
	if not notas:
		raise ZeroDivisionError("No hay calificaciones para calcular el promedio.")
	return sum(notas) / len(notas)


def sumar_notas_recursivo(notas, indice=0):
	"""Sumar recursivamente una secuencia de notas."""
	if indice >= len(notas):
		return 0
	return notas[indice] + sumar_notas_recursivo(notas, indice + 1)


def calcular_promedio_recursivo(calificaciones):
	"""Calcular recursivamente el promedio de todas las actas."""
	notas = [acta[3] for acta in obtener_actas(calificaciones)]
	if not notas:
		raise ZeroDivisionError("No hay calificaciones para calcular el promedio.")
	return sumar_notas_recursivo(notas) / len(notas)


def listar_materias_sin_calificados(materias, calificaciones):
	"""Devolver códigos de materias sin estudiantes calificados mediante diferencia de sets."""
	codigos_calificados = {acta[2] for acta in obtener_actas(calificaciones)}
	return sorted(set(materias.keys()) - codigos_calificados)


def listar_calificaciones(calificaciones, estudiantes=None, materias=None):
	"""Mostrar actas, resolviendo nombres si se reciben los diccionarios relacionados."""
	actas = obtener_actas(calificaciones)
	if not actas:
		print("No hay calificaciones cargadas.")
		return
	print("\nCódigo | Estudiante | Materia | Nota | Condición")
	for codigo, codigo_estudiante, codigo_materia, nota, condicion in actas:
		nombre_estudiante = (estudiantes or {}).get(codigo_estudiante, {}).get("nombre", str(codigo_estudiante))
		nombre_materia = (materias or {}).get(codigo_materia, {}).get("nombre", str(codigo_materia))
		print("{} | {} | {} | {} | {}".format(
			codigo, nombre_estudiante, nombre_materia, nota, condicion_a_texto(condicion)
		))


def mostrar_calificaciones_ordenadas(calificaciones, estudiantes, materias):
	"""Mostrar las actas ordenadas de menor a mayor nota."""
	actas = ordenar_calificaciones_por_nota(calificaciones)
	if not actas:
		print("No hay calificaciones cargadas.")
		return
	for codigo, codigo_estudiante, codigo_materia, nota, condicion in actas:
		nombre_estudiante = estudiantes.get(codigo_estudiante, {}).get("nombre", str(codigo_estudiante))
		nombre_materia = materias.get(codigo_materia, {}).get("nombre", str(codigo_materia))
		print("{} | {} | {} | {} | {}".format(
			codigo, nombre_estudiante, nombre_materia, nota, condicion_a_texto(condicion)
		))


def exportar_acta(calificaciones, estudiantes, materias, ruta, formato="txt"):
	"""Exportar actas a TXT tabulado o CSV utilizando únicamente la biblioteca estándar."""
	formato = formato.lower()
	if formato not in ("txt", "csv"):
		raise ValueError("El formato de exportación debe ser txt o csv.")
	filas = [("codigo_calificacion", "codigo_estudiante", "estudiante", "codigo_materia",
		  "materia", "nota", "condicion")]
	for codigo, codigo_estudiante, codigo_materia, nota, condicion in obtener_actas(calificaciones):
		filas.append((
			codigo,
			codigo_estudiante,
			estudiantes.get(codigo_estudiante, {}).get("nombre", str(codigo_estudiante)),
			codigo_materia,
			materias.get(codigo_materia, {}).get("nombre", str(codigo_materia)),
			nota,
			condicion_a_texto(condicion),
		))
	with open(ruta, "w", encoding="utf-8", newline="") as archivo:
		if formato == "csv":
			escritor = csv.writer(archivo)
			escritor.writerows(filas)
		else:
			for fila in filas:
				archivo.write("\t".join(str(valor) for valor in fila) + "\n")


def pedir_codigo_calificacion():
	"""Pedir un código de calificación entero positivo."""
	return pedir_dato("Código de calificación: ", validar_codigo_calificacion)


def pedir_nota_condicion():
	"""Solicitar nota y condición hasta que sean válidas y coherentes."""
	while True:
		nota = pedir_entero_en_rango("Nota (1-10): ", RANGO_NOTA, "nota")
		condicion = pedir_entero_en_rango(
			"Condición (1=regular, 2=promocionado, 3=desaprobado): ",
			(1, len(CONDICIONES)),
			"condición",
		)
		try:
			return validar_calificacion(nota, condicion)
		except ValueError as error:
			print("Error:", error)


def dar_alta_calificacion(estudiantes, materias, calificaciones):
	"""Solicitar datos válidos y dar de alta una calificación."""
	codigo = pedir_codigo_calificacion()
	codigo_estudiante = pedir_entero_en_rango(
		"Código de estudiante: ", RANGO_CODIGO_ESTUDIANTE, "código de estudiante"
	)
	codigo_materia = pedir_entero_en_rango(
		"Código de materia: ", RANGO_CODIGO_MATERIA, "código de materia"
	)
	nota, condicion = pedir_nota_condicion()
	try:
		crear_calificacion(
			calificaciones, codigo, codigo_estudiante, codigo_materia,
			nota, condicion, estudiantes, materias,
		)
		print("Calificación dada de alta correctamente.")
	except (ValueError, KeyError) as error:
		print("Error:", error)


def dar_baja_calificacion(calificaciones):
	"""Pedir el código y dar de baja el acta correspondiente."""
	codigo = pedir_codigo_calificacion()
	try:
		eliminar_calificacion(calificaciones, codigo)
		print("Calificación eliminada correctamente.")
	except (ValueError, KeyError) as error:
		print("Error:", error)


def modificar_datos_calificacion(estudiantes, materias, calificaciones):
	"""Pedir nuevos datos y modificar un acta existente."""
	codigo = pedir_codigo_calificacion()
	try:
		buscar_calificacion(calificaciones, codigo)
	except (ValueError, KeyError) as error:
		print("Error:", error)
		return
	codigo_estudiante = pedir_entero_en_rango(
		"Nuevo código de estudiante: ", RANGO_CODIGO_ESTUDIANTE, "código de estudiante"
	)
	codigo_materia = pedir_entero_en_rango(
		"Nuevo código de materia: ", RANGO_CODIGO_MATERIA, "código de materia"
	)
	nota, condicion = pedir_nota_condicion()
	try:
		modificar_calificacion(
			calificaciones, codigo, codigo_estudiante, codigo_materia,
			nota, condicion, estudiantes, materias,
		)
		print("Calificación modificada correctamente.")
	except (ValueError, KeyError) as error:
		print("Error:", error)


def mostrar_busqueda_calificacion(calificaciones):
	"""Pedir un código y mostrar el acta encontrada."""
	codigo = pedir_codigo_calificacion()
	try:
		print(buscar_calificacion(calificaciones, codigo))
	except (ValueError, KeyError) as error:
		print("Error:", error)


def mostrar_promedio(calificaciones):
	"""Mostrar el promedio general e informar si no existen actas."""
	try:
		print("Promedio de notas:", round(calcular_promedio(calificaciones), 2))
	except ZeroDivisionError as error:
		print("Error:", error)


def exportar_acta_interactiva(estudiantes, materias, calificaciones):
	"""Solicitar formato y ruta y exportar las actas."""
	formato = input("Formato (txt/csv): ").strip().lower()
	if formato not in ("txt", "csv"):
		print("Error: el formato debe ser txt o csv.")
		return
	ruta = input("Archivo de salida (Enter para acta_notas." + formato + "): ").strip()
	if not ruta:
		ruta = "acta_notas." + formato
	try:
		exportar_acta(calificaciones, estudiantes, materias, ruta, formato)
		print("Acta exportada en", ruta)
	except (OSError, ValueError) as error:
		print("Error:", error)


def mostrar_materias_sin_calificados(materias, calificaciones):
	"""Mostrar materias sin actas usando la diferencia entre conjuntos."""
	codigos = listar_materias_sin_calificados(materias, calificaciones)
	if not codigos:
		print("Todas las materias tienen estudiantes calificados.")
		return
	print("Materias sin estudiantes calificados:")
	for codigo in codigos:
		print(codigo, "-", materias.get(codigo, {}).get("nombre", "Desconocida"))


def submenu_calificaciones(estudiantes, materias, calificaciones):
	"""Ejecutar el submenú de calificaciones con los diccionarios recibidos."""
	try:
		normalizar_calificaciones(calificaciones)
	except (ValueError, KeyError) as error:
		print("No se pudieron cargar las calificaciones:", error)
		return
	opciones = (1, 2, 3, 4, 5, 6, 7, 8, 9, 0)
	while True:
		print("\n--- Submenú de calificaciones ---")
		print("1. Alta")
		print("2. Baja")
		print("3. Modificación")
		print("4. Búsqueda por código")
		print("5. Listado")
		print("6. Ordenar por nota")
		print("7. Promedio de notas")
		print("8. Materias sin estudiantes calificados")
		print("9. Exportar acta TXT/CSV")
		print("0. Volver")
		opcion = pedir_opcion(opciones, "Elija una opción: ")
		if opcion == 1:
			dar_alta_calificacion(estudiantes, materias, calificaciones)
		elif opcion == 2:
			dar_baja_calificacion(calificaciones)
		elif opcion == 3:
			modificar_datos_calificacion(estudiantes, materias, calificaciones)
		elif opcion == 4:
			mostrar_busqueda_calificacion(calificaciones)
		elif opcion == 5:
			listar_calificaciones(calificaciones, estudiantes, materias)
		elif opcion == 6:
			mostrar_calificaciones_ordenadas(calificaciones, estudiantes, materias)
		elif opcion == 7:
			mostrar_promedio(calificaciones)
		elif opcion == 8:
			mostrar_materias_sin_calificados(materias, calificaciones)
		elif opcion == 9:
			exportar_acta_interactiva(estudiantes, materias, calificaciones)
		else:
			return
