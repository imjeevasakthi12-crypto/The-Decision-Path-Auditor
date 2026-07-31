#!/bin/bash
set -e

# Download SpaCy model if not already downloaded
if ! python -c "import spacy; spacy.util.get_package_path('en_core_web_sm')" &> /dev/null; then
  python -m spacy download en_core_web_sm || true
fi

# Set default ports if not specified
PORT="${PORT:-8501}"
BACKEND_URL="${BACKEND_URL:-http://127.0.0.1:8000}"

echo "Starting FastAPI Backend on port 8000..."
uvicorn backend.main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Wait for backend to fully initialize before starting frontend
echo "Waiting for backend to initialize..."
MAX_RETRIES=30
RETRY_COUNT=0

while ! curl -s http://127.0.0.1:8000/health > /dev/null; do
  if ! kill -0 $BACKEND_PID 2>/dev/null; then
    echo "ERROR: Backend process crashed instantly! Please check the Render logs above for Python errors."
    exit 1
  fi
  sleep 2
  RETRY_COUNT=$((RETRY_COUNT+1))
  if [ $RETRY_COUNT -ge $MAX_RETRIES ]; then
    echo "ERROR: Backend health check timed out after 60 seconds."
    exit 1
  fi
done
echo "Backend is up and running!"

echo "Starting Streamlit Frontend on port $PORT..."
export BACKEND_URL="$BACKEND_URL"
exec streamlit run frontend/Home.py --server.port "$PORT" --server.address 0.0.0.0
