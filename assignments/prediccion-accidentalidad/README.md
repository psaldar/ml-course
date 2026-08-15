# Predicción de accidentalidad

Componente de leaderboard automático del taller **"Predicción de
accidentalidad"** (ver el PDF del taller para el enunciado completo:
contexto, EDA, calidad de datos, ingeniería de características, informe,
rúbrica). Este README documenta **solo la parte que se califica
automáticamente**.

## Cómo se relaciona con la nota del taller

El taller se sigue entregando y calificando como está descrito en el PDF
(informe + notebook, rúbrica por criterios). El score de este leaderboard
es el respaldo objetivo de la parte cuantitativa de esa rúbrica:

| Criterio del taller | Peso | Respaldado por el leaderboard |
|---|---|---|
| Manejo del desbalance | 20% | Sí |
| Modelado y validación | 20% | Sí |
| Métricas y selección del modelo final | 10% | Sí |
| EDA y calidad de datos | 15% | No — se sigue calificando por rúbrica |
| Ingeniería de características | 15% | No — se sigue calificando por rúbrica |
| Caso de uso y limitaciones | 10% | No — se sigue calificando por rúbrica |
| Calidad del informe y notebook | 10% | No — se sigue calificando por rúbrica |

## Los datos que reciben NO son exactamente el archivo original

El PDF del taller referencia un único SQLite con las tablas `accidentes`,
`raw_accidentes` y `clima` para 2017-2019 completos. La versión que
reciben para este reto es la **misma base de datos**, con una diferencia:

- `clima`: completa, sin cambios (2017-01-01 a 2019-12-31, las ~320
  combinaciones barrio×hora de cada hora del período).
- `accidentes` y `raw_accidentes`: **solo contienen registros hasta
  2019-09-30 23:00:00**. A partir de esa hora (2019-10-01 en adelante)
  estas dos tablas simplemente no tienen filas — no porque no haya
  ocurrido nada, sino porque esas etiquetas son las que evalúa el
  leaderboard y no pueden estar visibles.

Esto es intencional y es la base de todo el reto: `clima` les da todo lo
necesario para generar features y para saber para qué (barrio, hora) deben
predecir; `accidentes`/`raw_accidentes` les dan la señal de entrenamiento
solo hasta el corte. Aplica el mismo principio que ya explica el PDF del
taller (sección 2.3): "la tabla `accidentes` contiene únicamente las
horas-barrio en que sí hubo accidente [...] para el problema supervisado
debe construir también los casos negativos cruzando con `clima`" — aquí
además hay un corte temporal.

**Dónde conseguir el archivo**: es el mismo canal de siempre (ver el link
de descarga en el PDF del taller / EAFIT interactiva). El archivo pesa
~1.1GB — no vive en este repo de Git.

## Qué deben predecir

Para cada fila de `clima` con `TW >= '2019-10-01 00:00:00'` (son ~658,000
combinaciones barrio×hora, sobre las últimas 13 semanas del período), la
probabilidad de que ocurra al menos un accidente.

```sql
SELECT BARRIO, TW FROM clima WHERE TW >= '2019-10-01 00:00:00';
```

Con eso arman su propio `sample_submission.csv` — no hace falta que se
los demos, sale directo de la consulta anterior.

## Formato de la entrega

CSV con columnas `id,target`:

- `id`: `"{BARRIO}|{TW}"`, exactamente como viene cada fila (ej.
  `aguasfrias|2019-10-01 00:00:00`).
- `target`: un score/probabilidad continuo entre 0 y 1 (**no** una
  etiqueta dura 0/1 — el umbral de decisión final es algo que ustedes
  justifican en el informe, no algo que el leaderboard les exige de
  antemano).

Ver `sample_submission_example.csv` en esta carpeta (5 filas de ejemplo,
solo para mostrar el formato exacto).

```python
predictions["id"] = predictions["BARRIO"] + "|" + predictions["TW"].astype(str)
predictions[["id", "target"]].to_csv("mi_prediccion.csv", index=False)
```

## Métrica: average precision (PR-AUC)

Con ~1.5% de positivos, accuracy no sirve (predecir "no accidente"
siempre ya da >98%). Usamos **average precision** (área bajo la curva
precision-recall): evalúa qué tan bien su score ordena los positivos por
encima de los negativos, sin depender de un umbral. Se calcula sobre el
`target` continuo que entreguen — no hace falta binarizar antes de
enviar.

## Cómo enviar y consultar su score

Desde la raíz de este repo (`ml-course`), con su `.env` configurado (ver
`README.md` principal):

```bash
uv run scripts/submit.py prediccion-accidentalidad ./mi_prediccion.csv
uv run scripts/check_status.py prediccion-accidentalidad
uv run scripts/check_status.py prediccion-accidentalidad --leaderboard
```

## Fuga de información temporal — cuidado

Cualquier variable histórica que calculen (ej. "accidentes promedio en
este barrio en las últimas 4 semanas") debe construirse **solo con
información anterior al momento que están prediciendo**. Esto es más
fácil de violar de lo que parece cuando se calculan agregados sobre todo
el dataset de una vez — el propio PDF del taller lo advierte en la
sección 4.3. El leaderboard no puede detectar fuga de información por sí
solo (nada le impide a un modelo con fuga dar buen score); esa revisión
sigue siendo parte de la calificación cualitativa del informe/notebook.
