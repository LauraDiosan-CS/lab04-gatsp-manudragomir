class Consola:
    def __init__(self, serv):
        self.__serv = serv

    def run(self):
        menu = "Fisier de intrare al grafului, fisier de output"
        print(menu)
        args = input().split()
        self.__serv.compute(args[0], args[1])
        print("SOLVED")
