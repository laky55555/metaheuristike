#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QMainWindow, QAction, QFileDialog, QApplication, QDesktopWidget, QMessageBox, QStackedWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, Qt
from room import Room
from robot import Robot
from start_cleaning import StartCleaningWidget
from run_robot import RunRobotWidget
from make_room import MakeRoomWidget


class Main(QMainWindow):
    """
    Class for making main window and connecting all functionalities of program.
    """

    def __init__(self):
        super().__init__()

        self.appScreenSetup()
        self.addFunctionalities()

    def appScreenSetup(self):
        """ Initializing window, and icon. """

        self.central_widgets = QStackedWidget()
        self.setCentralWidget(self.central_widgets)

        self.setWindowIcon(QIcon('cleaning_robot.jpg'))
        self.statusBar()

        # self.showMaximized()
        self.resize(800, 600)
        self.centerScreen()

        self.setWindowTitle('Cleaning robot')
        self.show()

    def centerScreen(self):
        """ Moving window in center of screen. """

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeEvent(self, event):
        """ Overriding close event so before closing there is pop up question. """

        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def showDialog(self):
        """ Pop up for open existing room. Necessary for starting robot. """

        fname = QFileDialog.getOpenFileName(self, 'Open room', '', '*.room')

        if fname[0]:
            with open(fname[0], 'r') as f:
                data = [list(i) for i in f.read().splitlines()]

            # TODO: Do checkout if data is in appropriate format.
            self.startCleaning(data)

    def showRoomMaking(self):
        """ Starting widget for making new room. """

        make_room_widget = MakeRoomWidget(self)
        self.central_widgets.addWidget(make_room_widget)
        self.central_widgets.setCurrentWidget(make_room_widget)

    def startCleaning(self, room=[]):
        """ Starting widget for chosing start postion for start cleaning. """

        start_cleaning_widget = StartCleaningWidget(self, room)
        self.central_widgets.addWidget(start_cleaning_widget)
        self.central_widgets.setCurrentWidget(start_cleaning_widget)

    def addFunctionalities(self):
        """ Adding toolbar and file menu with appropriate functionalities. """

        openRoomAction = QAction(QIcon('open_room.ico'), 'Open room', self)
        openRoomAction.setShortcut('Ctrl+O')
        openRoomAction.setStatusTip('Open new file')
        openRoomAction.triggered.connect(self.showDialog)

        exitAction = QAction(QIcon('exit.ico'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)

        makeNewRoomAction = QAction(
            QIcon('make_new_room.ico'), 'New room', self)
        makeNewRoomAction.setShortcut('Ctrl+N')
        makeNewRoomAction.setStatusTip('Make new room')
        makeNewRoomAction.triggered.connect(self.showRoomMaking)

        pomagaj = QAction(QIcon('help.ico'), 'Help me!!!', self)
        pomagaj.setShortcut('Ctrl+H')
        pomagaj.setStatusTip('Nema ti pomoći')
        # TODO: Make help menu or pop up window.
        # pomagaj.triggered.connect(self.showRoomMaking)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openRoomAction)
        fileMenu.addAction(exitAction)
        fileMenu.addAction(makeNewRoomAction)
        helpMenu = menubar.addMenu('&Help')
        helpMenu.addAction(pomagaj)

        toolbar = self.addToolBar('Tools')
        # TODO: Decide of looks of toolbar, fixed or not.
        # self.addToolBar(QtCore.Qt.LeftToolBarArea,toolbar)
        # toolbar.setMovable(False)
        toolbar.addAction(openRoomAction)
        toolbar.addAction(exitAction)
        toolbar.addAction(makeNewRoomAction)
        toolbar.setIconSize(QSize(self.height() / 20, self.height() / 20))
        toolbar.setToolButtonStyle(
            Qt.ToolButtonTextBesideIcon | Qt.AlignLeading)  # <= Toolbuttonstyle

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Main()
    sys.exit(app.exec_())
