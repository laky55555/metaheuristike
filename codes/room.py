from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt
from enum import Enum
from sympy import Line


class Symbol(Enum):

    def __repr__(self):
        return self.value
    UNVISITED = '.'
    WALL = '#'
    OBSTACLE = 'x'
    VISITED = 'o'
    ROBOT = 'R'


# Widget for drawing room.
class Room(QWidget):
    """
    Widget for drawing room.
    Widget draws given room and robot path on it.
    Widget also depending of construction enable clicking on map
    for selecting start position for robot or modify room.
    """

    # Dictionary for decoding chars into hex_color. Using in coloring room.
    switch = {'.': 0x000000, '#': 0xCCCC66,
              'x': 0xCC66CC, 'o': 0x66CC66, 'R': 0xDAAA00}

    # Constructor needs expect parent so we know where we will draw widget.
    def __init__(self, parent=None, mode=0, data=[], robot=[]):
        """
        Initialize and draw map and robot moving postions.

        Parameters
        ----------
        parent : QWidget
            Widget in which we will draw room.
        mode : int
            Number that decide what can user do on map.
            0 for nothing, 1 for chosing robot start postion and 2 for making obstacles.
        data : list of lists
            List consisting of lists. Each inner list represents one row in room.
            Inner lists don't need to be with same length.
        robot : list of tuples
            List consisting of tuples which represents robot movements.

        """
        super().__init__(parent)

        self.mode = mode
        self.room_max_height = len(data)
        self.room_max_width = max(
            [len(row) for row in data]) if self.room_max_height > 0 else 0
        self.robot = robot
        self.room = data
        # Initialize minimum to 0 for easier handling clik events (avoiding
        # exceptins).
        self.minimum = 0
        self.start = self.findStart()

        self.directions = []
        self.number_of_turns = 0

        self.multiple_visits = 0

        # Debuging:
        # print ("Max room width = {0}, max room heigh = {1}".format(self.room_max_width, self.room_max_height))
        # print("Room:")
        # for row in self.room:
        #    print(row)
        # print('Robot movement:\n', self.robot)

    def update_room(self, data=[], robot=[]):
        """
        Reinitialize and draw map and robot moving postions.

        Parameters
        ----------
        data : list of lists
            List consisting of lists. Each inner list represents one row in room.
            Inner lists don't need to be with same length.
        robot : list of tuples
            List consisting of tuples which represents robot movements.

        """
        self.room_max_height = len(data)
        self.room_max_width = max(
            [len(row) for row in data]) if self.room_max_height > 0 else 0
        self.room = data
        self.robot = robot
        # Initialize minimum to 0 for easier handling clik events (avoiding
        # exceptins).
        self.minimum = 0
        self.start = self.findStart()
        # This automatically calls paintEvent()
        self.update()

    # Override default function for drawing widget.
    def paintEvent(self, e):
        """Default function for drawing widget."""
        if(self.room_max_height > 0 and self.room_max_width > 0):

            painter = QPainter()
            painter.begin(self)

            # Finding minimal dimension in pixels so we can draw squares.
            self.block_height = self.size().height() // self.room_max_height
            self.block_width = self.size().width() // self.room_max_width
            self.minimum = min(self.block_width, self.block_height)

            # Drawing all squares.
            for i in range(len(self.room)):
                for j in range(len(self.room[i])):
                    self.drawSquare(painter, self.minimum * j,
                                    self.minimum * i, self.switch[self.room[i][j]])

            # Drawing robot movement.
            pen = QPen(QColor(0xDAAA99), 3, Qt.DashLine)
            painter.setPen(pen)
            self.middle = self.minimum / 2
            for i, j in zip(self.robot[:-1], self.robot[1:]):
                self.drawMovement(painter, self.minimum * i[1], self.minimum * i[
                                  0], self.minimum * j[1], self.minimum * j[0])

            painter.end()

    def drawMovement(self, painter, x1, y1, x2, y2):
        """
        Drawing line on widget.

        Function draws line on widget square from start postion to end postion.

        Parameters
        ----------
        painter : QPainter
            PyQt5.QtGui class for drawing.
        x1 : int
            Coordinate on current widget on which x-coordinate of
            square where robot started.
        y1 : int
            Coordinate on current widget on which y-coordinate of
            square where robot started.
        x2 : int
            Coordinate on current widget on which x-coordinate of
            square where robot ended.
        y2 : int
            Coordinate on current widget on which y-coordinate of
            square where robot ended.
        """
        painter.drawLine(x1 + self.middle, y1 + self.middle,
                         x2 + self.middle, y2 + self.middle)

    def drawSquare(self, painter, x, y, hex_color):
        """
        Drawing square on widget.

        Function draws square on widget with dimension calculated before and
        saved in variable self.minimum starting on given postion with given color.

        Parameters
        ----------
        painter : QPainter
            PyQt5.QtGui class for drawing.
        x : int
            Coordinate on current widget on which x-coordinate of
            square that we will draw starts.
        y : int
            Coordinate on current widget on which y-coordinate of
            square that we will draw starts.
        hex_color : hex_int
            RGB number that determine in which color will we draw square.

        """
        painter.setBrush(QColor(hex_color))

        #painter.drawRect(x, y, self.block_width, self.block_height)
        painter.drawRect(x, y, self.minimum, self.minimum)

    def findStart(self):
        """ Metod for looking if start postion for robot has been selected. """
        for row in self.room:
            for cell in row:
                if cell == Symbol.ROBOT.value:
                    return True

        return False

    def delete_old_robot_position(self):
        """Replace all robot positions on the map with unvisited."""
        for row in range(len(self.room)):
            self.room[row] = [Symbol.UNVISITED.value if x == Symbol.ROBOT.value
                              else x for x in self.room[row]]

    # Override what happen on click.
    def mousePressEvent(self, event):
        """
        On each mouse click check if it was left click, and if it was
        depending on which mode widget is (making new map, chosing start position,...)
        mark new start position or make/remove obstacles.
        """
        if(event.button() == Qt.LeftButton and self.minimum > 0):
            x = event.pos().y() // self.minimum
            y = event.pos().x() // self.minimum
            if (x >= self.room_max_height or y >= len(self.room[x])):
                return

            # If we are in mode 1 and we clicked on empty place on map.
            if(self.mode == 1 and
                    (self.room[x][y] == Symbol.UNVISITED.value or self.room[x][y] == Symbol.VISITED.value)):
                self.delete_old_robot_position()
                self.room[x][y] = Symbol.ROBOT.value
                self.robot = [(x, y)]
                self.start = True

            # If we are in mode 2 and we clicked on empty or place with
            # obstacle.
            elif(self.mode == 2):
                if(self.room[x][y] == Symbol.UNVISITED.value or self.room[x][y] == Symbol.VISITED.value):
                    self.room[x][y] = Symbol.OBSTACLE.value
                elif(self.room[x][y] == Symbol.OBSTACLE.value):
                    self.room[x][y] = Symbol.UNVISITED.value
            self.update()

    def detect_room(self, sight_distance):
        """
        Method that return dictionary where key is tuple of row start position
        of the map and value list with all discovered space. Metod calculated
        all cells that can be seen form robots position with given sight_distance.
        Method return circle around current position of robot.

        Parameters
        ----------
        x : int
            Int that symbolise how far robot can see.

        Returns
        -------
        dictionary
            Key is tuple of row start position in wholee map and
            value list with all discovered space.

        """

        position = self.robot[-1]
        sight_distance_quad = sight_distance * sight_distance

        # Find first and last row in the map for robots position.
        minimal_x = max(position[0] - sight_distance, 0)
        maximal_x = min(position[0] + sight_distance + 1, self.room_max_height)
        minimal_y = max(position[1] - sight_distance, 0)

        number_of_rows = maximal_x - minimal_x
        detected = {}

        # For each row that robot can see find every cell that she can see.
        # TODO: Maybe change something so robot can't see through wall.
        for i in range(minimal_x, maximal_x):
            # Each rom can have different size.
            maximal_y = min(
                position[1] + sight_distance + 1, len(self.room[i]))
            initialized = False
            # For each cell check if it is inside line of sight.
            for j in range(minimal_y, maximal_y):
                if((position[0] - i) * (position[0] - i) + (position[1] - j) * (position[1] - j) <= sight_distance_quad):
                    # If this is first cell in row that has been seen
                    # initialize new key in dictionary.
                    if(initialized == False):
                        y = j
                        initialized = True
                        detected[(i, y)] = []
                    detected[(i, y)].append(self.room[i][j])

        return detected

    def new_change_of_direction(self, debug=False):
        if len(self.robot) < 3:
            self.directions.append(0)
            #return 0
        else:
            # TODO: mozda napraviti provjeru da li su sve tocke razlicite
            l1 = Line(self.robot[-3], self.robot[-2])
            l2 = Line(self.robot[-2], self.robot[-1])

            # TODO: mozda raditi razliku izmedu vrsta okreta
            turn = l1.angle_between(l2)
            self.directions.append(turn)
            if turn != 0:
                self.number_of_turns += 1
            #return l1.angle_between(l2)
        if debug:
            print("Number of turns = ", self.number_of_turns)
            print("Last turn = ", self.directions[-1])
            print("Multiple visits = ", self.multiple_visits)

    def update_change_of_directions(self):
        last_turn = self.directions.pop()
        if last_turn != 0:
            self.number_of_turns -= 1

    def do_move(self, direction):
        """
        Method that change robot position and refresh room map. Method get
        direction in which robot is headed and update its position accordingly.

        Parameters
        ----------
        direction : tuple
            Tuple of 2 elements, first is direction of robot movement in x axis,
            and second of movement in y axis. -1 is go left/up, 1 right/down and
            0 is stay in place.

        """
        self.room[self.robot[-1][0]][self.robot[-1][1]] = 'o'
        next_x_coord = self.robot[-1][0] + direction[0]
        next_y_coord = self.robot[-1][1] + direction[1]

        if self.room[next_x_coord][next_y_coord] != '.':
            self.multiple_visits += 1

        self.room[next_x_coord][next_y_coord] = 'R'
        self.robot.append((next_x_coord, next_y_coord))

        self.new_change_of_direction()
        self.update()

    def move_back(self):
        """ Undo last robot movement and refresh room map. """

        self.update_change_of_directions()
        last_position = self.robot.pop()
        # Check if robot visited last position already before now, and change
        # cell tip in UNVISITED or VISITED accordingly.
        if last_position in self.robot:
            self.room[last_position[0]][last_position[1]] = 'o'
            self.multiple_visits -= 1
        else:
            self.room[last_position[0]][last_position[1]] = '.'

        self.room[self.robot[-1][0]][self.robot[-1][1]] = 'R'
        self.update()

    def restart_cleaned(self):
        """ Restart all movement on map, make map as on start. """
        for i in range(len(self.room)):
            for j in range(len(self.room[i])):
                if(self.room[i][j] == 'o' or self.room[i][j] == 'R'):
                    self.room[i][j] = '.'

        robot_first = self.robot[0]
        self.directions = []
        self.number_of_turns = 0
        self.multiple_visits = 0
        self.robot = []
        self.robot.append(robot_first)
        self.room[robot_first[0]][robot_first[1]] = 'R'
        self.update()
