#!/usr/bin/env bash
set -euo pipefail

echo "==> Tworzenie .env z .env.example, jeśli brakuje"
for d in flipper-*; do
  [ -d "$d" ] || continue
  if [ ! -f "$d/.env" ]; then
    cp "$d/.env.example" "$d/.env"
    echo "Utworzono $d/.env"
  fi
done

echo "==> Uruchamianie workerów"
docker compose up -d --build
docker compose ps
