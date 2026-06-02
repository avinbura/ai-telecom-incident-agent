from kafka import KafkaConsumer
import json
import requests

consumer = KafkaConsumer(
    'telecom-alerts',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='telecom-agent-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

API_URL = "http://127.0.0.1:8000/analyze-alert"

print("Listening for telecom alerts...\n")

for message in consumer:

    alert = message.value

    print("Received alert:")
    print(alert)

    try:

        response = requests.post(API_URL, json=alert)

        print("Status Code:", response.status_code)
        print("Raw Response:", response.text)

        if response.status_code == 200:
            print("AI Agent Response:")
            print(response.json())
        else:
            print("AI Agent API returned an error.")

    except Exception as e:
        print(f"Error calling AI agent API: {e}")

    print("-" * 50)