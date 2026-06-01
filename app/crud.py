from app.models import Incident

def save_incident(db, result: dict):
    incident = Incident(
        tower_id = result["tower_id"],
        issue = result["issue"],
        packet_loss = result["packet_loss"],
        latency_ms = result["latency_ms"],
        severity = result["severity"],
        root_cause = result["root_cause"],
        recommendation = result["recommendation"],
        escalation_required = result["escalation_required"],
        escalation_team=result["escalation_team"],
        ai_summary=result["ai_summary"]
    )

    db.add(incident)
    db.commit()
    db.refresh(incident)

    return incident

def get_all_incidents(db):
    return db.query(Incident).order_by(Incident.id.desc()).all()

def get_incident_by_id(db,incident_id: int):
    return db.query(Incident).filter(Incident.id == incident_id).first()
