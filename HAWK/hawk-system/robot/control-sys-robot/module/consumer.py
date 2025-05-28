import os
import json
import threading

from confluent_kafka import Consumer, OFFSET_BEGINNING
from .producer import proceed_to_deliver

MODULE_NAME: str = os.getenv("MODULE_NAME")

def to_drivers(id, details):
    proceed_to_deliver(id, {
        "deliver_to": "drivers-robot",
        "operation": "pull",
        "data": "pull drivers"
    })
    print(f"[DEBUG] Pulling drivers")

def to_nav(id, details):
    print("[DEBUG] Drivers is ready...")
    proceed_to_deliver(id, {
        "deliver_to": "nav-robot",
        "operation": "get_nav",
        "data": "get_coords"
    })
    print(f"[DEBUG] Pulling drivers")

def to_controller(id, details):
    print("[DEBUG] Command to valid", details["data"])
    proceed_to_deliver(id, {
        "deliver_to": "controller-robot",
        "operation": "to_valid",
        "data": details["data"]
    })
    print(f"[DEBUG] Send to Controller: ", details["data"])

def to_audio(id, details):
    print("[DEBUG] Report: ", details["data"])
    proceed_to_deliver(id, {
        "deliver_to": "speakers-robot",
        "operation": "to_audio",
        "data": "Robot says something....."
    })
    print(f"[DEBUG] Send to Speakers: ", details["data"])
    
commands = {
    "valid_data": to_drivers,
    "push": to_nav,
    "send_coords": to_controller,
    "report_to_sys": to_audio
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