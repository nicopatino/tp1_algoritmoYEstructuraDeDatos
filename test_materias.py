"""Pruebas funcionales aisladas para las operaciones del módulo materias."""

from materias import (
	actualizar_materia,
	buscar_materia,
	crear_materia,
	eliminar_materia,
	ordenar_materias_por_cuatrimestre,
)


def crear_datos_prueba():
	"""Crear diccionarios nuevos para una prueba independiente."""
	materias = {
		200: {"nombre": "Álgebra", "cuatrimestre": 2, "carga_horaria": 4},
		201: {"nombre": "Programación", "cuatrimestre": 1, "carga_horaria": 6},
	}
	return materias, {}


def copiar_materias(materias):
	"""Copiar manualmente el diccionario y cada registro de materia."""
	return {codigo: dict(datos) for codigo, datos in materias.items()}


def copiar_calificaciones(calificaciones):
	"""Copiar los registros históricos dict y conservar las tuplas inmutables."""
	return {
		codigo: dict(acta) if isinstance(acta, dict) else acta
		for codigo, acta in calificaciones.items()
	}


def probar_alta_correcta():
	"""Dar de alta una materia y devolver código y registro obtenidos."""
	materias, calificaciones = crear_datos_prueba()
	codigo = crear_materia(materias, 202, "Estadística", 1, 5)
	return codigo, materias.get(202)


def probar_codigo_duplicado():
	"""Intentar dar de alta un código de materia existente."""
	materias, calificaciones = crear_datos_prueba()
	return crear_materia(materias, 200, "Materia duplicada", 1, 4)


def probar_rangos_invalidos(cuatrimestre, carga_horaria):
	"""Intentar crear una materia con cuatrimestre o carga fuera de rango."""
	materias, calificaciones = crear_datos_prueba()
	return crear_materia(materias, 300, "Materia de prueba", cuatrimestre, carga_horaria)


def probar_modificacion_correcta():
	"""Modificar todos los campos de una materia existente."""
	materias, calificaciones = crear_datos_prueba()
	actualizar_materia(materias, 200, "Álgebra II", 1, 8)
	return materias[200]


def probar_busqueda_inexistente():
	"""Buscar un código válido que no está en el diccionario."""
	materias, calificaciones = crear_datos_prueba()
	return buscar_materia(materias, 999)


def probar_baja_sin_calificaciones():
	"""Eliminar una materia sin actas y conservar intacto el diccionario de actas."""
	materias, calificaciones = crear_datos_prueba()
	calificaciones_antes = copiar_calificaciones(calificaciones)
	otras_materias_antes = copiar_materias(materias)
	del otras_materias_antes[200]
	eliminar_materia(materias, calificaciones, 200)
	return materias, calificaciones, calificaciones_antes, otras_materias_antes


def probar_baja_con_diccionario_historico():
	"""Rechazar la baja cuando una acta histórica refiere a la materia."""
	materias, calificaciones = crear_datos_prueba()
	calificaciones[1] = {
		"estudiante": 100,
		"materia": 200,
		"nota": 8,
		"condicion": 1,
	}
	materias_antes = copiar_materias(materias)
	calificaciones_antes = copiar_calificaciones(calificaciones)
	try:
		eliminar_materia(materias, calificaciones, 200)
	except ValueError:
		return materias, calificaciones, materias_antes, calificaciones_antes
	raise AssertionError("La baja no rechazó la materia con acta histórica")


def probar_baja_con_tupla():
	"""Rechazar la baja cuando una acta tuple refiere a la materia."""
	materias, calificaciones = crear_datos_prueba()
	calificaciones[1] = (1, 100, 200, 8, 1)
	materias_antes = copiar_materias(materias)
	calificaciones_antes = copiar_calificaciones(calificaciones)
	try:
		eliminar_materia(materias, calificaciones, 200)
	except ValueError:
		return materias, calificaciones, materias_antes, calificaciones_antes
	raise AssertionError("La baja no rechazó la materia con acta tuple")


def probar_baja_con_formato_desconocido():
	"""Bloquear la baja si el formato de un acta no puede interpretarse."""
	materias, calificaciones = crear_datos_prueba()
	calificaciones[1] = "registro no reconocido"
	materias_antes = copiar_materias(materias)
	calificaciones_antes = copiar_calificaciones(calificaciones)
	try:
		eliminar_materia(materias, calificaciones, 200)
	except ValueError:
		return materias, calificaciones, materias_antes, calificaciones_antes
	raise AssertionError("La baja no rechazó el formato desconocido")


def probar_ordenamiento():
	"""Ordenar materias por cuatrimestre y código ascendente."""
	materias, calificaciones = crear_datos_prueba()
	crear_materia(materias, 202, "Cálculo", 1, 4)
	ordenadas = ordenar_materias_por_cuatrimestre(materias)
	return (
		[codigo for codigo, materia in ordenadas],
		[materia["cuatrimestre"] for codigo, materia in ordenadas],
	)


