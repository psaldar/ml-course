# Los retos del curso

[← Volver al README principal](../README.md)

Los retos son la **nota de seguimiento del curso: 45% en total**, 15%
cada uno. Uno por fin de semana, y se van liberando progresivamente a
medida que avanza el curso — acá solo aparece el que ya está disponible.

## Cómo funcionan

Cada reto sigue el formato "predicciones sobre holdout privado" (estilo
Kaggle InClass):

1. Descargas los datos (train con la variable objetivo, test sin ella).
2. Entrenas tu modelo localmente.
3. Generas un CSV de predicciones y lo envías (dos formas, ver abajo).
4. El backend lo compara contra respuestas que nunca ves y te devuelve un
   score + tu posición en el leaderboard.

Ver el README de cada reto para el enunciado, la métrica y la rúbrica.

## Cómo entregar

Hay dos formas de enviar tu CSV de predicciones. Son equivalentes —
mismo backend, mismo resultado — así que usa la que te quede más cómoda.
Puedes mezclarlas: entregar hoy por la página y mañana por terminal, no
importa.

### Opción A: página web

**https://d3qixogk4zgixq.cloudfront.net**

1. Pega tu API key en el campo de arriba y da clic en **Entrar**. Queda
   guardada en ese navegador — no hace falta repetir esto cada vez.
2. En "Enviar una entrega": elige el reto, elige tu archivo `.csv`, dale
   a **Enviar**.
3. La tabla "Mis entregas" muestra el estado (`pending` → `graded` o
   `error`) de cada reto al que le hayas entregado — no solo la última.
4. Más abajo, el leaderboard es público: no necesitas la key para verlo.

### Opción B: terminal

Una sola vez, en la raíz del repo, copien el archivo de configuración y
peguen ahí su API key:

| Sistema | Comando |
|---|---|
| macOS / Linux | `cp .env.example .env` |
| Windows — PowerShell | `Copy-Item .env.example .env` |
| Windows — CMD | `copy .env.example .env` |

De ahí en adelante, estos comandos son iguales en los tres sistemas:

```bash
uv run scripts/submit.py <reto> mi_prediccion.csv
uv run scripts/check_status.py <reto>              # tu resultado en ese reto
uv run scripts/check_status.py --all               # tus resultados en TODOS los retos
uv run scripts/check_status.py <reto> --leaderboard
```

### Tu identidad es la API key

No hay usuario/contraseña por separado: la API key que te da el profesor
**es** tu identidad frente al backend, tanto en la página como en la
terminal. No la compartas — cualquiera con tu key puede entregar a tu
nombre. Si la pierdes o crees que se filtró, pide una nueva; no hay forma
de recuperar la anterior (se guarda hasheada, ni el profesor puede verla
en texto plano).

## Los retos

| # | Reto | Tipo | Métrica | Peso |
|---|---|---|---|---|
| 1 | [Tasación de diamantes](tasacion-diamantes/) | Regresión, split aleatorio, 43k diamantes | `rmse` | 15% |

### Cada reto tiene dos etapas

**Etapa 1 — Leaderboard (40% del reto).** Suben su CSV de predicciones y el
sistema lo califica solo contra un conjunto de respuestas que nunca ven. La
nota sale de umbrales absolutos, no de la posición relativa: igualar el
baseline trivial da 60%, igualar el baseline del profesor da 90%+, el top-3
da 100%. Pueden entregar las veces que quieran.

**Etapa 2 — Notebook (60% del reto).** Un notebook ejecutable y documentado
en español con el análisis completo: exploración, decisiones de modelado,
validación, análisis de errores e interpretación. **Pesa más que el score**
— un buen número sin entender de dónde salió no alcanza. El README de cada
reto trae la rúbrica detallada.

Los datos llegan tal como salen de la fuente. Tasación de diamantes no
tiene componente temporal: el split entre train y test es aleatorio.
