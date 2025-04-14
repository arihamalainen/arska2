from flask import Flask
import requests
import os

app = Flask(__name__)

HA_URL = os.getenv("HA_URL", "")
TOKEN = os.getenv("HA_TOKEN", "")
ENTITY = os.getenv("HA_ENTITY", "")

print(f"DEBUG: HA_URL = {HA_URL}")
print(f"DEBUG: TOKEN = {TOKEN[:5]}...")  # Ei printata koko tokenia!
print(f"DEBUG: ENTITY = {ENTITY}")

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

@app.route("/on", methods=["GET"])
def turn_on():
    if not HA_URL or not TOKEN or not ENTITY:
        return "Missing HA_URL, TOKEN or ENTITY", 500
    try:
        r = requests.post(f"{HA_URL}/api/services/switch/turn_on",
                          headers=headers,
                          json={"entity_id": ENTITY})
        return f"ON: {r.status_code} {r.text}", r.status_code
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route("/off", methods=["GET"])
def turn_off():
    if not HA_URL or not TOKEN or not ENTITY:
        return "Missing HA_URL, TOKEN or ENTITY", 500
    try:
        r = requests.post(f"{HA_URL}/api/services/switch/turn_off",
                          headers=headers,
                          json={"entity_id": ENTITY})
        return f"OFF: {r.status_code} {r.text}", r.status_code
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
