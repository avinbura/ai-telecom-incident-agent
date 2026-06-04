from kafka import KafkaConsumer
import json
import requests
import time

KAFKA_TOPIC = "telecom-alerts"
KAFKA_SERVER = "kafka:9092"

API_BASE_URL = "http://telecom-ai-agent:8000"

USERNAME = "admin"
PASSWORD = "admin123"


def register_default_user():
    register_url = f"{API_BASE_URL}/register"

    try:
        response = requests.post(
            register_url,
            json={
                "username": USERNAME,
                "password": PASSWORD
            }
        )

        print("Default user registration response:", flush=True)
        print(response.json(), flush=True)

    except Exception as e:
        print(f"Default user registration error: {e}", flush=True)


def get_jwt_token():
    login_url = f"{API_BASE_URL}/token"

    while True:
        try:
            response = requests.post(
                login_url,
                data={
                    "username": USERNAME,
                    "password": PASSWORD
                }
            )

            response_data = response.json()

            if "access_token" in response_data:
                print("JWT token received successfully", flush=True)
                return response_data["access_token"]

            print("Token not ready yet. Retrying...", flush=True)
            print(response_data, flush=True)

        except Exception as e:
            print(f"Login error: {e}", flush=True)

        time.sleep(5)


consumer = None

while consumer is None:
    try:
        consumer = KafkaConsumer(
            KAFKA_TOPIC,
            bootstrap_servers=KAFKA_SERVER,
            value_deserializer=lambda v: json.loads(v.decode("utf-8")),
            auto_offset_reset="earliest",
            group_id="telecom-group-v9-test-2"
        )

        print("Kafka Consumer connected successfully...", flush=True)

    except Exception as e:
        print(
            f"Kafka not ready yet. Retrying in 5 seconds... Error: {e}",
            flush=True
        )
        time.sleep(5)


time.sleep(10)

register_default_user()

jwt_token = get_jwt_token()

headers = {
    "Authorization": f"Bearer {jwt_token}"
}

print("Waiting for Kafka messages...", flush=True)

while True:
    records = consumer.poll(timeout_ms=5000)

    if not records:
        print("No Kafka messages yet. Waiting...", flush=True)
        continue

    for topic_partition, messages in records.items():
        for message in messages:
            alert_data = message.value

            print(f"Received Kafka alert: {alert_data}", flush=True)

            response = requests.post(
                f"{API_BASE_URL}/analyze-alert",
                json=alert_data,
                headers=headers
            )

            print("API Response:", flush=True)
            print(response.json(), flush=True)
