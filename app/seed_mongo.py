from app.mongo_db import logs_collection

sample_logs = [

    {
        "tower_id": "TX-DAL-102",
        "timestamp": "2026-05-20T09:15:00",
        "message": "Blackhaul link flapping detected. Packet drops increased."
    },
    {
        "tower_id": "TX-DAL-102",
        "timestamp": "2026-05-20T09:20:00",
        "message": "Latency increased above threshold. Multiple users impacted."
    },
    {
        "tower_id": "TX-AUS-220",
        "timestamp": "2026-05-20T10:05:00",
        "message": "Power backup warning from site controller."
    },
    {
        "tower_id": "TX-HOU-310",
        "timestamp": "2026-05-20T11:30:00",
        "message": "No major alarms detected. Traffic is normal."
    }
]

logs_collection.delete_many({})
logs_collection.insert_many(sample_logs)

print("Sample telecom logs inserted into MongoDB successfully.")

