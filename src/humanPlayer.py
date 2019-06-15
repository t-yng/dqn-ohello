class HumanPlayer:
  def act(self, board):
    valid = False
    while not valid:
      try:
        act = input("Please Enter 1-9: ")
        act = int(act)
        if act >= 1 and act <= 9 and board[act-1] == 0:
          valid = True
          return act - 1
        else:
          print("Invalid move")
      except Exception as e:
        print(act + "is invalid")