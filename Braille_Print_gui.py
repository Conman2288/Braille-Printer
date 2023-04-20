import sys
import os.path

# Import library to allow communication
# with Arduino
import serial
import time

# Imports a py library to process pdf files
import PyPDF2

# Pyqt5 gui library
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# import braille library
from pybraille import convertText

# Variable to set DEBUG mode
DEBUG = True

#########################################################################################
class Embosser:

    def __init__(self):
        self.state_dictionary = {'A': '10', 'B':'40', 'C':'11', 'D':'14', 'E':'12', 'F':'41',
                                'G':'44', 'H':'42', 'I':'21', 'J':'24', 'K':'60', 'L':'70',
                                'M':'61', 'N':'64', 'O':'62', 'P':'71', 'Q':'74', 'R':'72',
                                'S':'51', 'T':'54', 'U':'63', 'V':'73', 'W':'27', 'X':'66',
                                'Y':'67', 'Z':'65', ',':'20', ';':'50', ':':'22', '.':'25',
                                 '?':'53', '!':'52', '\'':'30', '-':'33', ' ':'00'}
        
    def state0(self):
        print("state 0")
        ser.write(bytes(str(0), "ascii"))
        # wait for a short time to allow the servo motor to move
        time.sleep(2.5)
    
    def state1(self):
        print("state 1")
        ser.write(bytes(str(25.7), 'ascii'))

        # wait for a short time to allow the servo motor to move
        time.sleep(2.5)

    def state2(self):
        print("state 2")
        ser.write(bytes(str(51.43), 'ascii'))

        # wait for a short time to allow the servo motor to move
        time.sleep(2.5)

    def state3(self):
        print("state 3")
        ser.write(bytes(str(77.13), 'ascii'))

        # wait for a short time to allow the servo motor to move
        time.sleep(2.5)

    def state4(self):
        print("state 4")
        ser.write(bytes(str(102.83), 'ascii'))

        # wait for a short time to allow the servo motor to move
        time.sleep(2.5)

    def state5(self):
        print("state 5")
        ser.write(bytes(str(128.53), 'ascii'))

        # wait for a short time to allow the servo motor to move
        time.sleep(2.5)

    def state6(self):
        print("state 6")
        ser.write(bytes(str(154.23), 'ascii'))

        # wait for a short time to allow the servo motor to move
        time.sleep(2.5)

    def state7(self):
        print("state 7")
        ser.write(bytes(str(180), 'ascii'))

        # wait for a short time to allow the servo motor to move
        time.sleep(2.5)

    def process_data(self, data):
        data = data.upper()
        key_list = list(self.state_dictionary.keys())
        print("there should be {} states for this print.".format(2*len(data)))
        for s in data:
            if (DEBUG):
                print("Printing {}".format(s))
            if s in key_list:
                if (self.state_dictionary[s].startswith('0')):
                    self.state0()
                elif (self.state_dictionary[s].startswith('1')):
                    self.state1()
                elif (self.state_dictionary[s].startswith('2')):
                    self.state2()
                elif (self.state_dictionary[s].startswith('3')):
                    self.state3()
                elif (self.state_dictionary[s].startswith('4')):
                    self.state4()
                elif (self.state_dictionary[s].startswith('5')):
                    self.state5()
                elif (self.state_dictionary[s].startswith('6')):
                    self.state6()
                elif (self.state_dictionary[s].startswith('7')):
                    self.state7()
                else:
                    pass

                if (self.state_dictionary[s].endswith('0')):
                    self.state0()
                elif (self.state_dictionary[s].endswith('1')):
                    self.state1()
                elif (self.state_dictionary[s].endswith('2')):
                    self.state2()
                elif (self.state_dictionary[s].endswith('3')):
                    self.state3()
                elif (self.state_dictionary[s].endswith('4')):
                    self.state4()
                elif (self.state_dictionary[s].endswith('5')):
                    self.state5()
                elif (self.state_dictionary[s].endswith('6')):
                    self.state6()
                elif (self.state_dictionary[s].endswith('7')):
                    self.state7()
                else:
                    pass
            else:
                self.state0()
                print("no state")
                time.sleep(2.5)
                print("no state")
                self.state0()
                print("no state")
                time.sleep(2.5)

#########################################################################################
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # sets up the timer widget
        self.timer = QElapsedTimer()

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
        button2.pressed.connect(self.print_dialog)
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

        # Set fixed size of window and adjust sizing of widgets
        self.setFixedSize(QSize(1600,900))
        widget.resize(640, 480)


    def print_dialog(self):
        try:
            # retrieve the input from user and prints
            # it to the console
            result = self.user_input.toPlainText()
            print(result)
            print()

            # convert results to braille
            print(convertText(result))

            # processes the user input and then a dialog
            # box pops up with the total print time
            self.timer.start()
            embosser = Embosser()
            embosser.process_data(result)
            print_time = self.timer.elapsed() / 1000
            print(f"Total print time: {print_time} seconds")
            
            # show print dialog with print time
            dialog = QDialog(self)
            dialog.setWindowTitle("Print")
            layout = QVBoxLayout()
            message = QLabel(f"Total print time: {print_time:.2f} seconds")
            message.setFont(QFont("Arial", 12))
            layout.addWidget(message)
            dialog.setLayout(layout)
            dialog.exec_()
            
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

#########################################################################################

# Define the serial port and baud rate
# of the Arduino
port = 'COM3'
baudrate = 9600

# define the Analog servo pin
servo_pin = 3

# Initial angle of embosser
angle = 0

# Open the serial port
ser = serial.Serial('COM3', 9600)
ser.close() # Closes any currently running programs

# Create a new serial object
ser = serial.Serial(port, baudrate)

# Send the inital angle to the servo motor
ser.write(bytes(str(angle), 'ascii'))
                
# create an embosser object
embosser = Embosser()

# runs the window
app = QApplication(sys.argv)
w = MainWindow()
w.show()
sys.exit(app.exec())
