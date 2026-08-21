# recomendador-peliculas

## Enunciado

En 2006, Netflix lanzó el **Netflix Prize**: un millón de dólares para
quien mejorara en un 10% el RMSE de su sistema de recomendación de
películas, usando únicamente el historial de calificaciones de sus
usuarios (sin atributos de las películas ni de los usuarios). Ese
concurso popularizó la **factorización de matrices** como técnica
central del *collaborative filtering*.

Esta actividad es una versión simplificada del mismo problema: tu
tarea es predecir el **rating** (1 a 5 estrellas) que un usuario le
daría a una película que no ha calificado, usando el dataset
[MovieLens 100k](https://grouplens.org/datasets/movielens/100k/).

No se trata de adivinar "a ojo" — con casi 1000 usuarios y más de 1600
películas, y una matriz de interacciones con más del 93% de celdas
vacías, solo un modelo que aprenda patrones colectivos (o de
contenido) generalizará bien sobre los pares `(user_id, item_id)` del
conjunto de evaluación.

Puedes resolverlo con la técnica que prefieras (o combinarlas):

- **Collaborative filtering** vía factorización de matrices (la
  técnica vista en el notebook de clase: `R ≈ U · Vᵀ`, entrenada con
  SGD en numpy puro), o similitud usuario-usuario / ítem-ítem sobre la
  matriz de utilidad.
- **Content-based filtering** usando los géneros de `movies.csv` para
  construir un perfil de usuario y estimar el rating por similitud.
- Un **baseline** simple (ej. promedio global, promedio por película,
  promedio por usuario) como punto de partida antes de algo más
  sofisticado.

Los pares `(usuario, película)` de `test.csv` son un split **distinto**
al que se usó en el notebook de clase (misma fuente de datos, semilla
de partición diferente), así que no vas a encontrar la respuesta ya
resuelta ahí — necesitas correr tu propio modelo sobre estos pares.

## Datos

Los datos no están en este repositorio: se descargan una sola vez
desde el almacenamiento del curso.

```bash
curl -O https://d3qixogk4zgixq.cloudfront.net/data/recomendador-peliculas/train.csv
curl -O https://d3qixogk4zgixq.cloudfront.net/data/recomendador-peliculas/test.csv
curl -O https://d3qixogk4zgixq.cloudfront.net/data/recomendador-peliculas/movies.csv
```

- `train.csv`: 80,000 interacciones (80% del dataset), con columnas
  `id, user_id, item_id, rating, timestamp`. Úsalo para entrenar tu
  modelo (construir la matriz de utilidad, entrenar la factorización,
  calcular perfiles de usuario, etc).
- `test.csv`: 20,000 interacciones (20% restante), con columnas
  `id, user_id, item_id` — **sin** la columna `rating`. Debes generar
  una predicción de rating para cada fila.
- `movies.csv`: metadata de las 1682 películas del catálogo —
  `item_id, title` y 19 columnas binarias de género (`Action`,
  `Comedy`, `Drama`, ...). Útil si quieres intentar un enfoque
  content-based.

El split de `train.csv` / `test.csv` es un particionamiento aleatorio
80/20 de las filas de interacciones de `u.data` (no por usuario ni por
película), con `random_state=123`.

## Qué debes entregar

Un CSV con columnas `id,rating` que contenga una predicción de rating
(idealmente en el rango 1-5, aunque no es obligatorio recortarlo) para
cada fila de `test.csv`. Usa `scripts/submit.py` desde la raíz del
repo para enviarlo:

```bash
uv run scripts/submit.py recomendador-peliculas ./mi_prediccion.csv
```

## Cómo se califica

Tu entrega se compara automáticamente contra un conjunto de labels
privado que no ves (los ratings reales de `test.csv`). La métrica
usada es: **RMSE** (raíz del error cuadrático medio) entre tu
predicción y el rating real. Un RMSE más bajo es mejor. Puedes ver tu
score y tu posición en el leaderboard con:

```bash
uv run scripts/check_status.py recomendador-peliculas
```

## Por qué este formato es "AI-proof"

Un chatbot puede generarte código plausible de un recomendador, pero
no puede adivinar los ratings reales de pares `(usuario, película)`
que nunca ha visto resueltos. Para obtener un buen RMSE necesitas
efectivamente construir la matriz de utilidad, entrenar un modelo
(factorización, similitud, o lo que elijas) y validar que generalice
sobre pares no vistos — no basta con copiar una respuesta.

## Nota para el profesor

`train.csv`, `test.csv`, `solution.csv` y `movies.csv` se generaron
localmente a partir de MovieLens 100k
(`https://files.grouplens.org/datasets/movielens/ml-100k.zip`, `u.data`
y `u.item`), con un split 80/20 de las filas de interacciones
(`random_state=123`, semilla distinta a la usada en el notebook de
clase `random_state=42`, para que el split del assignment sea
disjunto en la práctica del que ya se resuelve en clase). `movies.csv`
se deriva de `u.item` sin ninguna transformación de privacidad (es
metadata pública de películas, no hay filtración de labels ahí).

`solution.csv` (columnas `id,rating` del 20% de test) quedó **local y
gitignored** en esta misma carpeta (`assignments/recomendador-peliculas/.gitignore`)
para no filtrar el test set en el repo público. Para habilitar la
calificación automática real falta copiar `solution.csv` al repo
privado `ml-grading-infra`, que es el que compara las entregas de
`scripts/submit.py` contra este archivo. Ese paso queda fuera del
alcance de esta tarea.
