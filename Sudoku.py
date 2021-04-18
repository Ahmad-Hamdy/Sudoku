from PyQt5 import QtCore, QtGui, QtWidgets
from random import choice
from threads import Timer, signal_emitter
from patterns import *

empty_grid, grid = choice([
						(default_pattern, default_solution),
						(wall_pattern, default_solution),
						(corner_pattern, default_solution),
						(diagonal_pattern, default_solution)
						])

animation_grid = [ [x for x in row] for row in empty_grid]

class Ui_Sudoku(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui_Sudoku, self).__init__()
        self.field = [[0 for y in range(9)] for x in range(9)]
        self.empty_fields = [ (row, column) for row in range(9) for column in range(9) if not empty_grid[row][column]]
        self.wrong_moves = 0
        self.edited_fields = list()
        self.solution_state = 0

    def setupUi(self, Sudoku):
        Sudoku.setObjectName("Sudoku")
        Sudoku.resize(540, 680)
        Sudoku.setMinimumSize(QtCore.QSize(540, 680))
        Sudoku.setMaximumSize(QtCore.QSize(540, 680))
        Sudoku.setWindowIcon(QtGui.QIcon("sudoku.jfif"))

        self.solve_thread = signal_emitter()
        self.thread = QtCore.QThread(self)
        self.thread.start()
        self.solve_thread.moveToThread(self.thread)
        self.solve_thread.answer_signal.connect(self.show_cell_visual)
        self.solve_thread.finished.connect(self.animation_complete)

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
                self.field[row][col].textEdited.connect(lambda text, r=row, c=col: self.validate_field(text, r, c))
        
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
                    '\n' + "color: rgb(0, 170, 255);")

        self.info = QtWidgets.QFrame(self.centralwidget)
        self.info.setGeometry(QtCore.QRect(0, 540, 540, 140))
        self.info.setStyleSheet("background-color: rgb(170, 170, 255);")
        self.info.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.info.setFrameShadow(QtWidgets.QFrame.Raised)
        self.info.setObjectName("info")

        self.wrong_moves_label = QtWidgets.QLabel(self.info)
        self.wrong_moves_label.setGeometry(QtCore.QRect(10, 30, 145, 28))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.wrong_moves_label.setFont(font)
        self.wrong_moves_label.setObjectName("wrong_moves_label")

        self.wrong_moves_count = QtWidgets.QLabel(self.info)
        self.wrong_moves_count.setGeometry(QtCore.QRect(170, 30, 35, 28))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.wrong_moves_count.setFont(font)
        self.wrong_moves_count.setObjectName("wrong_moves_count")

        self.auto_solve = QtWidgets.QPushButton(self.info)
        self.auto_solve.setGeometry(QtCore.QRect(290, 20, 238, 42))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.auto_solve.setFont(font)
        self.auto_solve.setStyleSheet("background-color: rgb(209, 207, 255);\n")
        self.auto_solve.setObjectName("auto_solve")
        self.auto_solve.clicked.connect(self.show_hide_solution)

        self.timer = QtWidgets.QLabel(self.info)
        self.timer.setGeometry(QtCore.QRect(30, 90, 60, 28))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.timer.setFont(font)
        self.timer.setObjectName("timer")

        self.solve_animation = QtWidgets.QPushButton(self.info)
        self.solve_animation.setGeometry(QtCore.QRect(290, 80, 238, 42))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.solve_animation.setFont(font)
        self.solve_animation.setStyleSheet("background-color: rgb(209, 207, 255);")
        self.solve_animation.setObjectName("solve_animation")
        self.solve_animation.clicked.connect(self.solve_grid_visual)
        Sudoku.setCentralWidget(self.centralwidget)

        self.logger = Timer()
        self.logger.sec_signal.connect(self.timer.setText)
        self.logger.start()

        self.retranslateUi(Sudoku)
        QtCore.QMetaObject.connectSlotsByName(Sudoku)
        self.show_unsolved_grid()

    def retranslateUi(self, Sudoku):
        _translate = QtCore.QCoreApplication.translate
        Sudoku.setWindowTitle(_translate("Sudoku", "Sudoku"))
        self.wrong_moves_label.setText(_translate("Sudoku", "Wrong Moves:"))
        self.wrong_moves_count.setText(_translate("Sudoku", "0"))
        self.auto_solve.setText(_translate("Sudoku", "Show solution"))
        self.timer.setText(_translate("Sudoku", "00:00"))
        self.solve_animation.setText(_translate("Sudoku", "Play solving animation"))

    def validate_field(self, text, row, col):
        if not text.isdigit():
            self.field[row][col].setText("")
        else:
            self.edited_fields.append((row, col))

    def validate_answers(self):
        for row,col in self.edited_fields:
            if self.field[row][col].text() != str(grid[row][col]):
                self.field[row][col].setText("")
                self.wrong_moves += 1
                self.wrong_moves_count.setText(str(self.wrong_moves))
            
            elif self.field[row][col].text() == str(grid[row][col]):
                self.field[row][col].setReadOnly(True)
                self.field[row][col].setStyleSheet(
                        self.field[row][col].styleSheet() +
                        '\n' + "color: rgb(0, 199, 0);")
    
    def show_cell_visual(self, row, col, val, style):
    	self.field[row][col].setText(val)
    	if style:
    		self.field[row][col].setStyleSheet(self.field[row][col].styleSheet() + style)

    def show_unsolved_grid(self):
        for row in range(9):
            for col in range(9):
                if empty_grid[row][col]:
                    self.field[row][col].setText(str(empty_grid[row][col]))
                    self.field[row][col].setReadOnly(True)
                else:
                	self.field[row][col].setText("")

    def show_hide_solution(self):
        if self.solution_state:
            self.show_unsolved_grid()
            self.auto_solve.setText("Show solution")
        else:
            for row, col in self.empty_fields:
                self.field[row][col].setText(str(grid[row][col]))
            self.auto_solve.setText("Hide solution")
        self.solution_state = not self.solution_state
        self.logger.toggle_timer()


    def solve_grid_visual(self):
        for row, col in self.empty_fields:
            self.field[row][col].setStyleSheet(
                        self.field[row][col].styleSheet() +
                        '\n' + "color: rgb(0, 0, 0);")
        QtCore.QMetaObject.invokeMethod(self.solve_thread, "solve",
            QtCore.Qt.QueuedConnection,
            QtCore.Q_ARG(list, animation_grid),
            QtCore.Q_ARG(int, 0),
            QtCore.Q_ARG(int, 0))
        self.auto_solve.setDisabled(True)
        self.solve_animation.setDisabled(True)

    def animation_complete(self):
    	self.auto_solve.setEnabled(True)
    	self.solve_animation.setEnabled(True)
    	self.solution_state = 1
    	self.auto_solve.setText("Hide solution")
    

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Sudoku = QtWidgets.QMainWindow()
    ui = Ui_Sudoku()
    ui.setupUi(Sudoku)
    Sudoku.show()
    code = app.exec_()
    ui.thread.terminate()
    sys.exit(code)


#########STUFF TO DO###############
# figure out the problem with closeEvent
# add more grids
# add stting menu
# add start/pause timer
# solve animation speed contoller 