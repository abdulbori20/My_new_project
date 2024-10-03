from database.database_main import init_db
from PyQt5.QtWidgets import *
from windows.Register import Register_Window
from windows.Login import Login_Window
from PyQt5.QtCore import Qt
import sys
import styles

init_db()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(600, 250, 600, 600)
        self.setWindowTitle("Asosiy oyna")

        self.title = QLabel("Bosh sahifa")
        self.title.setStyleSheet("font-size: 20px;")
        self.title.setAlignment(Qt.AlignCenter)

        self.login = QPushButton("Tizimga kirish")
        self.login.setStyleSheet(styles.QPushButton_styles)
        self.login.clicked.connect(self.login_clicked)

        self.register = QPushButton("Ro'yxatdan o'tish")
        self.register.setStyleSheet(styles.QPushButton_styles)
        self.register.clicked.connect(self.register_clicked)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.title)
        main_layout.addWidget(self.login)
        main_layout.addWidget(self.register)

        self.setLayout(main_layout)

    def login_clicked(self):
        self.login = Login_Window()
        self.login.show()

        self.close()

    def register_clicked(self):
        self.register = Register_Window()
        self.register.show()

        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = MainWindow()
    main.show()

    sys.exit(app.exec_())
