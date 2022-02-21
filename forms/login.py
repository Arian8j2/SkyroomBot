from PyQt5.QtWidgets import (QWidget, QFormLayout, QVBoxLayout,
                             QPushButton, QLabel, QLineEdit, QGroupBox)
from typing import Dict

class Login(QWidget):
    def __init__(self, on_confirm):
        super().__init__()

        self.on_confirm = on_confirm
        self.line_edits: Dict[str, QLineEdit] = dict()
        self.ui()

    def ui(self):
        self.setGeometry(100, 100, 300, 400)

        # form section
        form = QGroupBox("Form")
        form_layout = QFormLayout()

        lines_name = ["url", "username", "password", "token"]

        for name in lines_name:
            self.line_edits[name] = QLineEdit()

            if name == "password" or name == "token":
                self.line_edits[name].setEchoMode(QLineEdit.Password)

            form_layout.addRow(QLabel(name), self.line_edits[name])
        
        form.setLayout(form_layout)

        # button
        button = QPushButton("Confirm")
        button.clicked.connect(self.on_confirm)

        # final layout
        layout = QVBoxLayout()
        layout.addWidget(form)
        layout.addWidget(button)
        self.setLayout(layout)