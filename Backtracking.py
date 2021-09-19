import numpy as np
from PuzzleImporter import PuzzleImporter
from RuleCheck import RuleCheck

class Backtracking:

    def __init__(self, puzzle, search_type):
        self.count = 0
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
        PuzzleImporter.PrintPuzzle(full)
        return False

    def backtrack(self, puzzle, assignment, search_type):
        if not self.incomplete_puzzle(puzzle, assignment):
            print(self.count)
            return True

        new_var = self.select_unassigned_variable(puzzle, assignment)
        list_of_potential_values = self.order_domain_values(puzzle, assignment, new_var[0], new_var[1])
        for p in range(9):
            if self.check_rules(puzzle, assignment, new_var[0], new_var[1], list_of_potential_values[p]):
                assignment[new_var[0]][new_var[1]] = list_of_potential_values[p]
                # TODO: inference (forward checking and arc-consistency)
                inferences = self.inference(puzzle, assignment, new_var[0], new_var[1], search_type)
                if inferences:
                    result = self.backtrack(puzzle, assignment, search_type)

                    if result:
                        return result
                assignment[new_var[0]][new_var[1]] = '?'
        self.count += 1
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
 # gotta check each unassigned variable, see if it has any possible moves with the current assignment!
    def inference(self, puzzle, assignment, xi, xj, search_type):
        if search_type == 0:
            return True
        elif search_type == 1:
            for p in range(9):
                for k in range(9):
                    if assignment[p][k] == '?':
                        result = self.forward_checking(puzzle, assignment, p, k)
                        if not result:
                            return result
            return True
        else:
            self.arc_consistency()

    def arc_consistency(self):
        # TODO: HELL YEAH
        print()

    def check_rules(self, puzzle, assignment, i, j, new_val):
        if self.col_check(puzzle, assignment, j, new_val) and self.row_check(puzzle, assignment, i, new_val) and self.square_check(puzzle, assignment, i, j, new_val):
            return True
        else:
            return False

    # checks to make sure every variable has the potential to be assigned, if not it fails
    def forward_checking(self, puzzle, assignment, i, j):
        # TODO: self.count += 1 Do I COUNT HERE????
        list_potential = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        actual_list = []
        for r in range(len(list_potential)):
            if self.check_rules(puzzle, assignment, i, j, list_potential[r]):
                actual_list.append(list_potential[r])
        if len(actual_list) == 0:
            return False
        return True


    @staticmethod
    def col_check(puzzle, assignment, j, new_val):
        for i in range(9):
            if (puzzle[i][j] == new_val) or (assignment[i][j] == new_val):
                return False
        return True

    @staticmethod
    def row_check(puzzle, assignment, i, new_val):
        for j in range(9):
            if (puzzle[i][j] == new_val) or (assignment[i][j] == new_val):
                return False
        return True

    @staticmethod
    def square_check(puzzle, assignment, i, j, new_val):
        start_row = i - i % 3
        start_col = j - j % 3

        full = RuleCheck.fullSolution(RuleCheck, puzzle, assignment)

        for p in range(3):
            for k in range(3):
                if full[p + start_row][k + start_col] == new_val:
                    return False
        return True
