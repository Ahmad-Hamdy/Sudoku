# This file contains all the utility funtions 
# used by the backtracking algorithm


def find_empty_cell(grid, r):
    """finds the next empt cell

    Args:
        grid (list): 2D list holding the values of the sudoku cells
        r (int): the index of the row to start searching from

    Returns:
        (row, col): A tuble with index of the next empty cell in the matrix
        (None, None): if the matrix has no empty values
    """
    for row in range(r, 9):
        for col in range(9):
            if not grid[row][col]:
                return (row, col)
    return (None, None)

def valid_row(row, num):
    """checks if a number is safe to be placed in a row

    Args:
        row (list): A list representing the row 
        num (int): A number to check it's validity in the row

    Returns:
        True: If the number is safe to be placed
        False: If the number is NOT safe to be placed
    """
    return False if num in row else True

def valid_column(grid, column, num):
    """checks if a number is safe to be placed in a column

    Args:
        grid (list): A 2d list representing the sudoku matrix
        column (int): The index of the column to check for
        num (int): A number to check it's validity in the column

    Returns:
        True: If the number is safe to be placed
        False: If the number is NOT safe to be placed
    """
    for row in range(9):
        if grid[row][column] == num:
            return False
    return True

def valid_box(grid, row, column, num):
    """checks if a number is safe to be placed in a 3x3 sub-grid

    Args:
        grid (list): A 2d list representing the sudoku matrix
        row (int): The row index of the cell
        column (int): The column index of the cell
        num (int): A number to check it's validity in the sub-grid

    Returns:
        True: If the number is safe to be placed
        False: If the number is NOT safe to be placed
    """
    box_start_row = row - (row % 3)
    box_start_col = column - (column % 3)
    for r in range(box_start_row , box_start_row + 3):
        for c in range(box_start_col , box_start_col + 3):
            if grid[r][c] == num:
                return False
    return True

def solve(grid, row, column):
    """The main function that is responsible for solving the given grid

    Args:
        grid (list): A 2d list representing the sudoku matrix
        row (int): The row index of the cell to start solving from
        column (int): The column index of the cell to start solving from

    Returns:
        True: If  the grid is solved
        False: If the grid has no solution
    """
    row, column = find_empty_cell(grid, row)

    # this is the bae case for recursion
    # if there are no more empty cells
    if (row, column) == (None,None):
        return True

    # recursively try each number between 0-9 for the empty cell currently soolving
    for num in range(1, 10):

        # validate if the number trying will satisfy the restirections of soduko
        if valid_row(grid[row], num
            ) and valid_column(grid, column, num
            ) and valid_box(grid, row, column, num):

            # if the number will not fail the restirection
            # place it in the cell
            grid[row][column] = num     

            # solve the next empty cell
            if solve(grid, row, column):
                return True

            # if failed to solve next cell
            # undo the solution of the current cell
            # and try the next num in loop 
            grid[row][column] = 0
    
    # if all the numbers were tried and none of them is valid return false
    # and baccktrack the previous solutions untill a valid one is found
    return False
