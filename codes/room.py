import sys
from PyQt5.QtWidgets import (QMainWindow, QTextEdit, QAction,
    QFileDialog, QApplication, QDesktopWidget, QMessageBox, QGridLayout,
     QHBoxLayout, QVBoxLayout, QStackedWidget, QWidget, QPushButton, QLabel,
     QLineEdit, QPushButton, QInputDialog, QDialog, QDateTimeEdit,
     QSpinBox, QDialogButtonBox, QToolTip)
from PyQt5.QtGui import QIcon, QPainter, QColor, QFont, QPalette
from PyQt5 import QtCore
from PyQt5.QtCore import QDateTime



def signs(arg):
    switch = {'.': 0, '#': 1,
              'x': 2, 'o': 3, 'R':4}
    return switch.get(arg, 'error')


class Room(QWidget):
    room = []
    robot = []
    ratio = -1
    room_width = -1
    room_height = -1
    block_width = -1
    block_height = -1

    def __init__(self, parent=None, data=[], robot=None):
        super().__init__(parent)

        #self.grid = QGridLayout()
        #self.grid.setSpacing(10)
        #self.setGeometry(300, 300, 350, 100)
        #self.setWindowTitle('Colours')
        self.show()

        if(len(data) > 0):
            self.room_height =len(data)
            self.room_width = len(data[0])
            self.robot = robot
            self.room = data
            #self.printMap()



    def new(self, data=[], robot=None):

        if(len(data) > 0):
            self.room_height =len(data)
            self.room_width = len(data[0])
            self.room = data
            self.robot = robot

            """print("self.heigth = "  + str(self.room_height) +
            "  self.size =  " + str(self.size()) +
            "  self.size().height() = " + str(self.size().height()) +
            "  self.size().width() = " + str(self.size().width()))"""

            self.robot = robot
            self.update()
            #self.printMap()
            #self.paintEvent()

    def paintEvent(self, e):
        if(self.room_height > 0 and self.room_width > 0):
            self.printMap()

    def printMap(self):

        painter = QPainter()
        painter.begin(self)

        self.block_height = self.size().height() // self.room_height
        self.block_width = self.size().width() // self.room_width
        self.minimum = min(self.block_width, self.block_height)
        #print ("Block height = " + str(self.block_height) + " Block width = " + str(self.block_width))
        #print ("Room height = " + str(self.room_height) + " Room width = " + str(self.room_width))
        for i in range(self.room_height):
            for j in range(self.room_width):
                #print("crtanje")
                #print("i=" + str(i) + " j=" + str(j) + " room[i][j]=" + str(self.room[i][j]) + " signs(room[][])=" + str(signs(self.room[i][j])) )
                #self.drawSquare(painter, self.block_width*j, self.block_height*i, signs(self.room[i][j]))
                self.drawSquare(painter, self.minimum*j, self.minimum*i, signs(self.room[i][j]))

        painter.end()

    def drawSquare(self, painter, x, y, shape):

        colorTable = [0x000000, 0xCC6666, 0x66CC66, 0x6666CC,
                      0xCCCC66, 0xCC66CC, 0x66CCCC, 0xDAAA00]

        painter.setBrush(QColor(colorTable[shape]))

        #painter.drawRect(x, y, self.block_width, self.block_height)
        painter.drawRect(x, y, self.minimum, self.minimum)
