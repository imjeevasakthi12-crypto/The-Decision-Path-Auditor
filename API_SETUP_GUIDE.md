# 🔌 Complete Guide: Connecting API & API Keys to Decision Path Auditor

This document provides a comprehensive, step-by-step guide on how to configure, connect, and verify API Keys and REST APIs across the **Decision Path Auditor** project.

---

## 📐 Architecture Overview

The system operates via a decoupled multi-layer architecture:

```
┌────────────────────────────────┐         REST HTTP (JSON)        ┌────────────────────────────────┐
│   Streamlit Frontend App       │  ────────────────────────────>  │    FastAPI Backend API         │
│   (Port 8501)                  │  <────────────────────────────  │    (Port 8000)                 │
└────────────────────────────────┘                                 └────────────────────────────────┘
                 │                                                                 │
                 ▼                                                                 ▼
   Sidebar Translator & UI Pages                                      Agent Executor & PII Redaction
                                                                                   │
                                                                                   ▼
                                                                      SQLite / PostgreSQL Database
```

---

## 🔑 Step 1: API Key & Environment Setup

### 1.1 Create the Environment File
Copy `.env.example` or create a `.env` file in the project root directory (`d:\The Decision Path Auditor\.env`):

```bash
cp .env.example .env
```

### 1.2 Edit `.env` Configuration
Open `.env` and enter your valid API Keys and configuration values:

```env
# -----------------------------------------------------------------------------
# LLM & AI Service API Keys
# -----------------------------------------------------------------------------
OPENAI_API_KEY=sk-proj-your-openai-api-key-here
GEMINI_API_KEY=AIzaSyYourGeminiApiKeyHere
ANTHROPIC_API_KEY=sk-ant-your-anthropic-api-key-here

# -----------------------------------------------------------------------------
# Application & Database Settings
# -----------------------------------------------------------------------------
PORT=8501
BACKEND_URL=http://localhost:8000
DATABASE_URL=sqlite:///./audit_logs.db
SECRET_KEY=super-secret-enterprise-key-do-not-use-in-prod
```

### 1.3 How Environment Variables Are Loaded
- The backend configuration ([`backend/core/config.py`](file:///d:/The%20Decision%20Path%20Auditor/backend/core/config.py)) uses `python-dotenv` to automatically load `.env` key-value pairs into system environment variables on startup.
- The multi-agent executor ([`audit/agent_executor.py`](file:///d:/The%20Decision%20Path%20Auditor/audit/agent_executor.py)) reads the configured `OPENAI_API_KEY` / `GEMINI_API_KEY` directly from `settings`.

---

## 🚀 Step 2: Launching Backend & Frontend APIs

### Method 1: Unified Launcher (Recommended)
Run the automated launcher script to launch both the FastAPI backend (Port 8000) and Streamlit frontend (Port 8501):

```bash
python run_app.py
```

### Method 2: Manual Execution (Two Terminals)

**Terminal 1: Start FastAPI Backend API**
```bash
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 2: Start Streamlit Frontend**
```bash
python -m streamlit run frontend/Home.py --server.port 8501
```

### Method 3: Docker Compose
```bash
docker-compose up --build
```

---

## 📡 Step 3: REST API Endpoint Usage & Testing

Once launched, interactive API documentation is available at:
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Endpoint Reference

#### 1. Execute AI Agent & Log Audit Trace
- **HTTP Method**: `POST`
- **URL**: `http://localhost:8000/api/agent/execute_trace`
- **Request Body**:
  ```json
  {
    "user_id": "AUDITOR_USER",
    "prompt": "Evaluate loan request for Rahul Kumar",
    "domain": "Loan Approval",
    "fields": [
      ["Customer Name", "Rahul Kumar"],
      ["Monthly Salary", "₹65,000"],
      ["Credit Score", "740"]
    ]
  }
  ```
- **Response**:
  ```json
  {
    "message": "Trace executed and logged successfully",
    "session_id": "DEC-20260731-8A1B2C",
    "hash_value": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "final_decision": "APPROVED",
    "risk_level": "LOW",
    "reasoning_steps": [...]
  }
  ```

#### 2. Retrieve All Audit Logs
- **HTTP Method**: `GET`
- **URL**: `http://localhost:8000/api/audit/logs`

#### 3. Reconstruct Decision Trace by Session ID
- **HTTP Method**: `GET`
- **URL**: `http://localhost:8000/api/audit/logs/{session_id}`

#### 4. Enterprise Login & Token Authentication
- **HTTP Method**: `POST`
- **URL**: `http://localhost:8000/api/auth/token`
- **Form Data**: `username=admin&password=admin123`

---

## 🧪 Step 4: Verification & Automated Tests

To test the API connections and endpoint contracts, run the automated test suite:

```bash
python -m pytest tests/
```

Expected Output:
```
======================== 4 passed, 4 warnings in 2.77s ========================
```
