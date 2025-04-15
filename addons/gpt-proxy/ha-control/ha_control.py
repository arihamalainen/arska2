
import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

HF_API_KEY = os.getenv("HF_API_KEY")
MODEL_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"

HEADERS = {"Authorization": f"Bearer {HF_API_KEY}"}

@app.route("/gpt", methods=["POST"])
def gpt_handler():
    data = request.json
    question = data.get("question", "")
    if not question:
        return jsonify({"error": "Missing question"}), 400

    payload = {
        "inputs": f"User: {question}
Assistant:",
        "parameters": {"max_new_tokens": 100, "return_full_text": False}
    }

    try:
        response = requests.post(MODEL_URL, headers=HEADERS, json=payload)
        response.raise_for_status()
        answer = response.json()[0]["generated_text"]
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
