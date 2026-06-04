from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from app.graph import build_incident_graph
from app import database
from app.database import SessionLocal
from app.crud import save_incident, get_all_incidents, get_incident_by_id
from app.redis_cache import redis_client
from app.schemas_auth import UserRegister, UserLogin, TokenResponse
from app.auth import hash_password, verify_password, create_access_token, get_current_user
from app.auth import get_current_user
import json
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

app = FastAPI(title="Minimal Telecom AI Incident Agent")

incident_graph = build_incident_graph()
fake_users_db = {}

class AlertRequest(BaseModel):
    tower_id: str
    issue: str
    packet_loss: float
    latency_ms: float


@app.get("/")
def home():
    return {
        "message": "Minimal Telecom AI Incident Agent is running with LangGraph"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "telecom-ai-agent",
        "version": "7.0"
    }


@app.get("/ready")
def readiness_check():
    return {
        "status": "ready",
        "dependencies": {
            "fastapi": "running",
            "langgraph": "loaded",
            "redis": "configured",
            "kafka": "configured",
            "postgresql": "configured",
            "mongodb": "configured"
        }
    }


@app.post("/register")
def register_user(user: UserRegister):
    if user.username in fake_users_db:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    hashed_password = hash_password(user.password)

    fake_users_db[user.username] = {
        "username": user.username,
        "hashed_password": hashed_password
    }

    return {
        "message": "User registered successfully",
        "username": user.username
    }


@app.post("/login", response_model=TokenResponse)
def login_user(user: UserLogin):
    db_user = fake_users_db.get(user.username)

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    if not verify_password(user.password, db_user["hashed_password"]):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    access_token = create_access_token(
        data={"sub": user.username}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@app.post("/token", response_model=TokenResponse)
def login_for_swagger(
    form_data: OAuth2PasswordRequestForm = Depends()
):
    db_user = fake_users_db.get(form_data.username)

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    if not verify_password(
        form_data.password,
        db_user["hashed_password"]
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    access_token = create_access_token(
        data={"sub": form_data.username}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@app.post("/analyze-alert")
def analyze_alert(
    alert: AlertRequest,
    current_user: str = Depends(get_current_user)
):

    logger.info(f"Received alert for tower: {alert.tower_id}")

    cache_key = f"{alert.tower_id}:{alert.issue}"

    cached_result = redis_client.get(cache_key)

    if cached_result:
        logger.info("Returning result from Redis cache")
        return json.loads(cached_result)

    result = incident_graph.invoke({
        "tower_id": alert.tower_id,
        "issue": alert.issue,
        "packet_loss": alert.packet_loss,
        "latency_ms": alert.latency_ms,
        "logs": [],
        "severity": "",
        "root_cause": "",
        "recommendation": "",
        "escalation_required": False,
        "escalation_team": "",
        "sop_guidelines": "",
        "ai_summary": "",
        "agents_executed": []
    })

    try:
        db = SessionLocal()
        saved_incident = save_incident(db, result)
        result["database_id"] = saved_incident.id
        db.close()
        logger.info(f"Incident saved with database_id: {saved_incident.id}")

    except Exception as e:
        logger.warning(f"Database save skipped: {e}")
        result["database_id"] = None

    redis_client.set(
        cache_key,
        json.dumps(result),
        ex=300
    )

    return result

@app.get("/incidents")
def get_incidents():
    db = SessionLocal()

    try:
        incidents = get_all_incidents(db)
        return incidents
    finally:
        db.close()

@app.get("/incidents/{incident_id}")
def get_incident(incident_id: int):
    db = SessionLocal()

    try:
        incident = get_incident_by_id(db, incident_id)

        if incident is None:
            raise HTTPException(
                status_code=404,
                detail="Incident not found"
            )
        return incident
    finally:
        db.close()