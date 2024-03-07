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
        # canvas draw lines and stuff

def main():
    win = Window(800, 600)
    p1 = Point(20,20)
    p2 = Point(70,70)
    p3 = Point(80,10)
    p4 = Point(90,150)
    l1 = Line(p1, p2)
    l2 = Line(p3, p4)

    win.draw_line(l1, "black")
    win.draw_line(l2, "red")

    win.wait_for_close()

main()