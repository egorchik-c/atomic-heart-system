import os
import json
import multiprocessing
import threading

from uuid  import uuid4
from confluent_kafka import Producer
from random import choice
from time import sleep

MODULE_NAME: str = os.getenv("MODULE_NAME")
requests_queue: multiprocessing.Queue = None

def get_video():
    while True:
        command = {"password": "monkey1234", "access_card": "valid", "command": "reboot"}

        print(f"[{MODULE_NAME}] Initiate to send command: {command["command"]}")

        proceed_to_deliver(uuid4().__str__(), {
            "deliver_to": "authentication",
            "operation": "send_pass",
            "data": command
        })

        proceed_to_deliver(uuid4().__str__(), {
            "deliver_to": "validator-card",
            "operation": "send_card",
            "data": command
        })

        sleep(10)

def proceed_to_deliver(id, details):
    details["id"] = id
    details["source"] = MODULE_NAME
    requests_queue.put(details)

def producer_job(_, config, request_queue: multiprocessing.Queue):
    producer = Producer(config)

    threading.Thread(target=get_video).start()
    def delivery_callback(err, msg):
        if err:
            print(f"[ERROR] Message failed delivery: {err}")

    topic = "monitor"
    while True:
        event_details = request_queue.get()
        producer.produce(
            topic,
            json.dumps(event_details),
            event_details["id"],
            callback=delivery_callback
        )
        producer.poll(35000)
        producer.flush()
        print(f"[{MODULE_NAME}] Send data: {event_details}")

def start_producer(args, config, request_queue):
    print(f"[{MODULE_NAME}] Producer started...")

    global requests_queue

    requests_queue = request_queue

    threading.Thread(
        target=lambda: producer_job(args, config, request_queue)
    ).start()