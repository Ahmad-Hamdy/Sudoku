from PyQt5 import QtCore, QtGui, QtWidgets
from random import choice
from threads import Timer, signal_emitter, delay_handler
from patterns import *
from UI_components import render_grid, render_footer, render_menu

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
        self.menu_opened = 0
        self.delay_handler = delay_handler

    def setupUi(self, Sudoku):
        Sudoku.setObjectName("Sudoku")
        Sudoku.resize(590, 630)
        Sudoku.setMinimumSize(QtCore.QSize(590, 630))
        Sudoku.setMaximumSize(QtCore.QSize(590, 630))
        Sudoku.setWindowIcon(QtGui.QIcon("sudoku.jfif"))

        self.solve_thread = signal_emitter()
        self.thread = QtCore.QThread(self)
        self.thread.start()
        self.solve_thread.moveToThread(self.thread)
        self.solve_thread.answer_signal.connect(self.show_cell_visual)
        self.solve_thread.finished.connect(self.animation_complete)

        self.centralwidget = QtWidgets.QWidget(Sudoku)
        self.centralwidget.setObjectName("centralwidget")

        render_grid(self, self.centralwidget, 50, 0)

        render_footer(self, self.centralwidget, 50, 540)
        
        render_menu(self, self.centralwidget, 0, 0)

        Sudoku.setCentralWidget(self.centralwidget)

        self.logger = Timer()
        self.logger.sec_signal.connect(self.timer.setText)
        self.pause_run_timer.clicked.connect(self.logger.toggle_timer)
        self.logger.start()

        self.auto_solve.clicked.connect(self.show_hide_solution)
        self.solve_animation.clicked.connect(self.solve_grid_visual)
        self.speed_slider.valueChanged['int'].connect(self.speed_value.setNum)
        self.speed_slider.valueChanged['int'].connect(self.set_delay)
        self.btn_toggle_menu.clicked.connect(lambda: self.open_menu() if not self.menu_opened else self.close_menu())

        QtCore.QMetaObject.connectSlotsByName(Sudoku)
        self.retranslateUi(Sudoku)
        self.show_unsolved_grid()

    def retranslateUi(self, Sudoku):
        _translate = QtCore.QCoreApplication.translate
        Sudoku.setWindowTitle(_translate("Sudoku", "Sudoku"))
        self.wrong_moves_label.setText(_translate("Sudoku", "Wrong Moves:"))
        self.wrong_moves_count.setText(_translate("Sudoku", "0"))
        self.timer.setText(_translate("Sudoku", "00:00"))
        self.solve_animation.setText(_translate("Sudoku", "Run solving animation"))
        self.auto_solve.setText(_translate("Sudoku", "Show Solution"))
        self.pause_run_timer.setText(_translate("Sudoku", "Pause Timer"))
        self.speed_label.setText(_translate("Sudoku", "Step delay (ms)"))
        self.speed_value.setText(_translate("Sudoku", "0"))

    def set_delay(self, delay):
        if isinstance(delay, int):
            self.delay_handler.delay = delay/100

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

    def open_menu(self):
        self.menu = QtCore.QPropertyAnimation(self.frame_left_menu, b"size")
        self.menu.setDuration(125)
        self.menu.setStartValue(QtCore.QSize(50, 631)) #width, height
        self.menu.setEndValue(QtCore.QSize(240, 631))
        self.menu.start()
        self.menu_opened = 1

    def close_menu(self):
        self.menu = QtCore.QPropertyAnimation(self.frame_left_menu, b"size")
        self.menu.setDuration(125)
        self.menu.setStartValue(QtCore.QSize(240, 631)) #width, height
        self.menu.setEndValue(QtCore.QSize(50, 631))
        self.menu.start()
        self.menu_opened = 0


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