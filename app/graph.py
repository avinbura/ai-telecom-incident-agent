import json
from typing import TypedDict, List
from langgraph.graph import StateGraph, END

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

def analyze_severity_node(state: IncidentState):
    if state["packet_loss"] > 10 and state["latency_ms"] > 250:
        severity = "critical"
    elif state["packet_loss"] > 5:
        severity = "medium" 
    else:
        severity = "low"
    
    return {"severity": severity}

def retrieve_logs_node(state:IncidentState):
    with open("app/sample_logs.json", "r") as file:
        all_logs = json.load(file)
    
    matching_logs = []

    for log in all_logs:
        if log["tower_id"] == state["tower_id"]:
            matching_logs.append(log["message"])
    
    return {"logs": matching_logs}

def read_sop_node(state: IncidentState):
    with open("app/telecom_sop.txt", "r") as file:
        sop_text = file.read()

    return {"sop_guidelines": sop_text}

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
    
    return {"root_cause": root_cause}

def recommendation_node(state: IncidentState):
    if state["severity"] == "critical":
        recommendation = "Escalate to Network operations center immediately."
    elif state["severity"] == "medium":
        recommendation = "Monitor tower and review logs."
    else:
        recommendation = "Continue monitoring."

    return {"recommendation": recommendation}

def escalation_node(state: IncidentState):
    return {
        "escalation_required": True,
        "escalation_team": "Network Operations Center"
    }


def no_escalation_node(state: IncidentState):
    return {
        "escalation_required": False,
        "escalation_team": "Not required"
    }


def route_escalation(state: IncidentState):
    if state["severity"] == "critical":
        return "escalate"
    else:
        return "no_escalation"


def summary_node(state: IncidentState):
    ai_summary = f"""
Tower {state["tower_id"]} is experiencing a {state["severity"]} network issue.

Issue detected:
{state["issue"]}

Possible root cause:
{state["root_cause"]}

Recommended action:
{state["recommendation"]}

Escalation required:
{state["escalation_required"]}

Escalation team:
{state["escalation_team"]}

SOP reference used:
{state["sop_guidelines"]}
"""

    return {"ai_summary": ai_summary}


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