import numpy as np
import time

impossible_array = np.array([[-1, -1, -1, -1, -1, -1, -1, -1, -1],
                            [-1, -1, -1, -1, -1, -1, -1, -1, -1],
                            [-1, -1, -1, -1, -1, -1, -1, -1, -1],
                            [-1, -1, -1, -1, -1, -1, -1, -1, -1],
                            [-1, -1, -1, -1, -1, -1, -1, -1, -1],
                            [-1, -1, -1, -1, -1, -1, -1, -1, -1],
                            [-1, -1, -1, -1, -1, -1, -1, -1, -1],
                            [-1, -1, -1, -1, -1, -1, -1, -1, -1],
                            [-1, -1, -1, -1, -1, -1, -1, -1, -1]])


#checks if value is already in row
def check_row(y, val, sudoku):
    for i in range(0, 9):
        if val == sudoku[y, i]:
            return False
    return True


#checks if value is already in column
def check_column(x, val, sudoku):
    for i in range(0, 9):
        if val == sudoku[i, x]:
            return False
    return True


#builds the local 3x3 square of given coordinates
def build_square(x, y, sudoku):
    local_x = x % 3
    local_y = y % 3

    upper_x = x - local_x
    upper_y = y - local_y

    return np.array([[sudoku[upper_y, upper_x], sudoku[upper_y, upper_x + 1], sudoku[upper_y, upper_x + 2]],
                     [sudoku[upper_y + 1, upper_x], sudoku[upper_y + 1, upper_x + 1], sudoku[upper_y + 1, upper_x + 2]],
                     [sudoku[upper_y + 2, upper_x], sudoku[upper_y + 2, upper_x + 1], sudoku[upper_y + 2, upper_x + 2]]])


#checks if value is already in 3x3 square of given tile
def check_square(x, y, val, sudoku):
    square = build_square(x, y, sudoku)
    for i in range(0, 3):
        for j in range(0, 3):
            if val == square[j, i]:
                return False
    return True


#checks all constraints of the trying value
def check_value(x, y, val, sudoku):
    return check_square(x, y, val, sudoku) and check_column(x, val, sudoku) and check_row(y, val, sudoku)


#goes through sudoku and gives possible values for each square
def get_possible_values(sudoku):
    possible_values = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0, 0]])

    for i in range(0, 9):
        for j in range(0, 9):
            if sudoku[j, i] == 0:
                for k in range(1, 10):
                    if check_value(i, j, k, sudoku):
                        if possible_values[j, i] == 0:
                            possible_values[j, i] = str(k)
                        else:
                            possible_values[j, i] = str(possible_values[j, i]) + str(k)
            else:
                possible_values[j, i] = sudoku[j, i]

    return possible_values


#fixes values already given, and determines if it's legal or not
def fix_values(sudoku):
    fixed_values = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0, 0]])

    for i in range(0,9):
        for j in range(0,9):
            if sudoku[j, i] <= 9:
                if sudoku[j, i] == 0:
                    return impossible_array
                else:
                    fixed_values[j, i] = sudoku[j, i]
    return fixed_values


#finds the next free square so we're only bothering with values we haven't completely determined
def find_empty_square(sudoku, loc):
    for i in range(9):
        for j in range(9):
            if sudoku[j, i] == 0:
                loc[0] = i
                loc[1] = j
                return True
    return False


def sudoku_solver(sudoku):
    possible_values = get_possible_values(sudoku)
    fixed_values = fix_values(possible_values)

    if np.array_equal(fixed_values, impossible_array):
        return impossible_array

    if solve(fixed_values, possible_values):
        return fixed_values

    return impossible_array


#recursive function for determining each value of the sudoku
def solve(fixed_values_sudoku, possible_values_sudoku):
    loc = np.array([0, 0])

    #determines if there's a free value to test, gets coordinates if so
    if not find_empty_square(fixed_values_sudoku, loc):
        return True

    x = loc[0]
    y = loc[1]

    #takes possible values and puts them into an array
    possible_values = np.array(list(map(int, str(possible_values_sudoku[y, x]))))

    #loops through each possible value, testing it and trying the next free square if there is
    for val in possible_values:
        if check_value(x, y, val, fixed_values_sudoku):
            fixed_values_sudoku[y, x] = val

            if solve(fixed_values_sudoku, possible_values_sudoku):
                return True

            fixed_values_sudoku[y, x] = 0

    #triggers the backtracking if it return false
    return False
