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
    self.board[27] = 1
    self.board[36] = 1
    self.board[28] = -1
    self.board[35] = -1
    self.winner = None
    self.missed = False
    self.done = False

  def move(self, act, turn):
    if self.__can_move(act):
      self.board[act] = turn
      for pos in self.__get_flip_positions(act):
        self.board[pos] = turn
      self.__check_winner()
    else:
      self.winner = turn*-1
      self.missed = True
      self.done = True

  def get_empty_positions(self):
    """配置可能な位置の配列を返す
    """
    enemies = np.where(self.board==-1)[0]
    empties = []
    for pos in enemies:
      for direction in DIRECTIONS:
        if self.__is_out_of_board(pos+direction) == False and self.board[pos+direction] == EMPTY:
          empties.append(pos+direction)

    empties = list(set(empties))
    return [pos for pos in empties if self.__can_move(pos)]

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

  def __check_winner(self):
    if EMPTY in self.board:
      return

    my_stones = np.count_nonzero(self.board == 1)
    enemy_stones = np.count_nonzero(self.board == -1)

    if my_stones > enemy_stones:
      self.winner = 1
    elif my_stones == enemy_stones:
      self.winner = 0
    else:
      self.winner = -1

    self.done = True

  def __can_move(self, pos):
    # 配置場所に既に石が存在
    if self.board[pos] != EMPTY:
      return False

    # 配置場所に置いて石を裏返せるか
    if self.__can_flip(pos) == False:
      return False

    return True

  def __can_flip(self, pos):
    """石を裏返し可能か

    Args:
      pos(int): 石の配置場所

    Returns:
      bool: True 裏返し可能, False 裏返し不可能
    """
    for direction in DIRECTIONS:
      if self.__exists_flip_stones(pos, direction):
        return True

    return False

  def __get_flip_positions(self, pos):
    positions = []
    for direction in DIRECTIONS:
      temp_positions = []
      next_position = pos+direction
      while self.__is_out_of_board(next_position) == False:
        if self.board[next_position] == EMPTY:
          break

        if self.board[next_position] == -1 and self.__is_edge_of_board(next_position):
          break

        if self.board[next_position] == 1:
          positions.extend(temp_positions)
          break

        if self.board[next_position] == -1:
          temp_positions.append(next_position)

        next_position += direction

    return list(set(positions))

  def __exists_flip_stones(self, pos, direction):
    """特定方向に裏返す石が存在するか

    Args:
      pos(int): 石の配置場所
      direction(int): 裏返しを確認する方向

    Returns:
      bool: True 裏返す石が存在, False 裏返す石が存在しない
    """
    positions = []
    next_position = pos+direction
    while self.__is_out_of_board(next_position) == False:
      if self.board[next_position] == EMPTY:
        return False

      if self.board[next_position] == -1 and self.__is_edge_of_board(next_position):
        return False

      if self.board[next_position] == 1:
        return positions != []

      if self.board[next_position] == -1:
        positions.append(pos)

      next_position += direction

    return False

  def __is_edge_of_board(self, pos):
    if pos % 8 == 0: # 左端
      return True

    if pos % 8 == 7: # 右端
      return True

    if pos >= 0 and pos <= 7: # 上端
      return True

    if pos >= 56 and pos <= 63: # 下端
      return True

    return False

  def __is_out_of_board(self, pos):
    return pos < 0 or 63 < pos
