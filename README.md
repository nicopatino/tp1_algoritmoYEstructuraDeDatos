# Sistema de Gestión Académica

## Versión oficial

La versión actualizada del sistema está en la **carpeta raíz** de este repositorio. Ejecutá todos los comandos de esta guía desde esa carpeta.

La carpeta `tpo2/` contiene una copia anterior: no incluye los módulos actuales `materias.py` y `calificaciones.py`, y su menú conserva submenús provisionales. No la uses para iniciar la versión actual. No fue eliminada para conservar esa copia de referencia.

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
| `materias.py` | Altas, bajas, modificaciones, búsqueda, listados y ordenamiento de materias. Rechaza la baja si existen calificaciones asociadas. |
| `calificaciones.py` | Gestión de actas como tuplas, validaciones, búsqueda, listados, promedios, materias sin calificaciones, recursividad y exportación TXT/CSV. |

El submenú de Estudiantes en `menu_principal.py` todavía está pendiente de integración.

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
