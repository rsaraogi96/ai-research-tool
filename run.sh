#!/bin/bash
set -e

mkdir -p data

echo "Starting backend on :8000..."
uvicorn backend.main:app --reload --port 8000 &
BACKEND_PID=$!

echo "Starting frontend on :5173..."
cd frontend && npm run dev &
FRONTEND_PID=$!

trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null" EXIT
wait
