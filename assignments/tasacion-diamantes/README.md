# Reto 1 — Tasación automática de diamantes

**Regresión · 15% de la nota del curso**

---

## El problema

Un marketplace de diamantes certificados recibe cientos de piedras al día
de proveedores que quieren venderlas en la plataforma. Cada una necesita
un precio de referencia antes de publicarse, y un tasador humano no da
abasto para revisarlas todas una por una.

> **Predecir el precio de venta de un diamante certificado, a partir de
> sus características físicas.**

## Los datos

43.035 diamantes con sus características y precio de venta.

**No hace falta descargar nada.** El notebook de partida lee los CSV
directamente desde la URL, y eso funciona igual en Windows, macOS y Linux:

```python
import pandas as pd

CDN = "https://d3qixogk4zgixq.cloudfront.net/data/tasacion-diamantes"
train = pd.read_csv(f"{CDN}/train.csv")
test  = pd.read_csv(f"{CDN}/test.csv")
```

Si los quieren en disco, abran esas URLs en el navegador o usen la terminal:
`curl -O <URL>` en macOS/Linux, `curl.exe -O <URL>` en CMD de Windows, o
`Invoke-WebRequest <URL> -OutFile train.csv` en PowerShell — donde `curl`
es un alias que **no** acepta `-O`.

| Columna | Qué es |
|---|---|
| `id` | Identificador de la fila. Es lo que va en la entrega. |
| `carat` | Quilates (peso) de la piedra |
| `cut` | Calidad del tallado: `Fair` < `Good` < `Very Good` < `Premium` < `Ideal` |
| `color` | Color de la piedra: `J` (peor) … `D` (mejor) |
| `clarity` | Claridad: `I1` (peor) … `IF` (mejor) |
| `depth` | Profundidad total, % del diámetro promedio |
| `table` | Ancho de la mesa superior, % del diámetro promedio |
| `x`, `y`, `z` | Largo, ancho y profundidad en mm |
| `price` | **Variable objetivo**: precio de venta — solo en train |

Es un corte transversal, no una serie de tiempo: **no hay componente
temporal** y la partición train/test es aleatoria. Eso no lo hace un reto
menor — la dificultad está en los datos mismos.

### Dos cosas que van a encontrar

**Medidas físicamente imposibles.** Algunas filas traen `x`, `y` o `z` en
0 — un diamante no puede tener una dimensión de tamaño cero. Es ruido real
de captura de datos, no un error de ustedes ni algo que deban ignorar sin
más: decidan qué hacer con esas filas y documenten por qué.

**Colinealidad entre `carat` y `x`/`y`/`z`.** Miden esencialmente lo
mismo — el tamaño de la piedra — así que van a estar fuertemente
correlacionadas entre sí. Si usan un modelo lineal, tenerlo en cuenta;
si usan árboles, importa menos pero vale la pena entenderlo al leer
importancias de variables.

`cut`, `color` y `clarity` son **ordinales**, no categorías sueltas: hay
un orden real de peor a mejor. Piensen si eso debería reflejarse en cómo
las codifican.

## Formato de la entrega

CSV con columnas `id,price` — una fila por cada `id` de `test.csv` (10.759):

```python
submission = pd.DataFrame({"id": test["id"], "price": predicciones})
submission.to_csv("mi_prediccion.csv", index=False)
```

`price` no puede ser negativo.

## Métrica: RMSE

Raíz del error cuadrático medio, en la misma unidad que `price`. **Más
bajo es mejor.**

| Referencia | RMSE |
|---|---|
| Predecir siempre el precio medio | 3988.24 |
| Regresión lineal solo con `carat` | 1548.20 |
| **Baseline del profesor** | **573.13** |

La segunda fila importa: **una regresión lineal de una sola variable ya
baja el error a la tercera parte** del baseline constante — `carat` por
sí solo explica gran parte del precio. Superarla claramente, no apenas
empatarla, es lo que separa un modelo real de uno perezoso. La brecha
hasta el baseline del profesor sale de tratar bien las categorías
ordinales, la asimetría de `price` y las relaciones no lineales entre
tamaño y precio — no de una variable oculta que se les esté escapando.

## Cómo se califica

### Etapa 1 — Leaderboard (40%)

| Resultado | Puntaje de esta etapa |
|---|---|
| No supera la regresión con `carat` (RMSE ≥ 1548.20) | 0 – 60%, proporcional al score |
| Iguala esa regresión (1548.20) | 60% |
| Entre esa regresión y el baseline del profesor | 60 – 90% (interpolado) |
| Iguala o supera el baseline del profesor (RMSE ≤ 573.13) | 90 – 100% |
| Top-3 del curso | 100% |

Pueden entregar las veces que quieran; cuenta la última.

### Etapa 2 — Notebook (60%)

Un notebook ejecutable de principio a fin, en español, que contenga:

| Sección | Peso | Qué se evalúa |
|---|---|---|
| Exploración y calidad de datos | 10% | Distribución de `price`, correlaciones, detección de las medidas en 0 y qué hicieron con ellas |
| Ingeniería de características | 15% | Codificación de las variables ordinales, manejo de la asimetría de `price`, qué hicieron con la colinealidad `carat`/`x`/`y`/`z` |
| Validación | 10% | Partición de validación bien montada; ausencia de fugas entre su train y su validación |
| Modelado | 15% | Modelos comparados, hiperparámetros, criterio de selección |
| Análisis de errores | 5% | ¿En qué rango de precio falla más? ¿Sub o sobre-estima los diamantes caros? |
| Interpretación y caso de uso | 5% | Qué variables pesan más, limitaciones, cómo se integraría esto en el flujo de tasación real |

## Entrega

Página web (https://d3qixogk4zgixq.cloudfront.net) o terminal:

```bash
uv run scripts/submit.py tasacion-diamantes mi_prediccion.csv
uv run scripts/check_status.py tasacion-diamantes
```

El notebook se entrega por EAFIT Interactiva.
