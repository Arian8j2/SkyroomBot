from PyQt5.QtWidgets import (QGridLayout, QGroupBox, QVBoxLayout,
                             QVBoxLayout, QTextBrowser, QWidget, QListWidget)

from typing import Optional, Dict

class Logs(QWidget):
    def __init__(self):
        super().__init__()
        self.text_browsers: Dict[str, QTextBrowser] = dict()
        self.users: Optional[QListWidget] = None
        self.ui()

    def ui(self):
        group_names = ["all", "users", "messages"]
        groups = list()

        for name in group_names:

            if name == "users":
                self.users = QListWidget()
                widget = self.users
            else:
                self.text_browsers[name] = QTextBrowser()
                widget = self.text_browsers[name]

            group_layout = QVBoxLayout()
            group_layout.addWidget(widget)

            group = QGroupBox(name)
            group.setLayout(group_layout)

            groups.append(group)

        grid = QGridLayout()
        grid.addWidget(groups[0], 1, 1, 2, 1)
        grid.addWidget(groups[1], 1, 2)
        grid.addWidget(groups[2], 2, 2)

        self.setLayout(grid)
