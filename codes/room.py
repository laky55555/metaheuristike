#import sys
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt
from enum import Enum


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
    switch = {'.': 0x000000, '#': 0xCCCC66, 'x': 0xCC66CC, 'o': 0x66CC66, 'R':0xDAAA00}


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
        self.room_max_height =len(data)
        self.room_max_width = max([len(row) for row in data]) if self.room_max_height > 0 else 0
        self.robot = robot
        self.room = data
        # Initialize minimum to 0 for easier handling clik events (avoiding exceptins).
        self.minimum = 0
        self.start = self.findStart()

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
        self.room_max_height =len(data)
        self.room_max_width = max([len(row) for row in data]) if self.room_max_height > 0 else 0
        self.room = data
        self.robot = robot
        # Initialize minimum to 0 for easier handling clik events (avoiding exceptins).
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
                    self.drawSquare(painter, self.minimum*j, self.minimum*i, self.switch[self.room[i][j]])

            #print(self.robot)
            pen = QPen(QColor(0xDAAA99), 3, Qt.DashLine)
            painter.setPen(pen)
            self.middle = self.minimum/2
            for i,j in zip(self.robot[:-1], self.robot[1:]):
                self.drawMovement(painter, self.minimum*i[1], self.minimum*i[0], self.minimum*j[1], self.minimum*j[0])

            painter.end()


    def drawMovement(self, painter, x1, y1, x2, y2):
        painter.drawLine(x1+self.middle, y1+self.middle, x2+self.middle, y2+self.middle)


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
        for row in self.room:
            for cell in row:
                if cell == Symbol.ROBOT.value:
                    return True

        return False

    def delete_old_robot_position(self):
        """Replace all robot positions on the map with unvisited."""
        for row in range(len(self.room)):
            self.room[row] = [Symbol.UNVISITED.value if x==Symbol.ROBOT.value
                                                    else x for x in self.room[row]]


    # Override what happen on click.
    def mousePressEvent(self, event):
        """
        On each mouse click check if it was left click, and if it was
        depending on which mode widget is (making new map, chosing start position,...)
        mark new start position or make/remove obstacles.
        """
        if(event.button() == Qt.LeftButton and self.minimum > 0):
            x = event.pos().y()//self.minimum
            y = event.pos().x()//self.minimum
            if (x >= self.room_max_height or y >= len(self.room[x])):
                return
            #print (event.pos().y()//self.minimum, event.pos().x()//self.minimum)
            #print(Symbol.UNVISITED.value is self.room[x][y])

            # If we are in mode 1 and we clicked on empty place on map.
            if(self.mode == 1 and
                (self.room[x][y] == Symbol.UNVISITED.value or self.room[x][y] == Symbol.VISITED.value)):
                self.delete_old_robot_position()
                self.room[x][y] = Symbol.ROBOT.value
                self.robot = [(x,y)]
                self.start = True

            # If we are in mode 2 and we clicked on empty or place with obstacle.
            elif(self.mode == 2):
                if(self.room[x][y] == Symbol.UNVISITED.value or self.room[x][y] == Symbol.VISITED.value):
                    self.room[x][y] = Symbol.OBSTACLE.value
                elif(self.room[x][y] == Symbol.OBSTACLE.value):
                    self.room[x][y] = Symbol.UNVISITED.value
            self.update()

    def detect_room(self, sight_distance):
        position = self.robot[-1]
        sight_distance_quad = sight_distance*sight_distance
        minimal_x = max(position[0]-sight_distance, 0)
        # mozda treba dodati -1 na self.room_max_height
        maximal_x = min(position[0]+sight_distance+1, self.room_max_height)

        minimal_y = max(position[1]-sight_distance, 0)
        # treba sigurno pametnije jer duljine redaka u sobi ne moraju biti jednake.
        #maximal_y = min(position[1]+sight_distance, self.room_max_width)

        number_of_rows = maximal_x - minimal_x
        #detected = [[] for i in range(number_of_rows)]
        detected = {}
        #print(minimal_x, maximal_x, minimal_y)
        for num, i in zip(range(number_of_rows), range(minimal_x, maximal_x)):
            maximal_y = min(position[1]+sight_distance+1, len(self.room[i]))
            initialized = False
            for j in range(minimal_y, maximal_y):
                if((position[0]-i)*(position[0]-i) + (position[1]-j)*(position[1]-j) <= sight_distance_quad):
                    #detected[num].append((i,j))
                    if(initialized == False):
                        y = j
                        initialized = True
                        detected[(i,y)] = []
                    detected[(i,y)].append(self.room[i][j])




        return detected

    def do_move(self, direction):
        #print(self.robot)
        self.room[self.robot[-1][0]][self.robot[-1][1]] = 'o'
        next_x_coord = self.robot[-1][0] + direction[0]
        next_y_coord = self.robot[-1][1] + direction[1]
        self.room[next_x_coord][next_y_coord] = 'R'
        self.robot.append((next_x_coord, next_y_coord))
        self.update()
        #print(self.robot)
