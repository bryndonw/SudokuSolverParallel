import sys
import time

import Backtracking as bt
from multiprocessing import Pool
from RuleCheck import RuleCheck

class ThreadBacktrack:
    def __init__(self,puzzle):
        self.puzzle = puzzle
        self.search_type = 0
        self.backtrack = bt.Backtracking(self.puzzle, 2)

        all_unassigned_vars = []

        self.assignment = []

        # print(self.assignment)
        # self.assignment = np.copy(self.puzzle)
        for i in range(len(self.puzzle)):
            listy = []
            for j in range(len(self.puzzle[i])):
                if self.puzzle[i][j] != '?':
                    listy.append(0)
                    # self.assignment[i][j] = '0'
                else:
                    listy.append('?')
                    all_unassigned_vars.append([i, j])
            self.assignment.append(listy)

        # print(self.puzzle)
        size = 10

        # print(self.assignment)
        # print('puzzle', self.puzzle)
        # gets the combined solution of assignment and og puzzle
        self.full = RuleCheck.fullSolution(RuleCheck, self.puzzle, self.assignment)
        # selects variable based on the full board and search type (random, next in line, minimum remaining values)
        self.new_var = self.backtrack.select_unassigned_variable(self.full, self.search_type)

        # print(self.new_var, 'NEWVAR')
        ## ITS GONNA COMBINE ONE UNASSIGNED VARIABLE WITH ALL OF THE POTENTIAL VALUES

        # gets list of potential values for spot on board (list of 1-9)
        self.val_list = self.backtrack.order_domain_values()

        self.val_var_list = []
        for u in all_unassigned_vars:
            for v in self.val_list:
                self.val_var_list.append([v, u])

    def ThreadStart(self):

        # print(val_var_list)
        t = time.time()
        with Pool(40) as p:
            p.map(self.threadbt, self.val_var_list)

        t2 = time.time() - t
        # print("Time it took for variables", t2)

        t3 = time.time()
        with Pool(40) as p:
            p.map(self.threadbtValues, self.val_list)

        t4 = time.time() - t3
        # print("Time it took for values", t4)

        return (t2, t4)

    def threadbt(self, val_var_list):
        v=val_var_list[0]
        new_var = val_var_list[1]
        self.assignment[new_var[0]][new_var[1]] = v
        something = self.backtrack.backtrack(self.puzzle, self.assignment, self.search_type)
        # print('returned value',something, 'v', v, 'newvar', new_var)

    def threadbtValues(self, v):
        self.assignment[self.new_var[0]][self.new_var[1]] = v
        something = self.backtrack.backtrack(self.puzzle, self.assignment, self.search_type)
        # print('returned value', something, 'v', v, 'newvar', self.new_var)
