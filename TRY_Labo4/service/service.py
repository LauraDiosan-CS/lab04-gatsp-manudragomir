from model.genetic_algo import GeneticAlgorithm
from model.graf import Graf
import networkx as nx
import matplotlib.pyplot as plt


class Service:
    def __init__(self, repo):
        self.__repo = repo

    def compute(self, fisier_in, fisier_out):
        params_genetic = {"function": self.fitness_one, "pop_size": 150, "selection": "roulette",
                  "start_probability": 0.025, "iterations": 300}
        params_chromo = {"mutation_iterations": 50}
        graf = self.__repo.read_again(fisier_in)
        ga = GeneticAlgorithm(graf, params_genetic, params_chromo)
        ga.initialisation()
        best = ga.generate_steady_state()
        self.__repo.print_data(best.get_genotype(), best.get_fitness(), fisier_out, 'w')


    def fitness_one(self, solution, graf):
        path_cost = 0
        for i in range(len(solution) - 1):
            path_cost += graf.get_cost(solution[i], solution[i+1])
        return path_cost + graf.get_cost(solution[len(solution) - 1], solution[0])