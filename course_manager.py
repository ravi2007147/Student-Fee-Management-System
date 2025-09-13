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
        self.setGeometry(150, 150, 800, 700)
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
            QTableWidget {
                background-color: white;
                alternate-background-color: #f8f9fa;
                gridline-color: #dee2e6;
                border: 1px solid #dee2e6;
                border-radius: 6px;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #f1f3f4;
            }
            QTableWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
            QHeaderView::section {
                background-color: #2c3e50;
                color: white;
                padding: 12px;
                border: none;
                font-weight: bold;
                font-size: 11px;
            }
            QHeaderView::section:hover {
                background-color: #34495e;
            }
        """)

        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(25, 25, 25, 25)

        # Title section
        title_label = QLabel("📚 Course Management")
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

        # Form section with better grouping
        form_group = QLabel("Add New Course")
        form_group.setStyleSheet("""
            font-size: 14px;
            font-weight: bold;
            color: #34495e;
            margin: 15px 0px 10px 0px;
            padding: 8px 0px;
            border-bottom: 2px solid #3498db;
        """)
        layout.addWidget(form_group)

        self.course_input = QLineEdit()
        self.course_input.setPlaceholderText("Enter course name")
        self.course_input.setFixedHeight(45)
        self.course_input.setStyleSheet("padding-left: 10px; padding-right: 10px;")
        layout.addWidget(self.course_input)

        self.fee_input = QLineEdit()
        self.fee_input.setPlaceholderText("Enter course fee")
        self.fee_input.setFixedHeight(45)
        self.fee_input.setStyleSheet("padding-left: 10px; padding-right: 10px;")
        layout.addWidget(self.fee_input)

        self.duration_input = QLineEdit()
        self.duration_input.setPlaceholderText("Enter duration (e.g., 3 months)")
        self.duration_input.setFixedHeight(45)
        self.duration_input.setStyleSheet("padding-left: 10px; padding-right: 10px;")
        layout.addWidget(self.duration_input)

        self.add_button = QPushButton("Add Course")
        self.add_button.clicked.connect(self.handle_add_course)
        self.add_button.setFixedHeight(45)
        layout.addWidget(self.add_button)

        # Search/filter bar
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by course name...")
        self.search_input.textChanged.connect(self.filter_courses)
        self.search_input.setFixedHeight(45)
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
        self.course_table.verticalHeader().setDefaultSectionSize(35)
        header = self.course_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        # Set fixed width for the delete column
        header.setSectionResizeMode(4, QHeaderView.Fixed)
        self.course_table.setColumnWidth(4, 60)
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
            btn.setText("🗑️")
        else:
            btn.setIcon(icon)
            btn.setText("")
        btn.setToolTip('Delete this course')
        btn.setFlat(True)
        btn.setFixedSize(28, 20)
        btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                padding: 0px;
                margin: 0px;
            }
            QPushButton:hover {
                background-color: #ffebee;
                border-radius: 3px;
            }
            QPushButton:pressed {
                background-color: #ffcdd2;
            }
        """)
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