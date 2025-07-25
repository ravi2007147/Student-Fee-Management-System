from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QTableWidget, QTableWidgetItem,
    QPushButton, QMessageBox, QFileDialog, QHeaderView
)
from PyQt5.QtPrintSupport import QPrinter
from PyQt5.QtGui import QPainter, QFont, QPen, QFontMetrics
from database import get_payment_history  # make sure this function works
from PyQt5.QtCore import Qt
import os

class ViewPaymentHistory(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("View Payment History")
        self.setGeometry(200, 200, 900, 500)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Search by Student ID or Name:"))
        self.student_input = QLineEdit()
        layout.addWidget(self.student_input)

        layout.addWidget(QLabel("Search by Course Name (optional):"))
        self.course_input = QLineEdit()
        layout.addWidget(self.course_input)

        self.search_btn = QPushButton("Search")
        self.search_btn.clicked.connect(self.search_payments)
        layout.addWidget(self.search_btn)

        self.results_table = QTableWidget()
        self.results_table.setColumnCount(6)
        self.results_table.setHorizontalHeaderLabels([
            "Receipt No", "Student Name", "Student ID", "Course", "Amount", "Date"
        ])
        self.results_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.results_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.results_table.setSelectionMode(QTableWidget.SingleSelection)
        self.results_table.setSortingEnabled(True)
        header = self.results_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.results_table, stretch=1)

        self.print_btn = QPushButton("Generate Payment Memo for Selected")
        self.print_btn.clicked.connect(self.generate_payment_memo)
        layout.addWidget(self.print_btn)

        self.setLayout(layout)
        self.payments = []

    def search_payments(self):
        student_key = self.student_input.text().strip()
        course_key = self.course_input.text().strip()

        if not student_key:
            QMessageBox.warning(self, "Input Error", "Student ID or Name is required.")
            return

        self.results_table.setRowCount(0)
        self.payments = get_payment_history(student_key, course_key)

        for payment in self.payments:
            pay_id, receipt_no, student_id, name, course, amount, date = payment
            row_idx = self.results_table.rowCount()
            self.results_table.insertRow(row_idx)
            self.results_table.setItem(row_idx, 0, QTableWidgetItem(receipt_no))
            self.results_table.setItem(row_idx, 1, QTableWidgetItem(name))
            self.results_table.setItem(row_idx, 2, QTableWidgetItem(student_id))
            self.results_table.setItem(row_idx, 3, QTableWidgetItem(course))
            self.results_table.setItem(row_idx, 4, QTableWidgetItem(f"₹{amount}"))
            self.results_table.setItem(row_idx, 5, QTableWidgetItem(date))

    def generate_payment_memo(self):
        selected_row = self.results_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "No Selection", "Select a payment record to generate PDF.")
            return

        payment = self.payments[selected_row]
        # Unpack: (payment_id, receipt_no, student_id, name, course, amount, date)
        pay_id, receipt_no, student_id, name, course, amount, date = payment

        receipts_dir = "receipts"
        os.makedirs(receipts_dir, exist_ok=True)
        filename = os.path.join(receipts_dir, f"receipt_{receipt_no}.pdf")

        printer = QPrinter()
        printer.setOutputFormat(QPrinter.PdfFormat)
        printer.setOutputFileName(filename)

        painter = QPainter()
        if not painter.begin(printer):
            QMessageBox.warning(self, "Error", "Failed to create PDF.")
            return

        try:
            painter.setRenderHint(QPainter.Antialiasing)
            margin = 50
            padding_right = 20
            page_rect = printer.pageRect()
            width = page_rect.width()
            height = page_rect.height()
            box_width = width - 2 * margin
            box_height = min(400, height - 2 * margin)
            painter.setPen(QPen(Qt.black, 2))
            painter.drawRect(margin, margin, box_width, box_height)
            painter.setFont(QFont("Arial", 10))
            font_metrics = QFontMetrics(painter.font())
            painter.setFont(QFont("Times", 14, QFont.Bold))
            font_metrics = QFontMetrics(painter.font())
            header_text = "COURSE FEE RECEIPT"
            text_width = font_metrics.horizontalAdvance(header_text)
            x_center = margin + box_width // 2 - text_width // 2
            painter.drawText(x_center, margin + 60, header_text)
            painter.setFont(QFont("Arial", 10))
            font_metrics = QFontMetrics(painter.font())
            institute_name = "PriorCoder Tech Studio"
            text_width = font_metrics.horizontalAdvance(institute_name)
            x_center = margin + box_width // 2 - text_width // 2
            painter.drawText(x_center, margin + 75, institute_name)
            address = "Gobind Nagar, St. No. 8, Chd Road, Ludhiana, Punjab - 141015"
            text_width = font_metrics.horizontalAdvance(address)
            x_center = margin + box_width // 2 - text_width // 2
            painter.drawText(x_center, margin + 90, address)
            painter.setFont(QFont("Arial", 10))
            receipt_text = f"Receipt No: {receipt_no}"
            receipt_text_width = font_metrics.horizontalAdvance(receipt_text)
            x_receipt = width - margin - receipt_text_width - padding_right
            painter.drawText(x_receipt, margin + 20, receipt_text)
            date_text = f"Date: {date}"
            date_text_width = font_metrics.horizontalAdvance(date_text)
            x_date = width - margin - date_text_width - padding_right
            painter.drawText(x_receipt, margin + 35, date_text)
            y = margin + 140
            spacing = 30
            x = margin + 20
            painter.setFont(QFont("Arial", 11))
            painter.drawText(x, y, f"Received from: {name}")
            y += spacing
            painter.drawText(x, y, f"Student ID: {student_id}")
            y += spacing
            painter.drawText(x, y, f"The sum of: ₹{amount} /-")
            y += spacing
            painter.drawText(x, y, f"Being payment of: {course}")
            y += spacing
            painter.drawText(x, y, "Cash / Cheque No: __________________________")
            y += spacing * 2
            painter.drawText(x, y, "Received by: _______________________        Signature: _______________________" )
        finally:
            painter.end()
        QMessageBox.information(self, "PDF Saved", f"Payment memo saved to:\n{filename}")


