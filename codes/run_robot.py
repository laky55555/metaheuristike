from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton
from robot import Robot


class RunRobotWidget(QWidget):
    """
    Widget for displaying robot moving through room.
    Include Room widget for drawing room and movement.
    """

    def __init__(self, parent=None, room_widget=None):
        """
        Initializing room_widget and buttons for movement.

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
        self.robot = Robot(self.room_widget)
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
        self.button_back_one.setShortcut('Ctrl+B')
        self.button_back_one.setStatusTip('Undo move')
        self.button_back_one.clicked.connect(self.robot.move_back)
        layout.addWidget(self.button_back_one)

        layout.addWidget(self.robot.room_widget)

        self.setLayout(layout)
