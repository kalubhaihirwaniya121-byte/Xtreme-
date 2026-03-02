from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
APP_PIN = os.getenv("APP_PIN")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json

    if data.get("pin") != APP_PIN:
        return jsonify({"error": "Unauthorized"}), 401

    user_message = data.get("message")

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "You are Xtreme, a private AI assistant."},
            {"role": "user", "content": user_message}
        ]
    }

    r = requests.post(
        "https://api.deepseek.com/v1/chat/completions",
        headers=headers,
        json=payload,
        timeout=30
    )

    reply = r.json()["choices"][0]["message"]["content"]
    return jsonify({"reply": reply})

@app.route("/")
def home():
    return "Xtreme backend running"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
