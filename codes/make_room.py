from PyQt5.QtWidgets import (QFileDialog, QGridLayout, QWidget,
                             QPushButton, QLabel, QLineEdit, QInputDialog)
from room import Room


class MakeRoomWidget(QWidget):
    """
    Widget for displaying all necessary items for creating new room.
    Widget also display additional widget Room for displaying and modifying room.
    """

    def __init__(self, parent=None):
        """
        Initialize widget layout and buttons.
        Initialize Room widget contained inside widget.

        Parameters
        ----------
        parent : QWidget
            Widget in which we will draw room.

        """
        super().__init__(parent)

        # Making default room with dimension 20x20.
        self.width = self.height = 20
        self.room = self.make_room_cells(self.width, self.height)

        self.file_name = QLabel('Room file name:')
        self.file_name_edit = QLineEdit("test", self)

        self.room_text = QLabel('Room preview')
        self.new_room_size = QPushButton('New room size')
        self.new_room_size.clicked.connect(self.getNewSize)
        self.new_room_size.setStatusTip('Start new room')

        self.room_all = Room(self, 2, self.room)

        self.save_button = QPushButton('Save')
        self.save_button.setShortcut('Ctrl+S')
        self.save_button.setStatusTip('Save this room')
        self.save_button.clicked.connect(self.saveRoom)

        # Making grid layout for easier positioning buttons and Room widget.
        self.grid = QGridLayout()
        self.grid.setSpacing(10)

        self.grid.addWidget(self.file_name, 1, 0)
        self.grid.addWidget(self.file_name_edit, 1, 1)

        self.grid.addWidget(self.room_text, 2, 0)
        self.grid.addWidget(self.new_room_size, 2, 2)

        self.grid.addWidget(self.room_all, 3, 0, 9, 2)

        self.grid.addWidget(self.save_button, 12, 0)

        self.setLayout(self.grid)

    def make_room_cells(self, width, height):
        """
        Auxyiliary method for creating empty room with given size.

        Parameters
        ----------
        width : int
            Width of new empty room, must be greater than 2.
        height : int
            Height of new empty room, must be greater than 2.

        Returns
        -------
        list
            Every element of list is list symbolising one row of room.
            Every inner list elements are # or . depending of position,
            where # are on borders.

        """
        if width < 3:
            width = 3
        if height < 3:
            height = 3
        room = [['.' for x in range(width)] for y in range(height)]
        room[0] = room[-1] = ['#' for x in range(width)]
        for row in room:
            row[0] = row[-1] = '#'

        return room

    def getNewSize(self):
        """
        Method called when user click on button New room size.
        After it has been called makes pop up menu for chosing new size of room.
        """

        ok = False
        while not ok:
            self.height, ok = QInputDialog.getInt(
                self, "HEIGHT", "Enter room height", value=20, min=3, max=500)
        ok = False
        while not ok:
            self.width, ok = QInputDialog.getInt(
                self, "WIDTH", "Enter room width", value=20, min=3, max=500)

        self.room = self.make_room_cells(self.width, self.height)
        self.room_all.update_room(self.room)

    def saveRoom(self):
        """
        Method for saving newly created room.
        If user worte something in file name, given name will be displayed
        for modifying.
        """

        fname = QFileDialog.getSaveFileName(
            self, 'Save room', self.file_name_edit.text(), '*.room')

        if fname[0]:
            with open(fname[0] + '.room', 'w') as f:
                for row in self.room_all.room:
                    for cell in row:
                        f.write(cell)
                    f.write('\n')

            self.setVisible(False)
