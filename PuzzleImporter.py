import numpy as np
class PuzzleImporter():
    def __init__(self, file):
        self.file = file

    def open(self):
        file = open(self.file, 'r')  # opens file
        print(file)
        numpy_array = np.loadtxt(file, dtype= str, delimiter=",")
        numpy_array[0][0] = numpy_array[0][0][-1]
        return numpy_array