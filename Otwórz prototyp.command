#!/bin/bash
# Uruchamia prototyp na lokalnym serwerze (potrzebne, żeby działał kalendarz rejestracji ProAssist) i otwiera przeglądarkę.
cd "$(dirname "$0")"
PORT=8765
python3 build.py >/dev/null 2>&1
lsof -ti tcp:$PORT >/dev/null 2>&1 || (python3 -m http.server $PORT >/dev/null 2>&1 &)
sleep 1
open "http://localhost:$PORT/index.html"
