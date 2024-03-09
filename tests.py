import unittest

from maze import Maze

class Tests(unittest.TestCase):
  def test_maze_create_cells(self):
    num_cols = 10
    num_rows = 100
    m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
    self.assertEqual(
			len(m1._cells),
   		num_cols
		)
    self.assertEqual(
			len(m1._cells[0]),
   		num_rows
		)
    self.assertFalse(m1._cells[0][0].has_top_wall)
    self.assertFalse(m1._cells[num_cols - 1][num_rows - 1].has_bottom_wall)

if __name__ == "__main__":
	unittest.main()