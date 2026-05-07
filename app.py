from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot running", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.data.decode("utf-8")

    print("WEBHOOK:")
    print(data)

    return "ok", 200