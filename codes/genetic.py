from math import sqrt
from random import sample, choice, random
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

    def __init__(self, discovered_space, current_position, population_size, length_of_mini_path,
                 mutation_probability, crossover_probability, number_of_iterations):
        self.discovered_space = discovered_space
        # self.current_position_x = current_position[0]
        # self.current_position_y = current_position[1]
        self.current_position = current_position
        self.population_size = population_size
        self.length_of_mini_path = length_of_mini_path
        self.mutation_probability = mutation_probability
        self.crossover_probability = crossover_probability
        self.number_of_iterations = number_of_iterations


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
            if(self.discovered_space[i][j] == '#' or self.discovered_space[i][j] == 'x'):
                continue
            positions.add((i, j))
            # print("position " + str(i) + str(j) + " bla " )
            # print(self.discovered_space[i][j])
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


    def calculate_fitness_function(self, mini_path):
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
            # print(x, y, z)
            # print("susjedi od x")
            # print(saved_neighbours[x])
            # print("susjedi od z")
            # print(saved_neighbours[z])
            intersection = saved_neighbours[x].intersection(saved_neighbours[z])
            if len(intersection):
                # print("prije micanja susjeda")
                # print (intersection)
                # remove position y from shared neighbours of x and z
                intersection.remove(y)
                # print("nakon micanja")
                # print(intersection)
                mutable_genes.append(intersection)

        if (len(mini_path) >= 2):
            # last position can be changed with any neighbouring position of second last position (except itself)
            mutable_genes.append(saved_neighbours[mini_path[-2]])
            mutable_genes[-1].remove(mini_path[-1])
        return mutable_genes


    # TODO: za svaki kromosom generiraj slucajan broj, ako je manji od vjerojatnosti mutiraj
    def mutation(self, mini_path):
        genes_for_mutation = self.find_mutable_genes(mini_path)

        # je li isto prolazit svaki gen i gledat vjerojatnost? -> nope
        index = choice(range(1, len(mini_path))) # choosing position to mutate
        while len(genes_for_mutation[index-1]) < 1: # if set is empty
            index = choice(range(1, len(mini_path)))

        new_gene = sample(genes_for_mutation[index-1], 1)[0] # choosing position that replaces previously chosen


        # #TODO: tu treba maknuti mini_path2
        # mini_path2 = mini_path[:]
        # mini_path2[index] = new_gene
        #
        # return mini_path2

        mini_path[index] = new_gene
        #return mini_path2

    def update_mutable_genes(self, mini_path, index_of_position_to_update, genes_for_mutation):
        # TODO: bolje to napravit
        print("UPDATEEE")
        neighbours_of_previous = self.get_available_positions(mini_path[index_of_position_to_update-1])
        neighbours_of_next = self.get_available_positions(mini_path[index_of_position_to_update+1])
        intersection = neighbours_of_previous.intersection(neighbours_of_next)
        if len(intersection):
            # remove position y from shared neighbours of x and z
            intersection.remove(mini_path[index_of_position_to_update])
            genes_for_mutation[index_of_position_to_update-1] = intersection


    def mutationVersion2(self, mini_path):
        print("voluuume 2")
        print(mini_path)
        genes_for_mutation = self.find_mutable_genes(mini_path)
        i = 1
        while i < self.length_of_mini_path+1:
        # for i in range(1, self.length_of_mini_path+1):
            print(i)
            rand = random()
            print(rand)
            if rand < self.mutation_probability:
                print(mini_path[i])
                # ako se moze mutirat mutiraj
                # nakon mutiranja triba update genes_for_mutation
                if len(genes_for_mutation[i-1]) >= 1:
                    print(genes_for_mutation)
                    new_gene = sample(genes_for_mutation[i-1], 1)[0]
                    print(new_gene)
                    mini_path[i] = new_gene

                    # ako minjamo zadnjeg nista
                    if(i == self.length_of_mini_path):
                        continue
                    if(i == self.length_of_mini_path-1):
                    # ako minjamo predzadnjeg drugaciji update za moguce promjene za zadnju poziciju
                        neighbours_of_second_last = self.get_available_positions(mini_path[i])
                        if neighbours_of_second_last.intersection(mini_path[i+1]):
                            neighbours_of_second_last.remove(mini_path[i+1])
                        genes_for_mutation[i] = neighbours_of_second_last
                        print("nakon updatea")
                        print(genes_for_mutation)
                    # inace
                    # nac mutable_genes za mini_path[i+1]
                    # nac susjede od mini_path[i] i mini_path[i+2]
                    # update genes_for_mutation na poziciji i
                    else:
                        self.update_mutable_genes(mini_path, i+1, genes_for_mutation)
            i += 1

        return mini_path


