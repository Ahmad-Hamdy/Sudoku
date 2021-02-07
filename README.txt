Sudoku game implemented with 4 different puzzles
and a solver algorithm to solve any sudoku puzzle 

This is a minor python project in which sudoku game was implemented
using PyQt5 module to create the interface of the game, the interface
consists of the sudoku 9x9 grid, a counter to keep track of wrong
moves made, and a button to auto-solve the game

The solver is implemented using the "back-tracking" algorithm, which
relies on solving the puzzle using brute-force, i.e recursively the
first possible value for each field is set until no valid values
exists for a field, that's when the algorithm back-track the solution
undoing a few steps of the solution until a valid solution is found