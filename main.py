from flask import Flask, request
from dotenv import load_dotenv
import requests
import logging
import hashlib
import hmac
import os

load_dotenv()

BOT_TOKEN = os.getenv('API_TOKEN')
CHANNELS = [
    '-1001928643461'
]

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route('/webhook', methods=['POST'])
def webhook():
    signature = request.headers.get('X-Hub-Signature')
    
    if signature:
        secret = bytes(os.getenv('GITHUB_WEBHOOK_SECRET'), 'utf-8')
        digest = 'sha1=' + hmac.new(secret, request.data, hashlib.sha1).hexdigest()

        if not hmac.compare_digest(signature, digest):
            return 'Invalid signature', 403
    else:
        return 'No signature provided', 403

    try:
        data = request.json
        handle_webhook(data)
    except KeyError as e:
        logging.error(f"Missing key in request data: {e}")
    except requests.RequestException as e:
        logging.error(f"Error sending message to Telegram: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")

    return ''

def handle_webhook(data):
    if data['action'] == 'labeled' and data['label']['name'] == 'approved':
        number = data['issue']['number']
        html_url = data['issue']['html_url']

        for chat_id in CHANNELS:
            send_message(chat_id, number, html_url)

def send_message(chat_id, number, html_url):
    response = requests.get('https://api.telegram.org/bot{}/sendMessage'.format(BOT_TOKEN), params=dict(
        chat_id=chat_id,
        text=f'[Footstep \\#{number}]({html_url}) was just approved\\!\nTake a look at the description and if the task seems interesting to you, offer yourself in the comments to complete it\\.',
        parse_mode='MarkdownV2'
    ))

    response.raise_for_status()

app.run(host='0.0.0.0', port=8000)
