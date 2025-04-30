from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QHBoxLayout, QTableWidget
from PyQt5.QtGui import QIcon, QStandardItem, QStandardItemModel
from PyQt5.QtCore import Qt

import sys, csv, copy, pymysql

from Images import header_rc
from Database_Manager.database import DatabaseManager
from SearchBar.searchTab import SearchBar
from Popups.AddStudent import AddStudent
from Popups.AddProgram import AddProgram
from Popups.AddCollege import AddCollege
from Buttons.addButton import AddButton
from Buttons.removeButton import RemoveButton
from Buttons.updateButton import UpdateButton
from Buttons.editButton import EditButton


class Display(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    '''=========================================================='''
    '''|                    WINDOW DISPLAY                      |'''
    '''=========================================================='''
    
    def setupUi(self, MainWindow):

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(878, 564)
        MainWindow.setMinimumSize(QtCore.QSize(878, 600))
        MainWindow.setMaximumSize(QtCore.QSize(878, 600))
        MainWindow.setWindowIcon(QIcon("Images/ChickIcon.png"))
        MainWindow.setStyleSheet("background-color: #fce090")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.header = QtWidgets.QLabel(self.centralwidget)
        self.header.setGeometry(QtCore.QRect(100, 18, 381, 41))
        font = QtGui.QFont()
        font.setFamily("Pixeboy")
        font.setPointSize(24)
        self.header.setFont(font)
        self.header.setObjectName("header")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 10, 81, 61))
        self.label.setStyleSheet("background-image: url(:/newPrefix/Icons for SSIS/Untitled_design-removebg-preview.png);")
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/newPrefix/Icons for SSIS/Untitled_design-removebg-preview.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        
        #INITIALIZED CONNECTION TO DATABASE
        #-------------------------------------------------
        self.database = DatabaseManager()

        # -------------------------------- #
        #             BUTTONS              #
        # -------------------------------- #    
        
        # ADD BUTTON
        # ------------------------------------------------
        AddButton(self) 
        self.addButton.clicked.connect(self.show_add_entry) 

        # REMOVE BUTTON
        # ------------------------------------------------
        RemoveButton(self)
        self.removeButton.clicked.connect(self.removeData)

        # UPDATE BUTTON
        # ------------------------------------------------
        UpdateButton(self) 
        self.updateButton.clicked.connect(self.performUpdate)
        self.updateButton.setVisible(False) 
        self.last_update_type = None

        # EDIT BUTTON
        # ------------------------------------------------
        EditButton(self)
        self.editButton.clicked.connect(self.edit_student)


        # -------------------------------- #
        #           SEARCH BAR             #
        # -------------------------------- #        
        self.searchTab = SearchBar(self.centralwidget)
        self.searchTab.setGeometry(QtCore.QRect(680, 52, 181, 25))
        self.searchTab.setObjectName("searchTab")
        self.searchTab.setStyleSheet("""background-color: white; 
                                        border: 3px solid peru; 
                                        border-radius: 9px; 
                                        padding: 2px;
                                        color: gray;
                                        font-family: "Fixedsys";
                                        font-size: 12px;""")
        self.searchTab.textChanged.connect(self.searchContent)
        

                    
        # -------------------------------- #
        #           TABLE DISPLAY          #
        # -------------------------------- #     
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setGeometry(QtCore.QRect(25, 130, 825, 401))
        self.tableView.setObjectName("tableView")
        self.tableView.setStyleSheet("""
            background-color: white;
            border: 3px solid peru;                      
            selection-background-color: #ffcc80;  /* Change highlight color */    
            selection-color: white;  /* Change text color of selected row */                                              
                                                 
        """)
        
        self.layout = QtWidgets.QVBoxLayout(self.centralwidget)

        self.model = QtGui.QStandardItemModel(MainWindow)

        # -------------------------------- #
        #         SORTING COLUMNS          #
        # -------------------------------- #   
        self.proxy_model = QtCore.QSortFilterProxyModel()
        self.proxy_model.setSourceModel(self.model)
        self.proxy_model.setSortCaseSensitivity(QtCore.Qt.CaseInsensitive)  # Case-insensitive sorting
        self.proxy_model.setSortRole(QtCore.Qt.DisplayRole)  # Sort by display text
        
        self.tableView.setModel(self.proxy_model)  # Apply proxy model to table
        self.tableView.setSortingEnabled(True)  # Enable sorting'''

        self.tableView.selectionModel().selectionChanged.connect(self.highlight_selected_row) #Selected row is bolder in color

        #self.tableView.setModel(self.model)
        self.tableView.verticalHeader().setVisible(False)
        self.tableView.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch) #For table display automatic fitting
        
        #Focus and Selection of Rows    
        self.tableView.setSelectionBehavior(QtWidgets.QTableView.SelectRows) #Highlight the entire rows
        self.tableView.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableView.setFocusPolicy(Qt.NoFocus)

        
        

        

        
        


        


        # -------------------------------- #
        #           TABS DISPLAY           #
        # -------------------------------- #  
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setStyleSheet("""
            QTabBar {                                                                   
            font-family: Fixedsys;                          
            font: bold;                                                
            }

            /* Tabs */
            QTabBar::tab {
                color: #BEA67A;                    
                min-width: 100px;  /* Tab width */
                height: 15px;  /* Tab height */                                
                padding: 10px;
                border: 2px solid black; /* Dark Brown Border */
                border-radius: 10px;
                
            }

            /* Selected Tab */
            QTabBar::tab:selected {
                background: #CD853F; 
                color: #fce090;
               
            }

            /* Unselected Tabs */
            QTabBar::tab:!selected {
                width: 69px;
                                                       
            }                                                                                                          
        """)
        self.tabWidget.setGeometry(QtCore.QRect(25, 91, 825, 432))
        self.tabWidget.setMouseTracking(False)
        self.tabWidget.setAutoFillBackground(False)
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.tabWidget.setMovable(False)
        self.tabWidget.setObjectName("tabWidget")
        self.studentTab = QtWidgets.QWidget()
        self.studentTab.setObjectName("studentTab")
        self.tabWidget.addTab(self.studentTab, "")
        self.programTab = QtWidgets.QWidget()
        self.programTab.setObjectName("programTab")
        self.tabWidget.addTab(self.programTab, "")
        self.collegeTab = QtWidgets.QWidget()
        self.collegeTab.setObjectName("collegeTab")
        self.tabWidget.addTab(self.collegeTab, "")
        self.tableView.raise_()
        
      
        # -------------------------------- #
        #       SEARCH BAR COMBO BOX       #
        # -------------------------------- #  
        self.searchComboBox = QtWidgets.QComboBox(self.centralwidget)
        self.searchComboBox.setGeometry(QtCore.QRect(547, 52, 123, 25)) 
        self.searchComboBox.setObjectName("searchComboBox")
        self.searchComboBox.setStyleSheet("""
            QComboBox {
                background-color: white; 
                border: 3px solid peru; 
                padding: 2px;
                color: gray;
                font-family: "Fixedsys";                                                                                 
            }      

            /* Dropdown Styling */
            QComboBox QAbstractItemView {
                background-color: white;
                selection-background-color: #ffcc80; /* Background color when selected */
                selection-color: white; /* Font color when selected */
                border: 1px solid peru;
            }

            QComboBox QAbstractItemView::item {
                color: black; 
            }

            QComboBox:on {
                color: peru;
            }
        """)
        #Default Combo Box Options
        self.searchComboBox.addItem("Search By:")
        self.searchComboBox.addItems(["Student ID", "First Name", "Last Name", "Year Level", "Gender", "Program Code"])
        

        #Invisible Features (not enabled in Qt Designer)
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        #CSV Display
        self.studentTable() #Display Student Tab after running
        self.tabWidget.currentChanged.connect(self.displayTabs)



    '''=========================================================='''
    '''|                   DATABASE MANAGEMENT                   '''
    '''=========================================================='''

    # DELETING ROWS FROM TABS  
    # ----------------------------------------------------------------
    def removeData(self):
        selected_tab = self.tabWidget.currentIndex()
        selected_rows = self.tableView.selectionModel().selectedRows()
        
        if not selected_rows:
            message = QMessageBox()
            message.setWindowIcon(QIcon("Images/ChickIcon.png"))
            QMessageBox.warning(None, "Warning", "Please select a row")
            return

        # Custom Messages Based on Tab
        if selected_tab == 0:  # Student Tab
            title = "Delete Student"
            message = "\nAre you sure you want to delete the selected student?\nThis action cannot be undone!"
            icon = QMessageBox.Warning

        elif selected_tab == 1:  # Program Tab
            title = "Delete Program"
            message = "\nAre you sure you want to delete this program?\n It will affect all students enrolled in it."
            icon = QMessageBox.Critical

        elif selected_tab == 2:  # College Tab
            title = "Delete College"
            message = "\nAre you sure you want to delete this college?\nAll associated entries will be affected."
            icon = QMessageBox.Question


        # Create Unique QMessageBox
        confirm = QMessageBox()
        confirm.setWindowTitle(title)
        confirm.setText(message)
        confirm.setIcon(icon)
        confirm.setWindowIcon(QIcon("Images/ChickIcon.png"))  # Set custom icon
        confirm.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        confirm.setDefaultButton(QMessageBox.No)
        
        response = confirm.exec_()

        if response == QMessageBox.No:
            return

        # Proceed with deletion logic
        selected_rows.sort(reverse=True, key=lambda x: x.row())  # Avoid shifting issues

        for index in selected_rows:
            source_index = self.proxy_model.mapToSource(index)
            actual_row = source_index.row()
            row_data = [self.model.item(actual_row, col).text() if self.model.item(actual_row, col) else "" 
                        for col in range(self.model.columnCount())]

            self.model.removeRow(actual_row)

            if selected_tab == 2:  # College Tab
                self.cascade_delete_college(row_data[0])

            elif selected_tab == 1:  # Program Tab
                self.cascade_delete_program(row_data[0])

            elif selected_tab == 0:  # Student Tab
                self.delete_student(row_data[0])
              
    

    # SAVING CSV CHANGES (UNRESOLVED)
    # ----------------------------------------------------------------
    def updateDatabase(self, table_name, pk_column, pk_value, updated_data: dict):
        try:
            self.database.connect_database()
            cursor = self.database.cursor
            conn = self.database.connection

            set_clause = ','.join([f"{col} = %s" for col in updated_data.keys()])
            values = list(updated_data.values()) 
            values.append(pk_value)


            query = f'''
                UPDATE {table_name}
                SET {set_clause}
                WHERE {pk_column} = %s
                
            '''
            
            cursor.execute(query, values)
            conn.commit()

            

        except Exception as e:
            conn.rollback()
            #QMessageBox.critical(None, "Update Error", f"Failed to update record:\n {str(e)}")
            print(f"Failed to update record:\n {str(e)}")
        finally:
            cursor.close()
            conn.close()

    def performUpdate(self):
        table_map = {
            "Student": ("studenttable", "studentId"),
            "Program": ("programtable", "programCode"),
            "College": ("collegetable", "collegeCode")
        }

        column_map = {
            "Student": {
                "STUDENT ID": "studentId",
                "FIRST NAME": "firstName",
                "LAST NAME": "lastName",
                "YEAR LEVEL": "yearLevel",
                "GENDER": "gender",
                "PROGRAM CODE": "programCode"
            },
            "Program": {
                "PROGRAM CODE": "programCode",
                "PROGRAM NAME": "programName",
                "COLLEGE CODE": "collegeCode"
            },
            "College": {
                "COLLEGE CODE": "collegeCode",
                "COLLEGE NAME": "collegeName"
            }
        }

        if self.last_update_type not in table_map:
            return

        table_name, pk_column = table_map[self.last_update_type]
        col_map = column_map[self.last_update_type]

        changes_made = False

        for row in range(self.model.rowCount()):
            pk_value = self.model.item(row, 0).text()
            updated_data = {}
            row_changed = False

            for col in range(1, self.model.columnCount()):
                column_name = self.model.headerData(col, Qt.Horizontal)
                db_col = col_map.get(column_name)
                if not db_col:
                    continue

                item = self.model.item(row, col)
                current_value = item.text() if item else ""
                original_value = item.data(Qt.UserRole) or ""

                if current_value.strip() != original_value.strip():
                    updated_data[db_col] = current_value
                    row_changed = True

            if row_changed:
                self.updateDatabase(table_name, pk_column, pk_value, updated_data)
                changes_made = True

        if changes_made:
            self.displayDatabase(table_name)
            QMessageBox.information(None, "Success", f"{self.last_update_type} records have been updated successfully!")
        else:
            QMessageBox.information(None, "No Changes", f"No changes detected in {self.last_update_type} records.")

        self.updateButton.setVisible(False)
        self.last_update_type = None





    # Update prompts when closing the application
    #--------------------------------------------
    def closeEvent(self, event):
        if self.updateButton.isVisible():
            reply = QMessageBox.question(
                self, "Unsaved Changes", 
                "You have unsaved Changes. Do you want to save them before exiting?",
                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
            )

            if reply == QMessageBox.Yes:
                self.performUpdate()
                event.accept()
            elif reply == QMessageBox.No:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()


    def getActiveTable(self):
        if self.tabWidget.currentIndex() == 0:
            return "studenttable"
        elif self.tabWidget.currentIndex() == 1:
            return "programtable"
        elif self.tabWidget.currentIndex() == 2:
            return "collegetable"
        return None

    '''=========================================================='''
    '''|                       SEARCHBAR                        |''' 
    '''==========================================================''' 
    def searchContent(self):
        search_text = self.searchTab.text().strip().lower()  # Get the text from search bar
        selected_column = self.searchComboBox.currentText()
        table_name = self.getActiveTable()
        self.database.connect_database()
        cursor = self.database.cursor
        conn = self.database.connection

        if not table_name:
            print("Error: No table selected")
            return

        if not search_text or selected_column == "Search By:":
            if table_name:
                self.displayDatabase(table_name)
            return
        
        column_mapping = {
                "studenttable": {     
                    "Student ID": "studentId",
                    "First Name": "firstName", 
                    "Last Name": "lastName", 
                    "Year Level": "yearLevel", 
                    "Gender": "gender", 
                    "Program Code": "programCode"
                },
                
                "programtable": {
                    "Program Code": "programCode",
                    "Program Name": "programName",
                    "College Code": "collegeCode"
                },

                "collegetable": {
                    "College Code": "collegeCode",
                    "College Name": "collegeName"
                }
            }

        try:   
            cursor.execute(f"SHOW COLUMNS FROM `{table_name}`")
            headers = [column[0] for column in cursor.fetchall()]
            self.model.clear()
            display_headers = self.getCustomHeaders(table_name, headers)
            self.model.setHorizontalHeaderLabels(display_headers)
            
            column_map = column_mapping.get(table_name, {})
            database_column  = column_map.get(selected_column)
            if not database_column or database_column not in headers:
                print(f"Column `{selected_column}` not found in table `{table_name}`")
                return
            
            query = f"""
                    SELECT * FROM `{table_name}` 
                    WHERE LOWER(`{database_column}`) LIKE %s
                    """
            
            cursor.execute(query, (f"%{search_text}%",))
            results = cursor.fetchall()

            for row in results:
                items = [QStandardItem(str(field)) for field in row]
                self.model.appendRow(items)

        except pymysql.MySQLError as err:
                print(f"MySQL error: {err}")

        finally:
            cursor.close()
            conn.close()
           

    def updateComboBox(self, items):
        self.searchComboBox.clear()  
        for item in items:
            self.searchComboBox.addItem(item)
            
    #Column Search
    def getColumnIndex(self, column_name):
        headers = [self.model.headerData(i, Qt.Horizontal) for i in range(self.model.columnCount())]
        
        if not headers:
            print("Error: No headers found in the table.")
            return None

        headers_upper = [header.upper() for header in headers if header]
        column_name_upper = column_name.upper()

        if column_name_upper in headers_upper:
            return headers_upper.index(column_name_upper)
        else:
            print(f"Error: Column '{column_name}' not found in headers: {headers}")
            return None
            
                                                #########################################################
                                                #                  TAB TABLE DISPLAY                    #
                                                #########################################################  
   
   
    def displayTabs(self, index):
        self.model.clear()
        
        # 1.) STUDENT TAB
        # ---------------------------------------------
        if index == 0:  
            self.studentTable() #Display correct csv
            self.proxy_model.sort(0, QtCore.Qt.AscendingOrder)
            self.addButton.setText("Add Student")
            self.removeButton.setText("Remove Student")
            self.updateButton.setText("Update Student")
            self.editButton.setText("Edit Student")
            self.editButton.clicked.disconnect()  
            self.editButton.clicked.connect(self.edit_student)
            self.updateComboBox(["Search By:", "Student ID", "First Name", "Last Name", "Year Level", "Gender", "Program Code"]) #Updates the search bar combo box
            
        # 2.) PROGRAM TAB
        # ---------------------------------------------
        elif index == 1:  
            self.programTable() #Display correct csv
            self.proxy_model.sort(0, QtCore.Qt.AscendingOrder)
            self.addButton.setText("Add Program")
            self.removeButton.setText("Remove Program")
            self.updateButton.setText("Update Program")
            self.editButton.setText("Edit Program")
            self.editButton.clicked.disconnect()  
            self.editButton.clicked.connect(self.edit_program)
            self.updateComboBox(["Search By:", "Program Code", "Program Name", "College Code"]) #Updates the search bar combo box
            
        # 2.) COLLEGE TAB
        # ---------------------------------------------
        elif index == 2:  
            self.collegeTable()#Display correct csv
            self.proxy_model.sort(0, QtCore.Qt.AscendingOrder)
            self.addButton.setText("Add College")
            self.removeButton.setText("Remove College")
            self.updateButton.setText("Update College")
            self.editButton.setText("Edit College")
            self.editButton.clicked.disconnect()  
            self.editButton.clicked.connect(self.edit_college)
            self.updateComboBox(["Search By:", "College Code", "College Name"]) #Updates the search bar combo box        

    
        # -------------------------------- #
        #       ROW HIGHLIGHT STYLE        #
        # -------------------------------- # 
    def highlight_selected_row(self, selected, deselected):
        # Reset font for all rows first
        for row in range(self.model.rowCount()):
            for col in range(self.model.columnCount()):
                item = self.model.item(row, col)
                if item:
                    font = item.font()
                    font.setBold(False)  # Reset to normal
                    item.setFont(font)

        # Apply bold font to selected rows
        for index in selected.indexes():
            row = index.row()
            for col in range(self.model.columnCount()):
                item = self.model.item(row, col)
                if item:
                    font = item.font()
                    font.setBold(True)  # Make selected row bold
                    item.setFont(font)

    # -------------------------------- #
    #         CUSTOM HEADERS           #
    # -------------------------------- #    
    def getCustomHeaders(self, table_name, db_headers):
        column_mapping = {
                "studenttable": {     
                    "studentId": "STUDENT ID",
                    "firstName": "FIRST NAME", 
                    "lastName": "LAST NAME", 
                    "yearLevel": "YEAR LEVEL", 
                    "gender": "GENDER", 
                    "programCode": "PROGRAM CODE"
                },
                
                "programtable": {
                    "programCode": "PROGRAM CODE",
                    "programName": "PROGRAM NAME",
                    "collegeCode": "COLLEGE CODE"
                },

                "collegetable": {
                    "collegeCode": "COLLEGE CODE",
                    "collegeName": "COLLEGE NAME"
                }
            }
        mapping = column_mapping.get(table_name, {})
        return [mapping.get(col, col) for col in db_headers]

    # -------------------------------- #
    #        DISPLAYING DATABASE       #
    # -------------------------------- #    
    def displayDatabase(self, table_name):
        try:
            self.database.connect_database()
            cursor = self.database.cursor
            conn = self.database.connection

            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]


            self.model.setHorizontalHeaderLabels(columns)
            self.model.removeRows(0, self.model.rowCount())

            if table_name == 'programtable':
                rows = [row for row in rows if row[columns.index('programCode')] != "UNENROLLED"]
                

            for row in rows: 
                new_row = []
                for idx, field in enumerate(row):
                    if columns[idx] == "programCode":
                        value = field if field and str(field).strip() else "UNENROLLED"
                    else:
                        value = field if field is not None else ""

                    item = QStandardItem(str(value))
                    item.setData(str(value), Qt.UserRole)
                    new_row.append(QStandardItem(str(value)))
                self.model.appendRow(new_row)
    
            # CUSTOM HEADERS
            #-----------------------------------
            
            table_name = self.getActiveTable()
            

            cursor.execute(f"SHOW COLUMNS FROM `{table_name}`")
            database_headers = [column[0] for column in cursor.fetchall()]

            
            display_headers = self.getCustomHeaders(table_name, database_headers)

            
            self.model.setHorizontalHeaderLabels(display_headers)
            self.model.layoutChanged.emit()
        
        except Exception as e:
            print(f"Error loading data from {table_name}: {e}")
        finally:
                try:
                    cursor.close()
                    conn.close()
                except:
                    pass
            
    def studentTable(self, force_refresh = False):
        self.proxy_model.sort(0, QtCore.Qt.AscendingOrder)
        self.displayDatabase("studenttable")
    
    def programTable(self):
        self.displayDatabase("programtable")
    
    def collegeTable(self):
        self.displayDatabase("collegetable")
    
    '''======================================================================='''
    '''|                                                                     |'''       
    '''|    SETTING DESIGN FOR BUTTONS, WINDOW TITLE, AND SEARCH COMBO BOX   |'''
    '''|                                                                     |'''
    '''======================================================================='''

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Student Information System"))
        self.addButton.setText(_translate("MainWindow", "Add Student"))
        self.removeButton.setText(_translate("MainWindow", "Remove Student"))
        self.updateButton.setText(_translate("MainWindow", "Update Student"))
        self.editButton.setText(_translate("MainWindow", "Edit Student"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.studentTab), _translate("MainWindow", "Student"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.programTab), _translate("MainWindow", "Program"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.collegeTab), _translate("MainWindow", "College"))
        self.header.setText(_translate("MainWindow", "STUDENT INFORMATION SYSTEM"))
        self.header.setStyleSheet("""color: peru
                                  """)
        button_style = """
        QPushButton {
            background-color: white;  /* White background */
            color: #4C4A4D;               /* Black Font */
            border: 1px solid #978C76;  /* Darker border */
            border-radius: 9px;         /* Rounded corners */
            padding: 5px;               /* Padding inside button */
        }
        QPushButton:hover {
            background-color: #c1c8d4;  /* When hovered */
        }
        QPushButton:pressed {
            background-color: #969ba3;  /* Darker gray when clicked */
        }
        """

        # Apply the style to all buttons
        self.addButton.setStyleSheet(button_style)
        self.removeButton.setStyleSheet(button_style)
        self.updateButton.setStyleSheet(button_style)
        self.editButton.setStyleSheet(button_style)


                                                        #########################################################
                                                        #                   MODIFYNG ENTRIES                    #
                                                        ######################################################### 

    '''=========================================================='''
    '''|                   EDITING ENTRIES                      |'''
    '''=========================================================='''
  
    def edit_student(self):
        self.database.connect_database()
        cursor = self.database.cursor
        conn = self.database.connection

        
        selected_index = self.tableView.selectionModel().currentIndex()
        if not selected_index.isValid():
            QMessageBox.warning(None, "Selection Error", "Please select a student to edit.")
            return
       
        if selected_index.model() != self.proxy_model:
            QMessageBox.critical(None, "Error", "Selected index is not from proxy model!")
            return

        
        source_index = self.proxy_model.mapToSource(selected_index)
        selected_row = source_index.row()

        
        student_id_index = self.model.index(selected_row, 0)
        student_id = self.model.data(student_id_index)

       

        if not student_id:
            QMessageBox.warning(None, "Error", "Selected row has no Student ID.")
            return

        try:
            query = '''
                SELECT studentId, firstName, lastName, yearLevel, gender, programCode 
                FROM studenttable
                WHERE studentId = %s
            '''
            cursor.execute(query, (student_id,))
            result = cursor.fetchone()

            if not result:
                QMessageBox.critical(None, "Error", "Student record not found in the database.")
                return

            student_data = list(result)

        except Exception as e:
            QMessageBox.critical(None, "Database Error", f"Failed to retrieve student:\n{str(e)}")
            return

        finally:
            cursor.close()
            conn.close()

        # Open the AddStudent dialog pre-filled with existing data
        edit_dialog = AddStudent(self.centralwidget, student_data, table_model=self.model)
        if edit_dialog.exec_() == QtWidgets.QDialog.Accepted:
            updated_data = edit_dialog.get_data()
            self.apply_student_edits(selected_row, updated_data)  




    # EDITING PROGRAM TAB
    #---------------------------
    def edit_program(self):
        self.database.connect_database()
        cursor = self.database.cursor
        conn = self.database.connection
    
        selected_index = self.tableView.selectionModel().currentIndex()
        if not selected_index.isValid():
            QMessageBox.warning(None, "Selection Error", "Please select a Program to edit.")
            return
     
        if selected_index.model() != self.proxy_model:
            QMessageBox.critical(None, "Error", "Selected index is not from proxy model!")
            return
   
        source_index = self.proxy_model.mapToSource(selected_index)
        selected_row = source_index.row()  

        program_code_index = self.model.index(selected_row, 0)
        program_code = self.model.data(program_code_index)

        if not program_code:
            QMessageBox.warning(None, "Error", "Selected row has no Program Code.")
            return

        '''program_data = [
            self.model.item(selected_row, col).text() if self.model.item(selected_row, col) else ""
            for col in range(self.model.columnCount())
        ]'''

        try:
            query = '''
                SELECT programCode, programName, collegeCode
                FROM programtable
                WHERE programCode = %s
            '''
        
            cursor.execute(query, (program_code,))
            result = cursor.fetchone()

            if not result:
                QMessageBox.critical(None, "Error", "Program record not found in the database.")
                return
            
            program_data = list(result)

        except Exception as e:
            QMessageBox.critical(None, "Database Error", f"Failed to retrieve program:\n{str(e)}")
            return
            
        finally:
            cursor.close()
            conn.close()
            
        edit_dialog = AddProgram(self.centralwidget, program_data, table_model = self.model)
        if edit_dialog.exec_() == QtWidgets.QDialog.Accepted:
            updated_data = edit_dialog.get_data()
            self.apply_program_edits(selected_index.row(), updated_data)

    # EDITING COLLEGE TAB
    #---------------------------
    def edit_college(self):
        self.database.connect_database()
        cursor = self.database.cursor 
        conn = self.database.connection


        selected_index = self.tableView.selectionModel().currentIndex()
        if not selected_index.isValid():
            QMessageBox.warning(None, "Selection Error", "Please select a College to edit.")
            return

        if selected_index.model() != self.proxy_model:
            QMessageBox.critical(None, "Error", "Selected index is not from proxy model!")
            return
        
        # Convert proxy index to source index
        source_index = self.proxy_model.mapToSource(selected_index)
        selected_row = source_index.row()

        college_code_index = self.model.index(selected_row, 0)
        college_code = self.model.data(college_code_index)

        if not college_code:
            QMessageBox.warning(None, "Error", "Selected row has no College Code.")
            return
        
        
        try:
            query = '''
                    Select collegeCode, collegeName
                    FROM collegetable
                    WHERE collegeCode = %s
            '''

            cursor.execute(query, (college_code,))
            result = cursor.fetchone()

            if not result:
                QMessageBox.critical(None, "Error", "College record not found in the database.")
                return

            college_data = list(result)

        except Exception as e:
            QMessageBox.critical(None, "Database Error", f"Failed to retrieve college:\n{str(e)}")
            return

        finally:
            cursor.close()
            conn.close()

  

        edit_dialog = AddCollege(self.centralwidget, college_data, table_model=self.model)
        if edit_dialog.exec_() == QtWidgets.QDialog.Accepted:
            updated_data = edit_dialog.get_data()

            #Prevent the College tab from resetting the table after editing
            self.is_editing = True

            self.apply_college_edits(selected_row, updated_data)






        
    '''=========================================================='''
    '''|          STORING CHANGES TO TEMPORARY STORAGE          |'''
    '''=========================================================='''

    #Stores the edit into a copy of CSV File for it to be saved manually later
    def apply_student_edits(self, row, updated_data):
       
        if not updated_data:
            QMessageBox.warning(None, "Error", "No data provided.")
            return

        for col, value in enumerate(updated_data):
            item = QtGui.QStandardItem(value)
            self.model.setItem(row, col, item)

        #proxy_model.sort(0, QtCore.Qt.AscendingOrder)
        self.last_update_type = "Student"
        self.updateButton.setVisible(True)

        QMessageBox.information(None, "Success", "Changes applied! Click 'Update' to save them permanently.")
    

    
    def apply_program_edits(self, proxy_row, updated_data):
        if not updated_data:
            QMessageBox.warning(None, "Error", "No data provided.")
            return

        # Convert proxy row to source row
        source_index = self.proxy_model.mapToSource(self.proxy_model.index(proxy_row, 0))
        row = source_index.row()

        old_program_code_item = self.model.item(row, 0)
        if old_program_code_item is None or old_program_code_item.text().strip() == "":
            QMessageBox.warning(None, "Error", "No valid Program Code found.")
            return

        old_program_code = old_program_code_item.text().strip()
        new_program_code = updated_data[0].strip()

        # Update UI Table Model (Program Tab)
        for col, value in enumerate(updated_data):
            item = QtGui.QStandardItem(value)
            self.model.setItem(row, col, item)

        # Update related students
        if old_program_code != new_program_code:
            self.cascade_programCode(old_program_code, new_program_code)

        self.programTable()

        QMessageBox.information(None, "Success", "Program Code updated and saved automatically!")

    def apply_college_edits(self, row, updated_data):
        if not updated_data:
            QMessageBox.warning(None, "Error", "No data provided.")
            return

        old_college_code_item = self.model.item(row, 0)
        if old_college_code_item is None or old_college_code_item.text().strip() == "":
            QMessageBox.warning(None, "Error", "No valid College Code found.")
            return

        old_college_code = old_college_code_item.text().strip()
        new_college_code = updated_data[0].strip()

        #  Update UI Table Model (College Tab)
        for col, value in enumerate(updated_data):
            item = self.model.item(row, col)
            if item:
                item.setData(value, QtCore.Qt.DisplayRole)
            else:
                self.model.setItem(row, col, QtGui.QStandardItem(value))

        # Update related programs if College Code changed
        if old_college_code != new_college_code:
            self.cascade_collegeCode(old_college_code, new_college_code)

        #  Save changes immediately
        self.collegeTable()

        QMessageBox.information(None, "Success", "College Code updated and saved automatically!")


    '''=========================================================='''
    '''|                  CASCADING EFFECT                      |'''
    '''=========================================================='''

    # Cascade changes in Program Code
    # -------------------------------
    def cascade_programCode(self, old_programCode, new_programCode):
        try:
            self.database.connect_database()
            cursor = self.database.cursor
            conn  = self.database.connection

           
            update_program_programCode = '''
                UPDATE programtable
                SET programCode = %s
                WHERE programCode = %s
            '''
            cursor.execute(update_program_programCode, (new_programCode, old_programCode))
             
            update_student_programCode = '''
                UPDATE studenttable
                SET programCode = %s
                WHERE programCode = %s
            '''
            cursor.execute(update_student_programCode, (new_programCode, old_programCode))
            
            conn.commit()

            self.studentTable()
            self.programTable()
            self.displayTabs(self.tabWidget.currentIndex())
        
        except Exception as e:
            conn.rollback()
            #QMessageBox.critical(None, "Database Error", f"Failed to update program code:\n{str(e)}")
            print(f"Failed to update program code:\n{str(e)}")

        finally:
            cursor.close()
            conn.close()

    # Cascade changes in College Code
    # -------------------------------
    def cascade_collegeCode(self, old_collegeCode, new_collegeCode):
        try:
            self.database.connect_database()
            cursor = self.database.cursor
            conn = self.database.connection

            update_college_collegeCode = '''
                UPDATE collegetable
                SET collegeCode = %s
                WHERE collegeCode = %s
            '''
            cursor.execute(update_college_collegeCode, (new_collegeCode, old_collegeCode))

            update_program_collegeCode = '''
                UPDATE programtable
                SET collegeCode = %s
                WHERE collegeCode = %s
            '''
            cursor.execute(update_program_collegeCode,(new_collegeCode, old_collegeCode))

            conn.commit()

            self.studentTable()
            self.programTable()
            self.collegeTable()
            self.displayTabs(self.tabWidget.currentIndex())

        except Exception as e:
            conn.rollback()
            QMessageBox.critical(None, "Database Error", f"Failed to update college code:\n{str(e)}")
        finally:
            cursor.close()
            conn.close()

    # Cascade on deleting College
    # ---------------------------
    def cascade_delete_college(self, college_code):
        try:     
            self.database.connect_database()
            cursor = self.database.cursor
            conn = self.database.connection

            select_programs = '''
                SELECT programCode from programtable 
                WHERE collegeCode = %s
            '''
            cursor.execute(select_programs, (college_code,))
            program_codes = cursor.fetchall()
            if program_codes:
                program_codes_list = [row[0] for row in program_codes]
                placeholders = ', '.join(['%s'] * len(program_codes_list))
                update_students = f'''
                    UPDATE studenttable
                    SET programCode = 'UNENROLLED'
                    WHERE programCode IN ({placeholders})
                '''
                cursor.execute(update_students, program_codes_list)
            
            deleting_programs = '''
                DELETE FROM programtable
                WHERE collegeCode = %s
            '''
            cursor.execute(deleting_programs, (college_code,))

            deleting_college = '''
                DELETE FROM collegetable
                WHERE collegeCode = %s
            '''
            cursor.execute(deleting_college, (college_code,))
                
            
            conn.commit()


            self.studentTable()
            self.programTable()
            self.collegeTable()
            self.displayTabs(self.tabWidget.currentIndex())

            
            QMessageBox.information(None, "Success", "College deleted and associated entries updated successfully!")

        except Exception as e:
            conn.rollback()  
            QMessageBox.critical(None, "Database Error", f"Failed to delete college:\n{str(e)}")
        finally:
            cursor.close()
            conn.close()

    # Cascade on deleting Program
    # ---------------------------
    def cascade_delete_program(self, program_code):
        try:
            self.database.connect_database()
            cursor = self.database.cursor
            conn = self.database.connection

            select_students = '''
                SELECT studentId from studenttable
                WHERE programCode = %s 
            '''
            cursor.execute(select_students,(program_code,))
            students = cursor.fetchall()

            if students:
                student_list = [row[0] for row in students]
                placeholders = ','.join(['%s'] * len(student_list))
                update_students = f'''
                    UPDATE studenttable
                    SET programCode = 'UNENROLLED'
                    WHERE programCode in ({placeholders})
                '''
                cursor.execute(update_students, student_list)

            deleting_programs = '''
                DELETE FROM programtable
                WHERE programCode = %s
            '''
            cursor.execute(deleting_programs, (program_code,))

            conn.commit()

            self.studentTable()
            self.programTable()
            self.displayTabs(self.tabWidget.currentIndex())

            QMessageBox.information(None, "Success", "Program deleted and students updated successfully!")
        
        except Exception as e:
            conn.rollback()  
            QMessageBox.critical(None, "Database Error", f"Failed to delete program:\n{str(e)}")
        finally:
            cursor.close()
            conn.close()

        
    def delete_student(self, student_data):
        try:
            self.database.connect_database()
            cursor = self.database.cursor
            conn = self.database.connection

            deleting_students = '''
                DELETE from studenttable
                WHERE studentId = %s
            '''

            cursor.execute(deleting_students, (student_data,))

            conn.commit()

            self.studentTable()
            self.displayTabs(self.tabWidget.currentIndex())

            QMessageBox.information(None, "Success", "Student deleted successfully!")

        except Exception as e:
            conn.rollback()
            QMessageBox.critical(None, "Error", f"Failed to delete student:\n{str(e)}")
        finally:
            cursor.close()
            conn.close()
            
    

    '''=========================================================='''
    '''|                   UPDATING RECORD                      |'''
    '''=========================================================='''

    # UPDATING STUDENT
    #-----------------------------------------------
    def update_student_record(self, updated_student):
        file_path = "CSV Files/SSIS - STUDENT.csv"
        students = []

        # Read all students
        with open(file_path, "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            students = [row for row in reader]

        # Update the student with the matching ID
        for i, student in enumerate(students):
            if student[0] == updated_student[0]:  # Match ID number
                students[i] = updated_student
                break

        # Save the updated list
        with open(file_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerows(students)

        QMessageBox.information(None, "Success", "Student added successfully! Click 'Update' to save changes.")
        
        self.studentCsv()
    
    # UPDATING PROGRAM
    #-----------------------------------------------
    def update_program_record(self, updated_program):
        file_path = "CSV Files/SSIS - PROGRAM.csv"
        programs = []

        # Read all programs
        with open(file_path, "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            programs = [row for row in reader]

        # Update the program with the matching program code
        for i, program in enumerate(programs):
            if program[0] == updated_program[0]:  # Match program code
                programs[i] = updated_program
                break

        # Save the updated list
        with open(file_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerows(programs)

        QMessageBox.information(None, "Success", "Program added successfully! Click 'Update' to save changes.")
        
        self.programCsv()

    # UPDATING COLLEGE
    #-----------------------------------------------
    def update_college_record(self, updated_college):
        file_path = "CSV Files/SSIS - COLLEGE.csv"
        colleges = []

        # Read all programs
        with open(file_path, "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            colleges = [row for row in reader]

        # Update the program with the matching program code
        for i, college in enumerate(colleges):
            if college[0] == updated_college[0]:  # Match program code
                colleges[i] = updated_college
                break

        # Save the updated list
        with open(file_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerows(colleges)

        QMessageBox.information(None, "Success", "College added successfully! Click 'Update' to save changes.")
        
        self.collegeCsv()

    '''=========================================================='''
    '''|                    ADDING ENTRY                        |'''
    '''=========================================================='''
    
    # ADDING STUDENT
    #-------------------------------------
    def add_student_to_db(self, new_data):
        self.database.connect_database()
        cursor = self.database.cursor
        conn = self.database.connection
        
        try:    
            studentId, firstName, lastName, yearLevel, gender, programCode = new_data

            query = '''
                    INSERT INTO studenttable(studentId, firstName, lastName, yearLevel, gender, programCode)
                    VALUES(%s, %s, %s, %s, %s, %s)
            '''
            cursor.execute(query, (studentId, firstName, lastName, yearLevel, gender, programCode))
            conn.commit()

            self.displayDatabase("studenttable")

            QMessageBox.information(None, "Success", "Student added successfully! Click 'Update' to save changes.")

            self.updateButton.setVisible(True)
        except Exception as e:
            conn.rollback()
            QMessageBox.critical(None, "Error", f"Failed to add student:\n{str(e)}")
        finally:
            cursor.close()
            conn.close()
            

    # ADDING PROGRAM
    #-------------------------------------
    def add_program_to_db(self, new_data):
        self.database.connect_database()
        cursor = self.database.cursor
        conn = self.database.connection

        try:
            programCode, programName, collegeCode = new_data

            query = '''
                    INSERT INTO programtable(programCode, programName, collegeCode)
                    VALUES(%s, %s, %s)
            '''

            cursor.execute(query, (programCode, programName, collegeCode))
            conn.commit()

            self.displayDatabase("programtable")

            QMessageBox.information(None, "Success", "Program added successfully! Click 'Update' to save changes.")

            self.updateButton.setVisible(True)

        except Exception as e:
            conn.rollback()
            QMessageBox.critical(None, "Error", f"Failed to add program:\n{str(e)}")
        finally:
            cursor.close()
            conn.close()

    def update_student_program_combobox(self, program_code):
        for i in range(self.studentProgram.count()):
            if self.studentProgram.itemText(i) == program_code:
                return  # Already exists

        self.studentProgram.addItem(program_code)

    # ADDING COLLEGE
    #-------------------------------------  
    def add_college_to_db(self, new_data):
        self.database.connect_database()
        cursor = self.database.cursor
        conn = self.database.connection


        try:
            collegeCode, collegeName = new_data 

            query = '''
                    INSERT INTO collegetable(collegeCode, collegeName)
                    VALUES(%s, %s)
            '''

            cursor.execute(query, (collegeCode, collegeName))
            conn.commit()
            
            self.displayDatabase("collegetable")

            QMessageBox.information(None, "Success", "College added successfully! Click 'Update' to save changes.")

            self.updateButton.setVisible(True)
        except Exception as e:
            conn.rollback()
            QMessageBox.critical(None, "Error", f"Failed to add college:\n{str(e)}")
        finally:
            cursor.close()
            conn.close()
    def update_college_code_combobox(self, college_code):
        for i in range(self.collegeCode.count()):
            if self.collegeCode.itemText(i) == college_code:
                return  # Already exists

        self.collegeCode.addItem(college_code)


    '''=========================================================='''
    '''|                     POPUP WINDOWS                      |'''
    '''=========================================================='''
    def show_add_entry(self):
        current_tab = self.tabWidget.currentIndex()

        if current_tab == 0:
            dialog = AddStudent(parent=self, student_data=None, table_model=self.model)
            
        elif current_tab == 1:
            dialog = AddProgram(parent=self, program_data=None, table_model=self.model)
            
        elif current_tab == 2:
            dialog = AddCollege(parent=self, college_data=None, table_model=self.model)
        
        else:
            return
        
        
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            new_data = dialog.get_data()
            if current_tab == 0:
                self.add_student_to_db(new_data)
            elif current_tab == 1:
                self.add_program_to_db(new_data)
            elif current_tab == 2:
                self.add_college_to_db(new_data)
