import json
import time
import uuid
import requests

from confluent_kafka import Producer

KAFKA_BOOTSTRAP = "broker:29092"
TOPIC = "monitor"
KOLLEKTIV_ENDPOINT = "http://kollektiv:8012/logs"

def send_test_message(test_id):
    payload = {
        "id": test_id,
        "source": "authorization",
        "deliver_to": "handle-command",
        "operation": "send_command",
        "data": {"command": "test-command"}
    }
    producer = Producer({'bootstrap.servers': KAFKA_BOOTSTRAP})
    producer.produce(TOPIC, json.dumps(payload), key=test_id)
    producer.flush()

def test_message_reaches_kollektiv():
    test_id = str(uuid.uuid4())
    send_test_message(test_id)

    timeout = 15
    found = False

    time.sleep(60)
    for i in range(timeout):
        time.sleep(1)
        print(f"[{i+1}/{timeout}] Проверка логов Коллектива...", flush=True)
        try:
            response = requests.get(KOLLEKTIV_ENDPOINT)
            if response.status_code == 200:
                logs = response.json()
                if any(log.get("id") == test_id for log in logs):
                    found = True
                    break
            else:
                print(f"[WARNING] Коллектив ответил с кодом {response.status_code}")
        except Exception as e:
            print(f"[WARNING] Ошибка при запросе: {e}")

    assert found, f"Сообщение с id={test_id} не дошло до Коллектива"
