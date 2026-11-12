"""Pruebas unitarias aisladas para el módulo de materias."""

from copy import deepcopy
import unittest

from materias import (
	actualizar_materia,
	buscar_materia,
	crear_materia,
	eliminar_materia,
	ordenar_materias_por_cuatrimestre,
)


class PruebasMaterias(unittest.TestCase):
	"""Probar operaciones de materias con datos locales a cada prueba."""

	def setUp(self):
		"""Crear diccionarios independientes, sin usar datos del sistema."""
		self.materias = {
			200: {"nombre": "Álgebra", "cuatrimestre": 2, "carga_horaria": 4},
			201: {"nombre": "Programación", "cuatrimestre": 1, "carga_horaria": 6},
		}
		self.calificaciones = {}

	def test_alta_correcta_de_materia(self):
		"""El alta guarda todos los campos y devuelve el código asignado."""
		codigo = crear_materia(self.materias, 202, "Estadística", 1, 5)

		self.assertEqual(codigo, 202)
		self.assertEqual(self.materias[202], {
			"nombre": "Estadística",
			"cuatrimestre": 1,
			"carga_horaria": 5,
		})

	def test_rechazar_codigo_duplicado(self):
		"""Un código existente no puede volver a darse de alta."""
		with self.assertRaises(ValueError):
			crear_materia(self.materias, 200, "Materia duplicada", 1, 4)

	def test_rechazar_cuatrimestre_y_carga_fuera_de_rango(self):
		"""Los cuatrimestres y las cargas horarias deben respetar sus límites."""
		casos_invalidos = ((0, 4), (3, 4), (1, 0), (1, 21))
		for indice, (cuatrimestre, carga_horaria) in enumerate(casos_invalidos):
			with self.subTest(cuatrimestre=cuatrimestre, carga_horaria=carga_horaria):
				with self.assertRaises(ValueError):
					crear_materia(
						self.materias,
						300 + indice,
					"Materia de prueba",
					cuatrimestre,
					carga_horaria,
					)

	def test_modificacion_correcta_de_materia(self):
		"""La modificación actualiza nombre, cuatrimestre y carga horaria."""
		actualizar_materia(self.materias, 200, "Álgebra II", 1, 8)

		self.assertEqual(self.materias[200], {
			"nombre": "Álgebra II",
			"cuatrimestre": 1,
			"carga_horaria": 8,
		})

	def test_buscar_materia_inexistente(self):
		"""La búsqueda de un código válido pero ausente lanza KeyError."""
		with self.assertRaises(KeyError):
			buscar_materia(self.materias, 999)

	def test_baja_correcta_sin_calificaciones(self):
		"""Una materia sin actas asociadas se elimina del diccionario."""
		calificaciones_antes = deepcopy(self.calificaciones)
		otras_materias_antes = deepcopy(self.materias)
		del otras_materias_antes[200]

		eliminar_materia(self.materias, self.calificaciones, 200)

		self.assertEqual(self.materias, otras_materias_antes)
		self.assertEqual(self.calificaciones, calificaciones_antes)

	def test_rechazar_baja_con_diccionario_historico(self):
		"""Rechazar la baja con actas históricas sin modificar ningún dato."""
		self.calificaciones[1] = {
			"estudiante": 100,
			"materia": 200,
			"nota": 8,
			"condicion": 1,
		}
		materias_antes = deepcopy(self.materias)
		calificaciones_antes = deepcopy(self.calificaciones)

		with self.assertRaises(ValueError):
			eliminar_materia(self.materias, self.calificaciones, 200)

		self.assertEqual(self.materias, materias_antes)
		self.assertEqual(self.calificaciones, calificaciones_antes)

	def test_rechazar_baja_con_tupla(self):
		"""Rechazar la baja con un acta tuple sin modificar ningún dato."""
		self.calificaciones[1] = (1, 100, 200, 8, 1)
		materias_antes = deepcopy(self.materias)
		calificaciones_antes = deepcopy(self.calificaciones)

		with self.assertRaises(ValueError):
			eliminar_materia(self.materias, self.calificaciones, 200)

		self.assertEqual(self.materias, materias_antes)
		self.assertEqual(self.calificaciones, calificaciones_antes)

	def test_rechazar_baja_con_formato_desconocido(self):
		"""Bloquear la baja si no se puede determinar la materia de un acta."""
		self.calificaciones[1] = "registro no reconocido"
		materias_antes = deepcopy(self.materias)
		calificaciones_antes = deepcopy(self.calificaciones)

		with self.assertRaises(ValueError):
			eliminar_materia(self.materias, self.calificaciones, 200)

		self.assertEqual(self.materias, materias_antes)
		self.assertEqual(self.calificaciones, calificaciones_antes)

	def test_ordenar_por_cuatrimestre_y_codigo(self):
		"""El orden agrupa por cuatrimestre y desempata por código."""
		crear_materia(self.materias, 202, "Cálculo", 1, 4)

		ordenadas = ordenar_materias_por_cuatrimestre(self.materias)

		self.assertEqual([codigo for codigo, materia in ordenadas], [201, 202, 200])
		self.assertEqual([materia["cuatrimestre"] for codigo, materia in ordenadas], [1, 1, 2])


if __name__ == "__main__":
	unittest.main()
