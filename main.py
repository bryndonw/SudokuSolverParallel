from PuzzleImporter import PuzzleImporter
from GA import GA
from SimulatedAnnealing import simulated_annealing


def main():
    """"Puzzle Selection"""
    puzzle = PuzzleImporter('Data/Med-P1.csv')
    array = puzzle.open()

    """BackTracking Algorithm Run"""
    Backtracking(array, 0)  #simple
    Backtracking(array, 1)  #forward checking
    Backtracking(array, 2)  #arc consistency


    """Genetic Algorithm Run"""
    GA(array)

    """"Simulated Annealing Algorithm Run"""
    #empty_puzzle, puzzle = PuzzleImporter.puzzleFormating(array)
    #PuzzleImporter.PrintPuzzle(simulated_annealing(empty_puzzle, puzzle))


if __name__ == '__main__':
    main()

