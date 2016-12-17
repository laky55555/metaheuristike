from math import sqrt
from random import sample, choice
import itertools


#a = new Genetski([],(0,0))
#[[(0, 0), (0, 0), (0, 0), (0, 0), (0, 0)], [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0)], [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0)],
#[(0, 0), (0, 0), (0, 0), (0, 0), (0, 0)], [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0)]]
#
#[['#','#','#','#','#','#','#'],
# ['#','.','.','.','.','.','#'],
# ['#','.','.','.','.','.','#'],
# ['#','.','.','.','.','.','#']]

class Genetski():

    def __init__(self, known_map, position):
        self.known_map = known_map
        self.current_position_x = position[0]
        self.current_position_y = position[1]


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
            if(a >= len(self.known_map) or b >= len(self.known_map[a]) ):
                continue
            if(self.known_map[a][b] == '#' or self.known_map[a][b] == 'x'):
                continue

            positions.add((a,b))

        return positions

    def generate_mini_paths(self, num_of_mini_paths, length_of_mini_path, pos_x, pos_y):

        mini_paths = [[(pos_x, pos_y)]*(length_of_mini_path + 1) for y in range(num_of_mini_paths)]
        saved_neighbours = {}

        for j in range(length_of_mini_path):
            for i in range(num_of_mini_paths):

                if (mini_paths[i][j]) in saved_neighbours:
                    positions = saved_neighbours[mini_paths[i][j] ]
                else:
                    positions = self.get_available_positions(mini_paths[i][j][0], mini_paths[i][j][1])
                    saved_neighbours[mini_paths[i][j]] = positions

                mini_paths[i][j+1] = sample(positions, 1)[0]

        return mini_paths

    def mini_path_distance(self, mini_path):
        distance = 0
        for (x,y) in zip(mini_path[:-1], mini_path[1:]):
            distance += sqrt((y[1] - x[1])**2 + (y[0] - x[0])**2)
        return distance

    def mini_path_uncleaned_cells(self, mini_path):
        free = 0
        for i,j in mini_path:
            if(self.known_map[i][j] == '.'):
                free += 1
        return free

    def mini_path_sum_distance(self, mini_path):
        distance = 0
        start_i = mini_path[0][0]
        start_j = mini_path[0][1]
        for i,j in mini_path:
            distance += sqrt((j - start_j)**2 + (i - start_i)**2)
        return distance

    def calculate_fittnes_function(self, mini_path):
        a = 2
        b = 2
        c = 2
        return (a*self.mini_path_distance(mini_path) + b*self.mini_path_uncleaned_cells(mini_path)
                + c*self.mini_path_sum_distance(mini_path))


    #TODO: napraviti da se ne ostaje u istom genu npr (1,1) -> (1,2) -> (2,2) u (1,1) -> (2,2) -> (2,2)
    def find_mutable_genes(self, mini_path):
        saved_neighbours = {}
        mutable_genes = {}
        for (i,j) in mini_path:
            saved_neighbours[(i,j)] = self.get_available_positions(i, j)

        for (x,y,z) in zip(mini_path[:-1], mini_path[1:], mini_path[2:]):
            intersection = saved_neighbours[x].intersection(saved_neighbours[z])
            if len(intersection):
                mutable_genes[y] = intersection

        if (len(mini_path) >= 2):
            mutable_genes[mini_path[-2]] = saved_neighbours[mini_path[-2]]
        return mutable_genes

    def mutation(self, mini_path):
        genes_for_mutation = self.find_mutable_genes(mini_path)
        chosen_gene = choice(list(genes_for_mutation.keys()))
        new_gene = sample(genes_for_mutation[chosen_gene], 1)[0]
        for n, i in enumerate(mini_path):
            if(i==chosen_gene):
                mini_path[n] = new_gene


    def next_move(self):

        mini_path = []
        self.generate_mini_path()
