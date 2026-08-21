#!/usr/bin/env python3
"""Consulta tu score y el leaderboard de un assignment.

Requiere el mismo .env que scripts/submit.py.

Uso:
    uv run scripts/check_status.py <assignment-slug>
"""
from __future__ import annotations

import argparse
import os
import sys

import requests
from dotenv import load_dotenv


def main() -> None:
    load_dotenv()

    parser = argparse.ArgumentParser()
    parser.add_argument("assignment_slug")
    parser.add_argument("--leaderboard", action="store_true", help="Muestra el leaderboard completo")
    args = parser.parse_args()

    api_url = _require_env("ML_COURSE_API_URL")
    api_key = _require_env("ML_COURSE_API_KEY")

    headers = {"x-api-key": api_key}

    if args.leaderboard:
        resp = requests.get(
            f"{api_url}/assignments/{args.assignment_slug}/leaderboard",
            timeout=15,
        )
        resp.raise_for_status()
        datos = resp.json()
        entradas = datos.get("leaderboard", [])
        if not entradas:
            print("Todavía no hay entregas para este assignment.")
            return
        print(f"Métrica: {datos.get('metric')}\n")
        for entry in entradas:
            print(f"{entry['rank']:>3}. {entry['student_id']:<24} {entry['score']}")
        return

    resp = requests.get(f"{api_url}/submissions/me", headers=headers, timeout=15)
    if resp.status_code == 401:
        sys.exit("API key inválida. Revisa ML_COURSE_API_KEY en tu .env")
    resp.raise_for_status()
    datos = resp.json()
    if not datos.get("assignment_id"):
        print("Aún no tienes entregas registradas.")
        return
    print(f"assignment : {datos.get('assignment_id')}")
    print(f"estado     : {datos.get('status')}")
    if "score" in datos:
        print(f"score      : {datos['score']}  ({datos.get('metric')})")


def _require_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        sys.exit(f"Falta la variable de entorno {name} (ver .env.example)")
    return value


if __name__ == "__main__":
    main()
