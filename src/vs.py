import numpy as np
import chainer
import chainerrl
from humanPlayer import HumanPlayer
from board import Board
from randomAct import RandomActor
from dqn import QFunction

if __name__ == "__main__":
  # ボードの準備
  board = Board()
  ra = RandomActor(board)

  # 環境と行動の次元数
  obs_size = 9
  n_actions = 9

  # Q-functionとオプティマイザのセットアップ
  q_func = QFunction(obs_size, n_actions)
  optimizer = chainer.optimizers.Adam(eps=1e-2)
  optimizer.setup(q_func)

  # 報酬の割引率
  gamma = 0.95

  # Epsilon-greedyを使ってたまに冒険。50000ステップでend_epsilonとなる
  explorer = chainerrl.explorers.LinearDecayEpsilonGreedy(
    start_epsilon=1.0, end_epsilon=0.3, decay_steps=50000, random_action_func=ra.random_action_func
  )

  # Experience ReplayというDQNで用いる学習手法で使うバッファ
  replay_buffer = chainerrl.replay_buffer.ReplayBuffer(capacity=10 ** 6)

  # Agentの生成(replay_bufferなどを共有する2つ)
  agent = chainerrl.agents.DoubleDQN(
    q_func, optimizer, replay_buffer, gamma, explorer,
    replay_start_size=500, update_interval=1,
    target_update_interval=100
  )
  agent.load("result_100000")

  humanPlayer = HumanPlayer()
  board = Board()

  for i in range(1):
    board.reset()
    dqn_first = np.random.choice([True, False])
    while not board.done:
      # DQN
      if dqn_first or np.count_nonzero(board.board) > 0:
        board.show()
        action = agent.act(board.board.copy())
        board.move(action, 1)

        if board.done:
          board.show()
          if board.winner == 1:
            print("DQN Win")
          elif board.winner == 0:
            print("Draw")
          else:
            print("DQN Missed")

          agent.stop_episode()
          continue

      # 人間
      board.show()
      action = humanPlayer.act(board.board.copy())
      board.move(action, -1)
      if board.done:
        board.show()
        if board.winner == -1:
          print("Human Win")
        elif board.winner == 0:
          print("Draw")
        agent.stop_episode()

  print("VS finished.")

