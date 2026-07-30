FROM python:3.12-slim

WORKDIR /app

# Install build essential dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
RUN python -m spacy download en_core_web_sm

COPY . .

# Create non-root user and grant permissions
RUN useradd -m appuser && chown -R appuser:appuser /app && chmod +x /app/start.sh
USER appuser

# Expose ports for both FastAPI and Streamlit
EXPOSE 8000 8501

CMD ["/app/start.sh"]
