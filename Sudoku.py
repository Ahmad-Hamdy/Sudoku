from PyQt5 import QtCore, QtGui, QtWidgets
from random import choice
from time import sleep
from utils import find_empty_cell, valid_row, valid_column, valid_box, solve
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
        self.auto_solve.clicked.connect(self.solve_grid)

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

        self.logger = Logger()
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
        self.auto_solve.setText(_translate("Sudoku", "Show/Hide solution"))
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

    def solve_grid(self):
        if self.solution_state:
            self.show_unsolved_grid()
        else:
            for row, col in self.empty_fields:
                self.field[row][col].setText(str(grid[row][col]))
        self.solution_state = not self.solution_state

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
    
    def closeEvent(self, event):
        self.thread.terminate()
        print("Closed")

class Logger(QtCore.QThread):
    sec_signal = QtCore.pyqtSignal(str)
    def __init__(self, parent=None):
        super(Logger, self).__init__(parent)
        self.current_time = 0
        self.go = True
    def run(self):
        #this is a special fxn that's called with the start() fxn
        while self.go:
            sleep(1)
            self.sec_signal.emit('{:02}:{:02}'.format(self.current_time//60, int(self.current_time%60)))
            self.current_time += 1

    def toggle_timer(self):
    	self.go = not self.go
            
class signal_emitter(QtCore.QObject):
    answer_signal = QtCore.pyqtSignal(int, int, str, str)
    finished = QtCore.pyqtSignal()

    @QtCore.pyqtSlot(list, int, int, result=bool)
    def solve(self, grid, row, column):
        row, column = find_empty_cell(grid, row)

        # this is the bae case for recursion
        # if there are no more empty cells
        if (row, column) == (None,None):
            self.finished.emit()
            return True

        # recursively try each number between 0-9 for the empty cell currently soolving
        for num in range(1, 10):

            # validate if the number trying will satisfy the restirections of soduko
            if valid_row(grid[row], num
                ) and valid_column(grid, column, num
                ) and valid_box(grid, row, column, num):
                grid[row][column] = num     
                self.answer_signal.emit(row, column, str(num), """color: rgb(170, 170, 255);
										border: 1px solid black;""")
                sleep(0.01)

                if self.solve(grid, row, column):
                    return True
 
                grid[row][column] = 0
                self.answer_signal.emit(row, column, "0", """color: rgb(255, 0, 0);
										border: 2px solid rgb(255, 0, 0);""")
                sleep(0.01)
        
        return False


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Sudoku = QtWidgets.QMainWindow()
    ui = Ui_Sudoku()
    ui.setupUi(Sudoku)
    Sudoku.show()
    sys.exit(app.exec_())


#########STUFF TO DO###############
# figure out the problem with closeEvent
# add more grids