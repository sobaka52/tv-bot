from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def home():
    return "WORKING"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    print(data)
    return {"ok": True}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
