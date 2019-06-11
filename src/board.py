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
    self.winner = None
    self.missed = False
    self.done = False

  def move(self, act, turn):
    if self.board[act] == 0:
      self.board[act] = turn
      self.check_winner()
    else:
      self.winner = turn*-1
      self.missed = True
      self.done = True

  def check_winner(self):
    if EMPTY in self.board:
      return

    myStones = self.board.count(1)
    enemyStones = self.board.count(-1)

    if myStones > enemyStones:
      self.winner = 1
    elif myStones == enemyStones:
      self.winner = 0
    else:
      self.winner = -1

    self.done = True

  def get_empty_positions(self):
    """配置可能な位置の配列を返す
    """
    enemies = np.where(self.board==-1)[0]
    positions = []
    for pos in enemies:
      for direction in DIRECTIONS:
        if self.can_move(pos, direction):
          positions.append(pos+direction)

    return positions

  def can_move(self, pos, direction):
    nextPosition = pos+direction

    # 配置場所に既に石が存在
    if self.board[nextPosition] != EMPTY:
      return False

    # 配置場所がボードの外
    if is_out_of_board(pos, direction):
      return False

    # 配置場所に置いて石を裏返せるか
    if self.can_flip(nextPosition) == False:
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
    while self.is_out_of_board(pos, direction) == False:
      nextPosition = pos + direction

      if self.board[nextPosition] == 1:
        return positions != []

      if self.board[nextPosition] == -1:
        positions.append(nextPosition)

    return False

  def is_out_of_board(self, pos, direction):
    isOutOfBoard = False
    if pos % 8 == 0:
      isOutOfBoard = isOutOfBoard or direction in [LEFT_UP, LEFT, LEFT_DOWN]

    if pos % 8 == 7:
      isOutOfBoard = isOutOfBoard or direction in [RIGHT_UP, RIGHT, RIGHT_DOWN]

    nextPostion = pos + direction
    isOutOfBoard = isOutOfBoard or nextPostion < 0 or 63 < nextPostion

    return isOutOfBoard

  def get_empty_pos(self):
      empties = np.where(self.board==EMPTY)[0]
      if len(empties) > 0:
        return np.random.choice(empties)
      else:
        return 0

  def show(self):
      row = " {} | {} | {} "
      hr = "\n-----------\n"
      tempboard = []
      for i in self.board:
        if i == 1:
          tempboard.append("○")
        elif i == -1:
          tempboard.append("×")
        else:
          tempboard.append(" ")

      print((row + hr + row + hr + row).format(*tempboard))
      print("\n")
