# Sistema de Gestión Académica

## Versión oficial

El sistema está en la **carpeta raíz** de este repositorio. Ejecutá todos los comandos de esta guía desde esa carpeta.

La copia anterior que estaba en `tpo2/` se eliminó para que haya un solo `menu_principal.py`; si hace falta consultarla, sigue disponible en el historial de git.

## Ejecución

Desde la raíz del repositorio:

```bash
python menu_principal.py
```

Usuario inicial: `admin`. Contraseña inicial: `admin`.

El menú principal guarda los cambios al volver de los submenús. Los archivos `datos_sistema.json` y `log_operaciones.txt` se crean en la carpeta desde la que se ejecuta el programa; están excluidos del control de versiones por `.gitignore`.

## Módulos

| Archivo | Responsabilidad |
|---|---|
| `base_comun.py` | Datos iniciales, constantes, validaciones compartidas, entrada de datos e inicio de sesión. |
| `persistencia.py` | Guardado y carga JSON, recuperación de claves numéricas, compatibilidad de calificaciones históricas y nuevas, y registro de operaciones. |
| `menu_principal.py` | Inicio del sistema, menú principal, consultas e informes; coordina el guardado al volver de los submenús. |
| `persona_1_estudiantes.py` | Altas, bajas, modificaciones, listado ordenado, búsqueda por nombre, conteo por año y control de correos repetidos de estudiantes. |
| `materias.py` | Altas, bajas, modificaciones, búsqueda, listados y ordenamiento de materias. Rechaza la baja si existen calificaciones asociadas. |
| `calificaciones.py` | Gestión de actas como tuplas, validaciones, búsqueda, listados, promedios, materias sin calificaciones, recursividad y exportación TXT/CSV. |

El menú principal integra los submenús de Estudiantes, Materias y Calificaciones, más el submenú de Consultas.

## Pruebas

Las pruebas se implementan como funciones y se ejecutan directamente desde la carpeta raíz:

```bash
python test_base_comun.py
python test_persistencia.py
python test_materias.py
python test_calificaciones.py
```

`test_materias.py` y `test_calificaciones.py` informan los resultados de sus casos y resumen cuántas pruebas aprobaron o fallaron. `python -m unittest discover -v` no descubre pruebas en la configuración actual.

`test_persistencia.py` crea archivos `prueba_*.json` y `prueba_*.txt` en el directorio de trabajo; esos nombres están excluidos en `.gitignore`.
