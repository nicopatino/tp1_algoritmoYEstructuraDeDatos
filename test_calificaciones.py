"""Pruebas funcionales aisladas para las operaciones de calificaciones."""

import os
import tempfile

from calificaciones import (
	buscar_calificacion,
	calcular_promedio,
	crear_calificacion,
	eliminar_calificacion,
	exportar_acta,
	listar_materias_sin_calificados,
	modificar_calificacion,
	sumar_notas_recursivo,
	validar_calificacion,
)


def crear_datos_prueba():
	"""Crear diccionarios nuevos para una prueba independiente."""
	estudiantes = {
		100: {"nombre": "Ada Lovelace"},
		101: {"nombre": "Grace Hopper"},
	}
	materias = {
		200: {"nombre": "Álgebra"},
		201: {"nombre": "Programación"},
		202: {"nombre": "Estadística"},
	}
	return estudiantes, materias, {}


def probar_alta_correcta():
	"""Dar de alta un acta y verificar que se almacena como tupla."""
	estudiantes, materias, calificaciones = crear_datos_prueba()
	acta = crear_calificacion(calificaciones, 1, 100, 200, 8, 2, estudiantes, materias)
	return acta, isinstance(calificaciones[1], tuple)


def probar_nota_fuera_de_rango(nota, condicion):
	"""Validar un límite inválido de nota."""
	return validar_calificacion(nota, condicion)


def probar_estudiante_inexistente():
	"""Intentar crear un acta para un estudiante que no existe."""
	estudiantes, materias, calificaciones = crear_datos_prueba()
	return crear_calificacion(calificaciones, 1, 999, 200, 8, 2, estudiantes, materias)


def probar_materia_inexistente():
	"""Intentar crear un acta para una materia que no existe."""
	estudiantes, materias, calificaciones = crear_datos_prueba()
	return crear_calificacion(calificaciones, 1, 100, 999, 8, 2, estudiantes, materias)


def probar_calificacion_duplicada():
	"""Intentar repetir el par estudiante-materia con otro código de acta."""
	estudiantes, materias, calificaciones = crear_datos_prueba()
	crear_calificacion(calificaciones, 1, 100, 200, 8, 2, estudiantes, materias)
	return crear_calificacion(calificaciones, 2, 100, 200, 9, 2, estudiantes, materias)


def probar_nota_condicion_valida(nota, condicion):
	"""Validar una combinación coherente de nota y condición."""
	return validar_calificacion(nota, condicion)


def probar_modificacion_correcta():
	"""Modificar el estudiante, la materia, la nota y la condición del acta."""
	estudiantes, materias, calificaciones = crear_datos_prueba()
	crear_calificacion(calificaciones, 1, 100, 200, 8, 2, estudiantes, materias)
	acta = modificar_calificacion(
		calificaciones, 1, 101, 201, 6, 1, estudiantes, materias
	)
	return acta, isinstance(calificaciones[1], tuple)


def probar_baja_correcta():
	"""Eliminar una calificación existente."""
	estudiantes, materias, calificaciones = crear_datos_prueba()
	crear_calificacion(calificaciones, 1, 100, 200, 8, 2, estudiantes, materias)
	eliminar_calificacion(calificaciones, 1)
	return 1 not in calificaciones


def probar_busqueda_inexistente():
	"""Buscar un código de calificación que no está en el diccionario."""
	estudiantes, materias, calificaciones = crear_datos_prueba()
	return buscar_calificacion(calificaciones, 1)


def probar_promedio_general():
	"""Calcular el promedio de notas de todas las actas."""
	estudiantes, materias, calificaciones = crear_datos_prueba()
	crear_calificacion(calificaciones, 1, 100, 200, 8, 2, estudiantes, materias)
	crear_calificacion(calificaciones, 2, 101, 201, 6, 1, estudiantes, materias)
	return calcular_promedio(calificaciones)


def probar_promedio_filtrado():
	"""Calcular el promedio de un estudiante específico."""
	estudiantes, materias, calificaciones = crear_datos_prueba()
	crear_calificacion(calificaciones, 1, 100, 200, 8, 2, estudiantes, materias)
	crear_calificacion(calificaciones, 2, 101, 201, 6, 1, estudiantes, materias)
	return calcular_promedio(calificaciones, codigo_estudiante=100)


def probar_promedio_sin_actas():
	"""Calcular el promedio de un diccionario vacío."""
	return calcular_promedio({})


def probar_materias_sin_calificados():
	"""Obtener por diferencia de conjuntos las materias sin actas."""
	estudiantes, materias, calificaciones = crear_datos_prueba()
	crear_calificacion(calificaciones, 1, 100, 200, 8, 2, estudiantes, materias)
	return listar_materias_sin_calificados(materias, calificaciones)


def probar_sumatoria_recursiva(notas):
	"""Sumar recursivamente la secuencia recibida."""
	return sumar_notas_recursivo(notas)


def probar_exportacion_txt():
	"""Exportar un acta TXT y devolver su contenido antes de limpiar el temporal."""
	estudiantes, materias, calificaciones = crear_datos_prueba()
	estudiantes[100]["nombre"] = "Ada, Lovelace"
	crear_calificacion(calificaciones, 1, 100, 200, 8, 2, estudiantes, materias)
	with tempfile.TemporaryDirectory() as directorio:
		ruta = os.path.join(directorio, "acta.txt")
		exportar_acta(calificaciones, estudiantes, materias, ruta, "txt")
		with open(ruta, "r", encoding="utf-8") as archivo:
			contenido = archivo.read()
		return "codigo_calificacion" in contenido and "Ada, Lovelace" in contenido


