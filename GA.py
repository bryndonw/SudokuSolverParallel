import numpy as np
import random
from PuzzleImporter import PuzzleImporter
from RuleCheck import RuleCheck

class GA():
    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.population, self.fitness = GA.createPop(self, self.puzzle)
        self.result = GA.evolve(self, self.population, self.fitness)


    def createPop(self, puzzle):
        pop = 100         #TUNE
        population = []
        fitness = []
        for i in range(pop):
            solution = []
            for i in range(len(puzzle)):
                row = []
                for j in range(len(puzzle[i])):
                    if puzzle[i][j] == "?":
                        row.append(str(random.randint(1,9)))
                    else:
                        row.append("?")
                solution.append(row)
            fit = self.calcfitness(puzzle, solution)
            population.append(solution)
            fitness.append(fit)
        return population, fitness

    def calcfitness(self, puzzle, solution):
        full = RuleCheck.fullSolution(RuleCheck, puzzle, solution)
        columns = 0
        rows = 0
        boxes = 0
        for row in full:
            rows += len(set(row))/9
        rows = rows/9
        transposed = [[row[i] for row in full] for i in range(len(full[0]))]
        for col in transposed:
            columns += len(set(col))/9
        columns = columns/9
        squares = np.array(full).reshape((3, 3, 3, 3)).transpose((0, 2, 1, 3)).reshape((9, 9))
        for square in squares:
            boxes += len(set(square))/9
        boxes = boxes/9
        return columns*rows*boxes

    def evolve(self, population, fitness):
        generations = 0
        while max(fitness) < 1:
            newpop = []
            newfitness = []
            generations += 1
            while len(newpop) < len(population):    #generational replacement
                parents = self.selection(population, fitness)
                child = self.crossover(parents)
                newchild = self.mutation(child)
                childfitness = self.calcfitness(self.puzzle, newchild)
                newpop.append(newchild)
                newfitness.append(childfitness)
            population = newpop
            fitness = newfitness
        PuzzleImporter.PrintPuzzle(self.puzzle)
        PuzzleImporter.PrintPuzzle(population[fitness.index(max(fitness))])
        PuzzleImporter.PrintPuzzle(RuleCheck.fullSolution(RuleCheck, self.puzzle, population[fitness.index(max(fitness))]))
        print(generations)

    def selection(self, population, fitness):
        """Kieran Ringel
        Tournament selection is used. A tournament is made by selecting the tournament size number of members from
        the loss list. The minimum loss in that list is then returned. The NN correlating to that loss is then
        added to the list of parents. Here 2 parents are used because that is what was discussed in class and
        it is what we are biologically familiar with."""
        tournamentsize = 30  #TUNE
        parents = []
        for parent in range(2):     #gets 2 parents as we typically think of
            tournament = random.sample(fitness, tournamentsize)  #selects random fitness that correlated to puzzle to fill tournament
            maxfit = max(tournament)         #gets greatest fitness
            parents.append(population[fitness.index(maxfit)]) #add the parent that correlated to that smallest error
        return(parents) #returns list of 2 parents

    def crossover(self, parents):
        """Kieran Ringel
       Uniform cross over is performed to create a child by going through all of the weights in this NN structure
       and "flipping a coin"/ selecting one of the 2 parents to provide each weight. A child is returned.
       """
        child = []
        for row in range(len(parents[0])):
            newrow = []
            for val in range(len(parents[0][row])):
                choice = random.randint(0, 1)  # randomly selects which parent to take that weight from
                newrow.append(parents[choice][row][val])
            child.append(newrow)
        return child

    def mutation(self, child):
        nummutations = 1       #TUNE
        for i in range(nummutations):
            num  = random.randint(0,80)
            row = num // 9
            col = num % 9
            while(child[row][col] == "?"):
                num = random.randint(0, 80)
                row = num // 9
                col = num % 9
            child[row][col] = random.randint(1,9)
        return child





