# Curso Aprendizaje Automático - 2026 2

Maestría en Ciencia de Datos y Analítica, Universidad EAFIT.

**Profesor:** Pablo Saldarriaga — psaldar2@eafit.edu.co
**Inicio de clases:** 25 de septiembre de 2026 · **Fin de curso:** 10 de octubre de 2026

Material y notebooks del curso.

## Setup

Necesitas **uv**, el gestor de entornos y dependencias de Python que usa
el curso. Reemplaza `venv` + `pip` + `requirements.txt`: no hay que crear
ni activar un entorno a mano, ni instalar paquetes uno por uno.

Instálalo una sola vez:

| Sistema | Comando |
|---|---|
| macOS / Linux | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| Windows — PowerShell | `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 \| iex"` |

Después, dentro de la carpeta del repositorio:

```bash
uv sync
```

Ese comando lee [`pyproject.toml`](pyproject.toml) —ahí están declaradas
**todas** las dependencias del curso, no hay `requirements.txt`—, crea un
entorno virtual en `.venv/` dentro del repo, e instala exactamente esas
versiones. Es igual en los tres sistemas, como todos los `uv run ...` de
más abajo.

### Abriendo los notebooks con el kernel correcto

No hace falta activar el entorno a mano. Dos formas de abrir un notebook
usando el `.venv` que acaba de crear `uv sync`:

- **Terminal:** `uv run jupyter lab` desde la carpeta del repo — abre
  Jupyter ya con el kernel correcto seleccionado.
- **VS Code u otro editor:** abre el notebook y, al elegir el kernel,
  selecciona el que está **dentro de la carpeta `.venv` del repo**
  (Python 3.12) — no el Python global del sistema.

Si una celda falla con `ModuleNotFoundError` aunque `uv sync` haya
terminado bien, casi siempre es que el kernel activo no es el de
`.venv`.

Después, abre [`00_verificacion_entorno.ipynb`](00_verificacion_entorno.ipynb)
y ejecútalo completo ("Run All"): confirma que Python, las librerías y la
conexión a los servicios del curso quedaron bien configurados, **antes**
de la primera clase.

| | |
|---|---|
| **Leaderboard + entregas por la web** | https://d3qixogk4zgixq.cloudfront.net |
| **API** | `https://6trg8jthgl.execute-api.us-east-1.amazonaws.com/dev` |

> **Windows, macOS o Linux.** Todo el curso funciona en los tres. Donde un
> comando cambia según el sistema, aparece una tabla con las tres versiones.
> Los notebooks y los comandos `uv run ...` son idénticos en todos.

## Estructura

```
00_verificacion_entorno.ipynb    corre esto antes de la primera clase
modules/            material teórico por módulo/semana
notebooks/           notebooks exploratorios de clase
assignments/
  README.md            cómo funcionan los retos y cómo entregar
  <reto>/              README con el enunciado + notebook de partida
scripts/
  submit.py            envía tu CSV de predicciones
  check_status.py       consulta tu score / leaderboard
```

## Notebooks de clase

Cada sesión son 4 horas: 3 h de exposición, 30 min de descanso y **30 min
de ejercicio** sobre el notebook de la sesión.

| # | Sesión | Tema |
|---|---|---|
| 1 | `sesion_01_fundamentos_regresion_clasificacion` | Fundamentos de ML, regresión y clasificación |

Las siguientes sesiones se agregan a medida que avanza el curso.

El ejercicio de cada notebook está dividido en 3 partes de 10 minutos.
