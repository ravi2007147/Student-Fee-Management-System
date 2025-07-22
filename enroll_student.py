from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QMessageBox, QSizePolicy, QHeaderView
)
from PyQt5.QtGui import QColor
from database import get_all_students, get_all_courses, enroll_student, get_student_enrollments, can_unenroll, unenroll_student
from datetime import datetime
from PyQt5.QtCore import Qt

class EnrollStudent(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Enroll Student")
        self.setGeometry(250, 250, 900, 600)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Search Student by Name:"))
        self.student_search = QLineEdit()
        self.student_search.setPlaceholderText("Search by student name...")
        self.student_search.setFixedHeight(32)
        self.student_search.setStyleSheet("padding-left: 10px; padding-right: 10px;")
        self.student_search.textChanged.connect(self.filter_students)
        layout.addWidget(self.student_search)

        self.student_table = QTableWidget()
        self.student_table.setColumnCount(3)
        self.student_table.setHorizontalHeaderLabels(["Student ID", "Name", "Select"])
        self.student_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.student_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.student_table.setSelectionMode(QTableWidget.SingleSelection)
        self.student_table.setSortingEnabled(True)
        self.student_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        header = self.student_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        self.student_table.itemSelectionChanged.connect(self.refresh_course_list_for_student)
        layout.addWidget(self.student_table, stretch=1)

        layout.addWidget(QLabel("Search Course by Name:"))
        self.course_search = QLineEdit()
        self.course_search.setPlaceholderText("Search by course name...")
        self.course_search.setFixedHeight(32)
        self.course_search.setStyleSheet("padding-left: 10px; padding-right: 10px;")
        self.course_search.textChanged.connect(self.filter_courses)
        layout.addWidget(self.course_search)

        self.course_table = QTableWidget()
        self.course_table.setColumnCount(3)
        self.course_table.setHorizontalHeaderLabels(["Course Name", "Fee", "Duration"])
        self.course_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.course_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.course_table.setSelectionMode(QTableWidget.SingleSelection)
        self.course_table.setSortingEnabled(True)
        self.course_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        header2 = self.course_table.horizontalHeader()
        header2.setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.course_table, stretch=1)

        self.enroll_button = QPushButton("Enroll")
        self.enroll_button.setFixedHeight(32)
        self.enroll_button.clicked.connect(self.enroll_selected)
        layout.addWidget(self.enroll_button)

        self.unenroll_button = QPushButton("Unenroll")
        self.unenroll_button.setFixedHeight(32)
        self.unenroll_button.clicked.connect(self.unenroll_selected)
        layout.addWidget(self.unenroll_button)

        self.setLayout(layout)

        self.all_students = get_all_students()
        self.all_courses = get_all_courses()
        self.selected_student_id = None
        self.enrolled_courses = []

        self.refresh_student_table()
        self.refresh_course_table()

    def refresh_student_table(self):
        self.student_table.setRowCount(0)
        for sid, student_id, name in self.all_students:
            row_idx = self.student_table.rowCount()
            self.student_table.insertRow(row_idx)
            self.student_table.setItem(row_idx, 0, QTableWidgetItem(student_id))
            self.student_table.setItem(row_idx, 1, QTableWidgetItem(name))
            self.student_table.setItem(row_idx, 2, QTableWidgetItem("Select"))
        self.filter_students()

    def refresh_course_table(self):
        self.course_table.setRowCount(0)
        for name, fee, duration in self.all_courses:
            row_idx = self.course_table.rowCount()
            self.course_table.insertRow(row_idx)
            self.course_table.setItem(row_idx, 0, QTableWidgetItem(name))
            self.course_table.setItem(row_idx, 1, QTableWidgetItem(f"₹{fee}"))
            self.course_table.setItem(row_idx, 2, QTableWidgetItem(str(duration)))
        self.filter_courses()

    def filter_students(self):
        filter_text = self.student_search.text().strip().lower()
        for row in range(self.student_table.rowCount()):
            name = self.student_table.item(row, 1).text().lower()
            self.student_table.setRowHidden(row, filter_text not in name)

    def filter_courses(self):
        filter_text = self.course_search.text().strip().lower()
        for row in range(self.course_table.rowCount()):
            name = self.course_table.item(row, 0).text().lower()
            self.course_table.setRowHidden(row, filter_text not in name)

    def refresh_course_list_for_student(self):
        selected_row = self.student_table.currentRow()
        if selected_row < 0:
            self.selected_student_id = None
            self.enrolled_courses = []
            self.refresh_course_table()  # Show all courses
            self.enroll_button.setEnabled(True)
            self.unenroll_button.setEnabled(True)
            return
        # Find the actual student id
        student_id_str = self.student_table.item(selected_row, 0).text()
        # Find sid from all_students
        sid = None
        for s in self.all_students:
            if s[1] == student_id_str:
                sid = s[0]
                break
        self.selected_student_id = sid
        self.enrolled_courses = get_student_enrollments(self.selected_student_id)
        for row in range(self.course_table.rowCount()):
            course_name = self.course_table.item(row, 0).text()
            orig_name = course_name.split(' (Already Enrolled)')[0]
            self.course_table.item(row, 0).setText(orig_name)
            is_enrolled = orig_name in self.enrolled_courses
            for col in range(self.course_table.columnCount()):
                item = self.course_table.item(row, col)
                if is_enrolled:
                    item.setForeground(QColor("red"))
                    item.setToolTip("Already Enrolled")
                else:
                    item.setForeground(QColor("black"))
                    item.setToolTip("")
        self.enroll_button.setEnabled(True)
        self.unenroll_button.setEnabled(True)

    def enroll_selected(self):
        student_row = self.student_table.currentRow()
        course_row = self.course_table.currentRow()
        if student_row < 0 or course_row < 0:
            QMessageBox.warning(self, "Selection Error", "Please select both student and course.")
            return
        student_id_str = self.student_table.item(student_row, 0).text()
        student_name = self.student_table.item(student_row, 1).text()
        sid = None
        for s in self.all_students:
            if s[1] == student_id_str:
                sid = s[0]
                break
        course_name = self.course_table.item(course_row, 0).text().split(' (Already Enrolled)')[0]
        if course_name in self.enrolled_courses:
            QMessageBox.warning(self, "Already Enrolled", f"{student_name} is already enrolled in {course_name}.")
            return
        fee = int(self.course_table.item(course_row, 1).text().replace("₹", ""))
        duration = self.course_table.item(course_row, 2).text().split()[0]
        enrollment_date = datetime.now().strftime("%Y-%m-%d")
        enroll_student(
            student_id=sid,
            student_name=student_name,
            course_name=course_name,
            fee=fee,
            duration=duration,
            date=enrollment_date
        )
        QMessageBox.information(self, "Success", f"{student_name} enrolled in {course_name}.")
        self.refresh_course_list_for_student()

    def unenroll_selected(self):
        print('Unenroll button clicked')
        student_row = self.student_table.currentRow()
        course_row = self.course_table.currentRow()
        print('Student row:', student_row)
        print('Course row:', course_row)
        if student_row < 0 or course_row < 0:
            QMessageBox.warning(self, "Selection Error", "Please select both student and course.")
            return
        student_id_str = self.student_table.item(student_row, 0).text()
        student_name = self.student_table.item(student_row, 1).text()
        sid = None
        for s in self.all_students:
            if s[1] == student_id_str:
                sid = s[0]
                break
        course_name = self.course_table.item(course_row, 0).text().split(' (Already Enrolled)')[0]
        print(f'Trying to unenroll student_id={sid}, course_name={course_name}')
        print('enrolled_courses:', self.enrolled_courses)
        print('course_name in enrolled_courses:', course_name in self.enrolled_courses)
        if course_name not in self.enrolled_courses:
            QMessageBox.warning(self, "Not Enrolled", f"{student_name} is not enrolled in {course_name}.")
            return
        can_unenroll_result = can_unenroll(sid, course_name)
        print('can_unenroll:', can_unenroll_result)
        if not can_unenroll_result:
            QMessageBox.warning(self, 'Cannot Unenroll', 'Cannot unenroll because payment has already been made.')
            return
        reply = QMessageBox.question(self, 'Confirm Unenroll', f'Are you sure you want to unenroll from {course_name}?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            unenroll_result = unenroll_student(sid, course_name)
            print('unenroll_student result:', unenroll_result)
            if unenroll_result:
                QMessageBox.information(self, 'Unenrolled', f'Successfully unenrolled from {course_name}.')
            else:
                QMessageBox.warning(self, 'Cannot Unenroll', 'Unenrollment failed.')
            self.refresh_course_list_for_student()

