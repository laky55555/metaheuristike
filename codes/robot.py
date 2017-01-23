import itertools
from genetic import Genetic
from find_path import ClosestPath


class Robot(object):
    """
    Class for comunication between room widget and algorithm for cleaning.
    Class has functions for making moves forward and backward.
    """

    def __init__(self, room_widget, sight_distance=6):
        """
        Initialize robot for moving and his memory.
        At start Initialize size of whole room for easier memory managmenet.

        Parameters
        ----------
        room_widget : QWidget
            Widget in which we will draw moves and buttons for making moves.
        sight_distance : int
            Number of fields robot can see around in each direction.

        """
        self.sight_distance = sight_distance
        self.room_widget = room_widget
        self.full_room = [[None] * len(i) for i in self.room_widget.room]
        self.previous_position = None

    def move_one(self):
        """
        Make one move using algorithm.
        If whole room is cleaned return True and message.

        Returns
        -------
        boolean
            True if every cell has been visited, else False.
        """

        print("move_one")
        # Search everything around robot and update robot map.
        self.detect_room()
        if(self.uncleaned_cells == 0):
            print("Everything is cleaned :)")
            return True

        # Find current position of robot and make it clean
        current_position = [(i, row.index('R'))
                            for i, row in enumerate(self.detected_room) if 'R' in row]
        self.detected_room[current_position[0][0]][
            current_position[0][1]] = 'o'


        # Get all unvisited postions on which robot can move.
        possible_next_uncleaned = self.get_available_positions(
            current_position[0][0], current_position[0][1], True)

        # If there is only 1 unvisited place go to that place,
        # if there are more then 1 call genetic algorithm to decide where to go,
        # else skip to closest unvisited place with ClosestPath class.
        if(len(possible_next_uncleaned) == 1):
            next_move = possible_next_uncleaned.pop()
            next_move = (next_move[0] - current_position[0]
                         [0], next_move[1] - current_position[0][1])
            print("Samo je jedan moguci")
            print(next_move)

        elif(len(possible_next_uncleaned) == 0):
            closest_path = ClosestPath(self.detected_room, current_position[0])
            path = closest_path.find_shortest()
            print("Path zavrni")
            print(path)
            for i, j in path[1:]:
                next_move = (i - current_position[0][0], j - current_position[0][1])
                current_position[0] = (i, j)
                self.previous_position = current_position[0]
                self.room_widget.do_move(next_move)
                self.detect_room()
            print("Nema neociscenih, slijedeci potez ide na")
            print(path[-1])
            return False

        else:
            print(current_position)
            # Genetic(room, current_position, population_size, mini_path_len, mutation_probability, crossover_probability, number_of_iterations)
            if self.previous_position == None:
                gen = Genetic(self.detected_room, current_position[
                          0], None, 50, 5, 0.2, 0.85, 1)
            else:
                gen = Genetic(self.detected_room, current_position[
                          0], self.previous_position, 50, 5, 0.2, 0.85, 1)
            next_move = gen.next_move()

        self.previous_position = current_position[0]
        self.room_widget.do_move(next_move)

        return False

    def neighbours_of(self, i, j):
        """Positions of neighbours (includes out of bounds but excludes cell itself)."""
        neighbours = list(itertools.product(
            range(i - 1, i + 2), range(j - 1, j + 2)))
        neighbours.remove((i, j))
        return neighbours

    def get_available_positions(self, pos_x, pos_y, exclude_cleaned):
        positions = set()

        for a, b in self.neighbours_of(pos_x, pos_y):
            if(a < 0 or b < 0):
                continue
            if(a >= len(self.detected_room) or b >= len(self.detected_room[a])):
                continue
            if(self.detected_room[a][b] == '#' or self.detected_room[a][b] == 'x'):
                continue
            if(exclude_cleaned and self.detected_room[a][b] == 'o'):
                continue

            positions.add((a, b))

        return positions

    def move_all(self):
        """ Makes moves until whole room is cleared. """

        print("move_all")
        finished = self.move_one()
        while(not finished):
            finished = self.move_one()

    def move_back(self):
        """ Undo last move if there is at least one move made. """

        print("move_back")
        if len(self.room_widget.robot) > 1:
            self.room_widget.move_back()
        else:
            print("There are no moves to go back.")

    def extract_detected_only(self, debug=False):
        """
        Extract all known data from full_room into detected_room
        for sending it to algorithm for making new move.
        """

        self.detected_room = []
        self.uncleaned_cells = 0

        if(debug):
            print("Full room")
            for row in self.full_room:
                print(row)

        # Get all rows from map where something is discovered and put it in
        # detected_room, all elements that are not discovered but is same row
        # fulfill with wall sign '#'
        for i, row in zip(range(len(self.full_room)), self.full_room):
            if(next((True for item in row if item is not None), False)):
                new_row = [
                    symbol if symbol is not None else '#' for symbol in row]
                self.detected_room.append(new_row)
                self.uncleaned_cells += new_row.count('.')

        if(debug):
            print("detected_room")
            for row in self.detected_room:
                print(row)
            print(self.uncleaned_cells)

    def detect_room(self, debug=False):
        """
        Method for fulfilling whole room map.
        Everything robot can see from current postion is aquired and
        implemented in room map.
        """
        print("detect_room")

        # Get everything robot can see from current position.
        # Sensors input is dictionary where key is tuple of row start position
        # of map and value list with all discovered space .
        sensors_input = self.room_widget.detect_room(self.sight_distance)

        if(debug):
            print("sensors input")
            for row in sensors_input:
                print(row, sensors_input[row])

        # Update map with new elements from sensor.
        for start in sensors_input:
            for j, symbol in zip(range(start[1], len(sensors_input[start]) + start[1] + 1), sensors_input[start]):
                self.full_room[start[0]][j] = symbol

        self.extract_detected_only(True)
