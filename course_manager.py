from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QListWidget, QMessageBox
)
from database import get_courses, add_course, delete_course
from student_manager import StudentManager
from enroll_student import EnrollStudent
from record_payment import RecordPayment
from view_payment_history import ViewPaymentHistory


class CourseManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Course Manager")
        self.setGeometry(150, 150, 400, 500)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Add New Course:"))

        self.course_input = QLineEdit()
        self.course_input.setPlaceholderText("Enter course name")
        layout.addWidget(self.course_input)

        self.fee_input = QLineEdit()
        self.fee_input.setPlaceholderText("Enter course fee")
        layout.addWidget(self.fee_input)

        self.duration_input = QLineEdit()
        self.duration_input.setPlaceholderText("Enter duration (e.g., 3 months)")
        layout.addWidget(self.duration_input)

        self.add_button = QPushButton("Add Course")
        self.add_button.clicked.connect(self.handle_add_course)
        layout.addWidget(self.add_button)

        self.course_list = QListWidget()
        layout.addWidget(self.course_list)

        self.delete_button = QPushButton("Delete Selected Course")
        self.delete_button.clicked.connect(self.handle_delete_course)
        layout.addWidget(self.delete_button)

        self.setLayout(layout)
        self.refresh_course_list()

    def handle_add_course(self):
        name = self.course_input.text().strip()
        fee = self.fee_input.text().strip()
        duration = self.duration_input.text().strip()

        if not name or not fee or not duration:
            QMessageBox.warning(self, "Input Error", "All fields are required.")
            return

        if not fee.isdigit():
            QMessageBox.warning(self, "Input Error", "Fee must be a number.")
            return
        
        if not duration.isdigit():
            QMessageBox.warning(self, "Input Error", "Duration must be an integer.")
            return
        duration = int(duration)

        add_course(name, int(fee), duration)
        self.course_input.clear()
        self.fee_input.clear()
        self.duration_input.clear()
        self.refresh_course_list()

    def refresh_course_list(self):
        self.course_list.clear()
        courses = get_courses()
        for course in courses:
            course_id, name, fee, duration = course
            self.course_list.addItem(f"{course_id} - {name} | ₹{fee} | {duration}")

    def handle_delete_course(self):
        selected = self.course_list.currentItem()
        if not selected:
            QMessageBox.warning(self, "Selection Error", "Please select a course to delete.")
            return
        course_id = int(selected.text().split(" - ")[0])
        delete_course(course_id)
        self.refresh_course_list()


# Keep reference alive
open_windows = []
def open_course_manager():
    cm_window = CourseManager()
    cm_window.show()
    cm_window.raise_()
    open_windows.append(cm_window)

def open_student_manager():
    sm_window = StudentManager()
    sm_window.show()
    sm_window.raise_()
    open_windows.append(sm_window)
    
def open_enroll_window():
    enroll_window = EnrollStudent()
    enroll_window.show()
    open_windows.append(enroll_window)
    
def open_payment_window():
    payment_window = RecordPayment()
    payment_window.show()
    open_windows.append(payment_window)
    
def open_payment_history():
    win = ViewPaymentHistory()
    win.show()
    open_windows.append(win)