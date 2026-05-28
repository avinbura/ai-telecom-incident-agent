from fastapi import FastAPI
from pydantic import BaseModel
from app.graph import build_incident_graph
from app import database
from app.database import SessionLocal
from app.crud import save_incident
from app.redis_cache import redis_client
import json

app = FastAPI(title="Minimal Telecom AI Incident Agent")

incident_graph = build_incident_graph()


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


@app.post("/analyze-alert")
def analyze_alert(alert: AlertRequest):

    cache_key = f"{alert.tower_id}:{alert.issue}"

    cached_result = redis_client.get(cache_key)

    if cached_result:
        print("Returning result from Redis cache")
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
        "ai_summary": ""
    })

    db = SessionLocal()

    try:
        saved_incident = save_incident(db, result)
        result["database_id"] = saved_incident.id
    finally:
        db.close()

        redis_client.set(
        cache_key,
        json.dumps(result),
        ex=300
    )
    
    return result