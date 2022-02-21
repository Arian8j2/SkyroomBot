import logging
from requests import post
from json import loads, dumps
from time import time
from websocket import WebSocketApp
from threading import Thread
from typing import Callable

class SkyroomBot:
    def __init__(self, url: str, username: str, password: str, token: str, on_message: Callable[[str], None] = None):
        self.is_opened = False
        self.username = username
        self.password = password
        self.token = token

        self.url = url
        self.gather_data_from_url()

        self.logger = logging.getLogger(__class__.__name__)
        if on_message == None:
            on_message = self.on_message

        self.ws = WebSocketApp(self.websocket_addr, \
            on_open    = lambda ws: self.on_open(), \
            on_message = lambda ws, msg: on_message(msg),\
            on_close   = lambda ws: self.on_close()
        )

    def gather_data_from_url(self):
        if self.url[-1] == '/':
            self.url[: len(self.url) - 1]

        url_split = self.url.split("/")
        room = url_split[-1]
        customer = url_split[-2]

        data = '------WebKitFormBoundaryLYlCWZpm2cRdPd4B\r\nContent-Disposition: form-data; name="customer"\r\n\r\n%s\r\n------WebKitFormBoundaryLYlCWZpm2cRdPd4B\r\nContent-Disposition: form-data; name="room"\r\n\r\n%s\r\n------WebKitFormBoundaryLYlCWZpm2cRdPd4B\r\nContent-Disposition: form-data; name="gadget"\r\n\r\nSkyroom\r\n------WebKitFormBoundaryLYlCWZpm2cRdPd4B\r\nContent-Disposition: form-data; name="action"\r\n\r\nFetchRoom\r\n------WebKitFormBoundaryLYlCWZpm2cRdPd4B--\r\n' \
            % (customer, room)
        headers = {
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36",
            "content-type": "multipart/form-data; boundary=----WebKitFormBoundaryLYlCWZpm2cRdPd4B",
        }

        res = post("%s?%d" % (self.url, time()*1000), data=data, headers=headers)
        if res.status_code != 200:
            raise Exception("Invalid skyroom url")

        res = loads(res.content)["result"]
        self.customer_id = res["customer_id"]
        self.room_id = res["room_id"]
        self.websocket_addr = str(res["server"]).replace("https", "wss")

    def on_open(self):
        self.is_opened = True
        self.join_room()
        Thread(target=self.keep_alive).start()

    def on_message(self, msg: str):
        self.logger.info(msg)

    def send_chat(self, msg):
        msg_info = {
            "id": int(time()),
            "text": msg
        }
        self.ws.send(dumps(["s", "chat", "message-new", msg_info]))

    def on_close(self):
        self.is_opened = False

    def join_room(self):
        payload = [
            "s", "user", "join", {
                "origin": "www.skyroom.online",
                "app_id": "27642275",
                "room_id": self.room_id,
                "customer_id": self.customer_id,
                "username": self.username,
                "password": self.password,
                "token": self.token,
                "nickname": "",
                "platform": {
                    "version":"12.4.8",
                    "os": 1,
                    "browser": 0
                }
            }
        ]

        self.ws.send(dumps(payload))
        self.logger.info("Joined room")

    def keep_alive(self):
        alive_expire = time() + 5
        while self.is_opened:
            if alive_expire < time():
                self.ws.send("imalive")
                alive_expire = time() + 5
        
        self.logger.info("Connection closed!")

if __name__ == "__main__":
    url = input("url e kellaseto vared kon (https://www.skyroom.online/ch/madresegholam/shimi): ")
    username = input("username (140210743, skip if using token): ")
    password = input("password (140210743, skip if using token): ")

    token = str()
    if len(username) == 0:
        token = input("token (140210743, skip if using token): ")

    logging.basicConfig(level=logging.INFO, format="[%(name)s] %(message)s")
    bot = SkyroomBot(url, username, password, token)
    bot.ws.run_forever()