# 🎓 PriorCoder Tech Studio – Student Fee Management System

A desktop-based application built with **Python (PyQt5 + SQLite)** to manage student enrollments, course records, and payment tracking for a programming institute.

---

## ✅ Key Features

### 👨‍🎓 Student Management
- Add, view, and manage students with unique IDs and details.

### 📚 Course Management
- Maintain a list of courses (e.g., C, C++, Python) with configurable fees and durations.

### 📝 Enrollment System
- Enroll students into specific courses.
- Preserve historical enrollments and link them with payments.
- Prevents duplicate enrollments.

### 💰 Payment Tracking & History
- Log payments against enrollments.
- View full fee history by student or course.
- Check pending vs. fully paid records.

### 🧾 Professional Receipt Generation (PDF)
- Automatically generates clean, branded **course fee receipts** in PDF format.
- Saved into a structured `receipts/` folder.
- Includes: Receipt No, Student ID, Name, Course, Amount, Date.
- Fully styled with institute name and signature area.

### 🔍 Search & Filter
- Search payments by student name/ID or course name.

---

## 🛠️ Tech Stack

- **Frontend:** PyQt5 (Python GUI)
- **Backend:** SQLite3
- **PDF Generation:** QPainter + QPrinter
- **Local DB:** `institute.db` (no internet or server required)

---

## 💡 Ideal For

- Small to medium educational institutes
- Offline coaching centers
- Programming or skill-based training institutes needing printable receipts & local fee tracking

