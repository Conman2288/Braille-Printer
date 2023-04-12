import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Braille Print")

        page_layout = QHBoxLayout()

        button_layout = QVBoxLayout()

        # Set margins for buttons
        button_layout.setContentsMargins(0,0,0,0)
        button_layout.setSpacing(20)

        # add widgets to layout
        import_button = QPushButton("Import File")
        import_button.pressed.connect(self.import_pdf)
        import_button.setFont(QFont("Arial", 12))
        button_layout.addWidget(import_button)
        

        button2 = QPushButton("Button")
        button2.pressed.connect(self.button2)
        button2.setFont(QFont("Arial", 12))
        button_layout.addWidget(button2)

        button3 = QPushButton("Button")
        button3.pressed.connect(self.button3)
        button3.setFont(QFont("Arial", 12))
        button_layout.addWidget(button3)

        # adds button layout to page layout
        page_layout.addLayout(button_layout)

        user_input = QPlainTextEdit()
        user_input.setPlaceholderText("Enter text")


        page_layout.addWidget(user_input)


        # Initialize widgets
        widget = QWidget()
        widget.setLayout(page_layout)
        self.setCentralWidget(widget)

        # Set fixed size of window
        self.setFixedSize(QSize(900,600))

        widget.resize(640, 480)




    def import_pdf(self):
        pass

    def button2(self):
        pass

    def button3(self):
        pass

    def return_pressed(self):
        print("Return pressed!")

    def text_changed(self, s):
        print("Text changed ...")

    def text_edited(self, s):
        print("Text edited ...")
        print(s)

# runs the window
app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()
