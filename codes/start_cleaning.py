from PyQt5.QtWidgets import QWidget, QVBoxLayout, QMessageBox, QPushButton
from room import Room
from run_robot import RunRobotWidget

# TODO: Maybe transfer all functionalities from this class into
# RunRobotWidget and remove this class.


class StartCleaningWidget(QWidget):
    """
    Widget for selecting robots start position and after start postion
    has been set, enable running robot.
    """

    def __init__(self, parent=None, room_widget=None):
        """
        Initializing room_widget and button for start cleaning, and
        enabling clicking onto room map to select starting position.

        Parameters
        ----------
        parent : QWidget
            Widget in which we will draw buttons and room.
        room_widget : Room
            Widget that has all information about room and robot inside.

        """

        super().__init__(parent)

        self.parent = parent
        self.room_widget = room_widget

        layout = QVBoxLayout()

        self.button = QPushButton('Start cleaning')
        self.button.setShortcut('Ctrl+R')
        self.button.setStatusTip('Start cleaninig room')
        self.button.clicked.connect(self.startCleaning)
        layout.addWidget(self.button)

        # Second parameter is 1 so user can select starting postion.
        self.room = Room(self, 1, room_widget)
        layout.addWidget(self.room)

        self.setLayout(layout)

    def startCleaning(self):
        """
        Execute after button was clicked.
        If starting postion has been selected start run_robot widget for
        cleaninig room.
        """

        # Checking if start postion has been selected.
        if(self.room.start is False):
            self.infoMessage()
        else:
            # Changing room mode to 0 so no click onto room map will be
            # processed.
            self.room.mode = 0
            run_robot_widget = RunRobotWidget(self.parent, self.room)
            self.parent.central_widgets.addWidget(run_robot_widget)
            self.parent.central_widgets.setCurrentWidget(run_robot_widget)

    def infoMessage(self):
        """
        Pop up message that will appear if user click on start cleaning
        button without setting start position for robot.
        """

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)

        msg.setText("Starting position not selected")
        msg.setWindowTitle("Select starting position")
        msg.setDetailedText("Before cleaning starts, you need to select " +
                            "pozition on which will robot start cleaning.\n" +
                            "You can select position by clicking on room map on free cell.")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
