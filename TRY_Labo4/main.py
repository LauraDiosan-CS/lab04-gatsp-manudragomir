from random import seed

import numpy as np

from model.chromosome import Chromosome
from model.graf import Graf
from repository.repository import Repository
from service.service import Service
from ui.consola import Consola


def main():
    repo = Repository()
    serv = Service(repo)
    cons = Consola(serv)
    cons.run()

main()