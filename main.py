from tkinter import Tk, BOTH, Canvas

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
    def __init__(self, top_left_point, bottom_right_point, window):
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

def main():
    win = Window(800, 600)
    p1 = Point(20,20)
    p2 = Point(40,40)
    p3 = Point(40,20)
    p4 = Point(60,40)

    c1 = Cell(p1, p2, win)
    c2 = Cell(p3, p4, win)
    c1.has_bottom_wall = False
    c2.has_top_wall = False
    c1.draw()
    c2.draw()

    c1.draw_move(c2)

    win.wait_for_close()

main()