from sqlalchemy import Column, Integer, String, Float, Boolean, Text, DateTime
from datetime import datetime
from app.database import Base


class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    tower_id = Column(String, index=True)
    issue = Column(Text)
    packet_loss = Column(Float)
    latency_ms = Column(Float)
    severity = Column(String)
    root_cause = Column(Text)
    recommendation = Column(Text)
    escalation_required = Column(Boolean)
    escalation_team = Column(String)
    ai_summary = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
