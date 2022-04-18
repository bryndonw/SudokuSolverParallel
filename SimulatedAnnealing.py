import random
from numpy import exp
from numpy.random import rand

"""Initial Values to control temp and number of iterations before stopping the search"""
temp = 100
n_iterations = 100000
step_counter = 0


def simulated_annealing(empty_puzzle, puzzle):
    """ Mason Medina
    Simulated annealing function that controls the temperature of the algorithm to influence moves within the
    solve """
    best = fitness(puzzle)
    current = best
    counter = 0

    """Reheat function, counts iterations if the solution is stuck in local maxima"""
    for i in range(n_iterations):
        if best == 0:
            break
        if counter > 500:
            break

        """Performs random swap and fitness test on puzzle to determine improvements"""
        temp_puzzle = puzzle.copy()
        random_swap(empty_puzzle, temp_puzzle)
        next = fitness(temp_puzzle)

        """Increments if function is stuck in local maxima"""
        if next <= best:
            puzzle = temp_puzzle
            """Fitness debug statement"""
            # print('fitness has increased from {} to {}'.format(best, next))

            best = next
            counter += 1

        """Temperature function"""
        diff = next - current

        t = temp / float(i + 1)

        value = exp(-diff / t)

        if diff < 0 or rand() < value:
            current = next

    print(step_counter, "steps")

    if fitness(puzzle) > 0:
        print("Unable to find solution in", n_iterations, "iterations")

    return puzzle


def fill_puzzle(row, column, puzzle):
    """ Mason Medina
    Checks which numbers are missing in a 3x3 block"""
    checklist = [False] * 9
    for i in range(row, row + 3):  # Iterates through the rows
        for j in range(column, column + 3):  # Iterates through columns
            if puzzle[i][j] != 0:  # Checks for zeros
                checklist[puzzle[i][j] - 1] = True

    """Adds them to a list"""
    addlist = []
    for i in range(len(checklist)):
        if not checklist[i]:
            addlist.append(i + 1)  # Adds set variables to the list

    """Fill the 3x3 box without repeating any numbers"""
    for i in range(len(addlist)):
        breakcheck = False
        index = random.randint(0, len(addlist) - 1)  # picks a random int from 1-9 that isnt already in the box
        for j in range(row, row + 3):
            for k in range(column, column + 3):
                if puzzle[j][k] == 0:
                    number = addlist[index]
                    puzzle[j][k] = number
                    addlist.remove(number)
                    breakcheck = True
                    break

            if breakcheck:
                break


def fitness(puzzle):
    """ Mason Medina
    Scores the puzzle based upon its current state and the next state using the cost function"""
    score = cost(puzzle) + cost(puzzle.transpose())

    return score


def cost(puzzle):
    """ Mason Medina
    Calculate the total cost of the puzzle by checking the values"""
    score = 0
    for i in range(9):
        checklist = [False] * 9
        for j in range(9):
            if not checklist[puzzle[i][j] - 1]:
                checklist[puzzle[i][j] - 1] = True
            else:
                score += 1

    return score


def random_swap(empty_puzzle, puzzle):
    """ Mason Medina
    Selects two ints from the puzzle and swaps them"""

    x, y = random.randint(0, 2), random.randint(0, 2)
    zero_counter = 0

    for i in range(3 * x, 3 * x + 3):
        for j in range(3 * y, 3 * y + 3):
            if empty_puzzle[i][j] == 0:
                zero_counter += 1

    if zero_counter > 1:

        sample1, sample2 = random.sample(range(1, zero_counter + 1), k=2) #Radomly selects 2 samples to swap within a box

        global step_counter
        step_counter += 1

        i1, i2, j1, j2 = 0, 0, 0, 0

        for i in range(3 * x, 3 * x + 3):
            for j in range(3 * y, 3 * y + 3):
                if empty_puzzle[i][j] == 0:
                    sample1 -= 1
                    sample2 -= 1
                if sample1 == 0:
                    i1, j1 = i, j
                    sample1 -= 1
                if sample2 == 0:
                    i2, j2 = i, j
                    sample2 -= 1

        puzzle[i1][j1], puzzle[i2][j2] = puzzle[i2][j2], puzzle[i1][j1]
