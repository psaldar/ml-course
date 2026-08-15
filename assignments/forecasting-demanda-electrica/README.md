# forecasting-demanda-electrica

## Enunciado

Una empresa distribuidora de energía necesita **pronosticar la demanda
eléctrica diaria** (en GW) para planear su operación con anticipación:
cuánta energía comprar/generar, cómo programar mantenimientos, etc. Tienes
el historial diario de demanda de un periodo reciente, junto con dos
variables que se conocen de antemano para cualquier día (pasado o futuro):
si es día laboral y la temperatura de ese día.

Tu tarea es construir un modelo que prediga la **demanda eléctrica diaria**
(`demand`) para un bloque de días que va cronológicamente **después** del
periodo de entrenamiento — es decir, un problema real de **pronóstico
(forecasting)**, no de interpolación.

Este es un problema de dominio distinto al que vimos en clase (demanda de
bicicletas por hora), pero la metodología es la misma que vimos en la
Sesión 4: reformular la serie como un problema supervisado construyendo
variables de **rezago (lags)** y **calendario** a partir del historial en
`train.csv`, y evaluar con **WMAPE**.

**Importante — cómo pensar este problema:** `test.csv` es el futuro
respecto a `train.csv`. Como es un ejercicio de práctica, no necesitas
pronosticar la temperatura ni si un día es laboral: esas dos variables ya
te las damos para los días de test tal como vendrían de un pronóstico
meteorológico y de un calendario laboral, ambos conocidos con anticipación.
Lo que sí debes construir tú son las **variables de lags/rolling** de la
demanda: para el primer día de test, el lag de "demanda de ayer" existe en
el histórico de `train.csv`; para días de test más adelante, tendrás que
decidir cómo generar esos lags (ej. usando tus propias predicciones
anteriores de forma recursiva, o usando solamente variables de calendario/
exógenas si prefieres no complicarte con eso). Documenta la decisión que
tomes en tu notebook.

## Datos

- `train.csv`: 292 días de historia (80% inicial de la serie, en orden
  cronológico), con la columna objetivo `demand`.
- `test.csv`: 73 días siguientes (20% final de la serie), **sin** la
  columna objetivo. Debes generar una predicción para cada fila.

Columnas de entrada:

| Columna       | Descripción                                                        |
|---------------|---------------------------------------------------------------------|
| `id`          | identificador secuencial del día (también es el orden temporal)     |
| `date`        | fecha del día (ver supuesto documentado abajo)                      |
| `workday`     | 1 si es día laboral, 0 si es fin de semana o festivo                |
| `temperature` | temperatura promedio del día (°C)                                   |
| `demand`      | demanda eléctrica diaria en GW (solo en `train.csv`) — **objetivo**  |

**Supuesto documentado sobre `date`**: el dataset original (`elecdaily` de
`fpp2`) no trae una columna de fecha explícita, solo un índice secuencial
de 365 observaciones diarias. Para poder construir variables de calendario
(día de la semana, mes, etc.) asumimos un rango de fechas diario
consecutivo iniciando en `2014-01-01` (365 días = un año no bisiesto
completo) — que además coincide con el periodo real que describe el
dataset (demanda eléctrica de Victoria, Australia, durante 2014).

## Qué debes entregar

Un CSV con columnas `id,demand` que contenga una predicción para cada fila
de `test.csv`. Usa `scripts/submit.py` desde la raíz del repo para
enviarlo:

```bash
uv run scripts/submit.py forecasting-demanda-electrica ./mi_prediccion.csv
```

## Cómo se califica

Tu entrega se compara automáticamente contra un conjunto de labels
privado que no ves (`solution.csv`, la demanda real de los 73 días de
test). La métrica usada es **WMAPE** (Weighted Mean Absolute Percentage
Error):

$$\text{WMAPE} = \frac{\sum_t |y_t - \hat{y}_t|}{\sum_t |y_t|}$$

Es decir, la suma de los errores absolutos dividida entre la suma de los
valores reales — pondera el error por la magnitud real de la demanda (a
diferencia del MAPE clásico, que se distorsiona cuando hay valores cercanos
a cero) y es el estándar de la industria en pronóstico de demanda. Un
WMAPE más bajo es mejor. Puedes ver tu score y tu posición en el
leaderboard con:

```bash
uv run scripts/check_status.py forecasting-demanda-electrica
```

## Por qué este formato es "AI-proof"

Un chatbot puede generarte código plausible, pero no puede adivinar las
predicciones correctas sobre datos que nunca ha visto. Para obtener un
buen score necesitas efectivamente construir features de series de tiempo,
entrenar, validar (¡con un split temporal, no aleatorio!) y ejecutar un
modelo que generalice hacia el futuro — no basta con copiar una respuesta.

## Nota para el profesor

`train.csv` / `test.csv` / `solution.csv` se generaron localmente a partir
de `fpp2::elecdaily` (vía Rdatasets), con split temporal 80/20 (292 días de
train, 73 de test, sin aleatoriedad). `solution.csv` (`id` + `demand` real
de los días de test) quedó **gitignored** en esta misma carpeta para no
filtrar el test set en el repo público. Para habilitar la calificación
automática real falta copiar `solution.csv` al repo privado
`ml-grading-infra`, que es el que compara las entregas de
`scripts/submit.py` contra este archivo. Ese paso queda fuera del alcance
de esta tarea.
