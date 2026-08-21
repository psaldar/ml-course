# ml-course

Material, notebooks y actividades evaluativas del curso de Machine
Learning. Las actividades se califican automáticamente contra un
[backend serverless](https://github.com/psaldar/ml-grading-infra) (repo
privado, ese sí tiene los datasets de evaluación y no es público).

## Setup

```bash
uv sync                       # instala el entorno (Python 3.12)
cp .env.example .env          # y completa con la API key que te dé el profesor
```

| | |
|---|---|
| **Leaderboard** | https://d3qixogk4zgixq.cloudfront.net |
| **API** | `https://6trg8jthgl.execute-api.us-east-1.amazonaws.com/dev` |

## Estructura

```
modules/            material teórico por módulo/semana
notebooks/           notebooks exploratorios de clase
assignments/
  _template/          plantilla para crear un nuevo assignment
  <slug>/              un assignment concreto: README + starter notebook + public_tests
scripts/
  submit.py            envía tu CSV de predicciones
  check_status.py       consulta tu score / leaderboard
```

## Cómo funcionan las actividades evaluativas

Cada assignment sigue el formato "predicciones sobre holdout privado"
(estilo Kaggle InClass):

1. Recibes un `train.csv` (con labels) y un `test.csv` (sin labels).
2. Entrenas tu propio modelo localmente (notebook de partida en
   `assignments/<slug>/starter_notebook.ipynb`).
3. Generas un CSV de predicciones y lo envías con `scripts/submit.py`.
4. El backend lo compara contra labels privados que nunca ves y te
   devuelve un score + tu posición en el leaderboard.

Ver el README de cada assignment para el detalle de la métrica usada.

## Assignments

| Assignment | Tipo | Métrica | Soportada hoy por ml-grading-infra |
|---|---|---|---|
| [`prediccion-accidentalidad-poblado`](assignments/prediccion-accidentalidad-poblado/) | Clasificación binaria, ~2% positivos, split temporal | `roc_auc` | Sí |
| [`clasificacion-diabetes`](assignments/clasificacion-diabetes/) | Clasificación binaria (Pima Diabetes) | F1-score | Sí |
| [`deteccion-churn`](assignments/deteccion-churn/) | Clasificación binaria (churn telco) | F1-score | Sí |
| [`regresion-abalone`](assignments/regresion-abalone/) | Regresión (edad de abalones) | RMSE | Sí |
| [`recomendador-peliculas`](assignments/recomendador-peliculas/) | Predicción de rating (MovieLens 100k) | RMSE | Sí |
| [`forecasting-demanda-electrica`](assignments/forecasting-demanda-electrica/) | Series de tiempo | WMAPE | **No** — falta agregar la métrica en `ml-grading-infra` |
| [`segmentacion-semillas`](assignments/segmentacion-semillas/) | Clustering (seeds dataset) | Adjusted Rand Index | **No** — falta agregar la métrica en `ml-grading-infra` |

La mayoría sigue el patrón `train.csv` (con target) + `test.csv` (sin
target) en cada carpeta, con `solution.csv` local (gitignored, nunca se
publica). `prediccion-accidentalidad-poblado` es la excepción: los datos
son un SQLite de ~85 MB que se distribuye aparte (no cabe en git).

## Leaderboard

Los rankings se publican en una página web pública (la URL sale del
output `leaderboard_url` de Terraform una vez desplegado
`ml-grading-infra`). Las entregas siempre se hacen desde la terminal con
`scripts/submit.py` — la página es solo de consulta.

## Notebooks de clase

`notebooks/sesion_01` a `sesion_06` — material de las sesiones (regresión,
clasificación y validación, árboles/ensambles/desbalance, series de
tiempo, reducción de dimensionalidad/clustering, sistemas de
recomendación). `sesion_04` y `sesion_06` incluyen datasets propios
(bike sharing, MovieLens 100k).

## Estado actual

Próximos pasos:

- [x] Desplegar `ml-grading-infra` (hecho: ver URLs arriba).
- [ ] Generar las API keys del roster real con
      `ml-grading-infra/scripts/create_student_keys.py` y repartirlas.
- [ ] Mover cada `solution.csv` (6 assignments nuevos) al repo privado
      `ml-grading-infra` una vez esté desplegado — hoy solo existen en
      local, gitignored, nunca se han subido a ningún repo.
- [x] Subir el holdout al bucket privado.
- [x] Servir el dataset desde CloudFront (ver el README del assignment).
- [x] Benchmark del profesor en el leaderboard (ROC-AUC = 0.77393).
- [ ] Agregar las métricas `WMAPE` y `adjusted_rand_index` a
      `ml-grading-infra/src/common/grading.py` (las necesitan
      `forecasting-demanda-electrica` y `segmentacion-semillas`).