###################################################

    def crossover_one_point(self, parent1, parent2):
        new_children1 = []

        # if random number is higher than crossover probability place parents directly into the new genration
        if self.crossover_probability < random():
            new_children1.extend([parent1, parent2])
            return new_children1
        # random point of crossover
        point_options = list(range(1,6))
        point_of_crossing = 3
        # ?? ako nije ponovno pogadjat point_of_crossing ili proglasit neuspjelim ili dodat roditelje
        if(parent2[point_of_crossing] in self.neighbours_of(parent1[point_of_crossing-1]) and
            parent1[point_of_crossing] in self.neighbours_of(parent2[point_of_crossing-1])):
            child1 = parent1[0:point_of_crossing]
            child2 = parent2[0:point_of_crossing]
            child1.extend(parent2[point_of_crossing:len(parent2)])
            child2.extend(parent1[point_of_crossing:len(parent1)])
            return new_children1.extend([child1, child2])
        return None



    def generate_initial_population(self):
        initial_population = self.generate_mini_paths(self.population_size, self.length_of_mini_path, self.current_position)
        return initial_population

### Propotionate selection ###
    def place_chromosomes_fitness_into_interval(self, current_population):
        dictionary_fitness_values = {}
        fitness_sum = 0
        probability = 0
        for index, mini_path in enumerate(current_population):
            value = self.calculate_fitness_function(mini_path)
            fitness_sum += value
            dictionary_fitness_values[index] = value

        for key, value in dictionary_fitness_values.items():
            probability += (value/fitness_sum)
            dictionary_fitness_values[key] = probability

        return dictionary_fitness_values


    def select_chromosome(self, dictionary_fitness_values):
        # >>> import os
        # >>> int.from_bytes(os.urandom(8), byteorder="big") / ((1 << 64) - 1)
        probability = random()
        for index, fitness_value in dictionary_fitness_values.items():
            if probability < fitness_value:
                #print(index)
                return index


    def make_one_iteration(self, current_population):
        print("make one iteration")
        #print(int(self.population_size/2) - 1)
        new_generation = []
        i = 0
        # highest fitness first
        current_population = sorted(current_population, key = self.calculate_fitness_function, reverse=True)
        new_generation.extend(current_population[:2])
        del current_population[:2]

        dictionary_fitness_values = self.place_chromosomes_fitness_into_interval(current_population)
        print(dictionary_fitness_values)
        # for i in range(int(self.population_size/2) -1):

        while i < (int(self.population_size/2) - 1):
            print("while")
            # select parents
            parent_one = current_population[self.select_chromosome(dictionary_fitness_values)]
            parent_two = current_population[self.select_chromosome(dictionary_fitness_values)]

            # crossover
            new_children = self.crossover_one_point(parent_one, parent_two)
            if(new_children != None):
                print("uspilo")
                #mutation
                # self.mutation(new_children[0])
                # self.mutation(new_children[1])
                #
                self.mutationVersion2(new_children[0])
                self.mutationVersion2(new_children[1])

                new_generation.extend(new_children)
                i += 1
            # neuspjelo krizanje
            # ?? detektirat ili ubacit roditelje bez krizanja

        return new_generation


    def next_move(self):
        current_population = self.generate_initial_population()
        print("inicijalna")
        print(current_population)

        for i in range(self.number_of_iterations):
            current_population = self.make_one_iteration(current_population)

        return current_population




# fun fun fun noot

