from PuzzleImporter import PuzzleImporter
from SimulatedAnnealing import FixedValues
def main():
    puzzle = PuzzleImporter('Data/Easy-P4.csv')
    array = puzzle.open()


    PrintPuzzle(array)


def PrintPuzzle(puzzle):
    print("\n")
    for i in range(len(puzzle)):
        line = ""
        if i == 3 or i == 6:
            print("---------------------")
        for j in range(len(puzzle[i])):
            if j == 3 or j == 6:
                line += "| "
            line += str(puzzle[i,j])+" "
        print(line)


main()
# Bryndon can push

