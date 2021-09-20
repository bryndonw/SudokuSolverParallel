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
        """Kieran Ringel
        Generates a population of solutions, the blanks in the puzzle are filled with random values"""
        pop = 100         #TUNE
        population = []
        fitness = []
        for i in range(pop):    #to get population size
            solution = []
            for i in range(len(puzzle)):    #iterates over rows
                row = []
                for j in range(len(puzzle[i])):     #iterates over values in row
                    if puzzle[i][j] == "?":         #if it is a blank
                        row.append(str(random.randint(1,9)))    #generate random value
                    else:   #if the value is given as a part of the puzzle
                        row.append("?") #store that as a empty spot in the solution
                solution.append(row)
            fit = self.calcfitness(puzzle, solution)
            population.append(solution)
            fitness.append(fit)
        return population, fitness

    def calcfitness(self, puzzle, solution):
        """Kieran Ringel
        Creates a fitness function for each possible solution that will equal 1 when a solution is found.
        Essentially gets % of unique values row, column and grid wise, each of these %s are averages across the puzzle.
        The row, column and grid fitness are multiplied together to get the overall fitness."""
        full = RuleCheck.fullSolution(RuleCheck, puzzle, solution)  #combine puzzle and solution to get full solution
        columns = 0
        rows = 0
        boxes = 0
        for row in full:    #iterate through rows
            rows += len(set(row))/9 #get % of row that is unique
        rows = rows/9   #average that percentage
        transposed = [[row[i] for row in full] for i in range(len(full[0]))]    #make rows of each column
        for col in transposed:  #iterate through columns
            columns += len(set(col))/9  #get % of column that is unique
        columns = columns/9 #average that percentage
        squares = np.array(full).reshape((3, 3, 3, 3)).transpose((0, 2, 1, 3)).reshape((9, 9))  #make rows of each 3x3 box
        for square in squares:  #iterate through 3x3 grids
            boxes += len(set(square))/9     #get % of grid that is unique
        boxes = boxes/9     #average that %
        return columns*rows*boxes   #return multiplied fitnesses, correct solution will equal one

    def evolve(self, population, fitness):
        """Kieran Ringel
        While there is not a solution continue to create new generations through selection, crossover and mutation"""
        generations = 0
        while (max(fitness) < 1) and (generations < 100000): #while there is not a solution
            newpop = []
            newfitness = []
            generations += 1        #to count generations
            while len(newpop) < len(population):    #generational replacement
                parents = self.selection(population, fitness)
                child = self.crossover(parents)
                newchild = self.mutation(child)
                childfitness = self.calcfitness(self.puzzle, newchild)
                newpop.append(newchild)     #add new child to population
                newfitness.append(childfitness)     #add corresponding fitness to population
            population = newpop     #generational replacement
            fitness = newfitness
        PuzzleImporter.PrintPuzzle(self.puzzle)
        PuzzleImporter.PrintPuzzle(population[fitness.index(max(fitness))])
        PuzzleImporter.PrintPuzzle(RuleCheck.fullSolution(RuleCheck, self.puzzle, population[fitness.index(max(fitness))]))
        print(generations)

    def selection(self, population, fitness):
        """Kieran Ringel
        Tournament selection is used. A tournament is made by selecting the tournament size number of members from
        the fitness list. The maximum fitness in that list is then returned. The solution correlating to that fitness is then
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
        for row in range(len(parents[0])):  #iterates over rows
            newrow = []
            for val in range(len(parents[0][row])):     #iterates over values in row
                choice = random.randint(0, 1)  # randomly selects which parent to take that value from
                newrow.append(parents[choice][row][val])    #create new row from parent
            child.append(newrow)    #create new child that is mix of parents
        return child

    def mutation(self, child):
        """Kieran Ringel
        A random location in the Sudoku puzzle is chosen to be mutated, the current value is replaced with a
        randomly selected number between 1 and 9. This is done the nummutations times."""
        nummutations = 3       #TUNE
        for i in range(nummutations):   #to mutate multiple times
            num  = random.randint(0,80) #get location on board
            row = num // 9              #get row location
            col = num % 9               #get column location
            while(child[row][col] == "?"):  #if the value cannot be altered (part of original puzzle)
                num = random.randint(0, 80) #get new location on board
                row = num // 9
                col = num % 9
            child[row][col] = str(random.randint(1,9))  #replace mutation location with randomly generated value
        return child





