#####################################################################################
#                          MySQL STUDENT INFORMATION SYSTEM                         #                 
#                                                                                   #
#  Made by: Ajman L. Mocsana                                                        #
#  Date finished: April 30, 2025                                                    #
#                                                                                   #
#####################################################################################


import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
from UI.display import Display

def main():
    app = QApplication(sys.argv)
    UI = Display()
    
    app.setStyleSheet("""
        QMessageBox {
            background-color: #fce090; 
            color: white;  
            font-family: "Fixedsys"; 
        }

        QPushButton {
                font-family: 'Fixedsys';
                background-color: white; 
                color: black;
                border-radius: 5px;
                padding: 10px
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



    UI.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()


