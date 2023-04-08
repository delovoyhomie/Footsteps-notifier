from flask import Flask, request
import requests
import json

token = 'YOUR-TOKEN-BOT'

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        data = request.json
        print(data)
        
        text = ''
        
        n = 1
        arr = ['-1000000000000']
        for chat_id in arr:
            response = requests.get('https://api.telegram.org/bot{}/sendMessage'.format(token), params=dict(
                chat_id = chat_id,
                text = text,
                parse_mode= 'markdown'
            )) 
            print(response.text)
        return 'GOOD!'
    else:
        return 'BAD!'

app.run(host='0.0.0.0', port=8000) 
