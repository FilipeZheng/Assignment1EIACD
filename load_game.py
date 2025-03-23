from game import *
from players import *
class Game():
    def __init__(self, player_1, player_2,board_=board0,p1_animals=INITIAL_P1_ANIMALS,p2_animals=INITIAL_P2_ANIMALS):
        self.board = board_
        self.initial_state = State(board0,p1_animals,p2_animals)
        self.player_1 = player_1
        self.player_2 = player_2
        self.log = []

    def play(self):
        if self.state.player == 1:
            self.player_1(self)
        else:                
            self.player_2(self)    
    def start(self, log_moves = False,log_game = True):
        self.state = deepcopy(self.initial_state)
        game_log = [self.state]
        self.log.append(game_log)
        while True:
            if log_moves:
                print(repr(self.state))
                self.play()
            if log_game:
                game_log.append(self.state)
            if (w:=self.state.winner) != -1:
                break
        if log_moves:
            print(repr(self.state))
            if self.state.winner == 0:
                print(f"End of game! Draw!")
            elif self.state.winner in (1,2):
              print(f"End of game! Player {self.state.winner} wins!")
        return w
    def run_n_matches(self, n, max_time = 3600, log_moves = False):
        start_time = time.time()

        results = [0,0,0] # [player 1 victories, player 2 victories]

        # Your Code Here
        for _ in range(n):
          results[self.start(log_moves)] += 1
          if time.time()-start_time > max_time:
            break
        print("\n=== Elapsed time: %s seconds ===" % (int(time.time() - start_time)))
        print(f"  Player 1: {results[0]} victories")
        print(f"  Player 2: {results[1]} victories")
        print("===============================")
    def run_match(self,log_moves=True):
        self.start(log_moves)


if __name__ == "__main__":
    game = Game(players["Human"], players["Human"])
    game.run_match()

