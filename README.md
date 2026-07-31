# 🛡️ Enterprise Decision Path Auditor

A production-ready AI governance application built to capture, redact, and securely store the complete reasoning path of AI agents across enterprise industries.

---

## 🔑 API Connection & Setup Guide

For detailed instructions on configuring API Keys (`OPENAI_API_KEY`, `GEMINI_API_KEY`, `ANTHROPIC_API_KEY`), connecting the FastAPI REST backend to the Streamlit frontend, and testing API endpoints, consult the **[API Setup Guide](API_SETUP_GUIDE.md)**.

### Quick Start API Key Setup
1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
2. Open `.env` and set your API keys:
   ```env
   OPENAI_API_KEY=sk-proj-your-openai-api-key-here
   GEMINI_API_KEY=AIzaSyYourGeminiApiKeyHere
   PORT=8501
   BACKEND_URL=http://localhost:8000
   DATABASE_URL=sqlite:///./audit_logs.db
   SECRET_KEY=super-secret-enterprise-key-do-not-use-in-prod
   ```

---

## 🏗️ Architecture Overview

- **Frontend**: Streamlit (Light corporate theme, multi-language sidebar translator, custom card grid layout, AI workflow diagrams)
- **Backend**: FastAPI (RESTful APIs, modular router structure)
- **Database**: PostgreSQL (SQLAlchemy ORM) / SQLite (Local fallback)
- **Security & PII**: JWT Authentication, RBAC, SHA-256 Tamper-evident Hashing, Presidio PII Redaction
- **Integration**: Google Stitch MCP Design Integration

---

## 🚀 Deployment Formats

### 1. Single Command Local Run
To run both the backend and frontend simultaneously in local development:
```bash
python run_app.py
```
- **Backend API**: `http://localhost:8000`
- **Frontend Dashboard**: `http://localhost:8501`

---

### 2. Docker Compose Deployment (Recommended for Local/Staging Containerization)
Includes PostgreSQL database, FastAPI backend container, and Streamlit frontend container:

```bash
# Build and start all services in detached mode
docker-compose up --build -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

---

### 3. Cloud Deployment: Render / Railway / Fly.io

1. **Backend Web Service**:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn backend.main:app --host 0.0.0.0 --port 8000`
   - Environment Variables:
     - `DATABASE_URL`: Your Managed Postgres connection string
     - `SECRET_KEY`: Random 32-byte secret key

2. **Frontend Web Service**:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `streamlit run frontend/Home.py --server.port $PORT --server.address 0.0.0.0`
   - Environment Variables:
     - `BACKEND_URL`: `https://your-backend-service.onrender.com`

---

### 4. Cloud Deployment: AWS (ECS / EKS / App Runner)

1. **Container Registry (ECR)**:
   ```bash
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com
   docker build -t decision-path-auditor .
   docker tag decision-path-auditor:latest <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/decision-path-auditor:latest
   docker push <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/decision-path-auditor:latest
   ```

2. **AWS ECS Task Definition**:
   - Deploy backend container exposing port 8000.
   - Deploy frontend container exposing port 8501.
   - Attach AWS RDS PostgreSQL for persistent audit trail storage.

---

## 🧪 Verification & Testing
To run the automated suite:
```bash
python -m pytest tests/
```
