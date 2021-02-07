from PyQt5 import QtCore, QtGui, QtWidgets
from random import choice


default_pattern = [  [3, 0, 6, 5, 0, 8, 4, 0, 0], 
			         [5, 2, 0, 0, 0, 0, 0, 0, 0], 
			         [0, 8, 7, 0, 0, 0, 0, 3, 1], 
			         [0, 0, 3, 0, 1, 0, 0, 8, 0], 
			         [9, 0, 0, 8, 6, 3, 0, 0, 5], 
			         [0, 5, 0, 0, 9, 0, 6, 0, 0], 
			         [1, 3, 0, 0, 0, 0, 2, 5, 0], 
			         [0, 0, 0, 0, 0, 0, 0, 7, 4], 
			         [0, 0, 5, 2, 0, 6, 3, 0, 0] ]

wall_pattern = [ [0, 5, 0, 0, 0, 1, 0, 0, 0], 
		         [0, 9, 0, 0, 0, 2, 0, 0, 0], 
		         [0, 8, 0, 0, 0, 3, 0, 0, 0], 
		         [0, 0, 0, 0, 0, 0, 0, 0, 0], 
		         [8, 7, 6, 0, 0, 0, 0, 0, 0], 
		         [0, 0, 0, 0, 0, 0, 0, 0, 0], 
		         [0, 0, 0, 0, 0, 0, 2, 0, 1], 
		         [0, 0, 0, 0, 0, 0, 9, 0, 8], 
		         [7, 4, 9, 0, 0, 0, 5, 0, 3] ]

corner_pattern = [   [0, 0, 3, 0, 4, 8, 0, 2, 5], 
			         [0, 8, 6, 0, 0, 2, 0, 9, 1], 
			         [0, 2, 5, 3, 0, 0, 0, 0, 0], 
			         [0, 6, 0, 7, 0, 0, 0, 0, 8], 
			         [1, 0, 0, 0, 0, 0, 0, 0, 2], 
			         [8, 0, 0, 0, 0, 5, 0, 6, 0], 
			         [0, 0, 0, 0, 0, 7, 2, 8, 0], 
			         [5, 7, 0, 2, 0, 0, 9, 4, 0], 
			         [3, 4, 0, 8, 6, 0, 5, 0, 0] ]

diagonal_pattern = [ [0, 0, 0, 3, 0, 1, 0, 0, 2], 
			         [0, 5, 2, 0, 0, 4, 0, 0, 0], 
			         [0, 0, 0, 0, 0, 0, 0, 4, 5], 
			         [0, 0, 0, 4, 0, 3, 0, 8, 0], 
			         [0, 0, 6, 7, 0, 9, 3, 0, 0], 
			         [0, 2, 0, 8, 0, 5, 0, 0, 0], 
			         [1, 7, 0, 0, 0, 0, 0, 0, 0], 
			         [0, 0, 0, 5, 0, 0, 8, 7, 0], 
			         [2, 0, 0, 1, 0, 8, 0, 0, 0] ]

patterns = [default_pattern, wall_pattern, corner_pattern, diagonal_pattern]
grid = choice(patterns)

def find_empty_cell(grid, r):
    for row in range(r, 9):
        for col in range(9):
            if not grid[row][col]:
                return (row, col)
    return (None, None)

def valid_row(row, num):
    for cell in row:
        if cell == num:
            return False
    return True

def valid_column(grid, column, num):
    for row in range(9):
        if grid[row][column] == num:
            return False
    return True

def valid_box(grid, row, column, num):
    box_start_row = row - (row % 3)
    box_start_col = column - (column % 3)
    for r in range(box_start_row , box_start_row + 3):
        for c in range(box_start_col , box_start_col + 3):
            if grid[r][c] == num:
                return False
    return True

def solve(grid, row, column):
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

base_grid = grid.copy()

