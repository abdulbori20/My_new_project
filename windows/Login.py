from PyQt5.QtWidgets import *

import styles
from database.connection import get_connection
from windows.Malumotlar_Oynasi import Info_Window


class Login_Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(600, 250, 500, 500)
        self.setWindowTitle("Tizimga kirish oynasi")

        self.username = QLineEdit()
        self.username.setPlaceholderText("Enter username")
        self.username.setStyleSheet(styles.QLineEdit_styles)

        self.password = QLineEdit()
        self.password.setStyleSheet(styles.QLineEdit_styles)
        self.password.setPlaceholderText("Enter password")

        self.kirish = QPushButton("Login")
        self.setStyleSheet(styles.QPushButton_styles)
        self.kirish.clicked.connect(self.kirish_clicked)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.username)
        main_layout.addWidget(self.password)
        main_layout.addWidget(self.kirish)

        self.setLayout(main_layout)

    def kirish_clicked(self):
        username = self.username.text()
        password = self.password.text()

        if not all([username, password]):
            QMessageBox.warning(self, "Warning", "Iltimos barcha qatorlarni to'ldiring!")
            return

        connection = get_connection()
        if connection.is_connected():
            try:
                cursor = connection.cursor()
                cursor.execute("""
                    SELECT * FROM users WHERE username = %s and password = %s
                """, (username, password))
                data = cursor.fetchone()
                cursor.close()
                connection.close()

                QMessageBox.information(self, "Information", "Siz tizimga muvaffaqiyatli kirdingiz!")

                if data:
                    self.info_window = Info_Window()
                    self.info_window.show()

                    self.close()
                else:
                    QMessageBox.warning(self, "Warning", "Username yoki password noto'g'ri!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Login qilishda xatolik yuz berdi: {e}")
        else:
            QMessageBox.critical(self, "Error", "Ma'lumotlar bazasiga ulanishda xatolik yuz berdi!")