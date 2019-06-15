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

  def test_move_when_finish_game_with_win(self):
    self.board.board = self.__make_board_array([
      [-1, -1, -1, -1, -1, -1, -1, -1],
      [-1, -1, -1, -1, -1, -1, -1, -1],
      [1, 1, 1, 1, 1, 1, 1, 1],
      [1, 1, 1, 1, 1, 1, 1, 1],
      [1, 1, 1, 1, 1, 1, 1, 1],
      [1, 1, 1, 1, 1, 1, 1, 1],
      [1, 1, 1, 1, 1, 1, -1, 1],
      [1, 1, 1, 1, 1, 1, 1, 0],
    ])

    self.board.move(63, 1)

    self.assertEqual(self.board.winner, 1)
    self.assertTrue(self.board.done)

  def test_move_when_finish_game_with_draw(self):
    self.board.board = self.__make_board_array([
      [-1, -1, -1, -1, -1, -1, -1, -1],
      [-1, -1, -1, -1, -1, -1, -1, -1],
      [-1, -1, -1, -1, -1, -1, -1, -1],
      [-1, -1, -1, -1, -1, -1, -1, -1],
      [1, 1, 1, 1, 1, 1, 1, 1],
      [1, 1, 1, 1, 1, 1, 1, 1],
      [1, 1, 1, 1, 1, 1, -1, 1],
      [1, 1, 1, 1, 1, 1, 1, 0],
    ])

    self.board.move(63, 1)

    self.assertEqual(self.board.winner, 0)
    self.assertTrue(self.board.done)

  def test_move_when_finish_game_with_lose(self):
    self.board.board = self.__make_board_array([
      [-1, -1, -1, -1, -1, -1, -1, -1],
      [-1, -1, -1, -1, -1, -1, -1, -1],
      [-1, -1, -1, -1, -1, -1, -1, -1],
      [-1, -1, -1, -1, -1, -1, -1, -1],
      [-1, -1, -1, -1, -1, -1, -1, -1],
      [1, 1, 1, 1, 1, 1, 1, 1],
      [1, 1, 1, 1, 1, 1, -1, 1],
      [1, 1, 1, 1, 1, 1, 1, 0],
    ])

    self.board.move(63, 1)

    self.assertEqual(self.board.winner, -1)
    self.assertTrue(self.board.done)

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

  def test_move_flip_stones_when_edge(self):
    self.board.board = self.__make_board_array([
      [0, -1, -1, 1, 0, 0, 0, 0],
      [-1, 0, 0, 0, 0, 0, 0, 0],
      [1, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0],
    ])

    expected = self.__make_board_array([
      [1, 1, 1, 1, 0, 0, 0, 0],
      [1, 0, 0, 0, 0, 0, 0, 0],
      [1, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0],
    ])

    self.board.move(0, 1)
    np.testing.assert_array_equal(self.board.board, expected)
    self.assertEqual(self.board.missed, False)

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

  def test_get_empty_positions_when_reset(self):
    [
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 1, -1, 0, 0, 0],
      [0, 0, 0, -1, 1, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0],
    ]

    result = self.board.get_empty_positions()
    expected = [20, 29, 34, 43]
    result.sort()
    expected.sort()
    self.assertEqual(result, expected)

  def test_get_empty_positions(self):
    self.board.board = self.__make_board_array([
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 1, 0, 0, 0, 0],
      [0, 0, -1, 1, -1, 0, 0, 0],
      [0, 0, 0, -1, -1, 0, 0, 0],
      [0, 0, 0, 1, -1, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0],
    ])

    result = self.board.get_empty_positions()
    expected = [25, 29, 33, 37, 45]

    result.sort()
    expected.sort()
    self.assertEqual(result, expected)

  def __make_board_array(self, board):
    return np.array(board, dtype=np.float32).ravel()


if __name__=='main':
  unittest.main()