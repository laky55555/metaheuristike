from math import sqrt
from random import sample, choice, random
import itertools
import os
from copy import deepcopy
from math import fabs


class Genetic():

    def __init__(self, discovered_space, current_position, previous_position, population_size, length_of_mini_path,
                 mutation_probability, crossover_probability, number_of_iterations, debug = False):
        self.discovered_space = discovered_space
        self.current_position = current_position
        self.population_size = population_size
        self.length_of_mini_path = length_of_mini_path
        self.mutation_probability = mutation_probability
        self.crossover_probability = crossover_probability
        self.number_of_iterations = number_of_iterations
        self.previous_position = previous_position
        self.debug = debug


    def neighbours_of(self, position):
        """Positions of neighbours (includes out of bounds but excludes cell itself)."""
        i = position[0]     # x coordinate
        j = position[1]     # y coordinate
        neighbours = list(itertools.product(range(i-1, i+2), range(j-1, j+2)))
        neighbours.remove(position)
        return neighbours

    # positions that robot can move to
    def get_available_positions(self, position, restricted = False):
        positions = set()
        for i, j in self.neighbours_of(position):
            # out of reach
            if(i < 0 or j < 0):
                continue
            if(i >= len(self.discovered_space) or  j>= len(self.discovered_space[i])):
                continue
            if restricted:
                if(self.discovered_space[i][j] == '#' or self.discovered_space[i][j] == 'o' or self.discovered_space[i][j] == 'x'):
                    continue
            else:
                if(self.discovered_space[i][j] == '#' or self.discovered_space[i][j] == 'x'):
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
                if j == 0:
                    positions = self.get_available_positions(mini_paths[i][j], True)
                else:
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
    def mini_path_consecutive_uncleaned_cells(self, mini_path):
        free = 0
        for index, postion in enumerate(mini_path[1:]):
            # print (i,j)
            if(self.discovered_space[postion[0]][postion[1]] == '.' and mini_path.index(postion) > index):
                free += 1
            else:
                return free
        return free

    def mini_path_uncleaned_cells(self, mini_path):
        free = 0
        for index, postion in enumerate(mini_path[1:]):
            # print (i,j)
            if(self.discovered_space[postion[0]][postion[1]] == '.' and mini_path.index(postion) > index):
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


    def mini_path_direction(self, mini_path):
        if self.previous_position[0] == mini_path[0][0] and mini_path[0][0] == mini_path[1][0]:
            return True
        elif self.previous_position[1] == mini_path[0][1] and mini_path[0][1] == mini_path[1][1]:
            return True
        return False

    def check_wall(self, x, y):
        if self.discovered_space[x][y] == '#' or self.discovered_space[x][y] == 'x':
            return True
        return False

    def check_wall_around(self, mini_path, vertical = False):
        wall_value = 0
        x_1 = mini_path[0][0]
        y_1 = mini_path[0][1]
        x_2 = mini_path[1][0]
        y_2 = mini_path[1][1]

        if (vertical):
            if self.check_wall(x_1+1, y_1) and self.check_wall(x_2+1, y_2) or self.check_wall(x_1-1, y_1) and self.check_wall(x_2-1, y_2):
                wall_value = 1
        else:
            if self.check_wall(x_1, y_1+1) and self.check_wall(x_2, y_2+1) or self.check_wall(x_1, y_1-1) and self.check_wall(x_2, y_2-1):
                wall_value = 1
        return wall_value

    def check_cleaned_cell(self, x, y):
        if self.discovered_space[x][y] == 'o':
            return True
        return False


    def check_cleaned_cells_around(self, mini_path, vertical = False):
        cleaned_value = 0

        x_1 = mini_path[0][0]
        y_1 = mini_path[0][1]
        x_2 = mini_path[1][0]
        y_2 = mini_path[1][1]

        if (vertical):
            if self.check_cleaned_cell(x_1+1, y_1) and self.check_cleaned_cell(x_2+1, y_2) or self.check_cleaned_cell(x_1-1, y_1) and self.check_cleaned_cell(x_2-1, y_2):
                cleaned_value = 1
        else:
            if self.check_cleaned_cell(x_1, y_1+1) and self.check_cleaned_cell(x_2, y_2+1) or self.check_cleaned_cell(x_1, y_1-1) and self.check_cleaned_cell(x_2, y_2-1):
                cleaned_value = 1

        return cleaned_value

    def check_transition(self, mini_path, vertical = False):
        transition_value = 0

        x_1 = mini_path[0][0]
        y_1 = mini_path[0][1]
        x_2 = mini_path[1][0]
        y_2 = mini_path[1][1]

        if (vertical):
            if self.check_cleaned_cell(x_1+1, y_1) and self.check_wall(x_2+1, y_2) or self.check_cleaned_cell(x_1-1, y_1) and self.check_wall(x_2-1, y_2):
                transition_value = 1
        else:
            if self.check_cleaned_cell(x_1, y_1+1) and self.check_wall(x_2, y_2+1) or self.check_cleaned_cell(x_1, y_1-1) and self.check_wall(x_2, y_2-1):
                transition_value = 1

        return transition_value

    def get_number_of_edges(self, position, mini_path):
        edges = 0

        for i, j in self.neighbours_of(mini_path[position]):
            # out of reach
            if(i < 0 or j < 0):
                continue
            elif(i >= len(self.discovered_space) or  j>= len(self.discovered_space[i])):
                continue
            #TODO: mozda bolje ne gledati or dio??????
            elif self.discovered_space[i][j] == 'o':
            # elif self.discovered_space[i][j] == 'o' or (i,j) in mini_path[:position]:
                edges += 2
            elif self.discovered_space[i][j] == '.':
                continue
            elif self.discovered_space[i][j] == '#' or self.discovered_space[i][j] == 'x':
                edges += 1
        return edges


    def check_edges(self, mini_path):
        edges = 0
        for i in range(1, len(mini_path)):
            if self.discovered_space[mini_path[i][0]][mini_path[i][1]] != 'o':
                edges = edges + (5 - i) * self.get_number_of_edges(i, mini_path)
            # edges = edges + (5 - i) * self.get_number_of_edges(i, mini_path)
        return edges


    def check_possible_bad_turning(self):
        x = self.current_position[0]
        y = self.current_position[1]

        if self.discovered_space[x-1][y+1] == '.' and self.discovered_space[x][y+1] == '.' and self.discovered_space[x+1][y+1] == '.':
            return True
        if self.discovered_space[x-1][y-1] == '.' and self.discovered_space[x][y-1] == '.' and self.discovered_space[x+1][y-1] == '.':
            return True
        if self.discovered_space[x+1][y-1] == '.' and self.discovered_space[x+1][y] == '.' and self.discovered_space[x+1][y+1] == '.':
            return True
        if self.discovered_space[x-1][y-1] == '.' and self.discovered_space[x-1][y] == '.' and self.discovered_space[x-1][y-1] == '.':
            return True

        return False




    def calculate_fitness_function(self, mini_path, debug = False):

        distance_koef = 0
        uncleaned_koef = 1
        sum_distance_koef = 1
        direction = wall_value = cleaned_value = transition_value = bad_turning = edges = 0
        direction_koef = 5
        wall_koef = 10
        cleaned_koef = 15
        transition_koef = 10
        edges_koef = 1.3
        bad_turning_koef = -3

        if self.check_possible_bad_turning():
            if mini_path[0][0] != mini_path[1][0] and mini_path[0][1] != mini_path[1][1]:
                bad_turning = 1

        if (mini_path[0][0] == mini_path[1][0]):
            wall_value = self.check_wall_around(mini_path, True)
            cleaned_value = self.check_cleaned_cells_around(mini_path, True)
            transition_value = self.check_transition(mini_path, True)
        elif (mini_path[0][1] == mini_path[1][1]):
            wall_value = self.check_wall_around(mini_path, False)
            cleaned_value = self.check_cleaned_cells_around(mini_path, False)
            transition_value = self.check_transition(mini_path, False)

        edges = self.check_edges(mini_path)

        if self.previous_position != None:
            if self.mini_path_direction(mini_path):
                direction = 1

        if(debug):
            if wall_value:
                print('IDE UZ ZID')
            if cleaned_value:
                print('IDE UZ OCISCENO')
            if direction:
                print('IDE PRAVOCRTNOOOO')
            if edges:
                print('uz rubove' + str(edges))
            if bad_turning:
                print('BAD TURNING?')
            print("Udaljenost koju je robot prosao " + str(self.mini_path_distance(mini_path)))
            print("Broj uzastopnih neocisceno " + str(uncleaned_koef*self.mini_path_consecutive_uncleaned_cells(mini_path)))
            #print("Broj ukupno neociscenih " + str(c*self.mini_path_uncleaned_cells(mini_path)))
            print("Razlika pocetne i svih pozicija " + str(sum_distance_koef*self.mini_path_sum_distance(mini_path)))
        return (distance_koef * abs(self.mini_path_distance(mini_path)-5) + uncleaned_koef*self.mini_path_consecutive_uncleaned_cells(mini_path)
                 + sum_distance_koef*self.mini_path_sum_distance(mini_path) +
                 direction_koef*direction + wall_koef*wall_value + cleaned_koef*cleaned_value + transition_koef*transition_value + sqrt(edges_koef*edges) + bad_turning_koef*bad_turning)


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
                # remove position y from shared neighbours of x and z
                intersection.remove(y)
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
        index = choice(range(2, len(mini_path))) # choosing position to mutate
        while len(genes_for_mutation[index-1]) < 1: # if set is empty
            index = choice(range(1, len(mini_path)))

        new_gene = sample(genes_for_mutation[index-1], 1)[0] # choosing position that replaces previously chosen

        mini_path[index] = new_gene