def probar_exportacion_csv():
	"""Exportar CSV escapando comas, comillas y saltos de línea en un campo."""
	estudiantes, materias, calificaciones = crear_datos_prueba()
	estudiantes[100]["nombre"] = 'Ada, "The Great"\nLovelace'
	crear_calificacion(calificaciones, 1, 100, 200, 8, 2, estudiantes, materias)
	with tempfile.TemporaryDirectory() as directorio:
		ruta = os.path.join(directorio, "acta.csv")
		exportar_acta(calificaciones, estudiantes, materias, ruta, "csv")
		with open(ruta, "r", encoding="utf-8", newline="") as archivo:
			contenido = archivo.read()
		return contenido


def ejecutar_prueba(numero, funcion, datos, esperado, ejecutar):
	"""Ejecutar y reportar una prueba, incluyendo excepciones esperadas."""
	try:
		obtenido = ejecutar()
		aprobada = obtenido == esperado
		resultado_obtenido = obtenido
	except Exception as error:
		aprobada = isinstance(esperado, type) and isinstance(error, esperado)
		resultado_obtenido = "{}: {}".format(type(error).__name__, error)
		if isinstance(esperado, type):
			esperado = esperado.__name__
	print("Prueba {}".format(numero))
	print("  Función:  ", funcion)
	print("  Datos:    ", datos)
	print("  Esperado: ", esperado)
	print("  Obtenido: ", resultado_obtenido)
	print("  Resultado:", "APROBADA" if aprobada else "FALLIDA")
	print()
	return aprobada


def correr_pruebas():
	"""Ejecutar todos los casos y devolver True solo si todos aprobaron."""
	resultados = []
	resultados.append(ejecutar_prueba(
		1, "crear_calificacion", "código 1, estudiante 100, materia 200, nota 8, condición 2",
		((1, 100, 200, 8, 2), True), probar_alta_correcta,
	))
	resultados.append(ejecutar_prueba(
		2, "validar_calificacion", "nota 0, condición 3", ValueError,
		lambda: probar_nota_fuera_de_rango(0, 3),
	))
	resultados.append(ejecutar_prueba(
		3, "validar_calificacion", "nota 11, condición 2", ValueError,
		lambda: probar_nota_fuera_de_rango(11, 2),
	))
	resultados.append(ejecutar_prueba(
		4, "crear_calificacion", "código de estudiante 999 inexistente", KeyError,
		probar_estudiante_inexistente,
	))
	resultados.append(ejecutar_prueba(
		5, "crear_calificacion", "código de materia 999 inexistente", KeyError,
		probar_materia_inexistente,
	))
	resultados.append(ejecutar_prueba(
		6, "crear_calificacion", "segundo acta del par estudiante 100-materia 200", ValueError,
		probar_calificacion_duplicada,
	))
	resultados.append(ejecutar_prueba(
		7, "validar_calificacion", "nota 6, condición 1", (6, 1),
		lambda: probar_nota_condicion_valida(6, 1),
	))
	resultados.append(ejecutar_prueba(
		8, "validar_calificacion", "nota 5, condición 3", (5, 3),
		lambda: probar_nota_condicion_valida(5, 3),
	))
	resultados.append(ejecutar_prueba(
		9, "validar_calificacion", "nota 5, condición 1 incoherentes", ValueError,
		lambda: probar_nota_condicion_valida(5, 1),
	))
	resultados.append(ejecutar_prueba(
		10, "validar_calificacion", "nota 8, condición 3 incoherentes", ValueError,
		lambda: probar_nota_condicion_valida(8, 3),
	))
	resultados.append(ejecutar_prueba(
		11, "modificar_calificacion", "código 1 a estudiante 101, materia 201, nota 6, condición 1",
		((1, 101, 201, 6, 1), True), probar_modificacion_correcta,
	))
	resultados.append(ejecutar_prueba(
		12, "eliminar_calificacion", "eliminar código 1", True, probar_baja_correcta,
	))
	resultados.append(ejecutar_prueba(
		13, "buscar_calificacion", "código ausente 1", KeyError,
		probar_busqueda_inexistente,
	))
	resultados.append(ejecutar_prueba(
		14, "calcular_promedio", "notas 8 y 6", 7, probar_promedio_general,
	))
	resultados.append(ejecutar_prueba(
		15, "calcular_promedio", "filtrar estudiante 100 con nota 8", 8,
		probar_promedio_filtrado,
	))
	resultados.append(ejecutar_prueba(
		16, "calcular_promedio", "sin actas", ZeroDivisionError,
		probar_promedio_sin_actas,
	))
	resultados.append(ejecutar_prueba(
		17, "listar_materias_sin_calificados", "materia 200 calificada; 201 y 202 sin actas",
		[201, 202], probar_materias_sin_calificados,
	))
	resultados.append(ejecutar_prueba(
		18, "sumar_notas_recursivo", "notas [2, 4, 6]", 12,
		lambda: probar_sumatoria_recursiva([2, 4, 6]),
	))
	resultados.append(ejecutar_prueba(
		19, "sumar_notas_recursivo", "secuencia vacía", 0,
		lambda: probar_sumatoria_recursiva([]),
	))
	resultados.append(ejecutar_prueba(
		20, "exportar_acta", "formato TXT; temporal con cabecera y nombre",
		True, probar_exportacion_txt,
	))
	resultados.append(ejecutar_prueba(
		21, "exportar_acta", "CSV con nombre que contiene coma, comillas y salto de línea",
		(
			"codigo_calificacion,codigo_estudiante,estudiante,codigo_materia,"
			"materia,nota,condicion\r\n"
			'1,100,"Ada, ""The Great""\nLovelace",200,Álgebra,8,promocionado\r\n'
		),
		probar_exportacion_csv,
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