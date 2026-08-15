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
    student_id = _require_env("ML_COURSE_STUDENT_ID")

    headers = {"x-api-key": api_key}

    if args.leaderboard:
        resp = requests.get(
            f"{api_url}/assignments/{args.assignment_slug}/leaderboard",
            headers=headers,
            timeout=15,
        )
        resp.raise_for_status()
        for entry in resp.json()["leaderboard"]:
            print(f"{entry['rank']:>3}. {entry['student_id']:<20} {entry['score']}")
        return

    resp = requests.get(f"{api_url}/submissions/{student_id}", headers=headers, timeout=15)
    if resp.status_code == 404:
        print("Aún no tienes entregas registradas.")
        return
    resp.raise_for_status()
    print(resp.json())


def _require_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        sys.exit(f"Falta la variable de entorno {name} (ver .env.example)")
    return value


if __name__ == "__main__":
    main()
