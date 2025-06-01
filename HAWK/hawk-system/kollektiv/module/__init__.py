import os

from flask import Flask, request

MODULE_NAME: str = os.getenv("MODULE_NAME")
app = Flask(__name__)

@app.route("/logs", methods=["POST"])
def receive_logs():
    details = request.json

    print(f"[{MODULE_NAME}] Report: {details}", flush=True)

    return {"status": "OK"}, 200

def main():
    app.run(host="0.0.0.0", port = "8012")