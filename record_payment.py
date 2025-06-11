from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QListWidget, QMessageBox, QInputDialog
)
from database import get_enrollments_by_student_identifier, add_payment, get_total_paid
from datetime import datetime


class RecordPayment(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Record Payment")
        self.setGeometry(300, 300, 600, 600)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Search Student by ID or Name:"))
        self.search_input = QLineEdit()
        self.search_input.textChanged.connect(self.search_enrollments)
        layout.addWidget(self.search_input)

        self.enrollment_list = QListWidget()
        layout.addWidget(self.enrollment_list)

        self.pay_button = QPushButton("Record Payment")
        self.pay_button.clicked.connect(self.record_payment)
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
