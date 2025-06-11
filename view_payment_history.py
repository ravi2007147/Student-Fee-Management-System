from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QListWidget,
    QPushButton, QMessageBox
)
from PyQt5.QtPrintSupport import QPrinter
from PyQt5.QtGui import QPainter, QFont, QPen
from database import get_payment_history  # make sure this function works
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontMetrics
import os

class ViewPaymentHistory(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("View Payment History")
        self.setGeometry(200, 200, 600, 500)

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

        self.results_list = QListWidget()
        layout.addWidget(self.results_list)

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

        self.results_list.clear()
        self.payments = get_payment_history(student_key, course_key)

        for payment in self.payments:
            pay_id, receipt_no, student_id, name, course, amount, date = payment
            self.results_list.addItem(
                f"{receipt_no} - {name} ({student_id}) | {course} | ₹{amount} | {date}"
            )
    
    def generate_payment_memo(self):
        selected = self.results_list.currentItem()
        if not selected:
            QMessageBox.warning(self, "No Selection", "Select a payment record to generate PDF.")
            return

        idx = self.results_list.currentRow()
        payment = self.payments[idx]

        # Unpack: (payment_id, receipt_no, student_id, name, course, amount, date)
        pay_id, receipt_no, student_id, name, course, amount, date = payment

        # Ensure the receipts folder exists
        receipts_dir = "receipts"
        os.makedirs(receipts_dir, exist_ok=True)

        # Create full path to save PDF
        filename = os.path.join(receipts_dir, f"receipt_{receipt_no}.pdf")

        # Set up printer for saving as PDF
        printer = QPrinter()
        printer.setOutputFormat(QPrinter.PdfFormat)
        printer.setOutputFileName(filename)

        painter = QPainter()
        if not painter.begin(printer):
            QMessageBox.warning(self, "Error", "Failed to create PDF.")
            return

        try:
            painter.setRenderHint(QPainter.Antialiasing)

            # Margins and page size
            margin = 50
            padding_right = 20
            page_rect = printer.pageRect()
            width = page_rect.width()
            height = page_rect.height()

            box_width = width - 2 * margin
            box_height = min(400, height - 2 * margin)

            # Draw outer rectangle (receipt box)
            painter.setPen(QPen(Qt.black, 2))
            painter.drawRect(margin, margin, box_width, box_height)

            # Fonts and metrics
            painter.setFont(QFont("Arial", 10))
            font_metrics = QFontMetrics(painter.font())

           # Set the font and measure box width
            painter.setFont(QFont("Times", 14, QFont.Bold))
            font_metrics = QFontMetrics(painter.font())
            header_text = "COURSE FEE RECEIPT"
            text_width = font_metrics.horizontalAdvance(header_text)
            x_center = margin + box_width // 2 - text_width // 2
            painter.drawText(x_center, margin + 60, header_text)

            # Second line - Institute Name
            painter.setFont(QFont("Arial", 10))
            font_metrics = QFontMetrics(painter.font())  # Update metrics after font change
            institute_name = "PriorCoder Tech Studio"
            text_width = font_metrics.horizontalAdvance(institute_name)
            x_center = margin + box_width // 2 - text_width // 2
            painter.drawText(x_center, margin + 75, institute_name)

            # Third line - Address
            address = "Gobind Nagar, St. No. 3, Chd Road, Ludhiana, Punjab - 141015"
            text_width = font_metrics.horizontalAdvance(address)
            x_center = margin + box_width // 2 - text_width // 2
            painter.drawText(x_center, margin + 90, address)


            # Right-aligned: Receipt No. and Date
            painter.setFont(QFont("Arial", 10))
            receipt_text = f"Receipt No: {receipt_no}"
            receipt_text_width = font_metrics.horizontalAdvance(receipt_text)
            x_receipt = width - margin - receipt_text_width - padding_right
            painter.drawText(x_receipt, margin + 20, receipt_text)

            date_text = f"Date: {date}"
            date_text_width = font_metrics.horizontalAdvance(date_text)
            x_date = width - margin - date_text_width - padding_right
            painter.drawText(x_receipt, margin + 35, date_text)

            # Body content
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

            # Signature line
            y += spacing * 2
            painter.drawText(x, y, "Received by: _______________________        Signature: _______________________")

        finally:
            painter.end()

        QMessageBox.information(self, "PDF Saved", f"Payment memo saved to:\n{filename}")


