from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import  QMessageBox, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QRegularExpressionValidator
from PyQt5.QtCore import QRegularExpression

import re, csv, os
from Database_Manager.database import DatabaseManager

class AddProgram(QtWidgets.QDialog):
    program_added = QtCore.pyqtSignal(list)
    program_edited = QtCore.pyqtSignal(list)

    def __init__(self, parent = None, program_data = None, table_model = None):
        super().__init__(parent if isinstance(parent, QWidget) else None)
        self.table_model = table_model
        self.program_data = program_data
        self.editing = program_data is not None

        self.original_code = program_data[0].strip().lower() if self.editing else None
        
        #Connecting to Database
        #--------------------------------
        self.database = DatabaseManager()

        self.setObjectName("Dialog")
        self.setWindowTitle("Student Information System")
        self.resize(411, 277)
        self.setWindowIcon(QIcon("Images/ChickIcon.png"))

        self.setStyleSheet("""
            QDialog {
                background-color: #fce090; 
            }  
                                                    
            QLineEdit {
                font-family: 'Fixedsys';
                color: black; 
                background-color: white; 
                border: 1px solid #5D6D7E; /* Border color */
                border-radius: 5px;
                
            }

            QComboBox {
                font-family: 'Fixedsys';
                color: black;
                background-color: white;
                border: 1px solid #5D6D7E;
                border-radius: 5px;
            }
                           

            QPushButton {
                font-family: 'Fixedsys';
                background-color: white; 
                color: black;
                border-radius: 5px;
                padding: 20px
            }

            QPushButton:hover {
                background-color: #ffb36b; 
                color: white;
            }

            QPushButton:pressed {
                background-color: #CD853F; 
                color: white;
            }
          
        """)
        




        #Set Fonts
        #----------------------------------
        fixedsys_font = QtGui.QFont()
        fixedsys_font.setFamily("Fixedsys")

        terminal_font = QtGui.QFont()
        terminal_font.setFamily("Terminal")
        terminal_font.setPointSize(14)
        terminal_font.setBold(True)
        terminal_font.setItalic(False)
        terminal_font.setWeight(75)

        #Title
        #-------------------------------------------------------
        self.addProgram = QtWidgets.QLabel("ADD PROGRAM", self)
        self.addProgram.setStyleSheet("color: #CD853F")
        self.addProgram.setGeometry(140, 20, 121, 18)
        self.addProgram.setFont(terminal_font)
        
        #Container for Widgets
        #---------------------------------------------------
        self.verticalLayoutWidget = QtWidgets.QWidget(self)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 60, 371, 151))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        #Program Code
        #----------------------------------------------------------------------------------
        self.programCodeText = QtWidgets.QLabel("PROGRAM CODE:", self.verticalLayoutWidget)
        self.programCodeText.setFont(fixedsys_font)
        self.programCodeText.setObjectName("programCodeText")
        self.verticalLayout.addWidget(self.programCodeText)
       
        self.programCode = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.programCode.setFont(fixedsys_font)
        self.programCode.setObjectName("programCode")
        self.verticalLayout.addWidget(self.programCode)
       
        #Program Name
        #------------------------------------------------------------------------------------
        self.programNameText = QtWidgets.QLabel ("PROGRAM NAME:", self.verticalLayoutWidget)
        self.programNameText.setFont(fixedsys_font)
        self.programNameText.setObjectName("programNameText")
        self.verticalLayout.addWidget(self.programNameText)

        self.programName= QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.programName.setFont(fixedsys_font)
        self.programName.setObjectName("programName")
        self.verticalLayout.addWidget(self.programName)

        #College Code
        #----------------------------------------------------------------------------------
        self.collegeCodeText = QtWidgets.QLabel("COLLEGE CODE:", self.verticalLayoutWidget) 
        self.collegeCodeText.setFont(fixedsys_font)
        self.collegeCodeText.setObjectName("collegeCodeText")
        self.verticalLayout.addWidget(self.collegeCodeText)

        self.collegeCode = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.load_college_codes()
        self.collegeCode.setFont(fixedsys_font)
        self.collegeCode.setObjectName("collegeCode")
        self.verticalLayout.addWidget(self.collegeCode)


        # Confirmation Button
        #-----------------------------------------------------------------------------------------------------------------------------
        self.confirmationButton = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel, self)
        self.confirmationButton.setGeometry(QtCore.QRect(230, 230, 156, 30))
        self.confirmationButton.setFont(fixedsys_font)
        self.confirmationButton.setObjectName("confirmationButton")
        self.confirmationButton.accepted.connect(self.accept_data)
        self.confirmationButton.rejected.connect(self.reject)

        self.editing = program_data is not None
        if self.editing:
            self.addProgram.setText("EDIT PROGRAM")
            self.addProgram.setGeometry(QtCore.QRect(140, 20, 141, 18))
            self.programCode.setText(program_data[0])
            self.programName.setText(program_data[1])
            self.collegeCode.setCurrentText(program_data[2])
            

        #Validators
        #-------------------------------------------------------------------------------------------------------------
        text_validator = QRegularExpressionValidator(QRegularExpression(r"^[A-Za-z](?:[A-Za-z\s-]*[A-Za-z])?$"), self)
        self.programCode.setValidator(text_validator)
        self.programName.setValidator(text_validator)
        

        # -------------------------------- #
        #       Program Data Manager       #
        # -------------------------------- #
    def accept_data(self):
        program_code = re.sub(r'\s+', ' ', self.programCode.text().strip())
        program_name = re.sub(r'\s+', ' ', self.programName.text().strip())
       

        self.programCode.setText(program_code)
        self.programName.setText(program_name)
       

        if not program_code or not program_name:
            QMessageBox.warning(self, "Input Error", "All fields must be filled out before submitting.")
            return

        invalid_fields = []
        text_regex = r"^[A-Za-z]+(?:\s[A-Za-z]+)*(?:-[A-Za-z]+)?$"  # No numbers allowed

        if not re.match(text_regex, program_code):
            invalid_fields.append("Program Code")

        if not re.match(text_regex, program_name):
            invalid_fields.append("Program Name")

        if invalid_fields:
            QMessageBox.warning(self, "Input Error", f"{', '.join(invalid_fields)} should be properly formatted.")
            return

        if self.is_duplicate_program(program_code):
            QMessageBox.warning(self, "Duplicate Error", f"\nProgram Code: {program_code.upper()} already exists.")
            return

        program_data = self.get_data()

        if self.editing:
            self.program_edited.emit(program_data)
        else:
            self.program_added.emit(program_data)

        self.accept()

    def is_duplicate_program(self, program_code):
        self.database.connect_database()
        cursor = self.database.cursor
        conn = self.database.connection


        program_code_lower = program_code.strip().lower()
        

        if self.editing and program_code_lower == self.original_code:
            
            return False
        
        try:
            query = '''
                    SELECT programCode from programtable WHERE LOWER(programCode) = %s
            '''
            cursor.execute(query, (program_code_lower,))
            result = cursor.fetchone()

            if result:           
                if self.editing and program_code_lower == self.original_code:
                    return False
                return True
            
            return False
        
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Error checking duplicate program codes:\n{str(e)}")
            return True
        
        finally:
            cursor.close()
            conn.close()         

    def get_data(self):
        return [
            self.programCode.text(),
            self.programName.text(),
            self.collegeCode.currentText()
        ]
    def load_college_codes(self):
        self.collegeCode.clear()

        try:            
            self.database.connect_database()
            cursor = self.database.cursor
            conn = self.database.connection

            cursor.execute(f"SELECT collegeCode from collegetable")
            college_codes = cursor.fetchall()

            for code in college_codes:
                self.collegeCode.addItem(code[0])

        except Exception as e:
            QMessageBox.critical(None, "Error", f"Failed to load College codes:\n{str(e)}")   

        finally:
            cursor.close()
            conn.close()





