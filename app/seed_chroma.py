from app.vector_db import sop_collection

documents = [
    "If packet loss is above 10 percent and latency is above 250 ms, classify the incident as critical.",
    "If packet loss is between 5 and 10 percent, classify the incident as medium severity.",
    "If packet loss is below 5 percent and latency is below 150 ms, classify the incident as low severity.",
    "If backhaul link flapping is detected, possible root cause is backhaul instability or fiber provider issue.",
    "If power backup warning appears, possible root cause is power issue at tower site.",
    "For critical incidents, escalate to the Network Operations Center immediately.",
    "For low severity incidents, continue monitoring unless repeated alarms occur.",
    "For congestion or routing issues, review recent configuration changes and traffic utilization."
]

ids = [
    "sop_1",
    "sop_2",
    "sop_3",
    "sop_4",
    "sop_5",
    "sop_6",
    "sop_7",
    "sop_8"
]

sop_collection.upsert(
    ids=ids,
    documents=documents
)

print("Telecom SOP/runbook documents inserted into ChromaDB successfully.")