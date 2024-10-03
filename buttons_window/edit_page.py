from PyQt5.QtWidgets import *
from database.connection import get_connection
from PyQt5.QtCore import Qt
import styles


class Edit_Page(QDialog):
    def __init__(self, parent, student_id):
        super().__init__()

        self.id = student_id
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT * FROM users WHERE id = %s
        """, (student_id, ))

        data = cursor.fetchone()

        self.setWindowTitle("Edit Page")
        self.setMinimumSize(300, 300)

        self.title = QLabel("Edit Student")
        self.title.setStyleSheet("font-size: 20px;")
        self.title.setAlignment(Qt.AlignCenter)

        self.full_name = QLineEdit()
        self.full_name.setText(data[1])

        self.age = QLineEdit()
        self.age.setText(str(data[2]))

        self.major = QLineEdit()
        self.major.setText(data[3])

        self.username = QLineEdit()
        self.username.setText(data[4])

        self.password = QLineEdit()
        self.password.setText(data[5])

        self.submit_btn = QPushButton("submit")
        self.submit_btn.setStyleSheet(styles.QPushButton_styles)
        self.submit_btn.clicked.connect(self.submit_clicked)

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
                UPDATE users SET full_name = %s, age = %s, major = %s, username = %s, password = %s WHERE id = %s
            """, (full_name, age, major, username, password, self.id))

            connection.commit()
            self.accept()
        else:
            QMessageBox.warning(self, "Warning", "Iltimos barcha qatorlarni to'ldiring!")