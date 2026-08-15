# <nombre-del-assignment>

## Enunciado

<Descripción del problema, contexto de negocio/dominio, qué se espera que
el estudiante construya.>

## Datos

- `train.csv`: datos de entrenamiento (con la columna objetivo).
- `test.csv`: datos de evaluación, **sin** la columna objetivo. Debes
  generar predicciones para cada fila.

## Qué debes entregar

Un CSV con columnas `id,<target_col>` que contenga una predicción para
cada fila de `test.csv`. Usa `scripts/submit.py` desde la raíz del repo
para enviarlo:

```bash
uv run scripts/submit.py <slug-del-assignment> ./mi_prediccion.csv
```

## Cómo se califica

Tu entrega se compara automáticamente contra un conjunto de labels
privado que no ves. La métrica usada es: `<accuracy | f1 | rmse | mae>`.
Puedes ver tu score y tu posición en el leaderboard con:

```bash
uv run scripts/check_status.py <slug-del-assignment>
```

## Por qué este formato es "AI-proof"

Un chatbot puede generarte código plausible, pero no puede adivinar las
predicciones correctas sobre datos que nunca ha visto. Para obtener un
buen score necesitas efectivamente entrenar, validar y ejecutar un modelo
que generalice — no basta con copiar una respuesta.
