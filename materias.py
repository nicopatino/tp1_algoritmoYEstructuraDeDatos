"""Operaciones y submenú para la gestión de materias."""

from base_comun import (
	RANGO_CARGA_HORARIA,
	RANGO_CODIGO_MATERIA,
	RANGO_CUATRIMESTRE,
	convertir_entero,
	pedir_dato,
	pedir_entero_en_rango,
	pedir_opcion,
	validar_rango,
	validar_texto_obligatorio,
)


def validar_codigo_materia(codigo):
	"""Convertir y validar un código de materia entre 200 y 999."""
	codigo = convertir_entero(codigo, "código de materia")
	return validar_rango(codigo, RANGO_CODIGO_MATERIA, "código de materia")


def buscar_materia(materias, codigo):
	"""Devolver la materia indicada o lanzar KeyError si no existe."""
	codigo = validar_codigo_materia(codigo)
	materia = materias.get(codigo)
	if materia is None:
		raise KeyError(f"No existe una materia con código {codigo}.")
	return materia


def crear_materia(materias, codigo, nombre, cuatrimestre, carga_horaria):
	"""Validar y agregar una materia al diccionario recibido."""
	codigo = validar_codigo_materia(codigo)
	if codigo in materias:
		raise ValueError(f"Ya existe una materia con código {codigo}.")
	nombre = validar_texto_obligatorio(nombre, "nombre de materia")
	cuatrimestre = validar_rango(
		convertir_entero(cuatrimestre, "cuatrimestre"),
		RANGO_CUATRIMESTRE,
		"cuatrimestre",
	)
	carga_horaria = validar_rango(
		convertir_entero(carga_horaria, "carga horaria"),
		RANGO_CARGA_HORARIA,
		"carga horaria",
	)
	materias[codigo] = {
		"nombre": nombre,
		"cuatrimestre": cuatrimestre,
		"carga_horaria": carga_horaria,
	}
	return codigo


def eliminar_materia(materias, calificaciones, codigo):
	"""Eliminar una materia sin calificaciones asociadas, históricas o en tupla."""
	codigo = validar_codigo_materia(codigo)
	buscar_materia(materias, codigo)
	for calificacion in calificaciones.values():
		if isinstance(calificacion, dict):
			codigo_materia = calificacion.get("materia")
		elif isinstance(calificacion, (tuple, list)) and len(calificacion) == 5:
			codigo_materia = calificacion[2]
		else:
			raise ValueError("No se puede comprobar una calificación con formato desconocido.")
		if codigo_materia == codigo:
			raise ValueError(
				f"No se puede eliminar la materia {codigo}: tiene calificaciones asociadas."
			)
	del materias[codigo]


def actualizar_materia(materias, codigo, nombre, cuatrimestre, carga_horaria):
	"""Validar y modificar los datos de una materia existente."""
	materia = buscar_materia(materias, codigo)
	nombre = validar_texto_obligatorio(nombre, "nombre de materia")
	cuatrimestre = validar_rango(
		convertir_entero(cuatrimestre, "cuatrimestre"),
		RANGO_CUATRIMESTRE,
		"cuatrimestre",
	)
	carga_horaria = validar_rango(
		convertir_entero(carga_horaria, "carga horaria"),
		RANGO_CARGA_HORARIA,
		"carga horaria",
	)
	materia.update({
		"nombre": nombre,
		"cuatrimestre": cuatrimestre,
		"carga_horaria": carga_horaria,
	})


def listar_materias(materias):
	"""Mostrar las materias en el orden actual del diccionario."""
	if not materias:
		print("No hay materias cargadas.")
		return
	print("\nCódigo | Materia | Cuatrimestre | Carga horaria")
	for codigo, materia in materias.items():
		print("{} | {} | {} | {}".format(
			codigo,
			materia.get("nombre", "Sin nombre"),
			materia.get("cuatrimestre", "-"),
			materia.get("carga_horaria", "-"),
		))


def ordenar_materias_por_cuatrimestre(materias):
	"""Devolver las materias ordenadas por cuatrimestre y luego por código."""
	return sorted(
		materias.items(),
		key=lambda elemento: (elemento[1].get("cuatrimestre", 0), elemento[0]),
	)


