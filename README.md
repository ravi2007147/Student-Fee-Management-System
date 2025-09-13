# 🎓 Institute Management System

A comprehensive desktop application built with **Python (PyQt5 + SQLite)** to manage student enrollments, course records, payment tracking, and automated backup systems for educational institutes.

---

## ✅ Key Features

### 👨‍🎓 Student Management
- **Tabbed Interface**: Separate "Listing" and "Add New" tabs for better organization
- **Advanced Table View**: Sortable, searchable student table with inline editing
- **Unique ID Generation**: Automatic student ID creation with year-based numbering
- **Professional UI**: Modern, responsive design with proper input field sizing

### 📚 Course Management
- **Tabbed Interface**: Separate "Listing" and "Add New" tabs for better organization
- **Advanced Table View**: Sortable, searchable course table with inline editing
- **Delete Functionality**: Safe course deletion with confirmation dialogs
- **Professional UI**: Modern, responsive design with proper input field sizing

### 📝 Enrollment System
- **Split-Panel Layout**: Left panel for student search/list, right panel for course search/list
- **Smart Enrollment**: Enroll/unenroll students with payment status validation
- **Joining Date Display**: Shows enrollment dates in course table
- **Payment Protection**: Prevents unenrollment if payments have been made

### 💰 Payment Tracking & History
- **Advanced Table View**: Sortable, searchable payment history table
- **Comprehensive Records**: Track all payments with detailed information
- **Student-Course Linking**: Maintains relationships between students, courses, and payments

### 🧾 Professional Receipt Generation (PDF)
- **Automated PDF Creation**: Generates clean, branded course fee receipts
- **Structured Storage**: Organized `receipts/` folder with proper naming
- **Complete Information**: Receipt No, Student ID, Name, Course, Amount, Date
- **Professional Styling**: Institute branding with signature areas

### 🔍 Advanced Search & Filter
- **Multi-Table Search**: Search functionality across all tables
- **Real-time Filtering**: Instant search results as you type
- **Sortable Columns**: Click column headers to sort data
- **Professional UI**: Consistent search experience across all modules

### 💾 Automated Backup System
- **Dual Backup Methods**: Local drive and Dropbox cloud backup
- **Incremental Backups**: Uses SQLite's backup API for efficient storage
- **Configurable Revisions**: Keep 1-20 backup versions (default: 5)
- **Automatic Cleanup**: Removes old backups to prevent space issues
- **Secure Storage**: Dropbox tokens stored securely using keyring
- **Professional Loading**: Loading overlay with progress messages
- **Restore Functionality**: Restore from latest backup with validation
- **Error Handling**: Comprehensive error reporting and recovery

### 🎨 Professional User Interface
- **Modern Design**: Clean, professional appearance throughout
- **Responsive Layout**: Tables expand to full screen with auto-resizing columns
- **Consistent Styling**: Unified color scheme and typography
- **Input Field Enhancement**: Proper padding and sizing for better usability
- **Button Management**: Smart enabling/disabling during operations
- **Loading States**: Professional loading overlays during backup operations

---

## 🛠️ Tech Stack

- **Frontend:** PyQt5 (Python GUI)
- **Backend:** SQLite3
- **PDF Generation:** QPainter + QPrinter
- **Cloud Storage:** Dropbox API
- **Security:** Keyring for secure credential storage
- **Local DB:** `institute.db` (no internet required for core functionality)

---

## 🚀 Installation & Setup

### Prerequisites
```bash
pip install PyQt5==5.15.11 PyQt5-Qt5==5.15.17 PyQt5_sip==12.17.0
pip install dropbox>=11.0.0 keyring>=23.0.0
```

### Running the Application
```bash
python app.py
```

### Backup Configuration
1. **Local Backup**: Set backup directory path in Settings
2. **Dropbox Backup**: 
   - Create Dropbox app with required permissions
   - Generate access token
   - Configure in Settings with secure storage

---

## 💡 Ideal For

- **Educational Institutes**: Small to medium programming institutes
- **Coaching Centers**: Offline training centers needing local management
- **Skill-Based Training**: Institutes requiring printable receipts & fee tracking
- **Data Security**: Organizations needing automated backup systems
- **Professional Operations**: Businesses requiring modern, responsive UI

---

## 🔧 Configuration

### Backup Settings
- **Local Path**: Configure local backup directory
- **Dropbox Token**: Secure cloud backup configuration
- **Revision Limit**: Set number of backups to retain (1-20)
- **Automatic Cleanup**: Old backups automatically removed

### Database Management
- **Automatic Initialization**: Database created on first run
- **Backup Validation**: Restored databases validated before use
- **Safety Backups**: Current database backed up before restore operations

---

## 📱 User Interface Features

- **Tabbed Navigation**: Organized interface with clear separation of functions
- **Table-Based Views**: Professional data presentation with sorting and searching
- **Responsive Design**: Adapts to different window sizes and screen resolutions
- **Loading States**: Visual feedback during operations
- **Error Handling**: User-friendly error messages and recovery options
- **Professional Styling**: Consistent, modern appearance throughout

