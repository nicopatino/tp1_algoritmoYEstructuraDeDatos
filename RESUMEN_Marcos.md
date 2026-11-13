# Marcos — Base común, menú principal y persistencia

Archivos: `base_comun.py`, `persistencia.py`, `menu_principal.py`, `test_base_comun.py`, `test_persistencia.py`.

Cómo correr:
- `python menu_principal.py` → el sistema.
- `python test_base_comun.py` y `python test_persistencia.py` → las pruebas.

Archivos que genera el programa: `datos_sistema.json` y `log_operaciones.txt`. Si el JSON está dañado, también `datos_sistema.json.bak`.

## 1. Los 7 conceptos de la consigna en mi parte

| Concepto | Dónde | Para qué (justificación) |
|---|---|---|
| **Diccionarios** | `cargar_datos_iniciales` arma `{codigo: {campo: valor}}`. `USUARIOS = {usuario: contraseña}`. `resumir_log` y `ranking_estudiantes` usan diccionarios contadores. | Acceder a un registro por su código, sin búsqueda secuencial, y contabilizar elementos. |
| **Tuplas** | Constantes `RANGO_*`, `CONDICIONES`, `SECCIONES_DATOS`. `cargar_datos_json` devuelve `(est, mat, cal)`. `leer_log` devuelve cada línea como `(tipo, usuario, detalle)`. | Son datos fijos o registros ya escritos que no deben modificarse. |
| **Conjuntos** | `armar_diccionario` detecta códigos repetidos con `set`. `cargar_datos_json` calcula las secciones faltantes con una diferencia de sets. `detectar_calificaciones_huerfanas` devuelve un set. | Evitar duplicados y comparar lo esperado contra lo que trae el archivo. |
| **Excepciones** | Las validaciones lanzan `ValueError`. Además se capturan `FileNotFoundError` (primera ejecución), `json.JSONDecodeError` (archivo dañado) y `OSError` (sin permisos o disco lleno). | Cada `except` atrapa un error concreto y muestra un mensaje claro. Nunca se usa `except:` general. |
| **Archivo de texto** | `log_operaciones.txt`: `registrar_operacion` escribe (modo `"a"`), `leer_log` lee y `mostrar_historial` usa lo leído (Consultas → 4). | Auditoría de accesos: logins correctos, fallidos, bloqueos, guardados y cierres. La contraseña nunca se guarda. |
| **Archivo JSON** | `datos_sistema.json`: `guardar_datos_json` (`json.dump`) y `cargar_datos_json` (`json.load`). | Que los cambios no se pierdan al cerrar el programa. |
| **Pruebas unitarias** | 16 en total: 10 en `test_base_comun.py` y 6 en `test_persistencia.py`. | Ver la sección 4. |

## 2. Persistencia paso a paso (punto 8 de la consigna)

1. **Al iniciar** (`iniciar_datos`):
   - Si existe el JSON, se recupera y se muestra cuántos registros tiene.
   - Si no existe (`FileNotFoundError`, primera ejecución), se usan los datos de la Parte 1 y se crea el archivo.
   - Si está dañado (`ValueError`), se copia a `.bak` para no perderlo y se arranca con los datos iniciales.
   - Por último, `detectar_calificaciones_huerfanas` avisa si alguna calificación apunta a un estudiante o materia que no existe.
2. **Durante el uso:** al volver de Estudiantes, Materias o Calificaciones, `menu_principal` guarda automáticamente. Las Consultas no guardan, porque solo leen.
3. **Al cerrar sesión:** se guarda una última vez y se registra `CIERRE_SESION` en el log.
4. **Al volver a ejecutar:** se repite el paso 1 y se recupera lo guardado.

**Detalle técnico para la defensa:** JSON solo admite claves de texto, así que el código `100` se guarda como `"100"`. Por eso `convertir_claves_a_entero` las vuelve a pasar a `int` al cargar. Sin esa conversión, `100 in estudiantes` daría `False` después de reabrir el programa.

## 3. Funciones de la base común (de la entrega anterior)

