from fastapi import FastAPI
from database.postgres import engine, Base
from backend.api.routes import router as agent_router
from backend.api.auth import router as auth_router
from backend.api.audit_logs import router as logs_router

# Create DB Tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Enterprise Decision Path Auditor API")

app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(agent_router, prefix="/api/agent", tags=["AI Agent"])
app.include_router(logs_router, prefix="/api/audit", tags=["Audit Logs"])

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Enterprise API is running"}
