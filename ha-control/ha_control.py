from flask import Flask
import requests
import json

app = Flask(__name__)

# Lue HA:n lisäosan asetukset suoraan /data/options.json
with open("/data/options.json", "r") as f:
    options = json.load(f)

HA_URL = options.get("ha_url", "")
TOKEN = options.get("ha_token", "")
ENTITY = options.get("ha_entity", "")

print(f"🔧 HA_URL: {HA_URL}")
print(f"🔐 TOKEN: {TOKEN[:5]}... (piilotettu)")
print(f"💡 ENTITY: {ENTITY}")

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

@app.route("/on", methods=["GET"])
def turn_on():
    if not HA_URL or not TOKEN or not ENTITY:
        return "❌ Missing HA_URL, TOKEN or ENTITY", 500
    try:
        r = requests.post(f"{HA_URL}/api/services/switch/turn_on",
                          headers=headers,
                          json={"entity_id": ENTITY})
        return f"✅ ON: {r.status_code} {r.text}", r.status_code
    except Exception as e:
        return f"❌ Error: {str(e)}", 500

@app.route("/off", methods=["GET"])
def turn_off():
    if not HA_URL or not TOKEN or not ENTITY:
        return "❌ Missing HA_URL, TOKEN or ENTITY", 500
    try:
        r = requests.post(f"{HA_URL}/api/services/switch/turn_off",
                          headers=headers,
                          json={"entity_id": ENTITY})
        return f"✅ OFF: {r.status_code} {r.text}", r.status_code
    except Exception as e:
        return f"❌ Error: {str(e)}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
