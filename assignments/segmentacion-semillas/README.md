# segmentacion-semillas

## ⚠️ Este assignment es distinto a los demás: es no supervisado

Todos los demás assignments del curso son de **aprendizaje supervisado**:
recibes un `train.csv` con la variable objetivo, entrenas un modelo, y lo
usas para predecir esa misma variable en `test.csv`.

Este assignment es de **clustering (aprendizaje no supervisado)**. Eso
cambia el flujo de trabajo de forma importante:

- No vas a "predecir" nada en el sentido tradicional. Vas a **agrupar**
  las filas de `test.csv` en grupos (clusters) usando solamente las
  variables de entrada, sin usar ninguna etiqueta de variedad.
- La columna de variedad real existe (la incluimos en `train.csv` para
  que puedas explorar y validar tu intuición), pero el ejercicio de
  fondo es agrupar sin verla — igual que tendrías que hacerlo en un caso
  real donde no existieran etiquetas.
- La calificación no compara tu predicción exacta de la clase contra la
  clase real (porque tus clusters pueden estar numerados 0/1/2 en
  cualquier orden, sin relación con las etiquetas 1/2/3 originales). En
  su lugar se usa el **Adjusted Rand Index (ARI)**, una métrica que
  compara dos particiones de un conjunto de datos y que es **invariante
  a cómo se numeren los grupos**: le da un score alto si tu agrupación
  coincide en estructura con la variedad real, sin importar qué número
  le pusiste a cada cluster.

## Enunciado

Un agrónomo midió propiedades geométricas de granos de trigo
pertenecientes a tres variedades distintas (**Kama**, **Rosa** y
**Canadian**), usando una técnica de rayos X blandos para no destruir el
grano. A partir de la imagen se extrajeron 7 medidas geométricas por
grano.

Tu tarea: sin usar la variedad real, agrupa los granos en 3 clusters que
reflejen la estructura de variedades presente en los datos.

## Datos

Los datos no están en este repositorio: se descargan una sola vez
desde el almacenamiento del curso.

```bash
curl -O https://d3qixogk4zgixq.cloudfront.net/data/segmentacion-semillas/train.csv
curl -O https://d3qixogk4zgixq.cloudfront.net/data/segmentacion-semillas/test.csv
```

- `train.csv`: 80% de los granos, **con** la columna `variedad` (para
  que explores y valides tu intuición sobre los grupos, aunque el
  ejercicio real es no supervisado).
- `test.csv`: 20% de los granos, **sin** la columna `variedad`. Debes
  generar una asignación de cluster (una etiqueta arbitraria `0`, `1` o
  `2`) para cada fila.

Columnas:

| Columna           | Descripción                                             |
|-------------------|----------------------------------------------------------|
| `id`              | identificador de la fila                                  |
| `area`            | área del grano                                             |
| `perimetro`       | perímetro del grano                                        |
| `compacidad`      | compacidad = 4·π·área / perímetro²                         |
| `longitud_nucleo` | longitud del núcleo del grano                               |
| `ancho_nucleo`    | ancho del núcleo del grano                                  |
| `coef_asimetria`  | coeficiente de asimetría                                    |
| `longitud_surco`  | longitud del surco del núcleo                               |
| `variedad`        | variedad de trigo (1 = Kama, 2 = Rosa, 3 = Canadian; solo en `train.csv`) — **no disponible en test, es lo que estamos agrupando** |

## Qué debes entregar

Un CSV con columnas `id,cluster` que contenga una asignación de cluster
(un entero, por ejemplo `0`, `1`, `2`) para cada fila de `test.csv`. Usa
`scripts/submit.py` desde la raíz del repo para enviarlo:

```bash
uv run scripts/submit.py segmentacion-semillas ./mi_prediccion.csv
```

## Cómo se califica

Tu entrega se compara automáticamente contra la variedad real (oculta)
de cada grano de `test.csv`. La métrica usada es el **Adjusted Rand
Index (ARI)** entre tu columna `cluster` y la variedad real. ARI va de
aproximadamente -0.5 a 1: 1 significa una coincidencia perfecta de
estructura entre tus clusters y las variedades reales (aunque los
números no coincidan), 0 es lo esperado para una asignación aleatoria, y
valores negativos indican una agrupación peor que el azar. Un ARI más
alto es mejor. Puedes ver tu score y tu posición en el leaderboard con:

```bash
uv run scripts/check_status.py segmentacion-semillas
```

## Por qué este formato es "AI-proof"

Un chatbot puede generarte código de clustering plausible, pero el
número de cluster que le toque a cada grano depende de detalles del
algoritmo, del escalado de variables y de la semilla aleatoria usada
sobre datos de test que el modelo nunca ha visto — no hay una respuesta
que se pueda copiar de memoria. Para obtener un buen ARI necesitas
efectivamente explorar los datos, elegir y ajustar un algoritmo de
clustering razonable, y verificar que los grupos resultantes tengan
sentido.

## Nota para el profesor

`solution.csv` (columnas `id,variedad` del 20% de test) se generó
localmente a partir de `sklearn.datasets.fetch_openml('seeds')` (split
80/20 estratificado por variedad, `random_state=42`) y quedó
**gitignored** en esta misma carpeta para no filtrar las etiquetas
reales en el repo público. Para habilitar la calificación automática
real falta copiar `solution.csv` al repo privado `ml-grading-infra`, que
debe calcular `sklearn.metrics.adjusted_rand_score(solution.variedad,
submission.cluster)` en vez de una métrica de clasificación estándar
(accuracy/F1/RMSE) como en los demás assignments. Ese paso queda fuera
del alcance de esta tarea.
