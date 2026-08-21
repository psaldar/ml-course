# Predicción de accidentalidad — El Poblado

Competencia con leaderboard automático, asociada al taller **"Predicción
de accidentalidad"** (ver el PDF del taller para el enunciado completo:
contexto, EDA, calidad de datos, ingeniería de características, informe y
rúbrica). Este README cubre **solo la parte que se califica
automáticamente**.

## El problema

> ¿Cuál es la probabilidad de que ocurra al menos un accidente de tránsito
> en el barrio *B* a la hora *h*?

Ámbito: los **22 barrios de El Poblado**, Medellín. Cada fila del problema
es una pareja (barrio, hora). La mayoría de esas parejas no registra
accidentes — alrededor del **2%** sí. El desbalance es el corazón del
reto.

## Los datos

Un SQLite (~85 MB) con tres tablas:

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

## Métrica: average precision (PR-AUC)

Con ~2% de positivos, la accuracy no sirve: predecir "nunca hay
accidente" ya acierta el 98% de las veces sin haber aprendido nada. Usamos
**average precision** (área bajo la curva precision-recall), que mide qué
tan bien su score ordena los positivos por encima de los negativos, sin
depender de un umbral.

Referencias para ubicarse:

| Modelo | AP en el período de evaluación |
|---|---|
| Aleatorio (= tasa de positivos) | 0.0201 |
| **Baseline del profesor** | **0.0598** |

El baseline del profesor se entrenó únicamente con los mismos datos que
ustedes reciben. Superarlo es un objetivo razonable y alcanzable; no es
un techo.

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

## Relación con la nota del taller

El taller se entrega y califica como dice el PDF (informe + notebook,
rúbrica por criterios). Este leaderboard es el respaldo objetivo de la
parte cuantitativa:

| Criterio del taller | Peso | ¿Respaldado por el leaderboard? |
|---|---|---|
| Manejo del desbalance | 20% | Sí |
| Modelado y validación | 20% | Sí |
| Métricas y selección del modelo final | 10% | Sí |
| EDA y calidad de datos | 15% | No — rúbrica |
| Ingeniería de características | 15% | No — rúbrica |
| Caso de uso y limitaciones | 10% | No — rúbrica |
| Calidad del informe y del notebook | 10% | No — rúbrica |

## Por qué este formato es resistente a la IA

Un asistente de IA puede escribirles código plausible, pero no puede
adivinar qué parejas (barrio, hora) tuvieron accidente en un período que
nunca ha visto. Para subir en el leaderboard hay que entrenar, validar y
ejecutar de verdad un modelo que generalice.
