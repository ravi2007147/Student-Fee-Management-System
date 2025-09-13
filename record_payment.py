from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QListWidget, QMessageBox, QInputDialog
)
from database import get_enrollments_by_student_identifier, add_payment, get_total_paid
from datetime import datetime
from PyQt5.QtCore import Qt


class RecordPayment(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Record Payment")
        self.setGeometry(300, 300, 700, 600)
        self.setStyleSheet("""
            QWidget {
                background-color: #f8f9fa;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QLabel {
                color: #2c3e50;
                font-weight: 600;
                font-size: 12px;
                margin: 5px 0px;
            }
            QLineEdit {
                background-color: white;
                border: 2px solid #e9ecef;
                border-radius: 6px;
                padding: 10px;
                font-size: 12px;
                color: #495057;
            }
            QLineEdit:focus {
                border-color: #3498db;
                background-color: #f8f9fa;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 12px 20px;
                border-radius: 6px;
                font-size: 12px;
                font-weight: bold;
                min-height: 40px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
            QListWidget {
                background-color: white;
                alternate-background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 6px;
                padding: 5px;
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #f1f3f4;
                margin: 2px 0px;
            }
            QListWidget::item:selected {
                background-color: #3498db;
                color: white;
                border-radius: 4px;
            }
        """)

        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(25, 25, 25, 25)

        # Title section
        title_label = QLabel("💰 Record Payment")
        title_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #2c3e50;
            margin: 10px 0px 20px 0px;
            padding: 15px;
            background-color: white;
            border-radius: 8px;
            border-left: 4px solid #3498db;
        """)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Search section
        search_section = QLabel("🔍 Search Student")
        search_section.setStyleSheet("""
            font-size: 14px;
            font-weight: bold;
            color: #34495e;
            margin: 15px 0px 10px 0px;
            padding: 8px 0px;
            border-bottom: 2px solid #3498db;
        """)
        layout.addWidget(search_section)

        layout.addWidget(QLabel("Search Student by ID or Name:"))
        self.search_input = QLineEdit()
        self.search_input.textChanged.connect(self.search_enrollments)
        self.search_input.setFixedHeight(45)
        self.search_input.setStyleSheet("padding-left: 10px; padding-right: 10px;")
        layout.addWidget(self.search_input)

        self.enrollment_list = QListWidget()
        layout.addWidget(self.enrollment_list)

        self.pay_button = QPushButton("Record Payment")
        self.pay_button.clicked.connect(self.record_payment)
        self.pay_button.setFixedHeight(45)
        layout.addWidget(self.pay_button)

        self.setLayout(layout)
        self.enrollments = []

    def search_enrollments(self):
        keyword = self.search_input.text().strip()
        self.enrollment_list.clear()
        if not keyword:
            return
        self.enrollments = get_enrollments_by_student_identifier(keyword)
        for enroll_id, course_name, course_fee, paid in self.enrollments:
            pending = course_fee - paid
            self.enrollment_list.addItem(
                f"{enroll_id} - {course_name} | Total: ₹{course_fee} | Paid: ₹{paid} | Pending: ₹{pending}"
            )

    def record_payment(self):
        selected = self.enrollment_list.currentItem()
        if not selected:
            QMessageBox.warning(self, "Selection Error", "Please select a course.")
            return

        enrollment_id = int(selected.text().split(" - ")[0])
        total_paid = get_total_paid(enrollment_id)

        for enroll in self.enrollments:
            if enroll[0] == enrollment_id:
                total_fee = enroll[2]
                break
        else:
            QMessageBox.critical(self, "Error", "Enrollment not found.")
            return

        amount, ok = QInputDialog.getInt(self, "Enter Payment", f"Max allowed: ₹{total_fee - total_paid}")
        if not ok:
            return

        if amount <= 0:
            QMessageBox.warning(self, "Input Error", "Amount must be greater than 0.")
            return

        if total_paid + amount > total_fee:
            QMessageBox.critical(self, "Overpayment Error", "Cannot pay more than total fee.")
            return

        today = datetime.now().strftime("%Y-%m-%d")
        add_payment(enrollment_id, amount, today)
        QMessageBox.information(self, "Success", f"₹{amount} recorded.")
        self.search_enrollments()
