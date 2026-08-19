from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


# =========================================================
# API IMPORTS
# =========================================================

from api.auth import router as auth_router
from api.applications import router as applications_router
from api.architecture import router as architecture_router
from api.failures import router as failures_router
from api.root_cause import router as root_cause_router
from api.experiments import router as experiments_router
from api.ai_engineer import router as ai_engineer_router
from api.reports import router as reports_router


# =========================================================
# DATABASE
# =========================================================

from database.database import init_db


# =========================================================
# FASTAPI APPLICATION
# =========================================================

app = FastAPI(
    title="ChaosPilot API",
    description=(
        "AI-powered software resilience "
        "and failure analysis platform"
    ),
    version="1.0.0"
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://127.0.0.1:8000",
        "http://localhost:8000",
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


# =========================================================
# STARTUP
# =========================================================

@app.on_event("startup")
def startup():

    init_db()


# =========================================================
# ROOT
# =========================================================

@app.get("/")
def root():

    return {
        "name": "ChaosPilot",
        "message": "ChaosPilot backend is running",
        "status": "online",
        "version": "1.0.0"
    }


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/health")
def health():

    return {
        "status": "healthy",
        "service": "ChaosPilot API"
    }


# =========================================================
# API ROUTES
# =========================================================

app.include_router(
    auth_router
)

app.include_router(
    applications_router
)

app.include_router(
    architecture_router
)

app.include_router(
    failures_router
)

app.include_router(
    root_cause_router
)

app.include_router(
    experiments_router
)

app.include_router(
    ai_engineer_router
)

app.include_router(
    reports_router
)


# =========================================================
# RUN SERVER
# =========================================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
