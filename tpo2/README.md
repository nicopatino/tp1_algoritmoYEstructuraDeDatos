# Sistema de Gestión Académica — Segunda parte

## Cómo ejecutar

```bash
cd tpo2
python menu_principal.py      # el sistema (usuario: admin / contraseña: admin)
python test_base_comun.py     # 10 pruebas unitarias
python test_persistencia.py   # 6 pruebas unitarias
python test_estudiantes.py    # 5 pruebas de integración y baja de estudiantes
```

## Archivos

| Archivo | Contenido | Responsable |
|---|---|---|
| `base_comun.py` | Constantes (tuplas), datos iniciales en diccionarios, validaciones con `ValueError`, `pedir_dato`, login | Marcos Silva Sapia |
| `persistencia.py` | Guardado/carga en `datos_sistema.json` y log en `log_operaciones.txt` | Marcos Silva Sapia |
| `menu_principal.py` | Arranque, menú principal, guardado automático y submenú de consultas | Marcos Silva Sapia |
| `test_base_comun.py`, `test_persistencia.py`, `test_estudiantes.py` | Pruebas (21) | Marcos Silva Sapia |
| `RESUMEN_PERSONA3.md` | Explicación para la defensa y contrato de integración | Marcos Silva Sapia |

## Para integrar las otras partes

El submenú real de Estudiantes se importa desde `persona_1_estudiantes.py` y recibe `(estudiantes, calificaciones)`. Materias y Calificaciones todavía están pendientes de integración y reciben `(estudiantes, materias, calificaciones)`. Todos modifican los diccionarios en el lugar; el guardado lo hace el menú principal. El formato de los datos está en `RESUMEN_PERSONA3.md`, sección 5.

Los archivos `datos_sistema.json` y `log_operaciones.txt` se crean solos al ejecutar y están en `.gitignore`.
