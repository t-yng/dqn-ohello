import numpy as np

class RandomActor:
  def __init__(self, board):
    self.board = board
    self.random_count = 0

  def random_action_func(self):
    self.random_count += 1
    empties = self.board.get_empty_positions()

    if len(empties) > 0:
      return np.random.choice(empties)
    else:
      return 0
