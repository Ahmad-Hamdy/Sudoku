from PyQt5 import QtCore
from time import sleep
from utils import find_empty_cell, valid_row, valid_column, valid_box, solve


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
