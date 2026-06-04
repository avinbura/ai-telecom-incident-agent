from kafka import KafkaConsumer
import json
import requests
import time

KAFKA_TOPIC = "telecom-alerts"
KAFKA_SERVER = "localhost:9092"

API_BASE_URL = "http://127.0.0.1:8000"

USERNAME = "admin"
PASSWORD = "admin123"


def register_default_user():
    response = requests.post(
        f"{API_BASE_URL}/register",
        json={
            "username": USERNAME,
            "password": PASSWORD
        }
    )

    print("Register response:")
    print(response.json())


def get_jwt_token():
    response = requests.post(
        f"{API_BASE_URL}/token",
        data={
            "username": USERNAME,
            "password": PASSWORD
        }
    )

    print("Login response:")
    print(response.json())

    return response.json()["access_token"]


register_default_user()
token = get_jwt_token()

headers = {
    "Authorization": f"Bearer {token}"
}

consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_SERVER,
    value_deserializer=lambda v: json.loads(v.decode("utf-8")),
    auto_offset_reset="latest",
    group_id="local-consumer-v9"
)

print("Local Kafka consumer is waiting for alerts...")

for message in consumer:
    alert = message.value

    print("Received alert:")
    print(alert)

    response = requests.post(
        f"{API_BASE_URL}/analyze-alert",
        json=alert,
        headers=headers
    )

    print("AI API response:")
    print(response.json())