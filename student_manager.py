from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QSizePolicy, QHeaderView, QAbstractItemView
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from database import add_student, get_students, delete_student

class StudentManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Manager")
        self.setGeometry(200, 200, 700, 500)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Add New Student:"))

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Name (required)")
        self.name_input.setFixedHeight(32)
        self.name_input.setStyleSheet("padding-left: 10px; padding-right: 10px;")
        layout.addWidget(self.name_input)

        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Phone Number (required)")
        self.phone_input.setFixedHeight(32)
        self.phone_input.setStyleSheet("padding-left: 10px; padding-right: 10px;")
        layout.addWidget(self.phone_input)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email (optional)")
        self.email_input.setFixedHeight(32)
        self.email_input.setStyleSheet("padding-left: 10px; padding-right: 10px;")
        layout.addWidget(self.email_input)

        self.address_input = QLineEdit()
        self.address_input.setPlaceholderText("Address (optional)")
        self.address_input.setFixedHeight(32)
        self.address_input.setStyleSheet("padding-left: 10px; padding-right: 10px;")
        layout.addWidget(self.address_input)

        self.add_button = QPushButton("Add Student")
        self.add_button.clicked.connect(self.handle_add_student)
        self.add_button.setFixedHeight(32)
        layout.addWidget(self.add_button)

        # Search/filter bar
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by student name...")
        self.search_input.textChanged.connect(self.filter_students)
        self.search_input.setFixedHeight(32)
        self.search_input.setStyleSheet("padding-left: 10px; padding-right: 10px;")
        layout.addWidget(self.search_input)

        self.student_table = QTableWidget()
        self.student_table.setColumnCount(6)
        self.student_table.setHorizontalHeaderLabels(["ID", "Name", "Phone", "Email", "Address", "Delete"])
        self.student_table.setEditTriggers(QTableWidget.DoubleClicked | QTableWidget.SelectedClicked)
        self.student_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.student_table.setSortingEnabled(True)
        self.student_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        header = self.student_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        self.student_table.itemChanged.connect(self.handle_item_changed)
        self.student_table.setSelectionMode(QAbstractItemView.NoSelection)
        layout.addWidget(self.student_table, stretch=1)

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
        self.all_students = get_students()
        self.student_table.blockSignals(True)
        self.filter_students()
        self.student_table.blockSignals(False)

    def filter_students(self):
        filter_text = self.search_input.text().strip().lower() if hasattr(self, 'search_input') else ''
        self.student_table.blockSignals(True)
        self.student_table.setRowCount(0)
        for stu in getattr(self, 'all_students', get_students()):
            sid, name, phone, email, address = stu
            if filter_text and filter_text not in name.lower():
                continue
            row_idx = self.student_table.rowCount()
            self.student_table.insertRow(row_idx)
            self.student_table.setItem(row_idx, 0, QTableWidgetItem(str(sid)))
            self.student_table.setItem(row_idx, 1, QTableWidgetItem(name))
            self.student_table.setItem(row_idx, 2, QTableWidgetItem(phone))
            self.student_table.setItem(row_idx, 3, QTableWidgetItem(email or ''))
            self.student_table.setItem(row_idx, 4, QTableWidgetItem(address or ''))
            self.add_delete_button(row_idx, sid)
        self.student_table.blockSignals(False)

    def add_delete_button(self, row, student_id):
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
        btn.setToolTip('Delete this student')
        btn.setFlat(True)
        btn.clicked.connect(lambda _, sid=student_id: self.confirm_delete_student(sid))
        self.student_table.setCellWidget(row, 5, btn)

    def confirm_delete_student(self, student_id):
        reply = QMessageBox.question(self, 'Confirm Delete', 'Are you sure you want to delete this student?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            delete_student(student_id)
            self.refresh_students()

    def handle_item_changed(self, item):
        # Prevent editing ID column
        if item.column() == 0:
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            return
        row = item.row()
        sid = int(self.student_table.item(row, 0).text())
        name = self.student_table.item(row, 1).text().strip()
        phone = self.student_table.item(row, 2).text().strip()
        email = self.student_table.item(row, 3).text().strip()
        address = self.student_table.item(row, 4).text().strip()
        from database import get_connection
        conn = get_connection()
        c = conn.cursor()
        c.execute("UPDATE students SET name=?, phone=?, email=?, address=? WHERE id=?", (name, phone, email, address, sid))
        conn.commit()
        conn.close()
        self.refresh_students()
