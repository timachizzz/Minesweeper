import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton
from random import sample


class DoubleCLickButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            if not self.text():
                if not self.styleSheet():
                    self.setStyleSheet("background-color: rgb(255,100,0);")
                else:
                    self.setStyleSheet('')
        if event.button() == Qt.MouseButton.LeftButton:
            if not self.styleSheet():
                self.clicked.emit()
        else:
            super().mousePressEvent(event)


class Minesweeper(QMainWindow):
    def __init__(self):
        super().__init__()

        self.WIDTH, self.HEIGHT = 18, 14
        self.SIZE = 40
        self.setFixedSize(self.WIDTH * self.SIZE, self.HEIGHT * self.SIZE + 25)
        self.statusBar().setEnabled(True)
        self.statusBar().showMessage('Выберите клетку!')

        self.table = []
        self.BOMBS = 40
        self.safe_cells = self.WIDTH * self.HEIGHT - self.BOMBS
        self.bombs_positions = []

        for i in range(self.HEIGHT):
            line = []
            for r in range(self.WIDTH):
                button: DoubleCLickButton = DoubleCLickButton(self)
                button.resize(self.SIZE, self.SIZE)
                button.move(r * self.SIZE, i * self.SIZE)
                button.clicked.connect(self.check_button)
                line.append(button)
            self.table.append(line)

        self.first_move = True

    def check_button(self):
        button = self.sender()
        x, y = 0, 0
        if isinstance(button, QPushButton):
            for line in range(len(self.table)):
                if button in self.table[line]:
                    x, y = (line, self.table[line].index(button))
                    break
        if self.first_move:
            self.generate_bombs((x, y))
            self.first_move = False

        if (x, y) in self.bombs_positions:
            quit()
        counter = 0
        for i in range(x - 1, x + 2):
            if i < 0 or i >= self.HEIGHT:
                continue
            for r in range(y - 1, y + 2):
                if r < 0 or r >= self.WIDTH:
                    continue
                if (i, r) in self.bombs_positions:
                    counter += 1
        button.setStyleSheet("background-color: rgb(120,120,120);")
        button.repaint()
        button.setText(str(counter))
        self.safe_cells -= 1
        self.statusBar().showMessage(f'Осталось: {self.safe_cells}; ПКМ для флага')
        if self.safe_cells == 0:
            self.win()

        if counter == 0:
            for i in range(x - 1, x + 2):
                if i < 0 or i >= self.HEIGHT:
                    continue
                for r in range(y - 1, y + 2):
                    if r < 0 or r >= self.WIDTH:
                        continue
                    if (i != x or r != y) and not self.table[i][r].styleSheet():
                        self.table[i][r].clicked.emit()

    def generate_bombs(self, player_cell):
        field = [(i, r) for i in range(self.HEIGHT) for r in range(self.WIDTH)]
        field.pop(field.index(player_cell))
        self.bombs_positions = sample(field, k=self.BOMBS)
        return

    def win(self):
        self.statusBar().showMessage('Вы выиграли!')
        for x, y in self.bombs_positions:
            button: QPushButton = self.table[x][y]
            button.setStyleSheet("background-color: rgb(0,190,0);")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Minesweeper()
    ex.show()
    sys.exit(app.exec())
