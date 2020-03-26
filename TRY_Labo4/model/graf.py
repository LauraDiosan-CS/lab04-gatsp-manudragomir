import networkx as nx


class Graf:
    def __init__(self, number_of_nodes, adj_matrix):
        self.__number_of_nodes = number_of_nodes
        self.__adj_matrix = adj_matrix

    def get_nodes_number(self):
        return self.__number_of_nodes

    def get_cost(self, node1, node2):
        return self.__adj_matrix[node1][node2]

    def get_cost_edge(self, edge):
        return self.__adj_matrix[edge[0]][edge[1]]

    def get_adj_matrix(self):
        return self.__adj_matrix


