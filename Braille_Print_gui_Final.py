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
from PyQt5.QtCore import QThread, pyqtSignal


# import braille library
from pybraille import convertText

# voice assistant module
import pyttsx3

# Variable to set DEBUG mode
DEBUG = True

#########################################################################################
# The Embosser class holds the states associated with each letter in braille
# and the behaviors of this class are the physical change in state of the servo
# based on the angle sent to the receiving Arduino
class Embosser:

    def __init__(self):
        self.state_dictionary = {'A': '10', 'B':'40', 'C':'11', 'D':'14', 'E':'12', 'F':'41',
                                'G':'44', 'H':'42', 'I':'21', 'J':'24', 'K':'60', 'L':'70',
                                'M':'61', 'N':'64', 'O':'62', 'P':'71', 'Q':'74', 'R':'72',
                                'S':'51', 'T':'54', 'U':'63', 'V':'73', 'W':'27', 'X':'66',
                                'Y':'67', 'Z':'65', ',':'20', ';':'50', ':':'22', '.':'25',
                                 '?':'53', '!':'52', '\'':'30', '-':'33', ' ':'00', '1':'10',
                                 '2':'40', '3':'11', '4':'14', '5':'12', '6':'41', '7':'44',
                                 '8':'42', '9':'21', '0':'24'}

        self.state_time = 4.5
        self.state_count = 0
        
    def state0(self):
        # this state passes since no dots are printed
        print("state 0")
        ser.write(bytes(str(0), "ascii"))
        # wait for a short time to allow the servo motor to move
        time.sleep(self.state_time)
    
    def state1(self):
        print("state 1")
        ser.write(bytes(str(144.57), 'ascii'))

        # wait for a short time to allow the servo motor to move
        time.sleep(self.state_time)

    def state2(self):
        print("state 2")
        ser.write(bytes(str(170.28), 'ascii'))

        # wait for a short time to allow the servo motor to move
        time.sleep(self.state_time)

    def state3(self):
        print("state 3")
        ser.write(bytes(str(90.1423), 'ascii'))

        # wait for a short time to allow the servo motor to move
        time.sleep(self.state_time) 

    def state4(self):
        print("state 4")
        ser.write(bytes(str(118.6), 'ascii'))

        # wait for a short time to allow the servo motor to move
        time.sleep(self.state_time)

    def state5(self):
        print("state 5")
        ser.write(bytes(str(59.428), 'ascii'))

        # wait for a short time to allow the servo motor to move
        time.sleep(self.state_time)

    def state6(self):
        print("state 6")
        ser.write(bytes(str(8), 'ascii'))

        # wait for a short time to allow the servo motor to move
        time.sleep(self.state_time)

    def state7(self):
        print("state 7")
        ser.write(bytes(str(33.7143), 'ascii'))

        # wait for a short time to allow the servo motor to move
        time.sleep(self.state_time)

    # This function takes in the data and then processes each string and its two associated states
    # based on the key-value pair in the state dictionary. Every 5 states processed, the roller
    # is then activated to move the paper up a line.
    def process_data(self, data):
        # Placeholder variable for the braille exception of numbers
        consecutive_numbers = False
        data = data.upper()
        key_list = list(self.state_dictionary.keys())
        print("There should be {} states for this print.".format(2*len(data)))
        for s in data:
            if (DEBUG):
                print("Printing [{}, {}]".format(s, convertText(s.lower())))

            # Every 20 characters the paper moves up a line via the roller
            if (self.state_count == 20 and self.state_count != 0):
                print("roller moving")
                time.sleep(2.5)
                self.state_count = 0
                print("moving embosser to all the way left")
                time.sleep(48);

            # If the input data is a number, then a special character
            # is inserted in the braille to distinguish the numbers
            # from other letter configurations.
            if (s.isnumeric() and consecutive_numbers == False):
                print("Printing Number Signifier")
                self.state_count += 2
                self.state3()
                self.state7()
                consecutive_numbers = True

            if (not s.isnumeric()):
                consecutive_numbers = False
                
            self.state_count += 1
            print("Count = {}".format(self.state_count))
            
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

                if (self.state_count == 20 and self.state_count != 0):
                    print("roller moving")
                    time.sleep(2.5)
                    self.state_count = 0
                    print("moving embosser to all the way left")
                    time.sleep(48);
                
                self.state_count += 1
                print("Count = {}".format(self.state_count))

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
                print("no state")
                time.sleep(2.5)
                print("no state")

