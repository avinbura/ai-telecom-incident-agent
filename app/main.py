from fastapi import FastAPI
from pydantic import BaseModel
from app.graph import build_incident_graph

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

    return result