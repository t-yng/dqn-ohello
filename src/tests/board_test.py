import unittest
import numpy as np
from ..board import Board

class BoardTestCase(unittest.TestCase):
  def setUp(self):
    self.board = Board()
    self.board.reset()

  def test_reset(self):
    self.board.reset()

    expectedBoard = np.array([
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 1, -1, 0, 0, 0],
      [0, 0, 0, -1, 1, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0],
    ], dtype=np.float32).ravel()
    np.testing.assert_array_equal(self.board.board, expectedBoard)

    self.assertEqual(self.board.winner, None)
    self.assertEqual(self.board.missed, False)
    self.assertEqual(self.board.done, False)

  def test_move_when_act_is_correct(self):
    self.board.move(5*8+3, 1)

    expected = self.__make_board_array([
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 1, -1, 0, 0, 0],
      [0, 0, 0, 1, 1, 0, 0, 0],
      [0, 0, 0, 1, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0],
    ])

    np.testing.assert_array_equal(self.board.board, expected)
    self.assertEqual(self.board.missed, False)

  def test_move_flip_stones(self):
    self.board.board = self.__make_board_array([
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, -1, -1, -1, -1, 1],
      [0, 0, 0, -1, 1, 0, 0, 0],
      [0, 0, 0, 1, 1, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0],
    ])

    expected = self.__make_board_array([
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 1, 1, 1, 1, 1, 1],
      [0, 0, 0, 1, 1, 0, 0, 0],
      [0, 0, 0, 1, 1, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0],
    ])

    self.board.move(26, 1)
    np.testing.assert_array_equal(self.board.board, expected)

  def test_move_when_act_position_has_a_stone_already(self):
    self.board.move(27, 1)
    self.assertTrue(self.board.missed)

  def test_move_when_act_postion_has_no_flip_stones(self):
    self.board.board = self.__make_board_array([
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 1, -1, 0, 0, 0],
      [0, 0, 0, 1, 1, -1, 0, 0],
      [0, 0, 0, 1, 0, 0, -1, 0],
      [0, 0, 0, 0, 0, 0, 0, -1],
      [0, 0, 0, 0, 0, 0, 0, 0],
    ])

    positions = [0, 19, 26]

    for pos in positions:
      self.board.reset()
      with self.subTest(pos=pos):
        self.board.move(pos, 1)
        self.assertTrue(self.board.missed)

  def __make_board_array(self, board):
    return np.array(board, dtype=np.float32).ravel()


if __name__=='main':
  unittest.main()