###################################################

    def print_population(self, population):

        s = [[str(e) for e in row] for row in population]
        lens = [max(map(len, col)) for col in zip(*s)]
        fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
        table = [fmt.format(*row) for row in s]
        # print  ('\n'.join(table))

        # for x in population:
                # print (self.mini_path_distance(x), self.mini_path_uncleaned_cells(x), self.mini_path_sum_distance(x))

    def update_mutable_genes(self, mini_path, index_of_position_to_update, genes_for_mutation):
        # TODO: bolje to napravit
        neighbours_of_previous = self.get_available_positions(mini_path[index_of_position_to_update-1])
        neighbours_of_next = self.get_available_positions(mini_path[index_of_position_to_update+1])
        intersection = neighbours_of_previous.intersection(neighbours_of_next)
        if len(intersection):
            # remove position y from shared neighbours of x and z, so that gen can not mutate into the same gene
            intersection.remove(mini_path[index_of_position_to_update])
            genes_for_mutation[index_of_position_to_update-1] = intersection


    def mutationVersion2(self, mini_path):
        genes_for_mutation = self.find_mutable_genes(mini_path)
        i = 2
        # for each gene generate random number from [0,1], if number is less than self.mutation_probability mutate gene
        while i < self.length_of_mini_path+1:
            # rand = int.from_bytes(os.urandom(8), byteorder="big") / ((1 << 64) - 1)
            rand = random()
            if rand < self.mutation_probability:
                # if there are genes that can be placed instead current one, choose one randomly
                # print(genes_for_mutation[i-1], i)
                if len(genes_for_mutation[i-1]) >= 1:
                    new_gene = sample(genes_for_mutation[i-1], 1)[0]
                    mini_path[i] = new_gene

                    """
                    there are 3 cases:
                        1. mutating last gene
                        2. mutating second last gene
                        3. mutating any other
                    depending on each case we need to change certain genes in genes_for_mutation
                    """

                    # if last gene is being mutated no changes needed
                    if(i == self.length_of_mini_path):
                        i += 1
                        continue
                    if(i == self.length_of_mini_path-1):
                    # if second last is being changed, change genes_for_mutation of the last gene
                        neighbours_of_second_last = self.get_available_positions(mini_path[i])
                        if neighbours_of_second_last.intersection(mini_path[i+1]):
                            neighbours_of_second_last.remove(mini_path[i+1])
                        genes_for_mutation[i] = neighbours_of_second_last
                    # if any other gene is being mutated change genes_for_mutation of the next one (mini_path[i+1])
                    # update genes_for_mutation na poziciji i+1  -> find nighbours of mini_path[i] and mini_path[i+2] and find intersection
                    else:
                        self.update_mutable_genes(mini_path, i+1, genes_for_mutation)
            i += 1

        return mini_path


    # TODO: sta kad su isti
    # mozda kao djecu vratit najbolja 2
    def crossover_one_point(self, parent1, parent2, Debug = False):
        if (Debug):
            print('_______________________________KRIZANJE________________________')

        new_children1 = []
        point_options = []
        # if random number is higher than crossover probability place parents directly into the new genration
        # if self.crossover_probability < int.from_bytes(os.urandom(8), byteorder="big") / ((1 << 64) - 1):
        if self.crossover_probability < random():
            if (Debug):
                print("IDU DIREKTNO")
            new_children1.extend([parent1, parent2])
            return new_children1

        # nema smisla minjat prvu poziciju jer dobijemo dva ista puta
        for point_of_crossing in range(2,6):
            if(parent2[point_of_crossing] in self.neighbours_of(parent1[point_of_crossing-1]) and
                parent1[point_of_crossing] in self.neighbours_of(parent2[point_of_crossing-1])):
                    point_options.append(point_of_crossing)

        # if there are no points for crossover return None
        if not point_options:
            if (Debug):
                print("NEMA MOGUCNOSTI KRIZANJA")
            return None

        # choosing random point of crossover
        point_of_crossing = choice(point_options)

        if (Debug):
            print('Tocka krizanja: ' + str(point_of_crossing))
            self.isprintaj_mini_path(parent1)
            self.isprintaj_mini_path(parent2)
        child1 = parent1[0:point_of_crossing]
        child2 = parent2[0:point_of_crossing]
        child1.extend(parent2[point_of_crossing:len(parent2)])
        child2.extend(parent1[point_of_crossing:len(parent1)])
        if (Debug):
            print('--------------> DJECA')
            self.isprintaj_mini_path(child1)
            self.isprintaj_mini_path(child2)
        new_children1.extend([child1, child2])
        return new_children1



    def generate_initial_population(self):
        # TODO: vidit ima li ravnih i onda izgenerirat ostale
        initial_population = self.generate_mini_paths(self.population_size, self.length_of_mini_path, self.current_position)
        return initial_population


    def isprintaj_mini_path(self, mini_path):
        print(mini_path)
        # print(" " + str(self.calculate_fitness_function(mini_path, False)) + " " + str(self.mini_path_uncleaned_cells(mini_path))
        #      + " " + str(self.mini_path_distance(mini_path)) + " " + str(self.mini_path_sum_distance(mini_path)))
        debug = deepcopy(self.discovered_space)
        for i, row in enumerate(debug):
            for j, element in enumerate(row):
                if((i,j) in mini_path):
                    debug[i][j] = str(mini_path.index((i,j)))
        for row in debug:
            print(row)
        print("Vrijednost = " + str(self.calculate_fitness_function(mini_path, self.debug)) + " Iter = " + str(self.iteracija))


