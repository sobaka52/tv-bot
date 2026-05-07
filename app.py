from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot running"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    print(data)

    return "ok", 200
