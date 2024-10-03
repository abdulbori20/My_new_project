from PyQt5.QtWidgets import *

import styles
from database.connection import get_connection
from buttons_window.add_page import Add_Page
from buttons_window.edit_page import Edit_Page


class Info_Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(550, 250, 850, 700)
        self.setWindowTitle("Ma'lumotlar oynasi")

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("search...")
        self.search_input.textChanged.connect(self.search_clicked)
        self.search_input.setStyleSheet(styles.QLineEdit_styles)

        self.add_btn = QPushButton("add")
        self.add_btn.clicked.connect(self.add_clicked)

        self.edit_btn = QPushButton("edit")
        self.edit_btn.clicked.connect(self.edit_clicked)

        self.delete_btn = QPushButton("delete")
        self.delete_btn.clicked.connect(self.delete_clicked)

        buttons = [
            self.add_btn,
            self.edit_btn,
            self.delete_btn
        ]

        for button in buttons:
            button.setStyleSheet(styles.QPushButton_styles)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["id", "full_name", "age", "major", "username", "password"])
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)

        container1 = QHBoxLayout()
        container1.addWidget(self.add_btn)
        container1.addWidget(self.edit_btn)
        container1.addWidget(self.delete_btn)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.search_input)
        main_layout.addLayout(container1)
        main_layout.addWidget(self.table)

        self.setLayout(main_layout)

        self.load_data()

    def load_data(self):
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM users")
        data = cursor.fetchall()
        self.table.setRowCount(len(data))
        for row, user in enumerate(data):
            for column, data in enumerate(user):
                self.table.setItem(row, column, QTableWidgetItem(str(data)))

    def search_clicked(self):
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT * FROM users WHERE full_name LIKE %s OR major LIKE %s
        """, ('%' + self.search_input.text() + '%', '%' + self.search_input.text() + '%'))
        data = cursor.fetchall()
        self.table.setRowCount(len(data))
        for row, user in enumerate(data):
            for column, data in enumerate(user):
                self.table.setItem(row, column, QTableWidgetItem(str(data)))

    def add_clicked(self):
        self.add_page = Add_Page()
        if self.add_page.exec_():
            self.load_data()

    def edit_clicked(self):
        selected_items = self.table.selectedItems()
        if len(selected_items) < 1:
            QMessageBox.warning(self, "Warning", "You must select any field!")
            return

        student_id = selected_items[0].text()
        self.edit_page = Edit_Page(self, student_id)

        if self.edit_page.exec_():
            self.load_data()

    def delete_clicked(self):
        selected_items = self.table.selectedItems()
        if len(selected_items) < 1:
            QMessageBox.warning(self, "Warning", "You must select any field!")
        else:
            res = QMessageBox.question(self, "Question", "Are you sure ?", QMessageBox.Yes | QMessageBox.No)
            if res == QMessageBox.Yes:
                student_id = selected_items[0].text()
                connection = get_connection()
                cursor = connection.cursor()

                cursor.execute("""
                    DELETE FROM users WHERE id = %s
                """, (student_id, ))

                connection.commit()
                self.load_data()




