import os
import pandas as pd
from app.database import SessionLocal
from app.models import Incident

output_dir = "data/postgres_export"
os.makedirs(output_dir, exist_ok=True)

db = SessionLocal()

try:
    incidents = db.query(Incident).all()

    data = []

    for incident in incidents:
        data.append({
            "id": incident.id,
            "tower_id": incident.tower_id,
            "issue": incident.issue,
            "packet_loss": incident.packet_loss,
            "latency_ms": incident.latency_ms,
            "severity": incident.severity,
            "root_cause": incident.root_cause,
            "recommendation": incident.recommendation,
            "escalation_required": incident.escalation_required,
            "escalation_team": incident.escalation_team,
            "created_at": incident.created_at
        })

    df = pd.DataFrame(data)

    output_path = os.path.join(
        output_dir,
        "postgres_incidents_export.csv"
    )

    df.to_csv(output_path, index=False)

    print(f"PostgreSQL incidents exported to {output_path}")
    print(df.head())
    print(f"Total incidents exported: {len(df)}")

finally:
    db.close()
    