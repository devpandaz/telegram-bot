from bottle import run, post, request, response
from dotenv import load_dotenv
import os
import requests

load_dotenv()

BOT_URL = f"https://api.telegram.org/bot{os.getenv('BOT_TOKEN')}"


@post('/')
def main():
    data = request.json
    requests.post(f'{BOT_URL}/sendMessage',
                  json={
                      "chat_id": data['message']['chat']['id'],
                      "text": data['message']['text'][::-1],
                  })
    return response


if __name__ == "__main__":
    run(host='0.0.0.0', port=80)
