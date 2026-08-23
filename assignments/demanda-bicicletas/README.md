# Reto 2 — Demanda horaria de bicicletas compartidas

**Regresión con corte temporal · 15% de la nota del curso**

---

## El problema

Un sistema de bicicletas compartidas necesita saber **cuántas bicicletas
van a necesitarse en cada hora** de los próximos meses. De eso dependen
decisiones concretas y costosas: cuántas unidades mantener en circulación,
cómo programar el mantenimiento, cuándo reforzar la redistribución entre
estaciones, cuánto personal asignar.

Subestimar la demanda deja usuarios sin servicio. Sobreestimarla inmoviliza
capital en bicicletas que nadie usa. El operador quiere una predicción
horaria para el último trimestre del año.

> **Predecir el número de bicicletas alquiladas en una hora determinada.**

## Los datos

Dos años de operación con registro horario.

**No hace falta descargar nada.** El notebook de partida lee los CSV
directamente desde la URL, y eso funciona igual en Windows, macOS y Linux:

```python
import pandas as pd

CDN = "https://d3qixogk4zgixq.cloudfront.net/data/demanda-bicicletas"
train = pd.read_csv(f"{CDN}/train.csv")
test  = pd.read_csv(f"{CDN}/test.csv")
```

Si los quieren en disco, abran esas URLs en el navegador o usen la terminal:
`curl -O <URL>` en macOS/Linux, `curl.exe -O <URL>` en CMD de Windows, o
`Invoke-WebRequest <URL> -OutFile train.csv` en PowerShell — donde `curl`
es un alias que **no** acepta `-O`.

| Columna | Qué es |
|---|---|
| `id` | Identificador de la hora. Es lo que va en la entrega. |
| `dteday` | Fecha |
| `hr` | Hora del día (0–23) |
| `holiday` | Si el día es festivo |
| `weathersit` | Situación climática (1 despejado … 4 tormenta) |
| `temp`, `atemp` | Temperatura y sensación térmica (normalizadas) |
| `hum`, `windspeed` | Humedad y viento (normalizados) |
| `casual`, `registered` | Alquileres por tipo de usuario — **solo en train** |
| `cnt` | **Variable objetivo**: alquileres totales en esa hora — solo en train |

Eso es todo lo que hay: fecha, hora, clima y si el día es festivo. Cualquier
otra variable de calendario que su modelo necesite —estación, mes, día de la
semana, si es día laboral— la construyen ustedes a partir de `dteday`.

### El corte temporal

```
2011-01-01                                2012-10-01              2012-12-31
    |─────────── ENTRENAMIENTO ───────────────|──── EVALUACIÓN ────|
         15.211 horas con cnt conocido         2.168 horas a predecir
```

No es una partición aleatoria: se entrena con el pasado y se predice el
futuro. Y no es un detalle menor — en el período de evaluación la demanda
**cae** por la estacionalidad de otoño-invierno, mientras que los últimos
meses de entrenamiento son los más altos del histórico. Un modelo que
simplemente extienda el nivel reciente se va a equivocar sistemáticamente.

## La regla

**Toda variable debe poder calcularse en el momento de predecir.**

Comparen columna por columna qué trae `train.csv` y qué trae `test.csv`, y
pregúntense para cada variable si estaría disponible al predecir una hora de
noviembre de 2012. Si una variable les da un desempeño excelente en
validación pero no pueden calcularla sobre `test.csv`, ese modelo no sirve
por bueno que parezca.

Documenten en el notebook qué variables descartaron por esta razón.

## Formato de la entrega

CSV con columnas `id,cnt` — una fila por cada `id` de `test.csv` (2.168):

```python
submission = pd.DataFrame({"id": test["id"], "cnt": predicciones})
submission.to_csv("mi_prediccion.csv", index=False)
```

`cnt` es un conteo: no puede ser negativo.

## Métrica: RMSE

Raíz del error cuadrático medio, en bicicletas. **Más bajo es mejor.** Al
elevar el error al cuadrado, penaliza fuerte los errores grandes — que es
justo lo que le importa al operador: fallar por 200 bicicletas en la hora
pico cuesta mucho más que fallar por 5 a las 3 a.m.

| Referencia | RMSE |
|---|---|
| Predecir siempre la media histórica | 204.43 |
| Media por hora × fin de semana (un `groupby`) | 121.21 |
| **Baseline del profesor** | **82.43** |

La segunda fila importa: **tres líneas de `pandas` llegan a 121**. Superar
"predecir la media" no demuestra nada. Construyan ese baseline trivial
ustedes mismos el primer día y midan todo contra él.

## Cómo se califica

### Etapa 1 — Leaderboard (40%)

| Resultado | Puntaje de esta etapa |
|---|---|
| No supera el baseline trivial (RMSE ≥ 121.21) | 0 – 50% |
| Supera el baseline trivial | 60% |
| Entre el trivial y el del profesor | 60 – 90% (interpolado) |
| Supera el baseline del profesor (RMSE < 82.43) | 90 – 100% |
| Top-3 del curso | 100% |

Pueden entregar las veces que quieran; cuenta la última.

### Etapa 2 — Notebook (60%)

Un notebook ejecutable de principio a fin, en español, que contenga:

| Sección | Peso | Qué se evalúa |
|---|---|---|
| Exploración y calidad de datos | 10% | Estacionalidades encontradas (diaria, semanal, anual), efecto del clima, valores atípicos |
| Ingeniería de características | 15% | Qué construyeron desde `dteday` y por qué; codificación cíclica; justificación |
| Validación | 15% | Por qué una partición aleatoria sería un error aquí; cómo montaron la validación temporal |
| Modelado | 10% | Modelos comparados, hiperparámetros, criterio de selección |
| **Análisis de errores** | 10% | ¿En qué horas/días falla más? ¿Sub o sobre-estima? ¿Por qué? |
| Interpretación y caso de uso | 10% | Qué variables pesan, qué haría el operador con esto, limitaciones honestas |

**Lo que más pesa no es el score, es el razonamiento.** Un notebook que
explique con claridad por qué un modelo fracasó vale más que uno que
reporte un buen número sin entender de dónde salió.

## Entrega

Página web (https://d3qixogk4zgixq.cloudfront.net) o terminal:

```bash
uv run scripts/submit.py demanda-bicicletas mi_prediccion.csv
uv run scripts/check_status.py demanda-bicicletas
```

El notebook se entrega por EAFIT Interactiva.
