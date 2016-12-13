#!/usr/bin/python3
# -*- coding: utf-8 -*-

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



class MakeRoomWidget(QWidget):

    width = 20
    height = 20
    room = []

    def __init__(self, parent=None):
        super().__init__(parent)

        self.room = [['.' for x in range(self.width)] for y in range(self.height)]

        self.file_name = QLabel('Room file name:')
        self.file_name_edit = QLineEdit()

        self.room_text = QLabel('Room preview')
        self.new_room_size = QPushButton('New room size')
        self.new_room_size.clicked.connect(self.getNewSize)
        self.new_room_size.setStatusTip('Start new room')
        #TODO: tu ide glavni dio gdje crtamo trenutno stanje
        self.room_all = Room(self)

        self.save_button = QPushButton('Save')
        self.save_button.setShortcut('Ctrl+S')
        self.save_button.setStatusTip('Save this room')
        self.save_button.clicked.connect(self.saveRoom)


        self.grid = QGridLayout()
        self.grid.setSpacing(10)

        self.grid.addWidget(self.file_name, 1, 0)
        self.grid.addWidget(self.file_name_edit, 1, 1)

        self.grid.addWidget(self.room_text, 2, 0)
        self.grid.addWidget(self.new_room_size, 2, 2)

        self.grid.addWidget(self.room_all, 3, 0, 9, 2)

        self.grid.addWidget(self.save_button, 12, 0)

        self.setLayout(self.grid)

    def getNewSize(self):

        ok = False
        while not ok:
            self.height,ok = QInputDialog.getInt(self,"HEIGHT","Enter room height", value=20, min=3, max=500)
        ok = False
        while not ok:
            self.width,ok = QInputDialog.getInt(self,"WIDTH","Enter room width", value=20, min=3, max=500)

        self.room = [['.' for x in range(self.width)] for y in range(self.height)]
        self.room[0] = self.room[-1] = ['#' for x in range(self.width)]
        for row in self.room:
            row[0] = row[-1] = '#'
        #self.room_all.setText(str(self.room))
        self.room_all.new(self.room)


    def saveRoom(self):

        fname = QFileDialog.getSaveFileName(self, 'Save room', '', '.room')

        if fname[0]:
            with open(fname[0]+'.room', 'w') as f:
                for row in self.room_all.room:
                    for cell in row:
                        f.write(cell)
                    f.write('\n')

            self.setVisible(False)



class StartCleaningWidget(QWidget):

    start_postion = False

    def __init__(self, parent=None, input_room=None):
        super().__init__(parent)

        self.start_postion = False
        self.input_room = input_room

        layout = QVBoxLayout()

        self.button = QPushButton('Start cleaning')
        self.button.setShortcut('Ctrl+R')
        self.button.setStatusTip('Start cleaninig room')
        self.button.clicked.connect(self.startCleaning)
        layout.addWidget(self.button)


        self.room = Room(self, input_room)
        layout.addWidget(self.room)

        self.setLayout(layout)

    def startCleaning(self):
        if(self.start_postion is False):
            self.infoMessage()
        else:
            print("Poljećemo")
            #TODO: tu sad ide glavni dio

    def infoMessage(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)

        msg.setText("Starting position not selected")
        #msg.setInformativeText("This is additional information")
        msg.setWindowTitle("Select starting position")
        msg.setDetailedText("Before cleaning starts, you need to select " +
                            "pozition on which will robot start cleaning.\n" +
                            "You can select position by clicking on room map on free cell.")
        msg.setStandardButtons(QMessageBox.Ok)

        #retval = msg.exec_()
        #print ("value of pressed message box button:", retval)


class Main(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        #self.setStyleSheet('QMainWindow{background-color: black;border: 1px solid black;}')

        self.appScreenSetup()
        self.addFunctionalities()


    def appScreenSetup(self):

        self.central_widgets = QStackedWidget()
        self.setCentralWidget(self.central_widgets)

        self.setWindowIcon(QIcon('cleaning_robot.jpg'))
        self.statusBar()

        #self.showMaximized()
        self.resize(800,600)
        self.centerScreen()

        self.setWindowTitle('Cleaning robot')
        self.show()


    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QMessageBox.Yes |
            QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def centerScreen(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def showDialog(self):

        fname = QFileDialog.getOpenFileName(self, 'Open room', '', '*.room')

        if fname[0]:
            with open(fname[0], 'r') as f:
                data = f.read().splitlines()

            self.startCleaning(data)

    def showRoomMaking(self):
        print("showRoomMaking")
        make_room_widget = MakeRoomWidget(self)
        self.central_widgets.addWidget(make_room_widget)
        self.central_widgets.setCurrentWidget(make_room_widget)

    def startCleaning(self, room = []):
        print("startCleaning")
        start_cleaning_widget = StartCleaningWidget(self, room)
        self.central_widgets.addWidget(start_cleaning_widget)
        self.central_widgets.setCurrentWidget(start_cleaning_widget)
        #print(room)


    def addFunctionalities(self):


        openRoomAction = QAction(QIcon('open_room.ico'), 'Open room', self)
        openRoomAction.setShortcut('Ctrl+O')
        openRoomAction.setStatusTip('Open new file')
        openRoomAction.triggered.connect(self.showDialog)

        exitAction = QAction(QIcon('exit.ico'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)

        makeNewRoomAction = QAction(QIcon('make_new_room.ico'), 'New room', self)
        makeNewRoomAction.setShortcut('Ctrl+N')
        makeNewRoomAction.setStatusTip('Make new room')
        makeNewRoomAction.triggered.connect(self.showRoomMaking)

        pomagaj = QAction(QIcon('help.ico'), 'Help me!!!', self)
        pomagaj.setShortcut('Ctrl+H')
        pomagaj.setStatusTip('Nema ti pomoći')
        #pomagaj.triggered.connect(self.showRoomMaking)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openRoomAction)
        fileMenu.addAction(exitAction)
        fileMenu.addAction(makeNewRoomAction)
        helpMenu = menubar.addMenu('&Help')
        helpMenu.addAction(pomagaj)

        toolbar = self.addToolBar('Tools')

        #self.addToolBar(QtCore.Qt.LeftToolBarArea,toolbar)
        #toolbar.setMovable(False)
        toolbar.addAction(openRoomAction)
        toolbar.addAction(exitAction)
        toolbar.addAction(makeNewRoomAction)
        toolbar.setIconSize(QtCore.QSize(self.height()/20, self.height()/20))
        toolbar.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon|QtCore.Qt.AlignLeading) #<= Toolbuttonstyle

if __name__ == '__main__':

    print ("Prvooo")
    app = QApplication(sys.argv)
    print ("Drugo")
    ex = Main()
    print ("Trece")
    sys.exit(app.exec_())
    print ("Cetvrto")
