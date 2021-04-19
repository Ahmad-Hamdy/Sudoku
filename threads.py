# This file contains classes
# Responible for handling threads  

from PyQt5 import QtCore
from time import sleep
from utils import find_empty_cell, valid_row, valid_column, valid_box, solve

class delay_value():
    def __init__(self, delay = 0.01):
        self._delay = delay

    @property
    def delay(self):
        return self._delay

    @delay.setter
    def delay(self, delay):
        self._delay = delay    
delay_handler = delay_value()

class Timer(QtCore.QThread):
    sec_signal = QtCore.pyqtSignal(str)
    def __init__(self, parent=None):
        super(Timer, self).__init__(parent)
        self.current_time = 0
        self.go = True
    def run(self):
        #this is a special fxn that's called with the start() fxn
        while True:
            sleep(1)
            if self.go:
                self.sec_signal.emit('{:02}:{:02}'.format(self.current_time//60, int(self.current_time%60)))
                self.current_time += 1

    def toggle_timer(self):
        self.go = not self.go

            
class signal_emitter(QtCore.QObject):
    answer_signal = QtCore.pyqtSignal(int, int, str, str)
    finished = QtCore.pyqtSignal()

    # the funtion responsible for solving the Sudoku grid 
    # using backtracking algorithm
    @QtCore.pyqtSlot(list, int, int, result=bool)
    def solve(self, grid, row, column):
        row, column = find_empty_cell(grid, row)
        if (row, column) == (None,None):
            self.finished.emit()
            return True

        for num in range(1, 10):
            if valid_row(grid[row], num
                ) and valid_column(grid, column, num
                ) and valid_box(grid, row, column, num):
                grid[row][column] = num     
                self.answer_signal.emit(row, column, str(num), """color: rgb(170, 170, 255);
                                        border: 1px solid black;""")
                sleep(delay_handler.delay)

                if self.solve(grid, row, column):
                    return True
 
                grid[row][column] = 0
                self.answer_signal.emit(row, column, "0", """color: rgb(255, 0, 0);
                                        border: 2px solid rgb(255, 0, 0);""")
                sleep(delay_handler.delay)
        
        return False


