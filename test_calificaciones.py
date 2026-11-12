"""Pruebas unitarias aisladas para las operaciones de calificaciones."""

import csv
import os
import tempfile
import unittest

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


class PruebasCalificaciones(unittest.TestCase):
	"""Probar operaciones con diccionarios de prueba nuevos por caso."""

	def setUp(self):
		"""Inicializar datos locales independientes de los datos del sistema."""
		self.estudiantes = {
			100: {"nombre": "Ada Lovelace"},
			101: {"nombre": "Grace Hopper"},
		}
		self.materias = {
			200: {"nombre": "Álgebra"},
			201: {"nombre": "Programación"},
			202: {"nombre": "Estadística"},
		}
		self.calificaciones = {}

	def agregar_acta(self, codigo, estudiante, materia, nota=8, condicion=2):
		"""Crear una acta válida para preparar el estado de una prueba."""
		return crear_calificacion(
			self.calificaciones,
			codigo,
			estudiante,
			materia,
			nota,
			condicion,
			self.estudiantes,
			self.materias,
		)

	def test_alta_correcta_y_registro_como_tupla(self):
		"""El alta guarda la tupla en el orden definido por el módulo."""
		acta = self.agregar_acta(1, 100, 200, 8, 2)

		self.assertEqual(acta, (1, 100, 200, 8, 2))
		self.assertIsInstance(self.calificaciones[1], tuple)
		self.assertEqual(self.calificaciones[1], (1, 100, 200, 8, 2))

	def test_rechazar_notas_fuera_de_rango(self):
		"""Rechazar notas menores a 1 y mayores a 10."""
		for nota in (0, 11):
			with self.subTest(nota=nota):
				with self.assertRaises(ValueError):
					validar_calificacion(nota, 3 if nota < 6 else 2)

	def test_rechazar_estudiante_inexistente(self):
		"""El alta lanza KeyError si el código de estudiante no existe."""
		with self.assertRaises(KeyError):
			crear_calificacion(
				self.calificaciones, 1, 999, 200, 8, 2,
				self.estudiantes, self.materias,
			)

	def test_rechazar_materia_inexistente(self):
		"""El alta lanza KeyError si el código de materia no existe."""
		with self.assertRaises(KeyError):
			crear_calificacion(
				self.calificaciones, 1, 100, 999, 8, 2,
				self.estudiantes, self.materias,
			)

	def test_rechazar_calificacion_duplicada_por_estudiante_y_materia(self):
		"""Un estudiante no puede tener dos actas para la misma materia."""
		self.agregar_acta(1, 100, 200)

		with self.assertRaises(ValueError):
			self.agregar_acta(2, 100, 200, 9, 2)

	def test_validar_coherencia_entre_nota_y_condicion(self):
		"""Las notas aprobadas y desaprobadas deben tener condición coherente."""
		self.assertEqual(validar_calificacion(6, 1), (6, 1))
		self.assertEqual(validar_calificacion(5, 3), (5, 3))
		for nota, condicion in ((5, 1), (8, 3)):
			with self.subTest(nota=nota, condicion=condicion):
				with self.assertRaises(ValueError):
					validar_calificacion(nota, condicion)

	def test_modificacion_correcta(self):
		"""La modificación reemplaza el registro por una tupla actualizada."""
		self.agregar_acta(1, 100, 200, 8, 2)

		acta = modificar_calificacion(
			self.calificaciones, 1, 101, 201, 6, 1,
			self.estudiantes, self.materias,
		)

		self.assertEqual(acta, (1, 101, 201, 6, 1))
		self.assertIsInstance(self.calificaciones[1], tuple)

	def test_baja_correcta(self):
		"""La baja elimina del diccionario el código indicado."""
		self.agregar_acta(1, 100, 200)

		eliminar_calificacion(self.calificaciones, 1)

		self.assertNotIn(1, self.calificaciones)

	def test_buscar_calificacion_inexistente(self):
		"""La búsqueda de un código ausente lanza KeyError."""
		with self.assertRaises(KeyError):
			buscar_calificacion(self.calificaciones, 1)

	def test_calcular_promedio_y_rechazar_promedio_vacio(self):
		"""Calcular promedio general y lanzar ZeroDivisionError si no hay actas."""
		self.agregar_acta(1, 100, 200, 8, 2)
		self.agregar_acta(2, 101, 201, 6, 1)

		self.assertEqual(calcular_promedio(self.calificaciones), 7)
		self.assertEqual(calcular_promedio(self.calificaciones, codigo_estudiante=100), 8)
		with self.assertRaises(ZeroDivisionError):
			calcular_promedio({})

	def test_listar_materias_sin_calificaciones_por_diferencia(self):
		"""Devolver materias cuyos códigos no aparecen en ninguna acta."""
		self.agregar_acta(1, 100, 200)

		self.assertEqual(
			listar_materias_sin_calificados(self.materias, self.calificaciones),
			[201, 202],
		)

	def test_sumatoria_recursiva(self):
		"""La función recursiva suma todas las notas de la secuencia."""
		self.assertEqual(sumar_notas_recursivo([2, 4, 6]), 12)
		self.assertEqual(sumar_notas_recursivo([]), 0)

	def test_exportar_acta_txt_y_csv(self):
		"""Exportar actas en ambos formatos y validar su contenido."""
		self.estudiantes[100]["nombre"] = "Ada, Lovelace"
		self.agregar_acta(1, 100, 200, 8, 2)

		with tempfile.TemporaryDirectory() as directorio:
			ruta_txt = os.path.join(directorio, "acta.txt")
			ruta_csv = os.path.join(directorio, "acta.csv")
			exportar_acta(self.calificaciones, self.estudiantes, self.materias, ruta_txt, "txt")
			exportar_acta(self.calificaciones, self.estudiantes, self.materias, ruta_csv, "csv")

			with open(ruta_txt, "r", encoding="utf-8") as archivo:
				contenido_txt = archivo.read()
			self.assertIn("codigo_calificacion", contenido_txt)
			self.assertIn("Ada, Lovelace", contenido_txt)

			with open(ruta_csv, "r", encoding="utf-8", newline="") as archivo:
				filas_csv = list(csv.reader(archivo))
			self.assertEqual(filas_csv[0][0], "codigo_calificacion")
			self.assertEqual(filas_csv[1][2], "Ada, Lovelace")
			self.assertEqual(filas_csv[1][5:], ["8", "promocionado"])


if __name__ == "__main__":
	unittest.main()
