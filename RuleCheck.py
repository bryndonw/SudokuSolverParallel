from PuzzleImporter import PuzzleImporter
class RuleCheck():
    def __init__(self):
        pass

    def fullSolution(self, puzzle, solution):
        """Kieran Ringel
        Combines the original puzzle and the solution into one grid"""
        full = []
        for i in range(len(puzzle)):    #iterate over rows
            row = []
            for j in range(len(puzzle[i])): #iterate over values
                if puzzle[i][j] != '?':     #if it was not a blank in the original puzzle add it to full solution
                    row.append(puzzle[i][j])
                else:   #otherwise add solution to full solution
                    row.append(solution[i][j])
            full.append(row)
        return full