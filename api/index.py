"""
template from: https://gist.github.com/mdonkers/63e115cc0c79b4f6b8b3a6b797e485c7
License: MIT License
Copyright (c) 2023 Miel Donkers
Very simple HTTP server in python for logging requests
Usage::
    ./server.py [<port>]
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import json
from dotenv import load_dotenv
import os
import requests

load_dotenv()

BOT_URL = f"https://api.telegram.org/bot{os.getenv('BOT_TOKEN')}"


class handler(BaseHTTPRequestHandler):

    client_chat_id = ""
    jian_kai_memes_photo_id = [
        "AgACAgUAAxkBAAIBLGRWLvdJZk7cNG5zC3w832c8rToUAAKltTEbEwe5Vp-zoAEknAvdAQADAgADcwADLwQ",
        "AgACAgUAAxkBAAIBMWRWNBdMA8zrrLbkTliSTaW1Bai7AAKptTEbEwe5VkZDnCnDKuj3AQADAgADcwADLwQ"
    ]

    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path),
                     str(self.headers))
        self._set_response()
        self.wfile.write(
            "this is the api for devpandaz telegram bot\n".encode('utf-8'))
        # self.wfile.write("GET request for {}".format(
        # self.path).encode('utf-8'))

    def reply_user(self, data):
        requests.post(f'{BOT_URL}/sendMessage',
                      json={
                          "chat_id": self.client_chat_id,
                          **data,
                      })

    def do_POST(self):
        content_length = int(
            self.headers['Content-Length'])  # <--- Gets the size of data
        post_data = self.rfile.read(
            content_length)  # <--- Gets the data itself
        # logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
        #              str(self.path), str(self.headers),
        #              post_data.decode('utf-8'))

        self._set_response()
        self.wfile.write("POST request for {}".format(
            self.path).encode('utf-8'))

        data = json.loads(post_data.decode('utf-8'))
        print(json.dumps(data, indent=4))

        if "message" in data:

            # settings client chat id if havent already
            self.client_chat_id = data['message']['chat']['id']

            received = data['message']
            if "text" in received:
                try:
                    if received['entities'][0]['type'] == "bot_command":
                        user_command = received['text'][1:]
                        if user_command == 'anime_quote':
                            anime_quote_data = requests.get(
                                'https://animechan.vercel.app/api/random'
                            ).json()
                            self.reply_user({
                                "text":
                                f'"{anime_quote_data["quote"]}"\n\n---- a quote from {anime_quote_data["character"]} ({anime_quote_data["anime"]})',
                            })

                        if user_command == "jiankai":
                            self.reply_user(
                                {"text": 'here are some jian kai memes:'})
                            for photo_id in self.jian_kai_memes_photo_id:
                                requests.post(f'{BOT_URL}/sendPhoto',
                                              json={
                                                  "chat_id":
                                                  self.client_chat_id,
                                                  "photo": photo_id,
                                              })

                        if user_command == "page":
                            self.reply_user({
                                "text": "Page 1",
                                "reply_markup": {
                                    "inline_keyboard": [
                                        [
                                            {
                                                "text": "next page",
                                                "callback_data": "page 2"
                                            },
                                        ],
                                    ]
                                }
                            })

                except KeyError:
                    self.reply_user({
                        "text":
                        "hello! you can get a list of commands by pressing the menu button. "
                    })

        if "callback_query" in data:
            callback_query = data['callback_query']
            if callback_query['data'] == 'page 1':
                requests.post(f'{BOT_URL}/editMessageText',
                              json={
                                  "chat_id":
                                  callback_query['from']['id'],
                                  "message_id":
                                  callback_query['message']['message_id'],
                                  "text":
                                  "Page 1",
                                  "reply_markup": {
                                      "inline_keyboard": [
                                          [
                                              {
                                                  "text": "next page",
                                                  "callback_data": "page 2"
                                              },
                                          ],
                                      ]
                                  }
                              })
                requests.post(f'{BOT_URL}/answerCallbackQuery',
                              json={"callback_query_id": callback_query['id']})

            if callback_query['data'] == 'page 2':
                requests.post(f'{BOT_URL}/editMessageText',
                              json={
                                  "chat_id":
                                  callback_query['from']['id'],
                                  "message_id":
                                  callback_query['message']['message_id'],
                                  "text":
                                  "Page 2",
                                  "reply_markup": {
                                      "inline_keyboard": [
                                          [
                                              {
                                                  "text": "previous page",
                                                  "callback_data": "page 1"
                                              },
                                          ],
                                      ]
                                  }
                              })
                requests.post(f'{BOT_URL}/answerCallbackQuery',
                              json={"callback_query_id": callback_query['id']})


def run(server_class=HTTPServer, handler_class=handler, port=8080):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')


if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
