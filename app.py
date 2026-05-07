from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot running", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json(force=True)

        print("===== WEBHOOK RECEIVED =====")
        print(data)

        return "ok", 200

    except Exception as e:
        print("ERROR:", str(e))
        return "error", 200
