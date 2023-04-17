import sys
import os.path

# Imports a py library to process pdf files
import PyPDF2

# Pyqt5 gui library
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# import braille library
from pybraille import convertText


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Sets the background of mainwindow to alice blue
        self.setStyleSheet("background-color: lightblue")

        # adjusts the border of the main window


        self.setWindowTitle("Braille Print")

        page_layout = QHBoxLayout()

        button_layout = QVBoxLayout()

        # Set margins for buttons
        button_layout.setContentsMargins(0,0,0,0)
        button_layout.setSpacing(20)

        # add widgets to layout

        # Implements a button to import files
        import_button = QPushButton("Import File")
        import_button.setStyleSheet("background-color : white")
        import_button.pressed.connect(self.get_files)
        import_button.setFont(QFont("Arial", 12))
        button_layout.addWidget(import_button)
        
        # Implements a button to print out user input
        button2 = QPushButton("Print")
        button2.setStyleSheet("background-color : white")
        button2.pressed.connect(self.retrieve_text)
        button2.setFont(QFont("Arial", 12))
        
        button_layout.addWidget(button2)

        button3 = QPushButton("Clear")
        button3.pressed.connect(self.clear)
        button3.setStyleSheet("background-color : white")
        button3.setFont(QFont("Arial", 12))
        button_layout.addWidget(button3)

        # adds button layout to page layout
        page_layout.addLayout(button_layout)

        # Creates a field for user input to be processed
        self.user_input = QPlainTextEdit()
        self.user_input.setStyleSheet("background-color : white")
        self.user_input.setPlaceholderText("Enter text to be printed")
        self.user_input.setFont(QFont("Arial", 10))

        page_layout.addWidget(self.user_input)


        # Initialize widgets
        widget = QWidget()
        widget.setLayout(page_layout)
        self.setCentralWidget(widget)

        # Set fixed size of window
        self.setFixedSize(QSize(1600,900))

        widget.resize(640, 480)


    def retrieve_text(self):
        try:
            # retrieve the input from user and prints
            # it to the console
            result = self.user_input.toPlainText()
            print(result)
            print()

            # convert results to braille
            print(convertText(result))
            
        except Exception as e:
            print("Error retrieving text:", e)

    def clear(self):
        self.user_input.clear()

    def get_files(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.ExistingFile)
        dlg.setNameFilter("PDF files (*.pdf);;Text Files (*.txt)")
        
        if dlg.exec_():
            filenames = dlg.selectedFiles()
            filename = filenames[0]

            try:
                if filename.endswith(".pdf"):
                    with open(filename, 'rb') as f:
                        pdf_reader = PyPDF2.PdfReader(f)
                        page = pdf_reader.pages[0]
                        data = page.extract_text()

                elif filename.endswith('.txt'):
                    with open(filename, 'r') as f:
                        data = f.read()

                # Set the contents of the text edit field to the file's contents
                self.user_input.setPlainText(data.replace("None", ""))
                
            except Exception as e:
                print("Error reading file:", e)

# runs the window
app = QApplication(sys.argv)
w = MainWindow()
w.show()
sys.exit(app.exec())
