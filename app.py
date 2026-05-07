from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot running", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)

    print("===== WEBHOOK RECEIVED =====")
    print(data)

    return "ok", 200