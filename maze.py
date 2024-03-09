from tkinter import Tk, BOTH, Canvas
from time import sleep

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

    def draw(self):
        if not self._win:
            return
        if self.has_left_wall:
            line = Line(Point(self._x1, self._y1), Point(self._x1, self._y2))
            self._win.draw_line(line, "black")
        if self.has_right_wall:
            line = Line(Point(self._x2, self._y1), Point(self._x2, self._y2))
            self._win.draw_line(line, "black")
        if self.has_top_wall:
            line = Line(Point(self._x1, self._y1), Point(self._x2, self._y1))
            self._win.draw_line(line, "black")
        if self.has_bottom_wall:
            line = Line(Point(self._x1, self._y2), Point(self._x2, self._y2))
            self._win.draw_line(line, "black")

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
        ):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
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
                new_cell.draw()
                #self._draw_cell(ci, ri)
            self._cells.append(new_column)
        self._animate()

    def _draw_cell(self, i, j):
        # Whats the point of this if we already have Cell.draw()???
        pass

    def _animate(self):
        if not self._win:
            return
        self._win.redraw()
        sleep(0.05)