a = ([['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
      ['#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#'],
      ['#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#'],
      ['#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#'],
      ['#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#'],
      ['#', '.', '.', '.', '.', 'x', '.', '.', '.', '.', '.', '#'],
      ['#', '.', '.', 'x', 'x', 'x', '.', '.', '.', '.', '.', '#'],
      ['#', '.', '.', '.', 'x', 'x', '.', '.', '.', '.', '.', '#'],
      ['#', '.', '.', '.', 'x', '.', '.', '.', '.', '.', '.', '#'],
      ['#', '.', '.', '.', 'x', '.', '.', '.', '.', '.', '.', '#'],
      ['#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#'],
      ['#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#'],
      ['#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#'],
      ['#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#'],
      ['#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#'],
      ['#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#'],
      ['#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#']])

gen = Genetic(a, (5,3), 4, 5, 0.2, 0.8, 10)

#mini_paths  = gen.generate_mini_paths(5,5,(5,3))
# print(mini_paths)
#
#dict = gen.place_chromosomes_fitness_into_interval(mini_paths)
# print(dict)

# nova = gen.make_one_iteration(mini_paths)
# for i in range(10):
#     print("_______________________")
#     nova = gen.make_one_iteration(nova)
#     print(nova)
#
# dict_nova = gen.place_chromosomes_fitness_into_interval(nova)
# print(dict_nova)

zadnja_gen = gen.next_move()
print(zadnja_gen)
print("next moove")
zadnja_gen = sorted(zadnja_gen, key = gen.calculate_fitness_function, reverse=True)
print(zadnja_gen[0][1])

a = ([['#', '#', '#', '#', '#', '#', '#'],
      ['#', '.', '.', '.', '.', '.', '#'],
      ['#', '.', '.', '.', '.', '.', '#'],
      ['#', '.', '.', '.', '.', '.', '#'],
      ['#', '.', '.', '.', '.', '.', '#'],
      ['#', '.', '.', '.', '.', '.', '.', '#']])

# gen = Genetic(a, (2,3), 50, 5, 0.2, 0.8, 10)
#
# mini_paths  = gen.generate_mini_paths(5,5,(2,3))
#
# mini_path = mini_paths[0]
# print(mini_path)
#
# print("prije mutacije")
# mut = gen.mutationVersion2(mini_path)
# print("posli mutacije")
# print(mut)
# print(mini_path)



# a = gen.generate_mini_paths(3,5,(3,3))
# print(a)
# #b = a[1]
# b = [(3, 3), (3, 2), (2, 3), (3, 4), (4, 5), (5, 4)]
# c = [(3, 3), (2, 2), (1, 3), (4, 4), (2, 5), (5, 4)]
# b = [(3, 3), (4 ,3), (5, 3), (5, 4), (5, 5), (5, 6)]
#
# print(b)
# gen.mutation(b)
# print(b)



# print(gen.crossover(b, c, 1))
# print(gen.crossover(b, c, 2))
# print(gen.crossover(b, c, 3))
# print(gen.crossover(b, c, 4))
# print(gen.crossover(b, c, 5))
# gen.calculate_fitness_function([(1, 1), (1, 2), (1, 3), (1, 4), (1, 5)])
# gen.calculate_fitness_function([(1,1), (1, 2), (2, 3)])

#

#print(nova)



"""print(b)
print(gen.find_mutable_genes(b))
for i in range(10):
    mut = gen.mutation(b)
    print()
    print(b, mut, gen.calculate_fitness_function(mut))
    print(gen.crossover(b, mut, 2))"""



# for i in range(0,10):
#     line = ""
#     for j in range(0,10):
#         line += ("(" + str(i) + "," + str(j) + ") ")
#     print(line)



# (0,0) (0,1) (0,2) (0,3) (0,4) (0,5) (0,6) (0,7) (0,8) (0,9)
# (1,0) (1,1) (1,2) (1,3) (1,4) (1,5) (1,6) (1,7) (1,8) (1,9)
# (2,0) (2,1) (2,2) (2,3) (2,4) (2,5) (2,6) (2,7) (2,8) (2,9)
# (3,0) (3,1) (3,2) (3,3) (3,4) (3,5) (3,6) (3,7) (3,8) (3,9)
# (4,0) (4,1) (4,2) (4,3) (4,4) (4,5) (4,6) (4,7) (4,8) (4,9)
# (5,0) (5,1) (5,2) (5,3) (5,4) (5,5) (5,6) (5,7) (5,8) (5,9)
# (6,0) (6,1) (6,2) (6,3) (6,4) (6,5) (6,6) (6,7) (6,8) (6,9)
# (7,0) (7,1) (7,2) (7,3) (7,4) (7,5) (7,6) (7,7) (7,8) (7,9)
# (8,0) (8,1) (8,2) (8,3) (8,4) (8,5) (8,6) (8,7) (8,8) (8,9)
# (9,0) (9,1) (9,2) (9,3) (9,4) (9,5) (9,6) (9,7) (9,8) (9,9)
