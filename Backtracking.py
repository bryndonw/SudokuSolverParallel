import numpy as np
from PuzzleImporter import PuzzleImporter
from RuleCheck import RuleCheck
import random

class Backtracking:

    def __init__(self, puzzle, search_type):
        """ Bryndon Wilkerson
        We create an assignment array based on the problem provided.
        In assignment, a 0 indicates a constraint in puzzle and ? indicates an unassigned variable
        We call backtrack with our constraints and our unassigned variables
        If there's a solution, we print the number of steps it took
        If there isn't a solution, we print "Cannot Solve"
        """
        self.count = 0
        #
        # assignment = np.copy(puzzle)
        # for i in range(len(puzzle)):
        #     for j in range(len(puzzle[i])):
        #         if puzzle[i][j] != '?':
        #             assignment[i][j] = '0'
        #
        # PuzzleImporter.PrintPuzzle(puzzle)
        # if self.backtrack(puzzle, assignment, search_type):
        #     print(self.count)
        # else:
        #     print("Cannot solve")


    @staticmethod
    def incomplete_puzzle(puzzle, assignment):
        """ Bryndon Wilkerson
        Tests puzzle to see if it has any more unassigned spaces
        Returns True if the puzzle is incomplete
        """
        full = RuleCheck.fullSolution(RuleCheck, puzzle, assignment)
        for i in range(len(full)):
            for j in range(len(full[i])):
                if full[i][j] == '?':
                    return True
        return False

    def backtrack(self, puzzle, assignment, search_type):
        """Bryndon Wilkerson
        This recursive method takes in a set of constraints (puzzle) and our assigned variables (assignment)
        and a search type
        It iteratively checks every unassigned variable in puzzle and assigns a value to it
        If this new value fails to meet constraints, it backtracks
        Inference is where we take the search type and look further into the newly assigned variable
        and its repercussions on the rest of the unassigned variables
        """
        # If the puzzle and assignment are completed, return True
        if not self.incomplete_puzzle(puzzle, assignment):
            full = RuleCheck.fullSolution(RuleCheck, puzzle, assignment)
            PuzzleImporter.PrintPuzzle(full)
            return True


        full = RuleCheck.fullSolution(RuleCheck, puzzle, assignment)
        # We select a new variable and the heuristics depends on the search type
        new_var = self.select_unassigned_variable(full, search_type)
        # We generate a list of the potential values
        list_of_potential_values = self.order_domain_values()

        for p in range(len(list_of_potential_values)):
            if self.check_rules(full, new_var[0], new_var[1], list_of_potential_values[p]):
                # If the new value fits within the constraints, we add it to assignment
                assignment[new_var[0]][new_var[1]] = list_of_potential_values[p]
                # Since we added to assignment, we increment our count by 1
                self.count += 1

                # We send in the puzzle and the new assignment
                # and use the search_type to make an inference on whether we continue on this path
                inferences = self.inference(puzzle, assignment, search_type)
                if inferences:
                    result = self.backtrack(puzzle, assignment, search_type)
                    if result:
                        return result
                # If our inferences return false, we remove the value from assignment and try a new one
                assignment[new_var[0]][new_var[1]] = '?'
        return False

    # def backtrack(self, puzzle, assignment, search_type, new_var, possible_val):
    #     """Bryndon Wilkerson
    #     This recursive method takes in a set of constraints (puzzle) and our assigned variables (assignment)
    #     and a search type
    #     It iteratively checks every unassigned variable in puzzle and assigns a value to it
    #     If this new value fails to meet constraints, it backtracks
    #     Inference is where we take the search type and look further into the newly assigned variable
    #     and its repercussions on the rest of the unassigned variables
    #     """
    #     # If the puzzle and assignment are completed, return True
    #     if not self.incomplete_puzzle(puzzle, assignment):
    #         full = RuleCheck.fullSolution(RuleCheck, puzzle, assignment)
    #         PuzzleImporter.PrintPuzzle(full)
    #         return True
    #
    #     if self.count > 15000:
    #         return False
    #
    #     full = RuleCheck.fullSolution(RuleCheck, puzzle, assignment)
    #
    #     # We select a new variable (spot on board) and the heuristics depends on the search type
    #     # print("Variable: ", new_var)
    #
    #     # We generate a list of the potential values
    #     # list_of_potential_values = self.order_domain_values()
    #
    #     # print('list of potential values', list_of_potential_values)
    #     # for p in list_of_potential_values:
    #     if self.check_rules(full, new_var[0], new_var[1], possible_val):
    #         # print("Value added: ", list_of_potential_values[p])
    #         # If the new value fits within the constraints, we add it to assignment
    #         assignment[new_var[0]][new_var[1]] = possible_val
    #         # Since we added to assignment, we increment our count by 1
    #         self.count += 1
    #
    #         # We send in the puzzle and the new assignment
    #         # and use the search_type to make an inference on whether we continue on this path
    #         inferences = self.inference(puzzle, assignment, search_type)
    #         if inferences:
    #             result = self.backtrack2(puzzle, assignment, search_type)
    #             if result:
    #                 return result
    #         # If our inferences return false, we remove the value from assignment and try a new one
    #         assignment[new_var[0]][new_var[1]] = '?'
    #         print("Backtrack")
    #
    #     return assignment

    def select_unassigned_variable(self, full, search_type):

        """ Bryndon Wilkerson
        full is the current board that we have (it is a combination of our assigned var and the og board)
        Depending on the search_type, this will return an unassigned variable
        """

        # Static heuristic - returns the next unassigned variable
        if search_type == 0:
            empty_var = []
            for i in range(len(full)):
                for j in range(len(full[i])):
                    if full[i][j] == '?':
                        empty_var.append(i)
                        empty_var.append(j)
                        return empty_var

        # Random heuristic - returns a random unassigned variable
        elif search_type == 1:
            var_list = []
            for i in range(9):
                for j in range(9):
                    if full[i][j] == '?':
                        var_list.append([i, j])
            return random.choice(var_list)

        # minimum remaining values - returns a variable that has the smallest domain of values
        else:
            return self.minimum_remaining_values(full)

    @staticmethod
    def order_domain_values():
        """ Bryndon Wilkerson
        Returns an ordered list of values to try
        """
        list_potential = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        return list_potential

    def minimum_remaining_values(self, full):
        """ Bryndon Wilkerson
        Calculates the domain on every unassigned variable
        Returns the variable with the least amount of values that can be assigned to it
        """
        all_vars = []

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
                    # print("Number of remaining values in domain:", all_vars[i][2])
                    return all_vars[i]
        return

    def inference(self, puzzle, assignment, search_type):
        """" Bryndon Wilkerson
        Depending on search_type, this will take the current puzzle and decide whether to continue down this path
        """
        # Simple backtracking - returns true as we do not infer any more
        if search_type == 0:
            return True
        # Forward checking - returns true if the current assignment
        # doesn't cause any variable to have a domain size of 0
        elif search_type == 1:
            for p in range(9):
                for k in range(9):
                    if assignment[p][k] == '?':
                        result = self.forward_checking(puzzle, assignment, p, k)
                        if not result:
                            return result
            return True
        # Arc consistency - returns true if with the current assignment
        # every arc still has a domain size greater than 0
        else:
            return self.arc_consistency(puzzle, assignment)

    # Takes an unassigned variable and adds it and every other unassigned variable to a queue
    def find_vars_for_queue(self, puzzle, assignment, variable):
        """ Bryndon Wilkerson
        Creates arcs between this variable and every other unassigned variable in the puzzle
        Returns a queue of arcs for the current variable
        """
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
        """ Bryndon Wilkerson
        Takes in the current empty variable and returns the next unassigned variable
        """
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
        """ Bryndon Wilkerson
        Returns a queue of all of the arcs in the puzzle/assignment
        """
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


    def arc_consistency(self, puzzle, assignment):
        """ Bryndon Wilkerson
        Pops off the variable in queue and checks to make sure that it is arc-consistent
        Returns True if each variable is arc consistent with one another and
        False if an arc between 2 unassigned variables do not exist
        """
        full = RuleCheck.fullSolution(RuleCheck, puzzle, assignment)

        queue = self.create_queue(puzzle, assignment)
        # print(queue)
        while len(queue) > 0:
            variable = queue.pop(0)
            if not self.check_domain(full, variable):
                # print("Domain did not check out")
                return False
        return True

    # Checks the domains of each variable pair
    # to make sure there exists at least one value that is viable for current puzzle
    # If the two variables are not arc-consistent, returns false
    def check_domain(self, full, variable):
        """ Bryndon Wilkerson
        Checks the domains of each variable pair
        Makes sure there exists at least one value in the domain for the pair of variables
        If there isn't, the variables are not arc-consistent and it returns false
        """
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
        """ Bryndon Wilkerson
        Returns true if the new variable can be added without violating any constraints
        """
        if self.col_check(full, j, new_val) and self.row_check(full, i, new_val) and self.square_check(full, i, j, new_val):
            return True
        else:
            return False

    # checks to make sure every variable has the potential to be assigned
    # If not, returns False
    def forward_checking(self, puzzle, assignment, i, j):
        """ Bryndon Wilkerson
        Checks to make sure every next possible variable has a domain
        If not, return false
        """
        full = RuleCheck.fullSolution(RuleCheck, puzzle, assignment)
        list_potential = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        actual_list = []
        for r in range(len(list_potential)):
            if self.check_rules(full, i, j, list_potential[r]):
                actual_list.append(list_potential[r])
        if len(actual_list) == 0:
            # print("Empty List")
            return False
        return True


    @staticmethod
    def col_check(full, j, new_val):
        """ Bryndon Wilkerson
        Returns true if the new variable doesn't violate the column constraint
        """
        for i in range(9):
            if full[i][j] == new_val:
                return False
        return True


    @staticmethod
    def row_check(full, i, new_val):
        """" Bryndon Wilkerson
        Returns true if the new variable doesn't violate the row constraint
        """
        for j in range(9):
            if full[i][j] == new_val:
                return False
        return True


    @staticmethod
    def square_check(full, i, j, new_val):
        """ Bryndon Wilkerson
        Returns true if the new variable doesn't violate the 3x3 constraint
        """
        start_row = i - i % 3
        start_col = j - j % 3

        for p in range(3):
            for k in range(3):
                if full[p + start_row][k + start_col] == new_val:
                    return False
        return True
