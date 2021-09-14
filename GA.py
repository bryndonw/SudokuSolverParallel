import numpy as np
import random
from PuzzleImporter import PuzzleImporter
from RuleCheck import RuleCheck

class GA():
    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.population = GA.createPop(self, self.puzzle)


    def createPop(self, puzzle):
        pop = 1         #TUNE
        population = []
        for i in range(pop):
            solution = []
            PuzzleImporter.PrintPuzzle(puzzle)
            for i in range(len(puzzle)):
                row = []
                for j in range(len(puzzle[i])):
                    if puzzle[i][j] == "?":
                        row.append(str(random.randint(1,9)))
                    else:
                        row.append("?")
                solution.append(row)
            fit = self.fitness(puzzle, solution)
            population.append(solution)
        return population

    def fitness(self, puzzle, solution):
        full = RuleCheck.fullSolution(RuleCheck, puzzle, solution)

