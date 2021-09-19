import numpy as np
import PuzzleImporter as pp
from RuleCheck import RuleCheck

class Backtracking:

    def __init__(self, puzzle, search_type):
        assignment = np.copy(puzzle)
        for i in range(len(puzzle)):
            for j in range(len(puzzle[i])):
                if puzzle[i][j] != '?':
                    assignment[i][j] = '0'

        self.backtrack(puzzle, assignment, search_type)


    @staticmethod
    def incomplete_puzzle(puzzle, assignment):
        full = RuleCheck.fullSolution(RuleCheck, puzzle, assignment)
        for i in range(len(full)):
            for j in range(len(full[i])):
                if full[i][j] == '?':
                    return True
        pp.PrintPuzzle(full)
        return False

    def backtrack(self, puzzle, assignment, search_type):
        if not self.incomplete_puzzle(puzzle, assignment):
            return True

        new_var = self.select_unassigned_variable(puzzle, assignment)
        potential_stuff = self.order_domain_values(puzzle, assignment, new_var[0], new_var[1])
        for p in range(9):
            if self.check_rules(puzzle, assignment, new_var[0], new_var[1], potential_stuff[p]):
                assignment[new_var[0]][new_var[1]] = potential_stuff[p]
                # TODO: inference (forward checking and arc-consistency)
                inferences = self.inference(puzzle, assignment, new_var[0], new_var[1], search_type)
                if inferences:
                    result = self.backtrack(puzzle, assignment, search_type)
                    if result:
                        return result
                assignment[new_var[0]][new_var[1]] = '?'
        return False

    # selects variable to be tested to see if it should be added to assignment
    # (starts with top left corner continues to the right)
    @staticmethod
    def select_unassigned_variable(puzzle, assignment):
        empty_var = []
        for i in range(len(puzzle)):
            for j in range(len(puzzle[i])):
                if puzzle[i][j] == '?' and assignment[i][j] == '?':
                    empty_var.append(i)
                    empty_var.append(j)
                    return empty_var

    # selects values to be added to see if current variable is viable
    @staticmethod
    def order_domain_values(puzzle, assignment, i, j):
        # full = RuleCheck.fullSolution(RuleCheck, puzzle, assignment)
        list_potential = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        # TODO: order these in a certain way

        return list_potential

    def inference(self, puzzle, assignment, xi, xj, search_type):
        if search_type == 0:
            return True
        elif search_type == 1:
            # TODO: forward checking
            print()
        else:
            # TODO: arc
            print()
    def check_rules(self, puzzle, assignment, i, j, new_var):
        if self.col_check(puzzle, assignment, j, new_var) and self.row_check(puzzle, assignment, i, new_var) and self.square_check(puzzle, assignment, i, j, new_var):
            return True
        else:
            return False

    @staticmethod
    def col_check(puzzle, assignment, j, new_var):
        for i in range(9):
            if (puzzle[i][j] == new_var) or (assignment[i][j] == new_var):
                return False
        return True

    @staticmethod
    def row_check(puzzle, assignment, i, new_var):
        for j in range(9):
            if (puzzle[i][j] == new_var) or (assignment[i][j] == new_var):
                return False
        return True

    @staticmethod
    def square_check(puzzle, assignment, i, j, new_var):
        start_row = i - i % 3
        start_col = j - j % 3

        full = RuleCheck.fullSolution(RuleCheck, puzzle, assignment)

        for p in range(3):
            for k in range(3):
                if full[p + start_row][k + start_col] == new_var:
                    return False
        return True
