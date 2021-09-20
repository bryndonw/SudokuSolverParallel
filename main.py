from PuzzleImporter import PuzzleImporter
from GA import GA
import numpy as np
from SimulatedAnnealing import simulated_annealing, fill_puzzle


def main():
    # Use a breakpoint in the code line below to debug your script.
    puzzle = PuzzleImporter('Data/Easy-P2.csv')
    array = puzzle.open()
    # GA(array)

    empty_puzzle, puzzle = PuzzleImporter.puzzleFormating(array)
    PuzzleImporter.PrintPuzzle(simulated_annealing(empty_puzzle,puzzle))




# Bryndon can push

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
