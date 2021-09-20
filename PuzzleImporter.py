import numpy as np
from SimulatedAnnealing import fill_puzzle


class PuzzleImporter():
    def __init__(self, file):
        self.file = file

    def open(self):
        file = open(self.file, 'r')  # opens file
        numpy_array = np.loadtxt(file, dtype=str, delimiter=",")
        numpy_array[0][0] = numpy_array[0][0][-1]
        return numpy_array

    def PrintPuzzle(puzzle):
        print("\n")
        for i in range(len(puzzle)):
            line = ""
            if i == 3 or i == 6:
                print("---------------------")
            for j in range(len(puzzle[i])):
                if j == 3 or j == 6:
                    line += "| "
                line += str(puzzle[i][j]) + " "
            print(line)

    def puzzle_formating(array):
        for i in range(0, 9):
            for j in range(0, 9):
                if array[i, j] == '?':
                    array[i, j] = 0

        puzzle = np.zeros((9, 9), dtype=int)
        for i in range(9):
            for j in range(9):
                puzzle[i][j] = array[i][j]

        empty_puzzle = puzzle.copy()

        for i in range(0, 9)[::3]:
            for j in range(0, 9)[::3]:
                fill_puzzle(i, j, puzzle)

        return empty_puzzle, puzzle
