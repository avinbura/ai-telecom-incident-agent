from kafka import KafkaProducer
import json
import time


producer = KafkaProducer(
    bootstrap_servers = 'localhost:9092',
    value_serializer = lambda v: json.dumps(v).encode('utf-8')
)

alerts = [
    {
        "tower_id": "TX-DAL-102",
        "issue": "High packet loss and latency spike",
        "packet_loss": 18,
        "latency_ms": 340
    },
    {
        "tower_id": "TX-AUS-220",
        "issue": "Power backup warning",
        "packet_loss": 2,
        "latency_ms": 90
    },
    {
        "tower_id": "TX-HOU-310",
        "issue": "Minor latency fluctuation",
        "packet_loss": 3,
        "latency_ms": 140
    }
]

for alert in alerts:

    producer.send(
        'telecom-alerts',
        value=alert
    )

    print(f"Alert sent: {alert}")

    time.sleep(2)

producer.flush()