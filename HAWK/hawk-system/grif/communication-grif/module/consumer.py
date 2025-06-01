import os
import json
import threading
import requests

from confluent_kafka import Consumer, OFFSET_BEGINNING
from .producer import proceed_to_deliver

MODULE_NAME: str = os.getenv("MODULE_NAME")
KOLLEKTIV_URL: str = "http://kollektiv:8012/logs"

def to_chipher(id, details):
    proceed_to_deliver(id, {
        "deliver_to": "chipher-grif",
        "operation": "send_data",
        "data": details["data"]
    })
    print(f"[DEBUG] Send to Chipher: ", details["data"])

def to_kollektiv(id, details):
    print("[DEBUG] Send to Kollektiv", details["data"])

    requests.post(KOLLEKTIV_URL, json=details["data"])

def to_handler(id, details):
    proceed_to_deliver(id, {
        "deliver_to": "handler-grif",
        "operation": "send_data",
        "data": details["data"]
    })
    print(f"[DEBUG] Send to Handler: ", details["data"])
    
commands = {
    "to_grif": to_chipher,
    "valid_data": to_kollektiv,
    "to_grif_off": to_chipher,
    "to_reboot": to_handler,
    "report_off": to_kollektiv
}

def handle_event(id, details_str):
    """ Обработчик входящих в модуль задач. """
    details = json.loads(details_str)

    source: str = details.get("source")
    deliver_to: str = details.get("deliver_to")
    operation: str = details.get("operation")

    print(f"[info] handling event {id}, "
          f"{source}->{deliver_to}: {operation}")
    
    command = commands.get(operation)
    if command:
        command(id, details)

def consumer_job(args, config):
    consumer = Consumer(config)

    def reset_offset(verifier_consumer, partitions):
        if not args.reset:
            return

        for p in partitions:
            p.offset = OFFSET_BEGINNING
        verifier_consumer.assign(partitions)

    topic = MODULE_NAME
    consumer.subscribe([topic], on_assign=reset_offset)

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                pass
            elif msg.error():
                print(f"[error] {msg.error()}")
            else:
                try:
                    id = msg.key().decode('utf-8')
                    details_str = msg.value().decode('utf-8')
                    handle_event(id, details_str)
                except Exception as e:
                    print(f"[error] Malformed event received from " \
                          f"topic {topic}: {msg.value()}. {e}")
    except KeyboardInterrupt:
        pass

    finally:
        consumer.close()

def start_consumer(args, config):
    print(f'{MODULE_NAME}_consumer started')
    threading.Thread(target=lambda: consumer_job(args, config)).start()