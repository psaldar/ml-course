# Reto 1 — Predicción de accidentalidad vial

**Clasificación con clases desbalanceadas · 15% de la nota del curso**

---

## El problema

La Secretaría de Movilidad tiene agentes de tránsito limitados y necesita
decidir **dónde y a qué hora ubicarlos**. No puede cubrir los 22 barrios de
El Poblado las 24 horas: tiene que priorizar. Un modelo que anticipe dónde
es más probable un accidente permite pasar de reaccionar a prevenir.

> **Estimar la probabilidad de que ocurra al menos un accidente de tránsito
> en el barrio B a la hora h.**

Cada fila del problema es una pareja (barrio, hora). La mayoría no registra
accidentes — alrededor del **2%** sí. Ese desbalance es el corazón del reto:
un modelo que siempre diga "no habrá accidente" acierta el 98% de las veces
y es completamente inútil.

## Los datos

Descarga (~85 MB):

```bash
curl -O https://d3qixogk4zgixq.cloudfront.net/data/prediccion-accidentalidad-poblado/data_accidentes_poblado.sqlite3
```

Un SQLite con tres tablas:

| Tabla | Contenido |
|---|---|
| `clima` | Una fila por (barrio, hora) para **todo** 2017-2019. Variables meteorológicas. Es el universo de parejas a considerar. |
| `accidentes` | Parejas (barrio, hora) donde **sí** hubo al menos un accidente. |
| `raw_accidentes` | Detalle de cada accidente (clase, gravedad, diseño vial, coordenadas, dirección). |

Los datos vienen **crudos a propósito**. No hay variables de calendario
pre-calculadas, ni agregados, ni codificaciones: si quieren hora del día,
día de la semana, mes, festivo o cualquier otra cosa derivada de `TW`,
las construyen ustedes. Eso es justamente lo que evalúan las secciones
4.2 y 4.3 del taller.

Tampoco están limpios. Hay formatos inconsistentes, faltantes y al menos
una inconsistencia entre tablas. Encontrarlos y decidir qué hacer con
ellos es parte del trabajo, no un accidente del enunciado.

**Importante — el corte temporal.** `clima` cubre el período completo,
pero `accidentes` y `raw_accidentes` **solo llegan hasta el 2019-07-31**.
De ahí en adelante esas tablas no tienen filas: no porque no haya pasado
nada, sino porque esas etiquetas son las que evalúa el leaderboard.

```
2017-01-01                              2019-08-01        2019-12-30
    |------------ ENTRENAMIENTO ------------|--- EVALUACIÓN ---|
    clima: sí          accidentes: sí       | clima: sí
                                            | accidentes: OCULTOS
```

Como el propio taller explica (sección 2.3), `accidentes` solo trae los
positivos: los casos negativos los construyen ustedes cruzando contra
`clima`, que sí cubre todas las combinaciones.

## Qué deben predecir

Para cada fila de `clima` en el período de evaluación:

```sql
SELECT BARRIO, TW FROM clima
WHERE TW >= '2019-08-01 00:00:00' AND TW < '2019-12-31 00:00:00';
```

Son **80.256** parejas (barrio, hora). Con esa consulta arman su propio
archivo de predicciones — no necesitan que les demos un
`sample_submission`.

## Formato de la entrega

CSV con columnas `id,target`:

- `id`: `"{BARRIO}|{TW}"` exactamente como sale de la consulta
  (ej. `manila|2019-08-01 07:00:00`).
- `target`: probabilidad continua entre 0 y 1. **No** una etiqueta dura
  0/1 — la elección del umbral es parte de su análisis en el informe, no
  algo que el leaderboard les exija de antemano.

```python
submission = pd.DataFrame({
    "id": test["BARRIO"] + "|" + test["TW"].dt.strftime("%Y-%m-%d %H:%M:%S"),
    "target": modelo.predict_proba(X_test)[:, 1],
})
submission.to_csv("mi_prediccion.csv", index=False)
```

## Métrica: ROC-AUC

Con ~2% de positivos, la accuracy no sirve: predecir "nunca hay
accidente" ya acierta el 98% de las veces sin haber aprendido nada. El
leaderboard usa **ROC-AUC** (`sklearn.metrics.roc_auc_score`), que mide
qué tan bien su score ordena los positivos por encima de los negativos,
sin depender de un umbral. Por eso deben entregar una probabilidad
continua y no una etiqueta 0/1.

Referencias para ubicarse:

| Modelo | ROC-AUC en el período de evaluación |
|---|---|
| Aleatorio | 0.5000 |
| Tasa histórica por barrio × hora | 0.7589 |
| **Baseline del profesor** | **0.7739** |

