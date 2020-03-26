from model.chromosome import Chromosome

import random


class GeneticAlgorithm:
    def __init__(self, graf, probl_param=None, params=None):
        self.__probl_param = probl_param
        self.__params = params
        self.__graf = graf
        self.__population = []
        self.initialisation()

    def get_population(self):
        return self.__population

    def initialisation(self):
        for i in range(0, self.__probl_param["pop_size"]):
            c = Chromosome(self.__graf, self.__params)
            c.define_first_generation()
            c.set_fitness(self.__probl_param['function'](c.get_genotype(), self.__graf))
            self.__population.append(c)

    def bestChromosome(self):
        best = self.__population[0]
        for c in self.__population:
            if c.get_fitness() < best.get_fitness():
                best = c
        return best

    def worstChromosome(self):
        best = self.__population[0]
        index = 0
        for i in range(len(self.__population)):
            c = self.__population[i]
            if c.get_fitness() > best.get_fitness():
                best = c
                index = i
        return best, index

    def __better_selection(self):
        crom1 = random.choice(self.__population)
        crom2 = random.choice(self.__population)
        if crom1.get_fitness() < crom2.get_fitness():
            return crom1
        else:
            return crom2

    def __tournament_selection(self):
        return self.__better_selection(), self.__better_selection()

    def __roulette_selection(self):
        sum = 0
        for candidate in self.__population:
            sum += candidate.get_fitness()
        fitnesses = [(candidate.get_fitness() / sum) for candidate in self.__population]
        return tuple(random.choices(self.__population, weights=fitnesses, k=2))

    def __rank_selection(self):
        pc = self.__probl_param["start_probability"]
        sorted_list = sorted(self.__population, key=lambda x: x.get_fitness())
        heavy_fintesses = [pc]
        for index_crom in range(1, len(sorted_list) - 1):
            heavy_fintesses.append(heavy_fintesses[index_crom - 1] * (1 - pc))
        heavy_fintesses.append(1 - pc)
        return tuple(random.choices(self.__population, weights=heavy_fintesses, k=2))

    def __another_selection(self):
        generations = self.__probl_param["iterations"]
        fitnesses = [candidate.get_fitness() / (generations + 1 - candidate.get_generation())
                     for candidate in self.__population]
        return tuple(random.choices(self.__population, weights=fitnesses, k=2))

    def __best_worst_selection(self):
        return self.bestChromosome(), self.worstChromosome()[0]

    def selection(self):
        if self.__probl_param["selection"] == "rank":
            return self.__rank_selection()
        elif self.__probl_param["selection"] == "roulette":
            return self.__roulette_selection()
        elif self.__probl_param["selection"] == "tournament":
            return self.__tournament_selection()
        elif self.__probl_param["selection"] == "selection":
            return self.__another_selection()
        else:
            return self.__best_worst_selection()

    def generate_steady_state(self):
        it = 0
        while it < self.__probl_param["iterations"]:
            it += 1
            for i in range(self.__probl_param["pop_size"]):
                (p1, p2) = self.selection()
                off1, off2 = p1.crossover(p2)
                off1.mutation()
                off2.mutation()
                off1.set_fitness(self.__probl_param['function'](off1.get_genotype(), self.__graf))
                off2.set_fitness(self.__probl_param['function'](off2.get_genotype(), self.__graf))
                off = off1
                if off1.get_fitness() > off2.get_fitness():
                    off = off2
                off.set_generation(it)
                worst, index = self.worstChromosome()
                if off.get_fitness() < worst.get_fitness():
                    self.__population[index] = off

            best = self.bestChromosome()
            print("Generation " + str(it) + " " + str(best.get_fitness()))
        return self.bestChromosome()