import operator
import itertools
from math import sqrt, inf
from queue import Queue

class ClosestPath(object):

    def __init__(self, room, current_position):

        self.room = room
        self.start_position = current_position
        self.uncleaned_cells = self.find_uncleaned_cells()

        self.shortest_path_len = inf


    def neighbours_of(self, i, j):
        """Positions of neighbours (includes out of bounds but excludes cell itself)."""
        neighbours = list(itertools.product(range(i-1, i+2), range(j-1, j+2)))
        neighbours.remove((i, j))
        return neighbours

    def get_available_positions(self, pos_x, pos_y):
        positions = set()

        for a, b in self.neighbours_of(pos_x, pos_y):
            if(a < 0 or b < 0):
                continue
            if(a >= len(self.room) or b >= len(self.room[a]) ):
                continue
            if(self.room[a][b] == '#' or self.room[a][b] == 'x'):
                continue

            positions.add((a,b))

        return positions

    def find_uncleaned_cells(self):
        uncleaned = {}
        for i in range(len(self.room)):
            for j in range(len(self.room[i])):
                if(self.room[i][j] == '.'):
                    uncleaned[(i,j)] = self.euclidean_distance(self.start_position[0], self.start_position[1], i, j)
        return sorted(uncleaned.items(), key = operator.itemgetter(1))

    def euclidean_distance(self, x1, y1, x2, y2):
        return sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2))


    def find_shortest(self):
        for target in self.uncleaned_cells:
            if(self.shortest_path_len < target[1]):
                break;

            path = self.find_path(target[0], self.start_position)
            if (self.path_distance(path) < self.shortest_path_len):
                #TODO: tu mozda treba racunati duljinu puta
                self.shortest_path_len = self.path_distance(path)
                self.shortest_path = path

        return self.shortest_path

    def path_distance(self, path):
        distance = 0
        for (x,y) in zip(path[:-1], path[1:]):  # x and y are neighbouring positions
            distance += sqrt((y[1] - x[1])**2 + (y[0] - x[0])**2)
        return distance

    def in_visited(self, visited, current):
        for cell, parent in visited:
            if(cell == current):
                return True

        return False

    def recreate_path(self, current, parent, visited):
        print("Visited:")
        print(visited)
        path = []
        path.append(current)
        while parent != None:
            for cell, cell_parent in visited:
                if(cell == parent):
                    current = cell
                    parent = cell_parent
                    path.append(current)
                    break

        path.reverse()
        print("Path:")
        print(path)
        return path

    def find_path(self, end_postion, start_position):

        queue = Queue(1000)
        queue.put((start_position, None))

        visited = set()
        visited.add((start_position, None))

        while not queue.empty():
            current, parent = queue.get()
            print("current, parent")
            print(current, parent)
            if(current == end_postion):
                return self.recreate_path(current, parent, visited)

            possible_next_cell = self.get_available_positions(current[0], current[1])
            possible_next_cell = list(possible_next_cell)
            possible_next_cell.sort(key = lambda x: (x[0]-current[0])**2 + (x[1]-current[1])**2)
            #print("possible_next_cell")
            #print(possible_next_cell)
            for cell in possible_next_cell:
                if(not self.in_visited(visited, cell)):
                    queue.put((cell, current))
                    visited.add((cell, current))
