import sys

from PIL import Image, ImageQt
from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QMainWindow, QPushButton, QTextEdit, QLabel


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        uic.loadUi('autoFiller.ui', self)
        self.findChild(QPushButton, "startButton").clicked.connect(self.run)


    def run():
        print("Hello World!")


if __name__ == "__main__":
    application = QtWidgets.QApplication(sys.argv)
    currWindow = UI()
    sys.exit(application.exec_())


# # importing the required libraries

# from PyQt5.QtWidgets import *
# from PyQt5.QtGui import QPixmap
# import sys


# class UI(QMainWindow):
#     def __init__(self):
#         super().__init__()

#         self.acceptDrops()
#         # set the title
#         self.setWindowTitle("Image")

#         # setting the geometry of window
#         self.setGeometry(0, 0, 400, 300)

#         # creating label
#         self.label = QLabel(self)

#         # loading image
#         self.pixmap = QPixmap('image.png')

#         # adding image to label
#         self.label.setPixmap(self.pixmap)

#         # Optional, resize label to image size
#         self.label.resize(self.pixmap.width(),
#                           self.pixmap.height())

#         # show all the widgets
#         self.show()
#         # uploading image
#         self.findChild(QPushButton, "startButton").clicked.connect(self.run)

#         def run(self):
#             print("Hello World!")


# App = QApplication(sys.argv)


# window = UI()

# # start the app
# sys.exit(App.exec())