| Función | Qué hace |
|---|---|
| `convertir_entero`, `validar_rango`, `validar_texto_obligatorio`, `validar_nombre`, `validar_correo`, `validar_opcion` | Devuelven el dato limpio o lanzan `ValueError` con el motivo exacto. |
| `pedir_dato(mensaje, validador)` | El único `while` de "pedir hasta que sea válido". Captura el `ValueError` y vuelve a pedir. |
| `pedir_entero`, `pedir_entero_en_rango`, `pedir_opcion` | Atajos de `pedir_dato` armados con `lambda`. |
| `login()` | Hasta 3 intentos, registra cada uno en el log. **Ahora devuelve el nombre del usuario, o `""` si se bloqueó**, para poder registrar quién hizo cada operación. |
| `menu_principal(est, mat, cal, usuario)` | Coordina los submenús y guarda al volver de cada uno. |
| `submenu_consultas` | Analítico de un estudiante, ranking, informe por materia e historial de operaciones. |

## 4. Pruebas unitarias (16 de 16 aprobadas)

`test_base_comun.py` (10):

| # | Tipo | Función | Caso |
|---|---|---|---|
| 1 | Válido | `convertir_entero` | `"25"` → 25 |
| 2 | Válido | `validar_correo` | correo con dominio `.edu.ar` |
| 3 | Válido | `validar_nombre` | normaliza espacios de más |
| 4 | Válido | `cargar_datos_iniciales` | 10/10/10 registros |
| 5 | Inválido | `convertir_entero` | `"abc"` |
| 6 | Inválido | `validar_correo` | `marcos@gmail` |
| 7 | Inválido | `validar_opcion` | opción 9 inexistente |
| 8 | Límite | `validar_rango` | nota 10 (borde superior) |
| 9 | Límite | `convertir_entero` | solo espacios |
| 10 | Relevante | `analitico_estudiante` | analítico del 102 |

`test_persistencia.py` (6):

| # | Tipo | Función | Caso |
|---|---|---|---|
| 1 | Válido | `guardar_datos_json` + `cargar_datos_json` | guardar, volver a leer del disco y recuperar todo igual, con las claves como enteros |
| 2 | Inválido | `cargar_datos_json` | archivo inexistente → `FileNotFoundError` |
| 3 | Inválido | `cargar_datos_json` | JSON cortado a la mitad |
| 4 | Límite | `cargar_datos_json` | JSON válido pero sin la sección `materias` |
| 5 | Límite | `leer_log` + `resumir_log` | log con una línea rota en el medio |
| 6 | Relevante | `detectar_calificaciones_huerfanas` | calificación de un estudiante borrado |

Las pruebas de persistencia usan sus propios archivos `prueba_*.json` / `prueba_log.txt`, así no tocan los datos reales.

## 5. Contrato para P1 y P2

```python
estudiantes    = {100: {"nombre": "...", "edad": 21, "anio": 2, "correo": "..."}}
materias       = {200: {"nombre": "...", "cuatrimestre": 1, "carga_horaria": 4}}
calificaciones = {1:   {"estudiante": 100, "materia": 202, "nota": 8, "condicion": 2}}
```

- Sus submenús se llaman `submenu_estudiantes`, `submenu_materias` y `submenu_calificaciones`. Reciben `(estudiantes, materias, calificaciones)` y modifican los diccionarios en el lugar. **No necesitan guardar**: el menú principal guarda al volver de cada submenú.
- Si quieren dejar sus operaciones en el log: `registrar_operacion("ALTA_ESTUDIANTE", usuario, "código 110")`.
- Para pedir datos, usen `pedir_entero_en_rango(...)` y `pedir_dato(..., validar_nombre)`. Para aprobado/desaprobado, usen `es_aprobada(nota)`.

## 6. Cosas a corregir en el código base (avisar al grupo)

1. **Generadores prohibidos:** `all(... for ...)` en `pedir_nombre`, `any(... for ...)` en `alta_calificaciones` y `" | ".join(str(c) for c in ...)` en la matriz.
2. **`alta_materias` usa `pedir_nombre`:** no deja cargar "Inglés" ni "Cálculo I". Hay que usar `validar_texto_obligatorio`.
3. **Clave `"año"`:** unificar en `"anio"`.
4. **Regex:** se mantiene `re` porque se vio en la Clase VI y era obligatorio en la parte 1.
