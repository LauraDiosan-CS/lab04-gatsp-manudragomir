from model.graf import Graf


class Repository:
    def __init__(self):
        pass

    # scriem rezultatul
    def print_data(self, current_solution, cost, filename, mode):
        with open(filename, mode) as f:
            f.write(str(len(current_solution)) + "\n")
            for x in range(len(current_solution)):
                f.write(str(current_solution[x] + 1))
                if x < len(current_solution) - 1:
                    f.write(',')
            f.write("\n")
            f.write(str(cost) + "\n")

    def read_data(self, filename):
        adj_matrix = []
        with open(filename, 'r') as f:
            number_of_vertices = int(f.readline().strip())
            for i in range(number_of_vertices):
                nbrs = f.readline().strip().split(',')
                nbrs = list(map(int, nbrs))
                adj_matrix.append(nbrs)
        g = Graf(number_of_vertices, adj_matrix)
        return g

    def read_again(self, filename):
        with open(filename, 'r') as f:
            args = f.readline().strip().split()
            n, m = int(args[0]), int(args[1])
            adj_matrix = [[9999999999 for _ in range(m)] for _ in range(n)]
            for i in range(m):
                arg = f.readline().strip().split()
                n1 = int(arg[0])
                n2 = int(arg[1])
                c = int(arg[2])
                adj_matrix[n1][n2] = c
        for i in range(n):
            adj_matrix[i][i] = 0
        g = Graf(n, adj_matrix)
        return g


