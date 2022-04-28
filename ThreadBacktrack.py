import time

import Backtracking as bt
from multiprocessing import Pool
import numpy as np
from RuleCheck import RuleCheck

class ThreadBacktrack:
    def __init__(self,puzzle):
        self.puzzle = puzzle
        self.search_type = 0

        print(self.puzzle)
        all_unassigned_vars = []
        size = 10
        self.backtrack = bt.Backtracking(self.puzzle, 2)
        self.assignment = np.copy(self.puzzle)
        for i in range(len(self.puzzle)):
            for j in range(len(self.puzzle[i])):
                if self.puzzle[i][j] != '?':
                    self.assignment[i][j] = '0'
                else:
                    all_unassigned_vars.append([i,j])

        # gets the combined solution of assignment and og puzzle
        self.full = RuleCheck.fullSolution(RuleCheck, self.puzzle, self.assignment)
        # selects variable based on the full board and search type (random, next in line, minimum remaining values)
        self.new_var = self.backtrack.select_unassigned_variable(self.full, self.search_type)
        print(self.new_var, 'NEWVAR')
        ## ITS GONNA COMBINE ONE UNASSIGNED VARIABLE WITH ALL OF THE POTENTIAL VALUES

        # gets list of potential values for spot on board (list of 1-9)
        val_list = self.backtrack.order_domain_values()

        val_var_list = []
        for u in all_unassigned_vars:
            for v in val_list:
                val_var_list.append([v,u])
        print(val_var_list)
        t=time.time()
        self.movin=True
        with Pool(40) as p:
            if self.movin:
                p.map(self.threadbt, val_var_list)

        t2=time.time()-t
        # print(t)
        # print(t2)


    def threadbt(self, val_var_list):
        v=val_var_list[0]
        new_var = val_var_list[1]
        self.assignment[new_var[0]][new_var[1]] = v
        something = self.backtrack.backtrack(self.puzzle, self.assignment, self.search_type)
        print('returned value',something, 'v', v, 'newvar', new_var)
        if something is True:
            self.movin=False
            print('finished')
            quit()


