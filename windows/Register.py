from PyQt5.QtWidgets import *

import styles
from database.connection import get_connection
from windows.Malumotlar_Oynasi import Info_Window


class Register_Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(600, 250, 500, 500)
        self.setWindowTitle("Ro'yxatdan o'tish oynasi")

        self.full_name = QLineEdit()
        self.full_name.setPlaceholderText("Full name")

        self.age = QLineEdit()
        self.age.setPlaceholderText("Enter student's age")

        self.major = QLineEdit()
        self.major.setPlaceholderText("Enter student's major")

        self.username = QLineEdit()
        self.username.setPlaceholderText("Enter username")

        self.password = QLineEdit()
        self.password.setPlaceholderText("Enter password")

        self.signUp = QPushButton("Ro'yxatdan o'tish")
        self.signUp.setStyleSheet(styles.QPushButton_styles)
        self.signUp.clicked.connect(self.signUp_clicked)

        line_edits = [
            self.full_name,
            self.age,
            self.major,
            self.username,
            self.password
        ]

        for line_edit in line_edits:
            line_edit.setStyleSheet(styles.QLineEdit_styles)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.full_name)
        main_layout.addWidget(self.age)
        main_layout.addWidget(self.major)
        main_layout.addWidget(self.username)
        main_layout.addWidget(self.password)
        main_layout.addWidget(self.signUp)

        self.setLayout(main_layout)

    def signUp_clicked(self):
        if not all([self.full_name.text(), self.age.text(), self.major.text(), self.username.text(), self.password.text()]):
            QMessageBox.warning(self, "Warning", "Iltimos barcha qatorlarni to'ldiring!")

            return

        connection = get_connection()
        if connection.is_connected():
            try:
                cursor = connection.cursor()
                cursor.execute("""
                    INSERT IGNORE INTO users(full_name, age, major, username, password) VALUES
                    (%s, %s, %s, %s, %s)
                """, (self.full_name.text(),
                      self.age.text(),
                      self.major.text(),
                      self.username.text(),
                      self.password.text()))

                connection.commit()
                cursor.close()
                connection.close()

                res = QMessageBox.information(self, "Information", "Siz muvaffaqiyatli ro'yxatdan o'ttingiz!")

                if res:
                    self.info_window = Info_Window()
                    self.info_window.show()

                    self.close()

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Ro'yxatdan o'tishda xatolik yuz berdi: {e}")
        else:
            QMessageBox.critical(self, "Error", "Ma'lumotlar bazasiga ulanishda xatolik yuz berdi!")



