# Student Information System (PyQt5 + MySQL)

A desktop-based **Student Information System** built with **Python (PyQt5)** and **MySQL**, designed to manage **students**, **programs**, and **colleges**. The system supports adding, editing, deleting, searching, and updating across the the tables.

---

## 🚀 Features

### 🧑‍🎓 Student Management

* Add, edit, and delete student records
* Auto-updating program and college display
* Validations for contact number, email, and required fields

### 🏫 Program Management

* Add, edit, delete programs
* Linked to colleges
* Changes cascade to students (UI updates only unless specified otherwise)

### 🏛️ College Management

* Add, edit, delete colleges
* Deleting a college affects all programs and students linked to it (customizable: removal or just UI warning)

### 💾 Database Integration (MySQL)

* Uses a **DatabaseManager** class for all DB operations
* MySQL tables: `students`, `programs`, `colleges`
* HeidiSQL recommended for managing tables

### 🔄 Automatic and Manual Saving

* "Update" button commits all UI changes to the database
* Auto-save when closing the window (if enabled)

### 🔍 Search and Filtering

* Proxy models used for search, filtering, and sorting
---
### 📂 Project Structure

```
  StudentInformationSystem/
  ├── Buttons/
  │   ├── __init__.py     
  │   ├── addButton.py
  │   ├── editButton.py
  │   ├── removeButton.py
  │   └── updateButton.py
  ├── Database_Manager/
  │   └── database.py
  ├── Images/
  │   ├── ChickIcon.png
  │   ├── header_rc.py
  │   └── headerpic.qrc
  ├── Popups/
  │   ├── AddStudent.py
  │   ├── AddProgram.py
  │   └── AddCollege.py
  ├── SearchBar/
  │   ├── __init__.py
  │   └── searchTab.py
  ├── UI/
  │   └── display.ui
  ├── .gitignore
  ├── main.py
  └── README.md
```

---

## ⚙️ Installation & Setup

### 1️⃣ Install Dependencies

```
pip install pyqt5 mysql-connector-python
```

### 2️⃣ Create & Configure MySQL Database

```
CREATE DATABASE SSIS;
```
### 4️⃣ Run the Application

```
python main.py
```

---

## 🔄 Cascading Logic

* When **editing a college**, all linked programs remain intact
* When **deleting a college**:

  * Programs under that college are affected
  * Students under those programs may be updated or warned depending on your implementation
* When **deleting a program**:

  * Students enrolled in that program may be reassigned or trigger warnings

---

