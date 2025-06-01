import os
import json
import threading

from confluent_kafka import Consumer, OFFSET_BEGINNING
from .producer import proceed_to_deliver

MODULE_NAME: str = os.getenv("MODULE_NAME")
HASH_PATH: str = "/shared/hash"

def sending(id, details):
    with open(HASH_PATH, "r") as file:
        hash_val = file.readline()

    details["data"].update({"signature": hash_val})
    proceed_to_deliver(id, {
        "deliver_to": "chipher-robot",
        "operation": "send_data",
        "data": details["data"]
    })
    print(f"[DEBUG] Send to Chipher: ", details["data"])

def to_security(id, details):
    proceed_to_deliver(id, {
        "deliver_to": "communication-sec",
        "operation": "report_robot",
        "data": details["data"]
    })
    print(f"[DEBUG] Send to Security: ", details["data"])
    
commands = {
    "to_robot": sending,
    "report_robot": to_security
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