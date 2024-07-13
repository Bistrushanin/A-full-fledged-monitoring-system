from flask import Flask, request
import requests

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = '6955358415:AAElhspQEj42MN_GrJZFygvweEh4iqEo45Q'
TELEGRAM_CHAT_ID = '430815428'

@app.route('/alert', methods=['POST'])
def alert():
    data = request.json
    message = f"Alert: {data['alerts'][0]['annotations']['summary']}\nDescription: {data['alerts'][0]['annotations']['description']}"
    send_telegram_message(message)
    return '', 200

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message
    }
    requests.post(url, json=payload)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
