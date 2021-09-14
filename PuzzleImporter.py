import numpy as np
class PuzzleImporter():
    def __init__(self, file):
        self.file = file

    def open(self):
        file = open(self.file, 'r')  # opens file
        numpy_array = np.loadtxt(file, dtype= str, delimiter=",")
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