import time
from board import Board
from randomAct import RandomActor
from dqn import QFunction
import chainer
import chainerrl
import numpy as np

# 学習ゲーム回数
N_EPISODES = 20000

# イプシロンの上限値
END_EPSILON = 0.2

if __name__ == "__main__":
  # ボードの準備
  board = Board()
  ra = RandomActor(board)

  # 環境と行動の次元数
  obs_size = 64
  n_actions = 64

  # Q-functionとオプティマイザのセットアップ
  q_func = QFunction(obs_size, n_actions)
  optimizer = chainer.optimizers.Adam(eps=1e-2)
  optimizer.setup(q_func)

  # 報酬の割引率
  gamma = 0.95

  # Epsilon-greedyを使ってたまに冒険。50000ステップでend_epsilonとなる
  explorer = chainerrl.explorers.LinearDecayEpsilonGreedy(
    start_epsilon=1.0, end_epsilon=END_EPSILON, decay_steps=100000, random_action_func=ra.random_action_func
  )

  # Experience ReplayというDQNで用いる学習手法で使うバッファ
  replay_buffer = chainerrl.replay_buffer.ReplayBuffer(capacity=10 ** 6)

  # Agentの生成(replay_bufferなどを共有する2つ)
  agent_p1 = chainerrl.agents.DoubleDQN(
    q_func, optimizer, replay_buffer, gamma, explorer,
    replay_start_size=500, update_interval=1,
    target_update_interval=100
  )
  agent_p2 = chainerrl.agents.DoubleDQN(
    q_func, optimizer, replay_buffer, gamma, explorer,
    replay_start_size=500, update_interval=1,
    target_update_interval=100
  )

  # カウンタの宣言
  miss = 0
  win = 0
  draw = 0

  # エピソードの繰り返し実行
  for i in range(1, N_EPISODES + 1):
    board.reset()
    reward = 0
    agents = [agent_p1, agent_p2]
    turn = np.random.choice([0, 1])
    last_state = None
    while not board.done:
      # 配置マス取得
      action = agents[turn].act_and_train(board.board.copy(), reward)
      # 配置を実行
      board.move(action, 1)

      # 配置の結果、終了時には報酬とカウンタに値をセットして学習
      if board.done == True:
        if board.winner == 1:
          reward = 1
          win += 1
        elif board.winner == 0:
          draw += 1
        else:
          reward = -1

        if board.missed is True:
          miss += 1

        # エピソードを終了して学習
        agents[turn].stop_episode_and_train(board.board.copy(), reward, True)

        # 相手もエピソードを終了して学習。相手のミスは勝利として学習しないように
        if agents[1 if turn == 0 else 0].last_state is not None and board.missed is False:
          # 前のターンでとっておいたlast_stateをaction実行後の状態として渡す
          agents[1 if turn == 0 else 0].stop_episode_and_train(last_state, reward*-1, True)
      else:
        # 学習用にターン最後の状態を把握
        last_state = board.board.copy()
        # 継続のときは盤面の値を反転
        board.board = board.board * -1
        # ターンを切り替え
        turn = 1 if turn == 0 else 0

    # コンソールに進捗表示
    if i % 100 == 0:
      print("episode:", i, " / rnd:", ra.random_count, " / miss:", miss, " / win:", win, " / draw:", draw, " / statistics:", agent_p1.get_statistics(), " / epsilon:", agent_p1.explorer.epsilon)
      # カウンタの初期化
      miss = 0
      win = 0
      draw = 0
      ra.random_count = 0

    if i % 10000 == 0:
      # 10000エピソードごとにモデルを保存
      agent_p1.save("models/result_" + str(i))

  print("Training finished.")