class Ui_Sudoku(object):
    def setupUi(self, Sudoku):
        Sudoku.setObjectName("Sudoku")
        Sudoku.resize(540, 670)
        Sudoku.setMinimumSize(QtCore.QSize(540, 670))
        Sudoku.setMaximumSize(QtCore.QSize(540, 670))
        Sudoku.setWindowIcon(QtGui.QIcon("sudoku.jfif"))

        self.field = [[0 for y in range(9)] for x in range(9)]

        self.wrong_moves = 0

        self.empty_fields = []
        for row in range(9):
        	for column in range(9):
        		if not grid[row][column]:
        			self.empty_fields.append((row, column))

        self.centralwidget = QtWidgets.QWidget(Sudoku)
        self.centralwidget.setObjectName("centralwidget")

        self.sub_grid = QtWidgets.QFrame(self.centralwidget)
        self.sub_grid.setGeometry(QtCore.QRect(0, 0, 540, 540))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.sub_grid.setFont(font)


        for row in range(9):
            for col in range(9):
                self.field[row][col] = QtWidgets.QLineEdit(self.sub_grid)
                self.field[row][col].setGeometry(QtCore.QRect(60*col, 60*row, 60, 60))
                font = QtGui.QFont()
                font.setPointSize(28)
                self.field[row][col].setFont(font)
                self.field[row][col].setMaxLength(1)
                self.field[row][col].setAlignment(QtCore.Qt.AlignCenter)
                self.field[row][col].returnPressed.connect(self.validate_answers)
                self.field[row][col].textEdited.connect(self.validate_field)
        
        for row in range(3,6):
            for col in range(3):
                self.field[row][col].setStyleSheet("background-color: rgb(225, 225, 225);")

        for row in range(3):
            for col in range(3,6):
                self.field[row][col].setStyleSheet("background-color: rgb(225, 225, 225);")

        for row in range(6,9):
            for col in range(3,6):
                self.field[row][col].setStyleSheet("background-color: rgb(225, 225, 225);")

        for row in range(3,6):
            for col in range(6,9):
                self.field[row][col].setStyleSheet("background-color: rgb(225, 225, 225);")

        for row, column in self.empty_fields:
        	self.field[row][column].setStyleSheet(
	        		self.field[row][column].styleSheet() +
	        		'\n' + 
	        		"color: rgb(0, 170, 255);")

        
        self.info = QtWidgets.QFrame(self.centralwidget)
        self.info.setGeometry(QtCore.QRect(0, 540, 540, 70))
        self.info.setStyleSheet("background-color: rgb(170, 170, 255);")
        self.info.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.info.setFrameShadow(QtWidgets.QFrame.Raised)
        self.info.setObjectName("info")
        self.wrong_moves_label = QtWidgets.QLabel(self.info)
        self.wrong_moves_label.setGeometry(QtCore.QRect(10, 20, 145, 28))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.wrong_moves_label.setFont(font)
        self.wrong_moves_label.setObjectName("wrong_moves_label")
        self.wrong_moves_count = QtWidgets.QLabel(self.info)
        self.wrong_moves_count.setGeometry(QtCore.QRect(170, 20, 30, 28))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.wrong_moves_count.setFont(font)
        self.wrong_moves_count.setObjectName("wrong_moves_count")

        self.auto_solve = QtWidgets.QPushButton(self.info)
        self.auto_solve.setGeometry(QtCore.QRect(370, 15, 125, 40))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.auto_solve.setFont(font)
        self.auto_solve.setStyleSheet("background-color: rgb(209, 207, 255);")
        self.auto_solve.setObjectName("auto_solve")
        self.auto_solve.clicked.connect(self.solve_grid)

        Sudoku.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Sudoku)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 540, 26))
        self.menubar.setObjectName("menubar")
        Sudoku.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Sudoku)
        self.statusbar.setObjectName("statusbar")
        Sudoku.setStatusBar(self.statusbar)

        self.retranslateUi(Sudoku)
        self.populate()
        solve(grid, 0, 0)

    def retranslateUi(self, Sudoku):
        _translate = QtCore.QCoreApplication.translate
        Sudoku.setWindowTitle(_translate("Sudoku", "Sudoku"))
        self.wrong_moves_label.setText(_translate("Sudoku", "Wrong Moves:"))
        self.wrong_moves_count.setText(_translate("Sudoku", "0"))
        self.auto_solve.setText(_translate("Sudoku", "Solve"))

    def validate_field(self):
        for row,col in self.empty_fields:
            if not self.field[row][col].text().isdigit():
                self.field[row][col].setText("")

    def validate_answers(self):
        for row,col in self.empty_fields:
            if (self.field[row][col].text() != str(grid[row][col])) and self.field[row][col].text():

                self.field[row][col].setText("")
                self.wrong_moves += 1
                self.wrong_moves_count.setText(str(self.wrong_moves))
            elif self.field[row][col].text() == str(grid[row][col]):
            	self.field[row][col].setStyleSheet(
				        		self.field[row][col].styleSheet() +
				        		'\n' + "color: rgb(0, 199, 0);")
        

    def populate(self):
        for row in range(9):
            for col in range(9):
                if grid[row][col]:
                    self.field[row][col].setText(str(grid[row][col]))
                    self.field[row][col].setReadOnly(True)


    def solve_grid(self):
        for row, col in self.empty_fields:
            self.field[row][col].setText(str(grid[row][col]))
            self.field[row][col].setStyleSheet(
		        		self.field[row][col].styleSheet() +
		        		'\n' + "color: rgb(0, 199, 0);")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Sudoku = QtWidgets.QMainWindow()
    ui = Ui_Sudoku()
    ui.setupUi(Sudoku)
    Sudoku.show()
    sys.exit(app.exec_())
