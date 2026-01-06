from flask import Flask, request, jsonify, render_template_string
from collections import deque
import time

app = Flask(__name__)

roblox_queue = deque(maxlen=100)
recent_messages = deque(maxlen=50)

@app.route("/api/roblox-to-discord", methods=["POST"])
def roblox_to_discord():
    data = request.json
    msg = {
        "from": "Roblox",
        "sender": data.get("sender"),
        "message": data.get("message"),
        "time": time.strftime("%H:%M:%S")
    }
    roblox_queue.append(msg)
    recent_messages.appendleft(msg)
    return {"status": "ok"}

@app.route("/api/discord-to-roblox", methods=["POST"])
def discord_to_roblox():
    data = request.json
    msg = {
        "from": "Discord",
        "sender": data.get("sender"),
        "message": data.get("message"),
        "time": time.strftime("%H:%M:%S")
    }
    roblox_queue.append(msg)
    recent_messages.appendleft(msg)
    return {"status": "ok"}

@app.route("/api/get-for-roblox", methods=["GET"])
def get_for_roblox():
    msgs = list(roblox_queue)
    roblox_queue.clear()
    return jsonify(msgs)

@app.route("/dashboard")
def dashboard():
    return render_template_string("""
    <html>
    <head>
        <title>Relay Dashboard</title>
        <meta http-equiv="refresh" content="2">
        <style>
            body { font-family: Arial; background: #111; color: #eee; }
            .msg { padding: 6px; border-bottom: 1px solid #333; }
            .roblox { color: #4CAF50; }
            .discord { color: #7289DA; }
        </style>
    </head>
    <body>
        <h2>Relay Status</h2>
        <p>Queue size: {{ queue_size }}</p>
        <hr>
        {% for m in messages %}
            <div class="msg {{ m.from|lower }}">
                [{{ m.time }}] <b>{{ m.from }}</b> —
                <b>{{ m.sender }}</b>: {{ m.message }}
            </div>
        {% endfor %}
    </body>
    </html>
    """, messages=recent_messages, queue_size=len(roblox_queue))
