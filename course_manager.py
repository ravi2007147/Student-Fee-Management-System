from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QMessageBox, QSizePolicy, QHeaderView, QAbstractItemView
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from database import get_courses, add_course, delete_course, course_exists
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
        self.course_input.setFixedHeight(32)
        self.course_input.setStyleSheet("padding-left: 10px; padding-right: 10px;")
        layout.addWidget(self.course_input)

        self.fee_input = QLineEdit()
        self.fee_input.setPlaceholderText("Enter course fee")
        self.fee_input.setFixedHeight(32)
        self.fee_input.setStyleSheet("padding-left: 10px; padding-right: 10px;")
        layout.addWidget(self.fee_input)

        self.duration_input = QLineEdit()
        self.duration_input.setPlaceholderText("Enter duration (e.g., 3 months)")
        self.duration_input.setFixedHeight(32)
        self.duration_input.setStyleSheet("padding-left: 10px; padding-right: 10px;")
        layout.addWidget(self.duration_input)

        self.add_button = QPushButton("Add Course")
        self.add_button.clicked.connect(self.handle_add_course)
        self.add_button.setFixedHeight(32)
        layout.addWidget(self.add_button)

        # Search/filter bar
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by course name...")
        self.search_input.textChanged.connect(self.filter_courses)
        self.search_input.setFixedHeight(32)
        self.search_input.setStyleSheet("padding-left: 10px; padding-right: 10px;")
        layout.addWidget(self.search_input)

        self.course_table = QTableWidget()
        self.course_table.setColumnCount(5)
        self.course_table.setHorizontalHeaderLabels(["ID", "Name", "Fee", "Duration (months)", "Delete"])
        self.course_table.setEditTriggers(QTableWidget.DoubleClicked | QTableWidget.SelectedClicked)
        self.course_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.course_table.setSelectionMode(QTableWidget.SingleSelection)
        self.course_table.setSortingEnabled(True)
        self.course_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(self.course_table, stretch=1)
        header = self.course_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        self.course_table.itemChanged.connect(self.handle_item_changed)
        self.course_table.setSelectionMode(QAbstractItemView.NoSelection)  # Only allow row selection via delete button

        self.setLayout(layout)
        self.refresh_course_list()

    def handle_add_course(self):
        name = self.course_input.text().strip()
        fee = self.fee_input.text().strip()
        duration = self.duration_input.text().strip()

        # Validate all fields are filled
        if not name or not fee or not duration:
            QMessageBox.warning(self, "Input Error", "All fields are required.")
            return

        # Validate course name
        if name.isdigit():
            QMessageBox.warning(self, "Input Error", "Course name cannot be only numbers.")
            return
        if not any(c.isalpha() for c in name):
            QMessageBox.warning(self, "Input Error", "Course name must contain letters.")
            return
        if not name.replace(' ', '').isalnum():
            QMessageBox.warning(self, "Input Error", "Course name must not contain special characters.")
            return
        if course_exists(name):
            QMessageBox.warning(self, "Input Error", "A course with this name already exists.")
            return

        # Validate fee
        if not fee.isdigit():
            QMessageBox.warning(self, "Input Error", "Fee must be a number.")
            return
        fee_int = int(fee)
        if fee_int <= 0 or fee_int > 1000000:
            QMessageBox.warning(self, "Input Error", "Fee must be between 1 and 1,000,000.")
            return

        # Validate duration
        if not duration.isdigit():
            QMessageBox.warning(self, "Input Error", "Duration must be an integer (months).")
            return
        duration_int = int(duration)
        if duration_int <= 0 or duration_int > 60:
            QMessageBox.warning(self, "Input Error", "Duration must be between 1 and 60 months.")
            return

        add_course(name, fee_int, duration_int)
        self.course_input.clear()
        self.fee_input.clear()
        self.duration_input.clear()
        self.refresh_course_list()

    def refresh_course_list(self):
        self.all_courses = get_courses()
        self.course_table.blockSignals(True)
        self.filter_courses()
        self.course_table.blockSignals(False)

    def add_delete_button(self, row, course_id):
        btn = QPushButton()
        icon = QIcon.fromTheme('user-trash')
        if icon.isNull():
            icon = QIcon.fromTheme('edit-delete')
        if icon.isNull():
            icon = QIcon.fromTheme('window-close')
        if icon.isNull():
            # Fallback: use a trash unicode emoji as icon
            btn.setText("🗑️")
        else:
            btn.setIcon(icon)
            btn.setText("")
        btn.setToolTip('Delete this course')
        btn.setFlat(True)
        btn.clicked.connect(lambda _, cid=course_id: self.confirm_delete_course(cid))
        self.course_table.setCellWidget(row, 4, btn)

    def filter_courses(self):
        filter_text = self.search_input.text().strip().lower() if hasattr(self, 'search_input') else ''
        self.course_table.blockSignals(True)
        self.course_table.setRowCount(0)
        for course in getattr(self, 'all_courses', get_courses()):
            course_id, name, fee, duration = course
            if filter_text and filter_text not in name.lower():
                continue
            row_idx = self.course_table.rowCount()
            self.course_table.insertRow(row_idx)
            self.course_table.setItem(row_idx, 0, QTableWidgetItem(str(course_id)))
            self.course_table.setItem(row_idx, 1, QTableWidgetItem(name))
            self.course_table.setItem(row_idx, 2, QTableWidgetItem(f"₹{fee}"))
            self.course_table.setItem(row_idx, 3, QTableWidgetItem(str(duration)))
            self.add_delete_button(row_idx, course_id)
        self.course_table.blockSignals(False)

    def confirm_delete_course(self, course_id):
        reply = QMessageBox.question(self, 'Confirm Delete', 'Are you sure you want to delete this course?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            delete_course(course_id)
            self.refresh_course_list()

    def handle_item_changed(self, item):
        # Prevent editing ID column
        if item.column() == 0:
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            return
        row = item.row()
        course_id = int(self.course_table.item(row, 0).text())
        name = self.course_table.item(row, 1).text().strip()
        fee = self.course_table.item(row, 2).text().replace('₹', '').strip()
        duration = self.course_table.item(row, 3).text().strip()

        # Update database
        from database import get_connection
        conn = get_connection()
        c = conn.cursor()
        c.execute("UPDATE courses SET name=?, fee=?, duration=? WHERE id=?", (name, fee, duration, course_id))
        conn.commit()
        conn.close()
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