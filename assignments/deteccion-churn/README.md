# deteccion-churn

## Enunciado

Una compañía de telecomunicaciones quiere anticipar qué clientes están en
riesgo de **fuga (churn)**, es decir, de cancelar su servicio, para poder
ofrecerles retención (descuentos, mejoras de plan, atención proactiva) antes
de que se vayan. Contactar a un cliente que no iba a irse tiene un costo
bajo (una llamada, una oferta), pero no detectar a un cliente que sí se va
a ir significa perder ese ingreso por completo. Como en la mayoría de
problemas de churn, los clientes que cancelan son una **minoría**: la
mayoría de los clientes se queda.

Tu tarea es construir un modelo de **clasificación binaria** que prediga si
un cliente va a cancelar el servicio (`class = 1`) o no (`class = 0`), a
partir de su plan de servicio (plan internacional, buzón de voz) y su
patrón de consumo (minutos, llamadas y cargos en el día, la tarde, la noche
y llamadas internacionales), junto con el número de llamadas que ha hecho a
servicio al cliente (una señal típica de insatisfacción).

Este es un problema de dominio distinto al que vimos en clase (fraude en
tarjetas de crédito), pero la metodología es la misma: es un problema de
clasificación con **desbalance de clases**, así que las técnicas de la
Sesión 3 (árboles, ensambles, balanceo, métricas apropiadas para
desbalance) aplican directamente.

## Datos

- `train.csv`: datos de entrenamiento (con la columna objetivo `class`).
- `test.csv`: datos de evaluación, **sin** la columna objetivo. Debes
  generar predicciones para cada fila.

Columnas de entrada (además de `id`):

| Columna                          | Descripción                                              |
|-----------------------------------|-----------------------------------------------------------|
| `state`                           | código numérico del estado/región del cliente             |
| `account_length`                  | antigüedad de la cuenta (días)                             |
| `area_code`                       | código de área telefónico                                  |
| `phone_number`                    | identificador interno de la línea (no es predictivo per se) |
| `international_plan`              | si el cliente tiene plan internacional (`0`/`1`)           |
| `voice_mail_plan`                 | si el cliente tiene plan de buzón de voz (`0`/`1`)         |
| `number_vmail_messages`           | número de mensajes de voz                                  |
| `total_day_minutes`               | minutos consumidos en el día                               |
| `total_day_calls`                 | número de llamadas en el día                               |
| `total_day_charge`                | cargo monetario asociado al consumo diurno                 |
| `total_eve_minutes`               | minutos consumidos en la tarde                             |
| `total_eve_calls`                 | número de llamadas en la tarde                              |
| `total_eve_charge`                | cargo monetario asociado al consumo vespertino              |
| `total_night_minutes`             | minutos consumidos en la noche                              |
| `total_night_calls`               | número de llamadas en la noche                              |
| `total_night_charge`              | cargo monetario asociado al consumo nocturno                 |
| `total_intl_minutes`              | minutos de llamadas internacionales                        |
| `total_intl_calls`                | número de llamadas internacionales                          |
| `total_intl_charge`               | cargo monetario asociado a llamadas internacionales          |
| `number_customer_service_calls`   | número de llamadas a servicio al cliente                     |
| `class`                           | `1` = el cliente canceló el servicio (churn), `0` = se quedó — **solo en `train.csv`, es el objetivo** |

> Nota: `phone_number` y `state` son en la práctica identificadores/códigos
> internos; parte del ejercicio es decidir qué variables realmente aportan
> señal predictiva y cuáles no.

## Qué debes entregar

Un CSV con columnas `id,class` que contenga una predicción (`0` o `1`) para
cada fila de `test.csv`. Usa `scripts/submit.py` desde la raíz del repo para
enviarlo:

```bash
uv run scripts/submit.py deteccion-churn ./mi_prediccion.csv
```

## Cómo se califica

Tu entrega se compara automáticamente contra un conjunto de labels privado
que no ves. La métrica usada es: **F1-score** sobre la clase positiva
(`class = 1`, cliente que cancela). Se usa F1 (media armónica de precision y
recall) en lugar de accuracy porque el dataset está desbalanceado (~14% de
clientes cancelan): un modelo que siempre prediga "no cancela" ya tendría
una accuracy alta pero sería inútil para el negocio, exactamente el mismo
problema que discutimos en la Sesión 3 con el dataset de fraude. Puedes ver
tu score y tu posición en el leaderboard con:

```bash
uv run scripts/check_status.py deteccion-churn
```

## Por qué este formato es "AI-proof"

Un chatbot puede generarte código plausible, pero no puede adivinar las
predicciones correctas sobre datos que nunca ha visto. Para obtener un buen
score necesitas efectivamente entrenar, validar y ejecutar un modelo que
generalice — no basta con copiar una respuesta.

## Nota para el profesor

`solution.csv` se generó localmente a partir de
`sklearn.datasets.fetch_openml('churn')` (split 80/20 estratificado,
`random_state=42`) y quedó **gitignored** en esta misma carpeta para no
filtrar el test set en el repo público. Para habilitar la calificación
automática real falta copiar `solution.csv` (par `id,class` del 20% de
test) al repo privado `ml-grading-infra`, que es el que compara las
entregas de `scripts/submit.py` contra este archivo. Ese paso queda fuera
del alcance de esta tarea.