def ejecutar_prueba(numero, funcion, datos, esperado, ejecutar):
	"""Ejecutar y reportar una prueba, incluyendo excepciones inesperadas."""
	try:
		obtenido = ejecutar()
		aprobada = obtenido == esperado
		resultado_obtenido = obtenido
	except Exception as error:
		aprobada = esperado == type(error).__name__
		resultado_obtenido = "{}: {}".format(type(error).__name__, error)
	print("Prueba {}".format(numero))
	print("  Función:  ", funcion)
	print("  Datos:    ", datos)
	print("  Esperado: ", esperado)
	print("  Obtenido: ", resultado_obtenido)
	print("  Resultado:", "APROBADA" if aprobada else "FALLIDA")
	print()
	return aprobada


def correr_pruebas():
	"""Ejecutar todos los casos y mostrar el resumen de aprobadas y fallidas."""
	resultados = []
	resultados.append(ejecutar_prueba(
		1, "crear_materia", "código 202, Estadística, cuatrimestre 1, carga 5",
		(202, {"nombre": "Estadística", "cuatrimestre": 1, "carga_horaria": 5}),
		probar_alta_correcta,
	))
	resultados.append(ejecutar_prueba(
		2, "crear_materia", "código existente 200",
		"ValueError", probar_codigo_duplicado,
	))

	casos_invalidos = ((0, 4), (3, 4), (1, 0), (1, 21))
	for indice, (cuatrimestre, carga_horaria) in enumerate(casos_invalidos, start=3):
		resultados.append(ejecutar_prueba(
			indice,
			"crear_materia",
			"cuatrimestre {}, carga horaria {}".format(cuatrimestre, carga_horaria),
			"ValueError",
			lambda cuatrimestre=cuatrimestre, carga_horaria=carga_horaria:
				probar_rangos_invalidos(cuatrimestre, carga_horaria),
		))

	resultados.append(ejecutar_prueba(
		7, "actualizar_materia", "código 200, Álgebra II, cuatrimestre 1, carga 8",
		{"nombre": "Álgebra II", "cuatrimestre": 1, "carga_horaria": 8},
		probar_modificacion_correcta,
	))
	resultados.append(ejecutar_prueba(
		8, "buscar_materia", "código inexistente 999", "KeyError",
		probar_busqueda_inexistente,
	))
	resultados.append(ejecutar_prueba(
		9, "eliminar_materia", "código 200 sin actas",
		(
			{201: {"nombre": "Programación", "cuatrimestre": 1, "carga_horaria": 6}},
			{},
			{},
			{201: {"nombre": "Programación", "cuatrimestre": 1, "carga_horaria": 6}},
		),
		probar_baja_sin_calificaciones,
	))
	resultados.append(ejecutar_prueba(
		10, "eliminar_materia", "acta histórica dict asociada al código 200",
		(
			{200: {"nombre": "Álgebra", "cuatrimestre": 2, "carga_horaria": 4},
			 201: {"nombre": "Programación", "cuatrimestre": 1, "carga_horaria": 6}},
			{1: {"estudiante": 100, "materia": 200, "nota": 8, "condicion": 1}},
			{200: {"nombre": "Álgebra", "cuatrimestre": 2, "carga_horaria": 4},
			 201: {"nombre": "Programación", "cuatrimestre": 1, "carga_horaria": 6}},
			{1: {"estudiante": 100, "materia": 200, "nota": 8, "condicion": 1}},
		),
		probar_baja_con_diccionario_historico,
	))
	resultados.append(ejecutar_prueba(
		11, "eliminar_materia", "acta tuple (1, 100, 200, 8, 1)",
		(
			{200: {"nombre": "Álgebra", "cuatrimestre": 2, "carga_horaria": 4},
			 201: {"nombre": "Programación", "cuatrimestre": 1, "carga_horaria": 6}},
			{1: (1, 100, 200, 8, 1)},
			{200: {"nombre": "Álgebra", "cuatrimestre": 2, "carga_horaria": 4},
			 201: {"nombre": "Programación", "cuatrimestre": 1, "carga_horaria": 6}},
			{1: (1, 100, 200, 8, 1)},
		),
		probar_baja_con_tupla,
	))
	resultados.append(ejecutar_prueba(
		12, "eliminar_materia", "acta con formato desconocido",
		(
			{200: {"nombre": "Álgebra", "cuatrimestre": 2, "carga_horaria": 4},
			 201: {"nombre": "Programación", "cuatrimestre": 1, "carga_horaria": 6}},
			{1: "registro no reconocido"},
			{200: {"nombre": "Álgebra", "cuatrimestre": 2, "carga_horaria": 4},
			 201: {"nombre": "Programación", "cuatrimestre": 1, "carga_horaria": 6}},
			{1: "registro no reconocido"},
		),
		probar_baja_con_formato_desconocido,
	))
	resultados.append(ejecutar_prueba(
		13, "ordenar_materias_por_cuatrimestre", "cuatrimestres 1, 1, 2",
		([201, 202, 200], [1, 1, 2]), probar_ordenamiento,
	))

	aprobadas = resultados.count(True)
	fallidas = len(resultados) - aprobadas
	print("RESUMEN: {} aprobadas, {} fallidas de {} pruebas".format(
		aprobadas, fallidas, len(resultados)
	))
	return fallidas == 0


if __name__ == "__main__":
	if not correr_pruebas():
		raise SystemExit(1)