from Backtracking import Backtracking
from PuzzleImporter import PuzzleImporter
from ThreadBacktrack import ThreadBacktrack
from GA import GA
from SimulatedAnnealing import simulated_annealing


def main():
    """"Puzzle Selection"""
    puzzle = PuzzleImporter('Data/Evil-P2.csv')
    array = puzzle.open()

    """BackTracking Algorithm Run"""
    # print("Simple backtracking with static heuristics: ")
    # Backtracking(array, 0)
    # print("Backtracking with forward checking and random heuristics: ")
    # Backtracking(array, 1)
    print("Backtracking with arc-consistency and minimum remaining value heuristics: ")
    ThreadBacktrack(array)
    # Backtracking(array, 2)


    """Genetic Algorithm Run"""
    #GA(array)

    """"Simulated Annealing Algorithm Run"""
  #  empty_puzzle, puzzle = PuzzleImporter.puzzleFormating(array)
   # PuzzleImporter.PrintPuzzle(simulated_annealing(empty_puzzle, puzzle))


if __name__ == '__main__':
    main()

