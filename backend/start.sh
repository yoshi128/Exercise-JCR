#!/usr/bin/env bash
PORT=${PORT:-10000}
uvicorn main:app --host 0.0.0.0 --port $PORT
