# Reto 3 — Sistema de recomendación de películas

**Filtrado colaborativo · 15% de la nota del curso**

---

## El problema

Una plataforma de streaming quiere anticipar **qué calificación le daría un
usuario a una película que todavía no ha visto**. Con eso decide qué
recomendar en la portada de cada persona: si el modelo acierta, el usuario
encuentra qué ver y se queda; si falla, recomienda ruido y el usuario se va.

> **Predecir la calificación (1 a 5) que un usuario le dará a una película.**

## Los datos

100.000 calificaciones reales de 943 usuarios sobre 1.682 películas
(MovieLens). Descarga:

```bash
curl -O https://d3qixogk4zgixq.cloudfront.net/data/recomendador-peliculas/train.csv
curl -O https://d3qixogk4zgixq.cloudfront.net/data/recomendador-peliculas/test.csv
curl -O https://d3qixogk4zgixq.cloudfront.net/data/recomendador-peliculas/movies.csv
```

| Archivo | Contenido |
|---|---|
| `train.csv` | 79.619 calificaciones: `id`, `user_id`, `item_id`, `rating`, `timestamp` |
| `test.csv` | 20.381 pares (usuario, película) **sin** `rating` — es lo que deben predecir |
| `movies.csv` | Metadatos de las 1.682 películas: título, fecha de estreno, 19 géneros |

### El corte es temporal, por usuario

De cada usuario se reservó su **20% de calificaciones más reciente**. Es el
protocolo estándar en sistemas de recomendación, y tiene una consecuencia
directa:

> Para predecir lo que un usuario calificó en marzo, solo pueden usar lo que
> ese usuario calificó **antes**. Nunca después.

Esto importa más de lo que parece. Con una partición aleatoria —la que
usamos en clase— el modelo puede mirar calificaciones *posteriores* del
mismo usuario para predecir una anterior. Eso infla artificialmente el
desempeño y es imposible en operación: nadie conoce el futuro de sus
usuarios. Por eso el reto no es el mismo problema de la sesión 06 con otros
datos: **es más difícil, y su modelo de clase probablemente no transfiera
directamente.**

### Cold-start de películas

69 películas del período de evaluación **nunca aparecen en `train.csv`**
(86 filas, 0.4%). El filtrado colaborativo puro no tiene nada que decir
sobre ellas: no hay historial. Para eso les damos `movies.csv` — género y
año de estreno permiten un enfoque de contenido. Es poco volumen, pero
decidir qué hacer con esos casos (y justificarlo) es parte del trabajo.

## Formato de la entrega

CSV con columnas `id,rating` — una fila por cada `id` de `test.csv` (20.381):

```python
submission = pd.DataFrame({"id": test["id"], "rating": predicciones})
submission.to_csv("mi_prediccion.csv", index=False)
```

`rating` es continuo: **no lo redondeen a enteros.** Predecir 3.7 cuando la
calificación real es 4 da menos error que predecir 4 y equivocarse en otros
casos. El redondeo solo destruye información.

## Métrica: RMSE

Raíz del error cuadrático medio sobre la calificación. **Más bajo es mejor.**

| Referencia | RMSE |
|---|---|
| Predecir siempre la media global | 1.2079 |
| Media + sesgo de usuario + sesgo de película | 1.0139 |
| **Baseline del profesor** (factorización de matrices) | **0.9683** |

Presten atención a la segunda fila. El **modelo de sesgos** —"a este usuario
le gusta calificar alto, esta película gusta más que el promedio"— es
aritmética simple y ya llega a 1.01. Es un baseline notoriamente fuerte: en
la literatura, muchos sistemas elaborados no lo superan. Constrúyanlo
primero.

## Cómo se califica

### Etapa 1 — Leaderboard (40%)

| Resultado | Puntaje de esta etapa |
|---|---|
| No supera la media global (RMSE ≥ 1.2079) | 0 – 50% |
| Supera la media global | 60% |
| Entre la media global y el baseline del profesor | 60 – 90% (interpolado) |
| Supera el baseline del profesor (RMSE < 0.9683) | 90 – 100% |
| Top-3 del curso | 100% |

Pueden entregar las veces que quieran; cuenta la última.

### Etapa 2 — Notebook (60%)

Un notebook ejecutable de principio a fin, en español, que contenga:

| Sección | Peso | Qué se evalúa |
|---|---|---|
| Exploración | 10% | Distribución de calificaciones, dispersión de la matriz, usuarios/películas más activos, sesgos observados |
| Baseline de sesgos | 10% | Implementado y medido antes de cualquier modelo complejo |
| Modelo(s) de recomendación | 15% | Al menos dos enfoques (vecindario, factorización, híbrido), comparados con criterio |
| Validación | 10% | Cómo montaron el corte temporal por usuario dentro de train; por qué no sirve una partición aleatoria |
| **Cold-start** | 10% | Qué hicieron con las películas sin historial y por qué |
| Interpretación y caso de uso | 5% | Qué recomendaría el sistema, limitaciones, qué falta para producción |

## Entrega

Página web (https://d3qixogk4zgixq.cloudfront.net) o terminal:

```bash
uv run scripts/submit.py recomendador-peliculas ./mi_prediccion.csv
uv run scripts/check_status.py recomendador-peliculas
```

El notebook se entrega por EAFIT Interactiva.
