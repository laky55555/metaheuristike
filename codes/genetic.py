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

class Genetic():

    def __init__(self, discovered_space, current_position):
        self.discovered_space = discovered_space
        self.current_position_x = current_position[0]
        self.current_position_y = current_position[1]


    def neighbours_of(self, position):
        """Positions of neighbours (includes out of bounds but excludes cell itself)."""
        i = position[0]     # x coordinate
        j = position[1]     # y coordinate
        neighbours = list(itertools.product(range(i-1, i+2), range(j-1, j+2)))
        neighbours.remove(position)
        return neighbours

    # positions that robot can move to
    def get_available_positions(self, position):
        positions = set()
        for i, j in self.neighbours_of(position):
            # out of reach
            if(i < 0 or j < 0):
                continue
            if(i >= len(self.discovered_space) or  j>= len(self.discovered_space[i])):
                continue
            if(discovered_space[i][j] == '#' or discovered_space == 'x'):
                continue
            positions.add((i, j))
        return positions

    # generate mini paths from current robot position
    def generate_mini_paths(self, number_of_mini_paths, length_of_mini_path, robot_position):
        # every mini path begins with current robot position
        mini_paths = [[robot_position]*(length_of_mini_path + 1) for y in range(number_of_mini_paths)]
        # key -> position in mini path, value -> set of avaliable positions
        saved_neighbours = {}

        for j in range(length_of_mini_path):
            for i in range(number_of_mini_paths):
                if (mini_paths[i][j]) in saved_neighbours:  # neighbours already saved
                    positions = saved_neighbours[mini_paths[i][j] ]
                else:
                    positions = self.get_available_positions(mini_paths[i][j])
                    saved_neighbours[mini_paths[i][j]] = positions
                # choosing random next position in mini path from avaliable positions
                mini_paths[i][j+1] = sample(positions, 1)[0] # j+1 -> leaving current robot position in mini paths

        return mini_paths

    # sum of euclidean distances between neighbouring positions in mini path
    def mini_path_distance(self, mini_path):
        distance = 0
        for (x,y) in zip(mini_path[:-1], mini_path[1:]):  # x and y are neighbouring positions
            distance += sqrt((y[1] - x[1])**2 + (y[0] - x[0])**2)
        return distance

    # number of uncleaned positions in mini path
    def mini_path_uncleaned_cells(self, mini_path):
        free = 0
        for i,j in mini_path:
            if(self.discovered_space[i][j] == '.'):
                free += 1
        return free

    # sum of euclidean distance between robot position and each position in mini path
    def mini_path_sum_distance(self, mini_path):
        distance = 0
        robot_position_i = mini_path[0][0]
        robot_position_j = mini_path[0][1]
        for i,j in mini_path:
            distance += sqrt((j - robot_position_j)**2 + (i - robot_position_i)**2)
        return distance


    def calculate_fittnes_function(self, mini_path):
        a = 2
        b = 2
        c = 4
        return (-a*self.mini_path_distance(mini_path) + b*self.mini_path_uncleaned_cells(mini_path)
                + c*self.mini_path_sum_distance(mini_path))


    #TODO: napraviti da se ne ostaje u istom genu npr (1,1) -> (1,2) -> (2,2) u (1,1) -> (2,2) -> (2,2)
    def find_mutable_genes(self, mini_path):
        saved_neighbours = {}
        mutable_genes = [] # list of sets, list[index] contains set of positions that mini_path[index] can be changed with
        for (i,j) in mini_path:
            saved_neighbours[(i,j)] = self.get_available_positions((i, j))

        for (x,y,z) in zip(mini_path[:-1], mini_path[1:], mini_path[2:]):
            # same neighbours of positions x and z
            intersection = saved_neighbours[x].intersection(saved_neighbours[z])
            if len(intersection):
                #print (intersection, intersection.remove(y))
                # remove position y from shared neighbours of x and z
                intersection.remove(y)
                mutable_genes.append(intersection)

        if (len(mini_path) >= 2):
            # last position can be changed with any neighbouring position of second last position (except itself)
            mutable_genes.append(saved_neighbours[mini_path[-2]])
            mutable_genes[-1].remove(mini_path[-1])
        return mutable_genes

    def mutation(self, mini_path):
        genes_for_mutation = self.find_mutable_genes(mini_path)

        index = choice(range(1, len(mini_path))) # choosing position to mutate
        while len(genes_for_mutation[index-1]) < 1: # if set is empty
            index = choice(range(1, len(mini_path)))

        new_gene = sample(genes_for_mutation[index-1], 1)[0] # choosing position that replaces previously chosen one for mutation


        #TODO: tu treba maknuti mini_path2
        mini_path2 = mini_path[:]
        mini_path2[index] = new_gene

        return mini_path2

    def crossover(self, parent1, parent2, point_of_crossing):

        if(parent2[point_of_crossing] in self.neighbours_of(parent1[point_of_crossing-1]) and
            parent1[point_of_crossing] in self.neighbours_of(parent2[point_of_crossing-1])):
            child1 = parent1[0:point_of_crossing]
            child2 = parent2[0:point_of_crossing]
            child1.extend(parent2[point_of_crossing:len(parent2)])
            child2.extend(parent1[point_of_crossing:len(parent1)])
            return child1, child2

        return None


    def next_move(self):

        mini_path = []
        self.generate_mini_path()


a = ([['#', '#', '#', '#', '#', '#', '#'],
      ['#', '.', '.', '.', '.', '.', '#'],
      ['#', '.', '.', '.', '.', '.', '#'],
      ['#', '.', '.', '.', '.', '.', '#'],
      ['#', '.', '.', '.', '.', '.', '#'],
      ['#', '.', '.', '.', '.', '.', '.', '#']])
gen = Genetic(a, (2,3))
#a = gen.generate_mini_paths(3,5,3,3)
#b = a[1]
b = [(3, 3), (3, 2), (2, 3), (3, 4), (4, 5), (5, 4)]
c = [(3, 3), (2, 2), (1, 3), (4, 4), (2, 5), (5, 4)]
b = [(3, 3), (4 ,3), (5, 3), (5, 4), (5, 5), (5, 6)]

print(gen.crossover(b, c, 1))
print(gen.crossover(b, c, 2))
print(gen.crossover(b, c, 3))
print(gen.crossover(b, c, 4))
print(gen.crossover(b, c, 5))
gen.calculate_fittnes_function([(1, 1), (1, 2), (1, 3), (1, 4), (1, 5)])
gen.calculate_fittnes_function([(1,1), (1, 2), (2, 3)])

"""print(b)
print(gen.find_mutable_genes(b))
for i in range(10):
    mut = gen.mutation(b)
    print()
    print(b, mut, gen.calculate_fittnes_function(mut))
    print(gen.crossover(b, mut, 2))"""
