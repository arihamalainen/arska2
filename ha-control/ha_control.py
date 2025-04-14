from flask import Flask
import requests
import os

app = Flask(__name__)

HA_URL = os.getenv("HA_URL")
TOKEN = os.getenv("HA_TOKEN")
ENTITY = os.getenv("HA_ENTITY")

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

@app.route("/on", methods=["GET"])
def turn_on():
    r = requests.post(f"{HA_URL}/api/services/switch/turn_on",
                      headers=headers,
                      json={"entity_id": ENTITY})
    return f"ON: {r.status_code} {r.text}", r.status_code

@app.route("/off", methods=["GET"])
def turn_off():
    r = requests.post(f"{HA_URL}/api/services/switch/turn_off",
                      headers=headers,
                      json={"entity_id": ENTITY})
    return f"OFF: {r.status_code} {r.text}", r.status_code

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
