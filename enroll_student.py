from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QListWidget, QMessageBox, QListWidgetItem
)
from PyQt5.QtGui import QColor
from database import get_all_students, get_all_courses, enroll_student, get_student_enrollments
from datetime import datetime
from PyQt5.QtCore import Qt

class EnrollStudent(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Enroll Student")
        self.setGeometry(250, 250, 600, 600)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Search Student by Name:"))
        self.student_search = QLineEdit()
        self.student_search.textChanged.connect(self.filter_students)
        layout.addWidget(self.student_search)

        self.student_list = QListWidget()
        self.student_list.itemSelectionChanged.connect(self.refresh_course_list_for_student)
        layout.addWidget(self.student_list)

        layout.addWidget(QLabel("Search Course by Name:"))
        self.course_search = QLineEdit()
        self.course_search.textChanged.connect(self.filter_courses)
        layout.addWidget(self.course_search)

        self.course_list = QListWidget()
        layout.addWidget(self.course_list)

        self.enroll_button = QPushButton("Enroll Selected Student in Selected Course")
        self.enroll_button.clicked.connect(self.enroll_selected)
        layout.addWidget(self.enroll_button)

        self.setLayout(layout)

        self.all_students = get_all_students()
        self.all_courses = get_all_courses()
        self.selected_student_id = None
        self.enrolled_courses = []

        self.update_student_list()
        self.refresh_course_list_for_student()

    def update_student_list(self):
        self.student_list.clear()
        for sid, student_id, name in self.all_students:
            # Store the full info in item data
            item = QListWidgetItem(f"{student_id} - {name}")
            item.setData(Qt.UserRole, (sid, student_id, name))  # sid = integer id
            self.student_list.addItem(item)

    def refresh_course_list_for_student(self):
        self.course_list.clear()
        selected = self.student_list.currentItem()
        if not selected:
            return

        student_data = selected.data(Qt.UserRole)  # (id, student_id, name)
        if not student_data:
            return

        self.selected_student_id = student_data[0]  # actual integer ID

        self.enrolled_courses = get_student_enrollments(self.selected_student_id)

        for name, fee, duration in self.all_courses:
            item_text = f"{name} | ₹{fee} | {duration}"
            item = QListWidgetItem(item_text)

            if name in self.enrolled_courses:
                item.setForeground(QColor("red"))
                item.setText(item_text + " (Already Enrolled)")
                item.setFlags(item.flags() & ~Qt.ItemIsSelectable)

            self.course_list.addItem(item)


    def filter_students(self):
        keyword = self.student_search.text().lower()
        self.student_list.clear()
        for sid, name in self.all_students:
            if keyword in name.lower():
                self.student_list.addItem(f"{sid} - {name}")

    def filter_courses(self):
        self.refresh_course_list_for_student()  # Ensure filtering retains enrolled info
        keyword = self.course_search.text().lower()
        for i in range(self.course_list.count()):
            item = self.course_list.item(i)
            item.setHidden(keyword not in item.text().lower())

    def enroll_selected(self):
        student_item = self.student_list.currentItem()
        course_item = self.course_list.currentItem()

        if not student_item or not course_item:
            QMessageBox.warning(self, "Selection Error", "Please select both student and course.")
            return

        # Get the stored data
        sid, student_id_str, student_name = student_item.data(Qt.UserRole)  # sid = integer id

        course_parts = course_item.text().split(" | ")
        course_name = course_parts[0]

        if course_name in self.enrolled_courses:
            QMessageBox.warning(self, "Already Enrolled", f"{student_name} is already enrolled in {course_name}.")
            return

        fee = int(course_parts[1].replace("₹", ""))
        duration = course_parts[2].split()[0]
        enrollment_date = datetime.now().strftime("%Y-%m-%d")

        # Save the correct values (sid is int ID, student_id_str is external ID)
        enroll_student(
            student_id=sid,                  # integer ID for FK
            student_name=student_name,       # name
            course_name=course_name,
            fee=fee,
            duration=duration,
            date=enrollment_date
        )

        QMessageBox.information(self, "Success", f"{student_name} enrolled in {course_name}.")
        self.refresh_course_list_for_student()

