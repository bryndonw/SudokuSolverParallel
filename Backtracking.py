import numpy as np
from PuzzleImporter import PuzzleImporter
from RuleCheck import RuleCheck
import random

class Backtracking:

    def __init__(self, puzzle, search_type):
        self.count = 0
        assignment = np.copy(puzzle)
        for i in range(len(puzzle)):
            for j in range(len(puzzle[i])):
                if puzzle[i][j] != '?':
                    assignment[i][j] = '0'

        if self.backtrack(puzzle, assignment, search_type):
            print(self.count)
        else:
            print("Cannot solve")

    # Tests puzzle to see if it has any more unassigned spaces
    # Returns True if the puzzle is incomplete
    @staticmethod
    def incomplete_puzzle(puzzle, assignment):
        full = RuleCheck.fullSolution(RuleCheck, puzzle, assignment)
        for i in range(len(full)):
            for j in range(len(full[i])):
                if full[i][j] == '?':
                    return True
        return False

    def backtrack(self, puzzle, assignment, search_type):
        self.count += 1
        if not self.incomplete_puzzle(puzzle, assignment):
            full = RuleCheck.fullSolution(RuleCheck, puzzle, assignment)
            PuzzleImporter.PrintPuzzle(full)
            return True

        full = RuleCheck.fullSolution(RuleCheck, puzzle, assignment)
        new_var = self.select_unassigned_variable(full, search_type)

        list_of_potential_values = self.order_domain_values(search_type, full)

        for p in range(9):
            if self.check_rules(full, new_var[0], new_var[1], list_of_potential_values[p]):
                assignment[new_var[0]][new_var[1]] = list_of_potential_values[p]
                inferences = self.inference(puzzle, assignment, new_var[0], new_var[1], search_type)
                if inferences:
                    result = self.backtrack(puzzle, assignment, search_type)
                    if result:
                        return result
                assignment[new_var[0]][new_var[1]] = '?'

        return False


    # search_type determines heuristic to select variable
    def select_unassigned_variable(self, full, search_type):
        if search_type == 0:
            empty_var = []
            for i in range(len(full)):
                for j in range(len(full[i])):
                    if full[i][j] == '?':
                        empty_var.append(i)
                        empty_var.append(j)
                        return empty_var
        elif search_type == 1:
            return self.minimum_remaining_values(full)
        else:
            # TODO: add heuristic here
            empty_var = []
            for i in range(len(full)):
                for j in range(len(full[i])):
                    if full[i][j] == '?':
                        empty_var.append(i)
                        empty_var.append(j)
                        return empty_var


    # Returns an ordered list of values to try
    @staticmethod
    def order_domain_values(search_type, full):
        if search_type == 0:
            list_potential = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        elif search_type == 1:
            list_potential = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
            random.shuffle(list_potential)
        else:
            list_potential = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        return list_potential

    def minimum_remaining_values(self, full):
        all_vars = []
        ordered_vars = []

        domain = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        for i in range(9):
            for j in range(9):
                if full[i][j] == '?':
                    count = 0
                    for p in range(len(domain)):
                        if self.check_rules(full, i, j, domain[p]):
                            count += 1
                    all_vars.append([i, j, count])
        for j in range(9):
            for i in range(len(all_vars)):
                if all_vars[i][2] == j:
                    ordered_vars.append(all_vars[i])
        return ordered_vars.pop(0)


    # If search_type is
    #   1, it returns True because we are using simple backtracking
    #   2, it calls forward checking
    #   3, it calls arc-consistency
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
            return self.arc_consistency(puzzle, assignment)

    # Takes an unassigned variable and adds it and every other unassigned variable to a queue
    def find_vars_for_queue(self, puzzle, assignment, variable):
        full = RuleCheck.fullSolution(RuleCheck, puzzle, assignment)
        queue = []
        pair = []
        for i in range(9):
            for j in range(9):
                if variable[0] != i or variable[1] != j:
                    if full[i][j] == '?':
                        pair.append(variable[0])
                        pair.append(variable[1])
                        pair.append(i)
                        pair.append(j)
                        queue.append(pair)
                        pair = []
        return queue

    # Takes in the current variable and finds the next unassigned variable
    # Returns a queue of all of the variable pairs
    def next_empty_var(self, puzzle, assignment, variable):
        full = RuleCheck.fullSolution(RuleCheck, puzzle, assignment)
        valid = False
        while not valid:
            if variable[0] == 8 and variable[1] == 8:
                return
            if variable[1] < 8:
                variable[1] += 1
            elif variable[0] < 8:
                variable[0] += 1
                variable[1] = 0
            if full[variable[0]][variable[1]] == '?':
                return variable

    # Creates a queue of all of the arcs in the puzzle
    def create_queue(self, puzzle, assignment):
        full = RuleCheck.fullSolution(RuleCheck, puzzle, assignment)
        variable = self.select_unassigned_variable(full, 0)
        queue = []
        while variable is not None:
            new_queue = self.find_vars_for_queue(puzzle, assignment, variable)
            if new_queue:
                queue.append(new_queue)
            variable = self.next_empty_var(puzzle, assignment, variable)
        reform_queue = []
        for val in queue:
            for elem in val:
                reform_queue.append(elem)
        return reform_queue

    #
    def arc_consistency(self, puzzle, assignment):
        full = RuleCheck.fullSolution(RuleCheck, puzzle, assignment)

        queue = self.create_queue(puzzle, assignment)
        while len(queue) > 0:
            variable = queue.pop(0)
            if not self.check_domain(full, variable):
                return False
        return True

    # Checks the domains of each variable pair
    # to make sure there exists at least one value that is viable for current puzzle
    # If the two variables are not arc-consistent, returns false
    def check_domain(self, full, variable):
        list_potential1 = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        list_potential2 = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        actual_list1 = []
        actual_list2 = []
        for i in range(9):
            if self.check_rules(full, variable[0], variable[1], list_potential1[i]):
                full[variable[0]][variable[1]] = list_potential1[i]
                for j in range(9):
                    if self.check_rules(full, variable[2], variable[3], list_potential2[j]):
                        actual_list1.append(list_potential1[i])
                        actual_list2.append(list_potential2[j])
                full[variable[0]][variable[1]] = '?'

        if len(actual_list1) > 0 and len(actual_list2) > 0:
            return True
        else:
            return False


    # Returns true if the new variable can be added without violating any constraints
    def check_rules(self, full, i, j, new_val):
        if self.col_check(full, j, new_val) and self.row_check(full, i, new_val) and self.square_check(full, i, j, new_val):
            return True
        else:
            return False

    # checks to make sure every variable has the potential to be assigned
    # If not, returns False
    def forward_checking(self, puzzle, assignment, i, j):
        full = RuleCheck.fullSolution(RuleCheck, puzzle, assignment)
        list_potential = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        actual_list = []
        for r in range(len(list_potential)):
            if self.check_rules(full, i, j, list_potential[r]):
                actual_list.append(list_potential[r])
        if len(actual_list) == 0:
            return False
        return True

    # Returns true if the new variable doesn't violate the column constraint
    @staticmethod
    def col_check(full, j, new_val):
        for i in range(9):
            if full[i][j] == new_val:
                return False
        return True

    # Returns true if the new variable doesn't violate the row constraint
    @staticmethod
    def row_check(full, i, new_val):
        for j in range(9):
            if full[i][j] == new_val:
                return False
        return True

    # Returns true if the new variable doesn't violate the 3x3 constraint
    @staticmethod
    def square_check(full, i, j, new_val):
        start_row = i - i % 3
        start_col = j - j % 3

        for p in range(3):
            for k in range(3):
                if full[p + start_row][k + start_col] == new_val:
                    return False
        return True
