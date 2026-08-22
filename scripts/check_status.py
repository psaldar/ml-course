#!/usr/bin/env python3
"""Consulta tus entregas y el leaderboard de un assignment.

Requiere el mismo .env que scripts/submit.py.

Uso:
    uv run scripts/check_status.py <assignment-slug>
    uv run scripts/check_status.py <assignment-slug> --leaderboard
    uv run scripts/check_status.py --all   # todas tus entregas, en cualquier reto
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
    parser.add_argument("assignment_slug", nargs="?")
    parser.add_argument("--leaderboard", action="store_true", help="Muestra el leaderboard completo")
    parser.add_argument("--all", action="store_true", help="Lista todas tus entregas, en cualquier reto")
    args = parser.parse_args()

    if not args.all and not args.leaderboard and not args.assignment_slug:
        sys.exit("Falta el nombre del reto, o usa --all para ver todas tus entregas.")

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
    submissions = resp.json().get("submissions", [])

    if args.all:
        if not submissions:
            print("Todavía no tienes ninguna entrega registrada.")
            return
        for s in sorted(submissions, key=lambda s: s.get("assignment_id", "")):
            _imprimir(s)
        return

    mia = next(
        (s for s in submissions if s.get("assignment_id") == args.assignment_slug), None
    )
    if mia is None:
        print(f"Aún no tienes una entrega para '{args.assignment_slug}'.")
        return
    _imprimir(mia)


def _imprimir(s: dict) -> None:
    print(f"assignment : {s.get('assignment_id')}")
    print(f"estado     : {s.get('status')}")
    if "score" in s:
        print(f"score      : {s['score']}  ({s.get('metric')})")
    if "error" in s:
        print(f"error      : {s['error']}")
    print()


def _require_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        sys.exit(f"Falta la variable de entorno {name} (ver .env.example)")
    return value


if __name__ == "__main__":
    main()
