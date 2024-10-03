from PyQt5.QtWidgets import *

import styles
from database.connection import get_connection
from PyQt5.QtCore import Qt


class Add_Page(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Page")
        self.setMinimumSize(300, 300)

        self.title = QLabel("Add Student")
        self.title.setStyleSheet("font-size: 20px;")
        self.title.setAlignment(Qt.AlignCenter)

        self.full_name = QLineEdit()
        self.full_name.setPlaceholderText("Enter student's full name")

        self.age = QLineEdit()
        self.age.setPlaceholderText("Enter student's age")

        self.major = QLineEdit()
        self.major.setPlaceholderText("Enter student's major")

        self.username = QLineEdit()
        self.username.setPlaceholderText("Enter student's username")

        self.password = QLineEdit()
        self.password.setPlaceholderText("Enter password")

        line_edits = [
            self.full_name,
            self.age,
            self.major,
            self.username,
            self.password
        ]

        for line_edit in line_edits:
            line_edit.setStyleSheet(styles.QLineEdit_styles)

        self.submit_btn = QPushButton("submit")
        self.submit_btn.setStyleSheet(styles.QPushButton_styles)
        self.submit_btn.clicked.connect(self.submit_clicked)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.title)
        main_layout.addWidget(self.full_name)
        main_layout.addWidget(self.age)
        main_layout.addWidget(self.major)
        main_layout.addWidget(self.username)
        main_layout.addWidget(self.password)
        main_layout.addWidget(self.submit_btn)

        self.setLayout(main_layout)

    def submit_clicked(self):
        connection = get_connection()
        cursor = connection.cursor()

        full_name = self.full_name.text()
        age = self.age.text()
        major = self.major.text()
        username = self.username.text()
        password = self.password.text()

        if all([full_name, age, major, username, password]):
            cursor.execute("""
                INSERT IGNORE INTO users(full_name, age, major, username, password) VALUES
                (%s, %s, %s, %s, %s)
            """, (full_name, age, major, username, password))
            connection.commit()
            cursor.close()
            connection.close()
            self.accept()
        else:
            QMessageBox.warning(self, "Warning", "Iltimos barcha qatorlarni to'ldiring!")