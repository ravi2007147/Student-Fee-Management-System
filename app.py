import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
)
from database import initialize_db
from course_manager import open_course_manager,open_enroll_window,open_payment_window,open_payment_history  # Assume this will be converted too
from course_manager import open_student_manager

# Initialize DB on app startup
initialize_db()

class InstituteApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Institute Management System")
        self.setGeometry(100, 100, 400, 400)

        layout = QVBoxLayout()

        title = QLabel("PriorCoder Tech Studio Manager")
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(title)

        # Buttons
        btn_course = QPushButton("Add/View/Delete Courses")
        btn_course.setFixedHeight(40)
        btn_course.clicked.connect(open_course_manager)
        layout.addWidget(btn_course)

        # Placeholder buttons (can be connected later)
        btn_student = QPushButton("Add Student")
        btn_student.setFixedHeight(40)
        btn_student.clicked.connect(open_student_manager)
        layout.addWidget(btn_student)

        btn_enroll = QPushButton("Enroll Student")
        btn_enroll.setFixedHeight(40)
        btn_enroll.clicked.connect(open_enroll_window)
        layout.addWidget(btn_enroll)

        btn_payment = QPushButton("Record Payment")
        btn_payment.setFixedHeight(40)
        btn_payment.clicked.connect(open_payment_window)
        layout.addWidget(btn_payment)

        btn_history = QPushButton("View Payment History")
        btn_history.setFixedHeight(40)
        btn_history.clicked.connect(open_payment_history)
        layout.addWidget(btn_history)

        self.setLayout(layout)

# Main launcher
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InstituteApp()
    window.show()
    sys.exit(app.exec_())
