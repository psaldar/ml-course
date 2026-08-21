#!/usr/bin/env python3
"""CLI que los estudiantes usan para enviar sus predicciones.

Requiere un archivo .env con:
    ML_COURSE_API_URL=https://xxxx.execute-api.us-east-1.amazonaws.com/dev
    ML_COURSE_API_KEY=<tu api key, entregada por el profesor>

Tu identidad sale de la API key, así que no hay que declararla aparte.

Uso:
    uv run scripts/submit.py <assignment-slug> ./mi_prediccion.csv
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv


def main() -> None:
    load_dotenv()

    parser = argparse.ArgumentParser()
    parser.add_argument("assignment_slug")
    parser.add_argument("predictions_csv", type=Path)
    args = parser.parse_args()

    api_url = _require_env("ML_COURSE_API_URL")
    api_key = _require_env("ML_COURSE_API_KEY")

    if not args.predictions_csv.exists():
        sys.exit(f"No existe el archivo: {args.predictions_csv}")

    resp = requests.post(
        f"{api_url}/assignments/{args.assignment_slug}/upload-url",
        json={},
        headers={"x-api-key": api_key},
        timeout=15,
    )
    if resp.status_code == 401:
        sys.exit("API key inválida. Revisa ML_COURSE_API_KEY en tu .env")
    resp.raise_for_status()
    datos = resp.json()

    with open(args.predictions_csv, "rb") as fh:
        put_resp = requests.put(datos["upload_url"], data=fh, timeout=120)
    put_resp.raise_for_status()

    print(f"Entrega enviada como '{datos['student_id']}' para "
          f"'{args.assignment_slug}'.")
    print("La calificación tarda unos segundos. Revisa tu score con:")
    print(f"  uv run scripts/check_status.py {args.assignment_slug}")


def _require_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        sys.exit(f"Falta la variable de entorno {name} (ver .env.example)")
    return value


if __name__ == "__main__":
    main()
