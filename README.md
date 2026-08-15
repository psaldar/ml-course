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

## Estado actual

Repo recién creado — esqueleto inicial. Próximos pasos:

- [ ] Desplegar `ml-grading-infra` y poner la URL real en `.env.example` /
      comunicarla a los estudiantes.
- [ ] Definir el primer módulo y su assignment.
- [ ] Generar API keys del roster con
      `ml-grading-infra/scripts/create_student_keys.py`.
