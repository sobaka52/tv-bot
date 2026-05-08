from flask import Flask, request
from openai import OpenAI
import requests
import os
import traceback

app = Flask(__name__)

# ENV VARIABLES
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# OPENAI CLIENT
client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = """
Ты трейдинг-фильтр.

Отвечай только одним словом:
VALID
или
SKIP

Правило:
Сигнал должен иметь минимум 2 подтверждения.

Подтверждения:
- Тренд (SMA 50)
- RSI не экстремум (30-70)
- Уровень (поддержка/сопротивление)
- Импульс / пробой / паттерн

Важно:
- Импульс и тренд приоритетны
- Если есть сомнение -> SKIP
- Если флэт -> SKIP
- Избегай слабых сигналов

Если меньше 2 подтверждений -> SKIP
"""

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    requests.post(url, json={
        "chat_id": CHAT_ID,
        "text": text
    })

@app.route("/")
def home():
    return "Bot running", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json(force=True) or {}

        signal = data.get("text", "")

        print("SIGNAL:", signal)

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": signal}
            ]
        )

        decision = response.choices[0].message.content.strip()

        print("DECISION:", decision)

        if "VALID" in decision:
            send_telegram(f"✅ {decision}\n\n{signal}")
        else:
            send_telegram("❌ SKIP")

        return "ok", 200

    except Exception as e:
        print("ERROR:")
        traceback.print_exc()
        return str(e), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
