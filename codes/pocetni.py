#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import (QMainWindow, QTextEdit, QAction,
    QFileDialog, QApplication, QDesktopWidget, QMessageBox, QGridLayout)
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore



class Main(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        #self.setStyleSheet('QMainWindow{background-color: black;border: 1px solid black;}')

        self.appScreenSetup()
        self.addFunctionalities()


    def appScreenSetup(self):
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

        fname = QFileDialog.getOpenFileName(self, 'Open file', '', '*.room')

        #TODO:  otvaranje file-a bolje mouda napraviti, razmisliti
        #       da li otvaram file pa ga saljemo ili saljemo samo
        #       ime filea. Po meni saljemo samo podatke!!!
        if fname[0]:
            with open(fname[0], 'r') as f:
                data = f.read()
                #self.textEdit.setText(data)
                self.showRoom(data)

    def showFirstScreen(self):

        print("showFirstScreen")


    def showRoomMaking(self):

        print("showRoomMaking")

    def showRoom(self, room):
        print("showRoom funkcija")
        print(room)


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

    print ("Prvo")
    app = QApplication(sys.argv)
    print ("Drugo")
    ex = Main()
    print ("Trece")
    sys.exit(app.exec_())
    print ("Cetvrto")
