import time
import numpy as np

EMPTY = 0

LEFT_UP = -9
UP = -8
RIGHT_UP = -7
LEFT = -1
RIGHT = 1
LEFT_DOWN = 7
DOWN = 8
RIGHT_DOWN = 9

DIRECTIONS = [
  LEFT_UP,
  UP,
  RIGHT_UP,
  LEFT,
  RIGHT,
  LEFT_DOWN,
  DOWN,
  RIGHT_DOWN
]

class Board():
  def reset(self):
    self.board = np.array([EMPTY] * 64, dtype=np.float32)
    self.board[35] = 1
    self.board[44] = 1
    self.board[36] = -1
    self.board[43] = -1
    self.winner = None
    self.missed = False
    self.done = False

  def move(self, act, turn):
    if self.can_move(act):
      self.board[act] = turn
      self.check_winner()
    else:
      self.winner = turn*-1
      self.missed = True
      self.done = True

  def check_winner(self):
    if EMPTY in self.board:
      return

    my_stones = self.board.count(1)
    enemy_stones = self.board.count(-1)

    if my_stones > enemy_stones:
      self.winner = 1
    elif my_stones == enemy_stones:
      self.winner = 0
    else:
      self.winner = -1

    self.done = True

  def get_empty_positions(self):
    """配置可能な位置の配列を返す
    """
    enemies = np.where(self.board==-1)[0]
    empties = []
    for pos in enemies:
      empties.extend([pos+direction for direction in DIRECTIONS if self.board[pos+direction] == EMPTY])

    empties = list(set(empties))
    return [pos for pos in empties if self.can_move(pos)]

  def can_move(self, pos):
    # 配置場所に既に石が存在
    if self.board[pos] != EMPTY:
      return False

    # 配置場所がボードの外
    if self.is_out_of_board(pos):
      return False

    # 配置場所に置いて石を裏返せるか
    if self.can_flip(pos) == False:
      return False

    return True

  def can_flip(self, pos):
    """石を裏返し可能か

    Args:
      pos(int): 石の配置場所

    Returns:
      bool: True 裏返し可能, False 裏返し不可能
    """
    for direction in DIRECTIONS:
      if self.exists_flip_poitions(pos, direction):
        return True

    return False

  def exists_flip_stones(self, pos, direction):
    """特定方向に裏返す石が存在するか

    Args:
      pos(int): 石の配置場所
      direction(int): 裏返しを確認する方向

    Returns:
      bool: True 裏返す石が存在, False 裏返す石が存在しない
    """
    positions = []
    next_position = pos+direction
    while self.is_out_of_board(next_position) == False:
      if self.board[next_position] == EMPTY:
        return False

      if self.board[next_position] == 1:
        if positions == []:
          return False

        positions.sort()
        for i in range(len(positions)-1):
          if (positions[i+1] - positions[i]) not in [1,7,8,9]:
            return False

        return True

      if self.board[next_position] == -1:
        positions.append(pos)

      next_position += direction

    return False

  def is_out_of_board(self, pos):
    return pos < 0 or 63 < pos

  def get_empty_pos(self):
      empties = np.where(self.board==EMPTY)[0]
      if len(empties) > 0:
        return np.random.choice(empties)
      else:
        return 0

  def show(self):
      row = "| {} | {} | {} | {} | {} | {} | {} | {} |"
      hr = "\n|{}|\n".format("-"*31)
      tempboard = []
      for i in self.board:
        if i == 1:
          tempboard.append("○")
        elif i == -1:
          tempboard.append("×")
        else:
          tempboard.append(" ")

      print((hr + row)*8 + hr).format(*tempboard)
      print("\n")
