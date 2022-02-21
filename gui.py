from json import loads
from threading import Thread
from typing import Dict

from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QListWidgetItem

from forms.login import Login
from forms.logs import Logs

from skyroom_bot import SkyroomBot

class Gui:
    def __init__(self):
        self.app = QApplication([])
        self.login_form = Login(self.on_login_confirm)
        self.logs_form = Logs()
        self.users_list_items: Dict[int, QListWidgetItem] = dict()

    def run(self):
        self.login_form.show()
        self.app.exec()

    def on_login_confirm(self):
        inputs = [line.text() for line in self.login_form.line_edits.values()]
        self.skyroom_bot = SkyroomBot(*inputs, self.on_skyroom_message)

        Thread(target= self.skyroom_bot.ws.run_forever).start()
        self.app.aboutToQuit.connect(self.skyroom_bot.ws.close)

        self.login_form.close()
        self.logs_form.show()

    def on_skyroom_message(self, msg: str):
        self.logs_form.text_browsers["all"].append(msg)

        loaded_msg = loads(msg)
        if type(loaded_msg) != list:
            return

        section, action = loaded_msg[1:3]
        if len(loaded_msg) > 3:
            info = loaded_msg[3]

        if section == "chat" and action == "message-new":
            nickname, text = info["nickname"], info["text"]

            self.logs_form.text_browsers["messages"].append(f"{nickname}: {text}")

        if section == "user":
            def add_user(user_info):
                item = QListWidgetItem(user_info["nickname"])
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsSelectable)
                item.setTextAlignment(Qt.AlignRight)

                # make operators blue
                if user_info["role"] != 1:
                    item.setForeground(QColor(0, 0, 255, 255))

                self.users_list_items[user_info["id"]] = item
                self.logs_form.users.addItem(item)

            if action == "join":
                for user in info["room"]["users"].values():
                    add_user(user)

            elif action == "user-joined":
                add_user(info)

            elif action == "user-left" and info["id"] in self.users_list_items:
                item = self.users_list_items[info["id"]]
                row = self.logs_form.users.row(item)
                self.logs_form.users.takeItem(row)

if __name__ == "__main__":
    gui = Gui()
    gui.run()