import sys
import random
import math


def simulated_annealing(problem):
    current = problem[0,0]
    for t in range(sys.maxsize):
        T = schedule(t)
        if T == 0:
            return current
        neighbors = current
        if not neighbors:
            return current
        next = random.choice(neighbors)
        delta_e = problem.value(next.state) - problem.value(current.state)
        if delta_e > 0 or (math.exp(delta_e / T)):
            current = next


def schedule(k=20, lam = 0.005, limit = 100):
    return lambda t: (k *math.exp(-lam * t) if t < limit else 0)