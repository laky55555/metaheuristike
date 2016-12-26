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
from room import Room
from robot import Robot




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
        self.room_all = Room(self, 2)

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
        #TODO: to se brise
        robot = []
        #robot = [(1,1),(1,2),(1,3),(2,3),(3,2)]
        self.room_all.update_room(self.room, robot)


    def saveRoom(self):

        fname = QFileDialog.getSaveFileName(self, 'Save room', '', '.room')

        if fname[0]:
            with open(fname[0]+'.room', 'w') as f:
                for row in self.room_all.room:
                    for cell in row:
                        f.write(cell)
                    f.write('\n')

            self.setVisible(False)

class RunRobotWidget(QWidget):

    def __init__(self, parent=None, room=None):
        super().__init__(parent)

        self.parent = parent
        self.room = room
        #self.robot = Robot(self.room.room, self.room.robot)
        self.robot = Robot(self.room)
        layout = QVBoxLayout()

        self.button_move_one = QPushButton('Next move')
        self.button_move_one.setShortcut('Ctrl+D')
        self.button_move_one.setStatusTip('Make next move')
        self.button_move_one.clicked.connect(self.robot.move_one)
        layout.addWidget(self.button_move_one)

        self.button_move_all = QPushButton('Do all moves')
        self.button_move_all.setShortcut('Ctrl+A')
        self.button_move_all.setStatusTip('Make moves until end')
        self.button_move_all.clicked.connect(self.robot.move_all)
        layout.addWidget(self.button_move_all)

        self.button_back_one = QPushButton('Go back')
        self.button_back_one.setShortcut('Ctrl+P')
        self.button_back_one.setStatusTip('Undo move')
        self.button_back_one.clicked.connect(self.robot.move_back)
        layout.addWidget(self.button_back_one)

        layout.addWidget(self.robot.room_widget)

        self.setLayout(layout)

class StartCleaningWidget(QWidget):

    def __init__(self, parent=None, input_room_data=None):
        super().__init__(parent)

        self.parent = parent
        self.input_room_data = input_room_data

        layout = QVBoxLayout()

        self.button = QPushButton('Start cleaning')
        self.button.setShortcut('Ctrl+R')
        self.button.setStatusTip('Start cleaninig room')
        self.button.clicked.connect(self.startCleaning)
        layout.addWidget(self.button)


        self.room = Room(self, 1, input_room_data)
        layout.addWidget(self.room)

        self.setLayout(layout)

    def startCleaning(self):
        #print(self.room.start)
        if(self.room.start is False):
            self.infoMessage()
        else:
            print("Poljećemo")
            #TODO: tu sad ide glavni dio
            self.room.mode = 0
            run_robot_widget = RunRobotWidget(self.parent, self.room)
            self.parent.central_widgets.addWidget(run_robot_widget)
            self.parent.central_widgets.setCurrentWidget(run_robot_widget)


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
        msg.exec_()

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
                #data = f.read().splitlines()
                #data = [list(i) for i in data]
                data = [list(i) for i in f.read().splitlines()]

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
