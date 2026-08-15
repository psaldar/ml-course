# regresion-abalone

## Enunciado

En biología pesquera, estimar la edad de un abalón (un molusco marino)
es un proceso costoso: hay que cortar la concha, teñirla y contar los
anillos bajo microscopio, de forma parecida a contar los anillos de un
árbol. El número de anillos se relaciona con la edad del abalón
(edad ≈ anillos + 1.5 años).

Tu tarea es construir un modelo de **regresión** que prediga el número
de anillos (`Rings`) de un abalón a partir de medidas físicas fáciles y
baratas de tomar: sexo, largo, diámetro, altura y distintos pesos
(entero, de la carne, de las vísceras y de la concha). Si el modelo
funciona bien, se puede evitar el proceso manual de conteo.

Este es un problema de dominio distinto al que vimos en clase (precios
de vivienda), pero la metodología es la misma: exploración, limpieza,
selección de variables, entrenamiento, validación y evaluación con
métricas de regresión.

## Datos

- `train.csv`: datos de entrenamiento (con la columna objetivo `Rings`).
- `test.csv`: datos de evaluación, **sin** la columna objetivo. Debes
  generar predicciones para cada fila.

Columnas de entrada:

| Columna          | Descripción                                    |
|------------------|-------------------------------------------------|
| `id`             | identificador de la fila                        |
| `Sex`            | `M` (macho), `F` (hembra), `I` (inmaduro)       |
| `Length`         | largo de la concha (mm)                         |
| `Diameter`       | diámetro de la concha (mm)                      |
| `Height`         | altura de la concha (mm)                        |
| `Whole_weight`   | peso total del abalón (g)                       |
| `Shucked_weight` | peso de la carne (g)                            |
| `Viscera_weight` | peso de las vísceras (g)                        |
| `Shell_weight`   | peso de la concha seca (g)                      |
| `Rings`          | número de anillos (solo en `train.csv`) — **objetivo** |

## Qué debes entregar

Un CSV con columnas `id,Rings` que contenga una predicción para cada
fila de `test.csv`. Usa `scripts/submit.py` desde la raíz del repo para
enviarlo:

```bash
uv run scripts/submit.py regresion-abalone ./mi_prediccion.csv
```

## Cómo se califica

Tu entrega se compara automáticamente contra un conjunto de labels
privado que no ves. La métrica usada es: **RMSE** (raíz del error
cuadrático medio) entre tu predicción y el número real de anillos. Un
RMSE más bajo es mejor. Puedes ver tu score y tu posición en el
leaderboard con:

```bash
uv run scripts/check_status.py regresion-abalone
```

## Por qué este formato es "AI-proof"

Un chatbot puede generarte código plausible, pero no puede adivinar las
predicciones correctas sobre datos que nunca ha visto. Para obtener un
buen score necesitas efectivamente entrenar, validar y ejecutar un modelo
que generalice — no basta con copiar una respuesta.

## Nota para el profesor

`solution.csv` se generó localmente a partir de
`sklearn.datasets.fetch_openml('abalone')` (split 80/20,
`random_state=42`) y quedó **gitignored** en esta misma carpeta para no
filtrar el test set en el repo público. Para habilitar la calificación
automática real falta copiar `solution.csv` (par `id,Rings` del 20% de
test) al repo privado `ml-grading-infra`, que es el que compara las
entregas de `scripts/submit.py` contra este archivo. Ese paso queda
fuera del alcance de esta tarea.
