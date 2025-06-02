import os

from flask import Flask, request, jsonify

MODULE_NAME: str = os.getenv("MODULE_NAME")
app = Flask(__name__)

received_logs = []

@app.route("/logs", methods=["POST"])
def receive_logs():
    details = request.json
    global received_logs
    received_logs.append(details)

    print(f"[{MODULE_NAME}] Report: {details}", flush=True)

    return {"status": "OK"}, 200

@app.route("/logs", methods=["GET"])
def get_logs():
    return jsonify(received_logs), 200

def main():
    app.run(host="0.0.0.0", port = "8012")