def mostrar_materias_ordenadas(materias):
	"""Mostrar las materias ordenadas por cuatrimestre y código."""
	ordenadas = ordenar_materias_por_cuatrimestre(materias)
	if not ordenadas:
		print("No hay materias cargadas.")
		return
	print("\nMaterias ordenadas por cuatrimestre")
	for codigo, materia in ordenadas:
		print("{} | {} | Cuatrimestre {} | {} horas".format(
			codigo,
			materia.get("nombre", "Sin nombre"),
			materia.get("cuatrimestre", "-"),
			materia.get("carga_horaria", "-"),
		))


def mostrar_busqueda_materia(materias):
	"""Pedir un código y mostrar la materia encontrada."""
	codigo = pedir_entero_en_rango(
		"Ingrese el código de la materia: ", RANGO_CODIGO_MATERIA, "código de materia"
	)
	try:
		materia = buscar_materia(materias, codigo)
		print("{} | {} | Cuatrimestre {} | {} horas".format(
			codigo,
			materia.get("nombre", "Sin nombre"),
			materia.get("cuatrimestre", "-"),
			materia.get("carga_horaria", "-"),
		))
	except KeyError as error:
		print("Error:", error)


def dar_alta_materia(materias):
	"""Pedir los datos e incorporar una materia, informando errores de validación."""
	codigo = pedir_entero_en_rango(
		"Ingrese el código de la materia (200-999): ",
		RANGO_CODIGO_MATERIA,
		"código de materia",
	)
	nombre = pedir_dato(
		"Ingrese el nombre de la materia: ",
		lambda texto: validar_texto_obligatorio(texto, "nombre de materia"),
	)
	cuatrimestre = pedir_entero_en_rango(
		"Ingrese el cuatrimestre (1-2): ", RANGO_CUATRIMESTRE, "cuatrimestre"
	)
	carga_horaria = pedir_entero_en_rango(
		"Ingrese la carga horaria (1-20): ", RANGO_CARGA_HORARIA, "carga horaria"
	)
	try:
		crear_materia(materias, codigo, nombre, cuatrimestre, carga_horaria)
		print("Materia dada de alta correctamente.")
	except ValueError as error:
		print("Error:", error)


def dar_baja_materia(materias, calificaciones):
	"""Pedir el código y eliminar la materia si no tiene actas asociadas."""
	codigo = pedir_entero_en_rango(
		"Ingrese el código de la materia a eliminar: ",
		RANGO_CODIGO_MATERIA,
		"código de materia",
	)
	try:
		eliminar_materia(materias, calificaciones, codigo)
		print("Materia eliminada correctamente.")
	except (ValueError, KeyError) as error:
		print("Error:", error)


def modificar_datos_materia(materias):
	"""Pedir código y nuevos datos para modificar una materia."""
	codigo = pedir_entero_en_rango(
		"Ingrese el código de la materia a modificar: ",
		RANGO_CODIGO_MATERIA,
		"código de materia",
	)
	try:
		buscar_materia(materias, codigo)
	except KeyError as error:
		print("Error:", error)
		return
	nombre = pedir_dato(
		"Ingrese el nuevo nombre: ",
		lambda texto: validar_texto_obligatorio(texto, "nombre de materia"),
	)
	cuatrimestre = pedir_entero_en_rango(
		"Ingrese el nuevo cuatrimestre (1-2): ", RANGO_CUATRIMESTRE, "cuatrimestre"
	)
	carga_horaria = pedir_entero_en_rango(
		"Ingrese la nueva carga horaria (1-20): ", RANGO_CARGA_HORARIA, "carga horaria"
	)
	try:
		actualizar_materia(materias, codigo, nombre, cuatrimestre, carga_horaria)
		print("Materia modificada correctamente.")
	except (ValueError, KeyError) as error:
		print("Error:", error)


def submenu_materias(estudiantes, materias, calificaciones):
	"""Ejecutar el submenú de materias compatible con el menú principal."""
	opciones = (1, 2, 3, 4, 5, 6, 0)
	while True:
		print("\n--- Submenú de materias ---")
		print("1. Alta")
		print("2. Baja")
		print("3. Modificación")
		print("4. Listado")
		print("5. Ordenar por cuatrimestre")
		print("6. Buscar por código")
		print("0. Volver")
		opcion = pedir_opcion(opciones, "Elija una opción: ")
		if opcion == 1:
			dar_alta_materia(materias)
		elif opcion == 2:
			dar_baja_materia(materias, calificaciones)
		elif opcion == 3:
			modificar_datos_materia(materias)
		elif opcion == 4:
			listar_materias(materias)
		elif opcion == 5:
			mostrar_materias_ordenadas(materias)
		elif opcion == 6:
			mostrar_busqueda_materia(materias)
		else:
			return
