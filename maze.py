from tkinter import Tk, BOTH, Canvas
from time import sleep
import random

class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title = "Maze Solver"
        self.__canvas = Canvas(width = width, height = height)
        self.__canvas.pack()
        self.running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.running = True
        while self.running:
            self.redraw()

    def close(self):
        self.running = False

    def draw_line(self, line, fill):
        line.draw(self.__canvas, fill)

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2

    def draw(self, canvas, fill):
        canvas.create_line(self.point1.x, self.point1.y, self.point2.x, self.point2.y, fill = fill, width = 2)
        canvas.pack()

class Cell:
    def __init__(self, top_left_point, bottom_right_point, window, cell = None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._x1 = top_left_point.x
        self._y1 = top_left_point.y
        self._x2 = bottom_right_point.x
        self._y2 = bottom_right_point.y
        self._win = window
        self._visited = False

    def draw(self):
        if not self._win:
            return

        # left wall
        line = Line(Point(self._x1, self._y1), Point(self._x1, self._y2))
        color = "black" if self.has_left_wall else "white"
        self._win.draw_line(line, color)

        # right wall
        line = Line(Point(self._x2, self._y1), Point(self._x2, self._y2))
        color = "black" if self.has_right_wall else "white"
        self._win.draw_line(line, color)

        # top wall
        line = Line(Point(self._x1, self._y1), Point(self._x2, self._y1))
        color = "black" if self.has_top_wall else "white"
        self._win.draw_line(line, color)

        # bottom wall
        line = Line(Point(self._x1, self._y2), Point(self._x2, self._y2))
        color = "black" if self.has_bottom_wall else "white"
        self._win.draw_line(line, color)

    def draw_move(self, to_cell, undo=False):
        self_center_x = (self._x1 + self._x2) / 2
        self_center_y = (self._y1 + self._y2) / 2
        to_cell_center_x = (to_cell._x1 + to_cell._x2) / 2
        to_cell_center_y = (to_cell._y1 + to_cell._y2) / 2

        line = Line(Point(self_center_x, self_center_y), Point(to_cell_center_x, to_cell_center_y))
        if undo:
            self._win.draw_line(line,"gray")
        else:
            self._win.draw_line(line,"red")

class Maze:
    def __init__(
            self,
            x1,
            y1,
            num_rows,
            num_cols,
            cell_size_x,
            cell_size_y,
            win = None,
            seed = None
        ):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win

        if seed is not None:
            random.seed(seed)
        else:
            random.seed(0)

        self._create_cells()

    def _create_cells(self):
        self._cells = []
        for ci in range(self._num_cols):
            new_column = []
            x_offset = self._x1 + self._cell_size_x * ci

            for ri in range(self._num_rows):
                y_offset = self._y1 + self._cell_size_y * ri
                top_left = Point(x_offset, y_offset)
                bottom_right = Point(x_offset + self._cell_size_x, y_offset + self._cell_size_y)
                new_cell = Cell(top_left, bottom_right, self._win)
                new_column.append(new_cell)

            self._cells.append(new_column)

        for ci in range(self._num_cols):
            for ri in range(self._num_rows):
                self._draw_cell(ci, ri)

        self._break_entrance_and_exit()
        self._break_walls_r(0,0)
        self._animate()

    def _draw_cell(self, i, j):
        self._cells[i][j].draw()

    def _animate(self):
        if not self._win:
            return
        self._win.redraw()
        sleep(0.05)

    def _break_entrance_and_exit(self):
        top_left_cell = self._cells[0][0]
        top_left_cell.has_top_wall = False
        top_left_cell.draw()

        bottom_right_cell = self._cells[self._num_cols - 1][self._num_rows - 1]
        bottom_right_cell.has_bottom_wall = False
        bottom_right_cell.draw()

    def _break_walls_r(self, i, j):
        current_cell = self._cells[i][j]
        current_cell._visited = True

        to_visit = ['l', 'r', 't', 'b']
        random.shuffle(to_visit)

        for dir in to_visit:
            if dir == "l" and i > 0 and not self._cells[i - 1][j]._visited:
                current_cell.has_left_wall = False
                self._cells[i - 1][j].has_right_wall = False
                self._break_walls_r(i - 1, j)

            elif dir == "r" and i < self._num_cols - 1 and not self._cells[i + 1][j]._visited:
                current_cell.has_right_wall = False
                self._cells[i + 1][j].has_left_wall = False
                self._break_walls_r(i + 1, j)

            elif dir == "t" and j > 0 and not self._cells[i][j - 1]._visited:
                current_cell.has_top_wall = False
                self._cells[i][j - 1].has_bottom_wall = False
                self._break_walls_r(i, j - 1)

            elif dir == "b" and j < self._num_rows - 1 and not self._cells[i][j + 1]._visited:
                current_cell.has_bottom_wall = False
                self._cells[i][j + 1].has_top_wall = False
                self._break_walls_r(i, j + 1)

        self._draw_cell(i, j)
