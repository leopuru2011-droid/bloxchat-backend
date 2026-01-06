from flask import Flask, request, jsonify
from collections import deque
import time

app = Flask(__name__)

# Messages waiting to be delivered to Roblox
roblox_queue = deque(maxlen=100)

@app.route("/api/roblox-to-discord", methods=["POST"])
def roblox_to_discord():
    data = request.json
    if not data:
        return {"error": "Invalid payload"}, 400

    # Forwarded to Discord bot via polling
    roblox_queue.append({
        "sender": data.get("sender"),
        "message": data.get("message"),
        "timestamp": int(time.time())
    })
    return {"status": "ok"}

@app.route("/api/discord-to-roblox", methods=["POST"])
def discord_to_roblox():
    data = request.json
    if not data:
        return {"error": "Invalid payload"}, 400

    roblox_queue.append({
        "sender": data.get("sender"),
        "message": data.get("message"),
        "timestamp": int(time.time())
    })
    return {"status": "ok"}

@app.route("/api/get-for-roblox", methods=["GET"])
def get_for_roblox():
    messages = list(roblox_queue)
    roblox_queue.clear()
    return jsonify(messages)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
