from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QListWidget, QMessageBox
)
from database import add_student, get_students, delete_student

class StudentManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Manager")
        self.setGeometry(200, 200, 500, 500)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Add New Student:"))

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Name (required)")
        layout.addWidget(self.name_input)

        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Phone Number (required)")
        layout.addWidget(self.phone_input)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email (optional)")
        layout.addWidget(self.email_input)

        self.address_input = QLineEdit()
        self.address_input.setPlaceholderText("Address (optional)")
        layout.addWidget(self.address_input)

        self.add_button = QPushButton("Add Student")
        self.add_button.clicked.connect(self.handle_add_student)
        layout.addWidget(self.add_button)

        self.student_list = QListWidget()
        layout.addWidget(self.student_list)

        self.delete_button = QPushButton("Delete Selected Student")
        self.delete_button.clicked.connect(self.handle_delete_student)
        layout.addWidget(self.delete_button)

        self.setLayout(layout)
        self.refresh_students()

    def handle_add_student(self):
        name = self.name_input.text().strip()
        phone = self.phone_input.text().strip()
        email = self.email_input.text().strip()
        address = self.address_input.text().strip()

        if not name or not phone:
            QMessageBox.warning(self, "Input Error", "Name and phone number are required.")
            return

        add_student(name, phone, email, address)
        self.name_input.clear()
        self.phone_input.clear()
        self.email_input.clear()
        self.address_input.clear()
        self.refresh_students()

    def refresh_students(self):
        self.student_list.clear()
        students = get_students()
        for stu in students:
            sid, name, phone, email, address = stu
            self.student_list.addItem(f"{sid} - {name} | {phone} | {email or 'N/A'}")

    def handle_delete_student(self):
        selected = self.student_list.currentItem()
        if not selected:
            QMessageBox.warning(self, "Selection Error", "Please select a student to delete.")
            return

        student_id = int(selected.text().split(" - ")[0])
        confirm = QMessageBox.question(self, "Confirm Delete", f"Are you sure you want to delete this student?",
                                       QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            delete_student(student_id)
            self.refresh_students()
