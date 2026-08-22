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
  <slug>/              un reto: README con el enunciado + notebook de partida
scripts/
  submit.py            envía tu CSV de predicciones
  check_status.py       consulta tu score / leaderboard
```

## Cómo funcionan los retos

Cada reto sigue el formato "predicciones sobre holdout privado" (estilo
Kaggle InClass):

1. Descargas los datos (train con la variable objetivo, test sin ella).
2. Entrenas tu modelo localmente.
3. Generas un CSV de predicciones y lo envías (dos formas, ver abajo).
4. El backend lo compara contra respuestas que nunca ves y te devuelve un
   score + tu posición en el leaderboard.

Ver el README de cada reto para el enunciado, la métrica y la rúbrica.

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

## Los 3 retos

Los retos son la **nota de seguimiento del curso: 45% en total**, 15% cada
uno. Uno por fin de semana.

| # | Reto | Tipo | Métrica | Peso |
|---|---|---|---|---|
| 1 | [Predicción de accidentalidad](assignments/prediccion-accidentalidad-poblado/) | Clasificación desbalanceada (~2% positivos), datos en SQLite | `roc_auc` | 15% |
| 2 | [Demanda de bicicletas](assignments/demanda-bicicletas/) | Regresión con corte temporal, 17k horas | `rmse` | 15% |
| 3 | [Recomendador de películas](assignments/recomendador-peliculas/) | Filtrado colaborativo, corte temporal por usuario | `rmse` | 15% |

### Cada reto tiene dos etapas

**Etapa 1 — Leaderboard (40% del reto).** Suben su CSV de predicciones y el
sistema lo califica solo contra un conjunto de respuestas que nunca ven. La
nota sale de umbrales absolutos, no de la posición relativa: superar el
baseline trivial da 60%, superar el baseline del profesor da 90%+, el top-3
da 100%. Pueden entregar las veces que quieran.

**Etapa 2 — Notebook (60% del reto).** Un notebook ejecutable y documentado
en español con el análisis completo: exploración, decisiones de modelado,
validación, análisis de errores e interpretación. **Pesa más que el score**
— un buen número sin entender de dónde salió no alcanza. El README de cada
reto trae la rúbrica detallada.

Los tres retos entregan datos **crudos** (sin variables pre-calculadas, con
sus inconsistencias) y usan **corte temporal**, no particiones aleatorias.

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

Todo desplegado y probado de punta a punta. Los 17 estudiantes del roster
2026-1 tienen su API key generada.

Pendiente: repartir las API keys a cada estudiante.
