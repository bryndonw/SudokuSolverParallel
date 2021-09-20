from PuzzleImporter import PuzzleImporter
from GA import GA
from SimulatedAnnealing import simulated_annealing


def main():
    """"Puzzle Selection"""
    puzzle = PuzzleImporter('Data/Easy-P2.csv')
    array = puzzle.open()

    """BackTracking Algorithm Run"""


    """Genetic Algorithm Run"""
    GA(array)

    """"Simulated Annealing Algorithm Run"""
    empty_puzzle, puzzle = PuzzleImporter.puzzleFormating(array)
    PuzzleImporter.PrintPuzzle(simulated_annealing(empty_puzzle, puzzle))


if __name__ == '__main__':
    main()

