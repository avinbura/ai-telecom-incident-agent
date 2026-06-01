import json
from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from app.mongo_db import logs_collection
from app.vector_db import sop_collection
from app.llm_gateway import generate_incident_summary

class IncidentState(TypedDict):
    tower_id: str
    issue: str
    packet_loss: float
    latency_ms: float
    logs: List[str]
    severity: str
    root_cause: str 
    recommendation: str
    escalation_required: bool
    escalation_team: str
    sop_guidelines: str
    ai_summary: str
    agents_executed: List[str]

def analyze_severity_node(state: IncidentState):
    if state["packet_loss"] > 10 and state["latency_ms"] > 250:
        severity = "critical"
    elif state["packet_loss"] > 5:
        severity = "medium" 
    else:
        severity = "low"
    
    return {"severity": severity,
            "agents_executed": state["agents_executed"] + ["SeverityAnalysisAgent"]
        }

def retrieve_logs_node(state:IncidentState):
    mongo_logs = logs_collection.find(
        {"tower_id": state["tower_id"]},
        {"_id": 0, "message": 1}
    )
    
    matching_logs = []

    for log in mongo_logs:    
        matching_logs.append(log["message"])
    
    return {"logs": matching_logs,
            "agents_executed": state["agents_executed"] + ["MongoLogRetrievalAgent"]
        }

def read_sop_node(state: IncidentState):

    query_text = (
        f"{state['issue']} "
        f"{' '.join(state['logs'])}"
    )

    results = sop_collection.query(
        query_texts=[query_text],
        n_results=3
    )

    retrieved_docs = results["documents"][0]

    sop_text = "\n".join(retrieved_docs)

    return {"sop_guidelines": sop_text,
            "agents_executed": state["agents_executed"] + ["RAGSOPRetrievalAgent"]
        }

def root_cause_node(state: IncidentState):
    logs_text= " " .join(state["logs"]).lower()

    if "backhaul" in logs_text:
        root_cause = "Possible backhaul instability or fiber provider issue"
    elif "power" in logs_text:
        root_cause = "Possible power issue at tower site"
    elif "latency" in logs_text:
        root_cause = "Possible congestion or routing issue"
    else:
        root_cause = "Root cause unclear. More logs are needed."
    
    return {"root_cause": root_cause,
            "agents_executed": state["agents_executed"] + ["RootCauseAnalysisAgent"]
        }

def recommendation_node(state: IncidentState):
    if state["severity"] == "critical":
        recommendation = "Escalate to Network operations center immediately."
    elif state["severity"] == "medium":
        recommendation = "Monitor tower and review logs."
    else:
        recommendation = "Continue monitoring."

    return {"recommendation": recommendation,
            "agents_executed": state["agents_executed"] + ["RecommendationAgent"]
        }

def escalation_node(state: IncidentState):
    return {
    "escalation_required": True,
    "escalation_team": "Network Operations Center",
    "agents_executed": state["agents_executed"] + ["EscalationDecisionAgent"]
}

def no_escalation_node(state: IncidentState):
    return {
        "escalation_required": False,
        "escalation_team": "Not required",
        "agents_executed": state["agents_executed"] + ["EscalationDecisionAgent"]
    }


def route_escalation(state: IncidentState):
    if state["severity"] == "critical":
        return "escalate"
    else:
        return "no_escalation"


def summary_node(state: IncidentState):

    prompt = f"""
You are a telecom Network Operations Center assistant.

Create a clear incident summary using the information below.

Tower ID: {state["tower_id"]}
Issue: {state["issue"]}
Packet Loss: {state["packet_loss"]}%
Latency: {state["latency_ms"]} ms
Logs: {state["logs"]}
Severity: {state["severity"]}
Root Cause: {state["root_cause"]}
Recommendation: {state["recommendation"]}
Escalation Required: {state["escalation_required"]}
Escalation Team: {state["escalation_team"]}
Relevant SOP Guidance: {state["sop_guidelines"]}

Write the summary in a professional telecom operations style.
"""

    ai_summary = generate_incident_summary(prompt)

    return {"ai_summary": ai_summary,
            "agents_executed": state["agents_executed"] + ["LLMSummaryAgent"]
        }


def build_incident_graph():
    graph = StateGraph(IncidentState)

    graph.add_node("analyze_severity", analyze_severity_node)
    graph.add_node("retrieve_logs", retrieve_logs_node)
    graph.add_node("root_cause", root_cause_node)
    graph.add_node("recommendation", recommendation_node)
    graph.add_node("escalation", escalation_node)
    graph.add_node("no_escalation", no_escalation_node)
    graph.add_node("read_sop", read_sop_node)
    graph.add_node("summary", summary_node)

    graph.set_entry_point("analyze_severity")

    graph.add_edge("analyze_severity", "retrieve_logs")
    graph.add_edge("retrieve_logs", "read_sop")
    graph.add_edge("read_sop", "root_cause")
    graph.add_edge("root_cause", "recommendation")

    graph.add_conditional_edges(
        "recommendation",
        route_escalation,
        {
            "escalate": "escalation",
            "no_escalation": "no_escalation"
        }
    )

    graph.add_edge("escalation", "summary")
    graph.add_edge("no_escalation", "summary")
    graph.add_edge("summary", END)

    return graph.compile()