### Propotionate selection ###
    def place_chromosomes_fitness_into_interval(self, current_population):
        # current population is sorted
        # TODO: sort inside this function when calculating fitness function
        dictionary_fitness_values = {}
        fitness_sum = 0
        probability = 0
        # create dictionary with indexes of mini paths as keys and theirs fitnesses as values
        # e.g.
        for index, mini_path in enumerate(current_population):
            value = self.calculate_fitness_function(mini_path)
            fitness_sum += value
            dictionary_fitness_values[index] = value
            #self.isprintaj_mini_path(mini_path)

        # scale fitness values into interval [0, 1]
        # e.g.
        for key, value in dictionary_fitness_values.items():
            probability += (value/fitness_sum)
            dictionary_fitness_values[key] = probability


        return dictionary_fitness_values


    def select_chromosome(self, dictionary_fitness_values):
        # >>> import os
        # >>> int.from_bytes(os.urandom(8), byteorder="big") / ((1 << 64) - 1)
        # probability = random()

        # generate random number from [0,1]
        probability = int.from_bytes(os.urandom(8), byteorder="big") / ((1 << 64) - 1)
        # go trough dictionary and find index of mini_path whose interval containes generated number
        for index, fitness_value in dictionary_fitness_values.items():
            if probability < fitness_value:
                return index


    def make_one_iteration(self, current_population):
        new_generation = []
        i = 0
        # sort current population -> highest fitness first
        current_population = sorted(current_population, key = self.calculate_fitness_function, reverse=True)
        # place two best chromosomes directly into the new generation
        new_generation.extend(current_population[:2])

        # del current_population[:2]

        # TODO: sort inside place_chromosomes_fitness_into_interval ?
        dictionary_fitness_values = self.place_chromosomes_fitness_into_interval(current_population)

        while i < (int(self.population_size/2) - 1):
            # selecting parents
            parent_one = current_population[self.select_chromosome(dictionary_fitness_values)]
            parent_two = current_population[self.select_chromosome(dictionary_fitness_values)]

            # crossover
            new_children = self.crossover_one_point(parent_one, parent_two, self.debug)
            if(new_children != None):
                # if crossover was successful mutate children
                self.mutationVersion2(new_children[0])
                self.mutationVersion2(new_children[1])
                # add children to the new generation
                new_generation.extend(new_children)
                i += 1

        return new_generation



    def next_move(self):
        # generate initial population

        current_population = self.generate_initial_population()
        print('////////////////////////////////   NOVI POTEZ   /////////////////////////////////')
        self.iteracija = 0

        for i in range(self.number_of_iterations):
            current_population = self.make_one_iteration(current_population)
            # current_population = sorted(current_population, key = self.calculate_fitness_function, reverse=True)
            if(self.debug):
                for mini_path in current_population:
                    self.isprintaj_mini_path(mini_path)

            self.iteracija += 1

        current_population = sorted(current_population, key = self.calculate_fitness_function, reverse=True)

        # for mini_path in current_population:
        #     self.isprintaj_mini_path(mini_path)

        # first position from the best mini_path from the last generation
        next_move = current_population[0][1]
        # direction is difference between next and current possition
        direction = (next_move[0] - self.current_position[0], next_move[1] - self.current_position[1])

        return direction
