from PuzzleImporter import PuzzleImporter
from ThreadBacktrack import ThreadBacktrack
from NormalBacktrack import NormalBacktrack
import time


def main():
    begin = 'Data/'
    levels = ['Easy-P', 'Hard-P', 'Med-P', 'Evil-P']
    numbers = ['1', '2', '3', '4', '5']
    end = '.csv'
    puzzleNames = []
    for l in levels:
        for num in numbers:
            name = begin + l + num + end
            puzzleNames.append(name)

    # print(puzzleNames)
    aveTimeVal = 0
    aveTimeVar = 0
    aveTimeNorm = 0
    count = 0
    difficulty_level = 0
    """"Puzzle Selection"""
    for p in puzzleNames:
        puzzle = PuzzleImporter(p)
        array = puzzle.open()

        varTime, valTime = ThreadBacktrack(array).ThreadStart()

        t = time.time()
        NormalBacktrack(array, 0)

        t2 = time.time() - t
        # print("Time it took with no parallelization", t2)
        aveTimeVal += valTime
        aveTimeVar += varTime
        aveTimeNorm += t2
        count += 1
        if count == 5:
            print("\n\nAverage Time for " + levels[difficulty_level] + " Puzzles")
            print("Value Time: ", aveTimeVal/5)
            print("Variable Time: ", aveTimeVar/5)
            print("Normal Time: ", aveTimeNorm/5)
            difficulty_level += 1
            count = 0


if __name__ == '__main__':
    main()