El baseline del profesor se entrenó únicamente con los mismos datos que
ustedes reciben. Superarlo es un objetivo razonable y alcanzable; no es
un techo.

Fíjense en la segunda fila: **un `groupby` de tres líneas ya llega a
0.7589**. No basta con entrenar un modelo grande y reportar que superó al
azar — la vara real es lo que aporta su modelo *por encima* de un
promedio histórico. Construyan ese baseline trivial ustedes mismos y
midan contra él: si su modelo sofisticado no lo mejora, descubrirlo
temprano vale más que descubrirlo el día de la entrega.

### Ojo: el ROC-AUC no lo es todo

El ROC-AUC es la métrica del ranking, pero **no es suficiente para el
informe**. Con clases muy desbalanceadas tiende a verse optimista, porque
premia ordenar bien los negativos, que son el 98% de los datos y no le
interesan a nadie que quiera enviar patrullas. Un modelo con ROC-AUC de
0.77 puede tener una precisión bajísima en el umbral que ustedes elijan.

Para las secciones 4.5 y 4.7 del taller reporten además **precision,
recall, la curva precision-recall y la matriz de confusión** en el umbral
que propongan, y justifiquen ese umbral con el costo de cada tipo de
error. Discutir la diferencia entre lo que dice el ROC-AUC y lo que dice
la curva precision-recall en este problema es exactamente el tipo de
análisis que se evalúa.

## La regla que deben respetar

**Toda variable debe ser calculable en el momento de la predicción, con
información que realmente estaría disponible en ese momento.**

Esa sola frase tiene una consecuencia fuerte en este problema. Piensen
con cuidado qué información tienen —y cuál no— para una fila del período
de evaluación, tabla por tabla. Si una variable que les funciona muy bien
en entrenamiento resulta imposible de calcular para diciembre de 2019,
eso les está diciendo algo.

El leaderboard **no puede detectar la fuga de información por sí solo**:
un modelo con fuga puede dar buen score. Pero la revisión del notebook y
del informe sí, y ahí se penaliza. El taller lo advierte en la sección
4.3: *"toda variable histórica debe calcularse únicamente con información
disponible antes del momento de predicción"*.

Documenten en el informe cómo resolvieron esto. Es uno de los puntos más
interesantes del problema.

## Cómo enviar y consultar su score

Desde la raíz de este repo, con su `.env` configurado (ver el README
principal):

```bash
uv run scripts/submit.py prediccion-accidentalidad-poblado ./mi_prediccion.csv
uv run scripts/check_status.py prediccion-accidentalidad-poblado
```

El leaderboard público se consulta en la página web del curso (ver el
README principal) o desde la terminal:

```bash
uv run scripts/check_status.py prediccion-accidentalidad-poblado --leaderboard
```

## Cómo se califica

### Etapa 1 — Leaderboard (40%)

| Resultado | Puntaje de esta etapa |
|---|---|
| No supera la tasa histórica (ROC-AUC ≤ 0.7589) | 0 – 50% |
| Supera la tasa histórica | 60% |
| Entre la tasa histórica y el baseline del profesor | 60 – 90% (interpolado) |
| Supera el baseline del profesor (ROC-AUC > 0.7739) | 90 – 100% |
| Top-3 del curso | 100% |

Pueden entregar las veces que quieran; cuenta la última.

### Etapa 2 — Notebook (60%)

Un notebook ejecutable de principio a fin, en español, que contenga:

| Sección | Peso | Qué se evalúa |
|---|---|---|
| Exploración y calidad de datos | 15% | Distribución temporal y espacial, clima, y qué hicieron con los faltantes y las inconsistencias entre tablas |
| Construcción del target y unión de tablas | 10% | Cómo definieron la unidad de análisis y construyeron los casos negativos |
| Ingeniería de características | 10% | Qué variables crearon y por qué; codificación de cíclicas y categóricas |
| **Manejo del desbalance** | 10% | Estrategias probadas y comparadas; ajuste del umbral de decisión |
| Validación | 5% | Partición temporal; por qué una aleatoria sería un error |
| Métricas más allá del ROC-AUC | 5% | Precision, recall, curva PR y matriz de confusión en el umbral elegido |
| Caso de uso y limitaciones | 5% | Cómo se usaría en operación (turnos, mapa de calor), sesgos y límites |

El PDF del taller amplía el contexto y el detalle de cada sección.

## Por qué este formato es resistente a la IA

Un asistente de IA puede escribirles código plausible, pero no puede
adivinar qué parejas (barrio, hora) tuvieron accidente en un período que
nunca ha visto. Para subir en el leaderboard hay que entrenar, validar y
ejecutar de verdad un modelo que generalice.
