import csv

class PuzzleImporter():
    def __init__(self, file):
        self.file = file

    def open(self):
        array=[]
        with open(self.file, encoding='utf-8-sig') as csvDataFile:
            csvReader = csv.reader(csvDataFile)
            for row in csvReader:
                array.append(row)
        new_array = []
        for row in array:
            small = []
            for r in row:
                small.append(r)
            new_array.append(small)
        # print(new_array)
        return new_array
        # """Kieran Ringel
        # Opens csv and gets rid of extra letters at beginning of [0][0]"""
        # file = open(self.file, 'r')  # opens file
        #
        # numpy_array = np.loadtxt(file, dtype=str, delimiter=",")    #puts in 2d array
        # numpy_array[0][0] = numpy_array[0][0][-1]   #removes unnecessary letters
        # return numpy_array

    def PrintPuzzle(puzzle):
        """Mason Medina
        Iterates through puzzle and prints in simple to read way"""
        print("\n")
        for i in range(len(puzzle)):
            line = ""
            if i == 3 or i == 6:
                print("---------------------")  #every 3 rows print a line
            for j in range(len(puzzle[i])):
                if j == 3 or j == 6:
                    line += "| "                #every 3 columns print a divider
                line += str(puzzle[i][j]) + " "
            print(line)

    # def puzzle_formating(array):
    #     """Mason Medina
    #     Changes puzzle from char array to int array replacing ? with 0"""
    #     puzzle = []
    #     for i in range(0, 9):
    #         zero = []
    #         for j in range(0, 9):
    #             zero.append(0)
    #             if array[i, j] == '?':  #if its a ?
    #                 array[i, j] = 0     #replace with 0
    #         puzzle.append(zero)
    #
    #     # puzzle = np.zeros((9, 9), dtype=int)    #create 9x9 of 0s
    #     for i in range(9):
    #         for j in range(9):
    #             puzzle[i][j] = array[i][j]      #copy array onto puzzle
    #
    #     empty_puzzle = puzzle.copy()        #copy puzzle
    #
    #     for i in range(0, 9)[::3]:
    #         for j in range(0, 9)[::3]:
    #             fill_puzzle(i, j, puzzle)
    #
    #     return empty_puzzle, puzzle
