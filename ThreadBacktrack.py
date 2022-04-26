import time

import Backtracking as bt
from multiprocessing import Array, Pool
import numpy as np
from RuleCheck import RuleCheck

class ThreadBacktrack:
    def __init__(self,puzzle):
        self.puzzle = puzzle
        self.search_type = 0

        print(self.puzzle)
        size = 10
        self.backtrack = bt.Backtracking(self.puzzle, 2)
        self.assignment = np.copy(self.puzzle)
        for i in range(len(self.puzzle)):
            for j in range(len(self.puzzle[i])):
                if self.puzzle[i][j] != '?':
                    self.assignment[i][j] = '0'

        # gets the combined solution of assignment and og puzzle
        self.full = RuleCheck.fullSolution(RuleCheck, self.puzzle, self.assignment)
        # selects variable based on the full board and search type (random, next in line, minimum remaining values)
        self.new_var = self.backtrack.select_unassigned_variable(self.full, self.search_type)
        print(self.new_var, 'NEWVAR')

        # gets list of potential values for spot on board (list of 1-9)
        val_list = self.backtrack.order_domain_values()

        t=time.time()
        with Pool(40) as p:
            p.map(self.threadbt, val_list)
        t2=time.time()-t
        print(t)
        print(t2)


    def threadbt(self, v):
        self.assignment[self.new_var[0]][self.new_var[1]] = v
        something = self.backtrack.backtrack(self.puzzle, self.assignment, self.search_type)
        print('returned value',something, 'v', v, 'newvar', self.new_var)
        if something is True:
            print('finished')
            exit()


