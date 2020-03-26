from random import randint

import numpy as np

# integer representation
class Chromosome:
    def __init__(self, g, params=None):
        self.__genotype = []
        self.__fitness = 0.0
        self.__graph = g
        self.__len = self.__graph.get_nodes_number()
        self.__params = params
        self.__generation = 0

    def set_generation(self, gen=0):
        self.__generation = gen

    def get_genotype(self):
        return self.__genotype

    def set_genotype(self, new_genotype=[]):
        self.__genotype = new_genotype

    def get_fitness(self):
        return self.__fitness

    def set_fitness(self, fit=0.0):
        self.__fitness = fit

    def get_generation(self):
        return self.__generation

    def define_first_generation(self):
        self.__genotype = np.random.permutation(self.__len)
        pos1 = -1
        for i in range(len(self.__genotype)):
            if self.__genotype[i] == 0:
                pos1 = i

        self.__genotype[0], self.__genotype[pos1] = self.__genotype[pos1], self.__genotype[0]

    def __generate_random(self):
        i = j = 1
        while i == j:
            i = randint(0, self.__len - 1)
            j = randint(0, self.__len - 1)
        if i > j:
            return j, i
        return i, j

    def __compute_off1(self, i, j, genotype2):
        new_geno = [0] * self.__len
        visited = [0] * self.__len
        dict = {}
        for k in range(i, j):
            new_geno[k] = genotype2[k]
            visited[new_geno[k]] = 1
            dict[genotype2[k]] = self.__genotype[k]

        for k in range(i):
            value = self.__genotype[k]
            while visited[value] == 1:
                value = dict[value]
            new_geno[k] = value
            visited[value] = 1

        for k in range(j, self.__len):
            value = self.__genotype[k]
            while visited[value] == 1:
                value = dict[value]
            new_geno[k] = value
            visited[value] = 1
        return new_geno

    def __compute_off2(self, i, j, genotype2):
        new_geno = [0] * self.__len
        visited = [0] * self.__len
        dict = {}
        for k in range(i, j):
            new_geno[k] = self.__genotype[k]
            visited[new_geno[k]] = 1
            dict[self.__genotype[k]] = genotype2[k]

        for k in range(i):
            value = genotype2[k]
            while visited[value] == 1:
                value = dict[value]
            new_geno[k] = value
            visited[value] = 1

        for k in range(j, self.__len):
            value = genotype2[k]
            while visited[value] == 1:
                value = dict[value]
            new_geno[k] = value
            visited[value] = 1
        return new_geno

    def crossover(self, another_chromosome):
        off1 = Chromosome(self.__graph, self.__params)
        off2 = Chromosome(self.__graph, self.__params)
        i, j = self.__generate_random()
        off1.set_genotype(self.__compute_off1(i, j, another_chromosome.get_genotype()))
        off2.set_genotype(self.__compute_off2(i, j, another_chromosome.get_genotype()))
        return off1, off2

    def mutation(self):
        total_number_of_iterations = self.__params["mutation_iterations"]
        current_iterations = 0
        max_improvement = 0
        best_edge_swaps = (0, 2)
        while current_iterations < total_number_of_iterations:
            # choose edges (i, i+1) and (j, j+1)
            i = randint(0, self.__len - 1)
            j = randint(0, self.__len - 1)
            if i > j:
                i, j = j, i
            if j - i >= 2 and not (i == 0 and j == self.__len-1):
                a = self.__genotype[i]
                b = self.__genotype[i+1]
                c = self.__genotype[j]
                if j + 1 == self.__len:
                    d = 1
                else:
                    d = self.__genotype[j+1]

                edge1 = (a, b)
                edge2 = (c, d)
                new_edge1 = (a, c)
                new_edge2 = (b, d)
                curr_improvement = self.__graph.get_cost_edge(edge1) + self.__graph.get_cost_edge(edge2) -\
                        self.__graph.get_cost_edge(new_edge1) - self.__graph.get_cost_edge(new_edge2)
                if curr_improvement > max_improvement:
                    max_improvement = curr_improvement
                    best_edge_swaps = (i, j)

            current_iterations += 1
        i = best_edge_swaps[0]
        j = best_edge_swaps[1]
        self.__genotype[i + 1], self.__genotype[j] = self.__genotype[j], self.__genotype[i+1]

    def __str__(self):
        return "\nChromo: " + str(self.__genotype) + " has fit: " + str(self.__fitness)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, c):
        return self.__genotype == c.__genotype and self.__fitness == c.__fitness
