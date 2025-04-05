from game import *
from players import *
class Game():
    def __init__(self, player_1, player_2,board_=board0):
        self.board = board_
        self.state = State(board_)
        self.player_1 = player_1
        self.player_2 = player_2
        self.log = []
        self.turns = 0

    def play(self):     # function used to make a play
        while True:
            if self.state.player == 1:
                t = self.player_1(self)
            else:                
                t = self.player_2(self)
            if t :        # t != 0 means going back two moves
                if self.turns>1:
                    del self.log[-1]
                    del self.log[-1]
                    self.turns -= 2
                    self.state = self.log[-1]
            else:
                self.turns += 1
                return
    def start(self, log_moves = False,log_game = True):
        self.log.append(self.state)
        while True:
            if log_moves:
                print(repr(self.state))
            self.play()
            if log_game:
                self.log.append(self.state)
            if (w:=self.state.winner) != -1:
                break
        if log_moves:
            print(repr(self.state))
            if self.state.winner == 0:
                print(f"End of game! Draw!")
            elif self.state.winner in (1,2):
              print(f"End of game! Player {self.state.winner} wins!")
        return w
    def run_match(self,log_moves=True):
        self.start(log_moves)


if __name__ == "__main__":
    game = Game(players["Human"], players["Human"])
    game.run_match()