#########################################################################################
# This class is neccesary so that the GUI can still be processed while the
# program is executing the data_process function.
class PrintThread(QThread):
    finished = pyqtSignal()

    def __init__(self, result):
        super().__init__()
        self.result = result

    def run(self):
        embosser = Embosser()

        embosser.process_data(self.result)
        
        self.finished.emit()
        
#########################################################################################
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        #Initializes the voice assistant instance
        self.engine = pyttsx3.init()

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
        import_button.installEventFilter(self)
        button_layout.addWidget(import_button)
        
        # Implements a button to print out user input
        self.button2 = QPushButton("Print")
        self.button2.setStyleSheet("background-color : white")
        self.button2.pressed.connect(self.print_dialog)
        self.button2.installEventFilter(self)
        self.button2.setFont(QFont("Arial", 12))
        button_layout.addWidget(self.button2)

        # Adds a button to clear text in the edit box
        button3 = QPushButton("Clear")
        button3.pressed.connect(self.clear)
        button3.setStyleSheet("background-color : white")
        button3.setFont(QFont("Arial", 12))
        button3.installEventFilter(self)
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

    # Changes the background of buttons when the mouse hovers over them
    def eventFilter(self, obj, event):
        if event.type() == QEvent.HoverEnter:
            obj.setStyleSheet("background-color : gray")
        elif event.type() == QEvent.HoverLeave:
            obj.setStyleSheet("background-color : white")
        return super().eventFilter(obj, event)

    def print_dialog(self):
        try:
            
            # disable the print button while printing is ongoing
            self.button2.setEnabled(False)
            
            # retrieve the input from user and prints
            # it to the console
            result = self.user_input.toPlainText()
            print(result)
            print()

            # convert results to braille
            print(convertText(result))

            # voice assistant reads out what is being printed
            # except when the details are too long
            if (len(str(result)) > 50):
                self.engine.say("Printing Document")
                self.engine.runAndWait()
            else:
                self.engine.say("Printing: " + str(result))
                self.engine.runAndWait()

            # create a PrintThread and start it
            # sets up the timer widget
            self.timer = QElapsedTimer()
            self.timer.start()
            self.thread = PrintThread(result)
            self.thread.finished.connect(self.print_finished)
            self.thread.start()
            
        except Exception as e:
            print("Error retrieving text:", e)

    def print_finished(self):

        # enable the print button again
        self.button2.setEnabled(True)
        
        # display a dialog box with the total print time
        # and the user voice assistant notifies the user that
        # the print is done.
        elapsed_time = self.timer.elapsed() / 1000
        self.engine.say("Print complete")
        self.engine.runAndWait()
        message = "Total print time was\n {} seconds".format(elapsed_time)
        QMessageBox.information(self, "Print", message)

    # Clears the user input currently in the edit box
    def clear(self):
        self.engine.say("Clear")
        self.engine.runAndWait()
        self.user_input.clear()

    # Opens a file dialog box so that the user can
    # upload basic text and pdf files
    def get_files(self):
        self.engine.say("Getting Files")
        self.engine.runAndWait()
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.ExistingFile)
        dlg.setNameFilter("PDF files (*.pdf);;Text Files (*.txt)")
        
        if dlg.exec_():
            filenames = dlg.selectedFiles()
            filename = filenames[0]

            # Adds masking to the file input to ensure
            # that the user is not uploading files without
            # the .pdf or .txt extensions.

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
sys.exit()
