# clasificacion-diabetes

## Enunciado

Un centro de salud quiere anticipar qué pacientes tienen mayor riesgo de
tener diabetes a partir de indicadores clínicos rutinarios (sin necesidad de
un examen especializado), para priorizar exámenes de seguimiento. Tu tarea es
construir un **clasificador binario** que, a partir de las medidas clínicas
de una paciente, prediga si el resultado de su prueba de diabetes es
`tested_positive` o `tested_negative`.

Los datos corresponden al dataset **Pima Indians Diabetes**, muy usado como
referencia en clasificación binaria. Cada fila es una paciente (mujeres de al
menos 21 años) descrita por 8 variables clínicas:

| Columna | Descripción |
|---|---|
| `preg` | Número de embarazos |
| `plas` | Concentración de glucosa en plasma (test oral de tolerancia a la glucosa, 2 horas) |
| `pres` | Presión arterial diastólica (mm Hg) |
| `skin` | Espesor del pliegue cutáneo del tríceps (mm) |
| `insu` | Insulina sérica a 2 horas (mu U/ml) |
| `mass` | Índice de masa corporal — IMC (kg/m²) |
| `pedi` | Función de pedigrí de diabetes (estima el riesgo genético/familiar) |
| `age` | Edad (años) |
| `class` | **Variable objetivo**: `tested_positive` / `tested_negative` |

Nota: este es un dominio clínico distinto al usado en la clase (riesgo
crediticio) — el objetivo es que apliques los mismos conceptos de
clasificación, sesgo-varianza y validación cruzada sobre datos que no has
visto antes, no que reutilices código de la sesión sin pensarlo.

## Datos

Los datos no están en este repositorio: se descargan una sola vez
desde el almacenamiento del curso.

```bash
curl -O https://d3qixogk4zgixq.cloudfront.net/data/clasificacion-diabetes/train.csv
curl -O https://d3qixogk4zgixq.cloudfront.net/data/clasificacion-diabetes/test.csv
```

- `train.csv`: datos de entrenamiento (614 filas, 80%), con la columna
  objetivo `class`.
- `test.csv`: datos de evaluación (154 filas, 20%), **sin** la columna
  `class`. Debes generar una predicción para cada fila (identificada por
  `id`).

## Qué debes entregar

Un CSV con columnas `id,class` que contenga una predicción (`tested_positive`
o `tested_negative`) para cada fila de `test.csv`. Usa `scripts/submit.py`
desde la raíz del repo para enviarlo:

```bash
uv run scripts/submit.py clasificacion-diabetes ./mi_prediccion.csv
```

## Cómo se califica

Tu entrega se compara automáticamente contra un conjunto de labels privado
que no ves. La métrica usada es **F1-score** (sobre la clase
`tested_positive`).

¿Por qué F1 y no accuracy? Las clases están moderadamente desbalanceadas
(~65% `tested_negative` / ~35% `tested_positive`): un modelo que siempre
prediga `tested_negative` ya tendría cerca de 65% de accuracy sin haber
aprendido nada útil. El F1-score, al combinar precisión y recall de la clase
positiva, penaliza ese tipo de atajo y refleja mejor qué tan bien el modelo
detecta realmente los casos positivos.

Puedes ver tu score y tu posición en el leaderboard con:

```bash
uv run scripts/check_status.py clasificacion-diabetes
```

## Por qué este formato es "AI-proof"

Un chatbot puede generarte código plausible, pero no puede adivinar las
predicciones correctas sobre datos que nunca ha visto. Para obtener un buen
score necesitas efectivamente entrenar, validar y ejecutar un modelo que
generalice — no basta con copiar una respuesta.

---

### Nota para el profesor

`solution.csv` se generó localmente junto con `train.csv`/`test.csv` (split
80/20 estratificado, `random_state=42`) y está excluido de git vía el
`.gitignore` de esta carpeta — **no debe publicarse**. Para habilitar la
calificación automática real, `solution.csv` debe moverse al repo privado
`ml-grading-infra` (fuera del alcance de este repo).
