from PuzzleImporter import PuzzleImporter
class RuleCheck():
    def __init__(self):
        pass

    def fullSolution(self, puzzle, solution):
        full = []
        for i in range(len(puzzle)):
            row = []
            for j in range(len(puzzle[i])):
                if puzzle[i][j] != '?':
                    row.append(puzzle[i][j])
                else:
                    row.append(solution[i][j])
            full.append(row)
        return full