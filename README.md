# ml-course

Material, notebooks y actividades evaluativas del curso de Machine
Learning. Las actividades se califican automáticamente contra un
[backend serverless](https://github.com/psaldar/ml-grading-infra) (repo
privado, ese sí tiene los datasets de evaluación y no es público).

## Setup

```bash
uv sync   # instala el entorno (Python 3.12) -- lo necesitas para los
          # notebooks de clase y para entregar por terminal
```

| | |
|---|---|
| **Leaderboard + entregas por la web** | https://d3qixogk4zgixq.cloudfront.net |
| **API** | `https://6trg8jthgl.execute-api.us-east-1.amazonaws.com/dev` |

Ver [Cómo entregar](#cómo-entregar) más abajo — hay dos formas, elige la
que prefieras.

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

1. Recibes un `train.csv` (con labels) y un `test.csv` (sin labels), o el
   SQLite del reto de accidentalidad.
2. Entrenas tu propio modelo localmente (notebook de partida en
   `assignments/<slug>/starter_notebook.ipynb`).
3. Generas un CSV de predicciones y lo envías (dos formas, ver abajo).
4. El backend lo compara contra labels privados que nunca ves y te
   devuelve un score + tu posición en el leaderboard.

Ver el README de cada assignment para el detalle de la métrica usada.

## Cómo entregar

Hay dos formas de enviar tu CSV de predicciones. Son equivalentes —
mismo backend, mismo resultado — así que usa la que te quede más cómoda.
Puedes mezclarlas: entregar hoy por la página y mañana por terminal, no
importa.

### Opción A: página web

**https://d3qixogk4zgixq.cloudfront.net**

1. Pega tu API key en el campo de arriba y da clic en **Entrar**. Queda
   guardada en ese navegador — no hace falta repetir esto cada vez.
2. En "Enviar una entrega": elige el reto, elige tu archivo `.csv`, dale
   a **Enviar**.
3. La tabla "Mis entregas" muestra el estado (`pending` → `graded` o
   `error`) de cada reto al que le hayas entregado — no solo la última.
4. Más abajo, el leaderboard es público: no necesitas la key para verlo.

### Opción B: terminal

```bash
uv sync                       # una sola vez
cp .env.example .env          # una sola vez, con la API key que te dé el profesor

uv run scripts/submit.py <reto> ./mi_prediccion.csv
uv run scripts/check_status.py <reto>              # tu resultado en ese reto
uv run scripts/check_status.py --all               # tus resultados en TODOS los retos
uv run scripts/check_status.py <reto> --leaderboard
```

### Tu identidad es la API key

No hay usuario/contraseña por separado: la API key que te da el profesor
**es** tu identidad frente al backend, tanto en la página como en la
terminal. No la compartas — cualquiera con tu key puede entregar a tu
nombre. Si la pierdes o crees que se filtró, pide una nueva; no hay forma
de recuperar la anterior (se guarda hasheada, ni el profesor puede verla
en texto plano).

## Assignments

| Assignment | Tipo | Métrica | Soportada hoy por ml-grading-infra |
|---|---|---|---|
| [`prediccion-accidentalidad-poblado`](assignments/prediccion-accidentalidad-poblado/) | Clasificación binaria, ~2% positivos, split temporal | `roc_auc` | Sí |
| [`clasificacion-diabetes`](assignments/clasificacion-diabetes/) | Clasificación binaria (Pima Diabetes) | F1-score | Sí |
| [`deteccion-churn`](assignments/deteccion-churn/) | Clasificación binaria (churn telco) | F1-score | Sí |
| [`regresion-abalone`](assignments/regresion-abalone/) | Regresión (edad de abalones) | RMSE | Sí |
| [`recomendador-peliculas`](assignments/recomendador-peliculas/) | Predicción de rating (MovieLens 100k) | RMSE | Sí |
| [`forecasting-demanda-electrica`](assignments/forecasting-demanda-electrica/) | Series de tiempo | WMAPE | Sí |
| [`segmentacion-semillas`](assignments/segmentacion-semillas/) | Clustering (seeds dataset) | Adjusted Rand Index | Sí |

## Los datos

**Este repositorio no contiene datos.** La única fuente es el
almacenamiento del curso, servido por CloudFront. Cada README trae el
comando de descarga de su assignment, y los notebooks de clase bajan sus
datasets solos al ejecutarse.

```
https://d3qixogk4zgixq.cloudfront.net/data/
  <assignment>/train.csv, test.csv                       datos de cada reto
  prediccion-accidentalidad-poblado/*.sqlite3            el SQLite de 85 MB
  sesiones/                                              datasets de las clases 04 y 06
```

Las respuestas viven en un bucket privado aparte al que solo accede la
función que califica.

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
- [x] Respuestas de los 7 retos en el bucket privado de S3.
- [x] Subir el holdout al bucket privado.
- [x] Servir el dataset desde CloudFront (ver el README del assignment).
- [x] Benchmark del profesor en el leaderboard (ROC-AUC = 0.77393).
- [x] Métricas `wmape` y `adjusted_rand_index` implementadas.
- [x] Página web para entregar y ver el leaderboard, con login por API key.
- [x] Autenticación real: `/submissions/me` y la subida exigen `x-api-key`.
- [x] Un estudiante puede tener entregas independientes en varios retos
      (antes una entrega nueva podía borrar el resultado de otro reto).
