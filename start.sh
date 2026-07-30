#!/bin/bash
set -e

# Download SpaCy model if not already downloaded
python -m spacy download en_core_web_sm || true

# Set default ports if not specified
PORT="${PORT:-8501}"
BACKEND_URL="${BACKEND_URL:-http://127.0.0.1:8000}"

echo "Starting FastAPI Backend on port 8000..."
uvicorn backend.main:app --host 0.0.0.0 --port 8000 &

# Wait for backend to initialize
sleep 3

echo "Starting Streamlit Frontend on port $PORT..."
export BACKEND_URL="$BACKEND_URL"
exec streamlit run frontend/Home.py --server.port "$PORT" --server.address 0.0.0.0
