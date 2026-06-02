import os
import random
from datetime import datetime, timedelta
import pandas as pd

output_dir = "data/synthetic"
os.makedirs(output_dir, exist_ok=True)

tower_ids = [
    "TX-DAL-102",
    "TX-AUS-220",
    "TX-HOU-310",
    "TX-SAN-410",
    "TX-ELP-510",
    "TX-FRW-610"
]

regions = {
    "TX-DAL-102": "Dallas",
    "TX-AUS-220": "Austin",
    "TX-HOU-310": "Houston",
    "TX-SAN-410": "SanAntonio",
    "TX-ELP-510": "ElPaso",
    "TX-FRW-610": "FortWorth"
}

issues = [
    "High packet loss",
    "Latency spike",
    "Backhaul instability",
    "Power backup warning",
    "Routing issue",
    "Minor packet drops"
]

root_causes = [
    "Backhaul instability",
    "Power issue",
    "Routing congestion",
    "Fiber provider issue",
    "Unknown"
]

records = []

start_time = datetime(2026, 6, 1, 0, 0, 0)

for i in range(10000):
    tower_id = random.choice(tower_ids)
    issue = random.choice(issues)

    packet_loss = round(random.uniform(0, 25), 2)
    latency_ms = round(random.uniform(50, 500), 2)

    if packet_loss > 10 and latency_ms > 250:
        severity = "critical"
    elif packet_loss > 5:
        severity = "medium"
    else:
        severity = "low"

    record = {
        "event_id": i + 1,
        "tower_id": tower_id,
        "region": regions[tower_id],
        "issue": issue,
        "packet_loss": packet_loss,
        "latency_ms": latency_ms,
        "severity": severity,
        "root_cause": random.choice(root_causes),
        "timestamp": start_time + timedelta(minutes=i)
    }

    records.append(record)

df = pd.DataFrame(records)

output_path = os.path.join(output_dir, "synthetic_telecom_incidents.csv")

df.to_csv(output_path, index=False)

print(f"Synthetic telecom dataset saved to {output_path}")
print(df.head())
print(f"Total records generated: {len(df)}")
