from maze import Maze, Window

def run():
    win = Window(800, 600)
    mz = Maze(5,5,15,15,20,20,win)

    win.wait_for_close()

run()