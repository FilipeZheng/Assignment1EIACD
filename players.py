from game import *
import random


def execute_random_move(game):      #player function
    move = random.choice(tuple(game.state.available_moves))
    game.state = game.state.move(move)

# The following dict is for heuristic funtions
strengths = {"Elephant":10,"Lion":9,"Tiger":8,"Leopard":5,"Wolf":4,"Dog":3,"Cat":2,"Mouse":1}


# Maybe using decorators was a bad idea
def heuristic(func):        # Add this decorator to heuristic functions to make it automatically calculate the difference between the heuristic of both players. Heuristic functions with this decorator should have at least 2 arguments: the first one being the state of the game and the last one being the player
    def wrapper(state):
        return func(state,player=1)-func(state,player=2)    # *args is for in case the heuristic function requires more arguments than just the player and the state
    return wrapper

@heuristic
def strength_heuristic(state,player):
    global strengths
    sum = 0
    for animal in state.animals[player].values():
        sum += strengths[animal.type_]
    return sum

@heuristic
def pos_STR_heuristic(state,player):
    max_dist = 15
    global strengths
    sum = 0
    for i in state.board.lairs[3-player]: objx,objy = i
    for pos,animal in state.animals[player].items():
        x,y = pos
        sum += strengths[animal.type_]*(15-(abs(objx-x)+abs(objy-y)))
    return sum
  
# There are more heuristic functions to make

def execute_minimax_move(evaluate_func, depth):
    def execute(game):                                  # This is the function the function will return
      move,h = minimax(game.state,depth,float("-inf"),float("inf"),game.state.player,evaluate_func)
      print(h)
      game.state=game.state.move(move)
    return execute

def minimax(state, depth, alpha, beta, player, evaluate_func)->(list,int):
        if not depth: return (None,evaluate_func(state))
        if state.winner != -1: return (None,0) if state.winner == 0 else (None,float("-inf")*(-1)**state.winner)
        nextMove = None
        moves = tuple(map(lambda move: (move,state.move(move)),state.available_moves))
        if player == 1:
          for move,new_state in sorted(moves,key=lambda x:-evaluate_func(x[1])):
            t=minimax(new_state,depth-1,alpha,beta,3-player,evaluate_func)[1]
            if t>=beta:
              return (move,t+1)
            if t>alpha:
              alpha=t
              nextMove = move
        elif player == 2:
          for move,new_state in sorted(moves,key=lambda x:evaluate_func(x[1])):
            t=minimax(state.move(move),depth-1,alpha,beta,3-player,evaluate_func)[1]
            if t<=alpha:
              return (move,t-1)
            if t<beta:
              nextMove = move
              beta=t
        return (nextMove if nextMove else random.choice(tuple(state.available_moves)),alpha if player==1 else beta)

""" #The following program is an attempt at making minimax random when choosing between two moves that seem to have equal outcomes
def execute_minimax_move(evaluate_func, depth):     #This is for generating a player
    def execute(game):                                  # This is the function the function will return
      move = minimax(game.state,depth,float("-inf"),float("inf"),game.state.player,evaluate_func)[0]
      game.state=game.state.move(random.choice(move))   # I decided that the AI would randomly choose a move from the best possible moves to allow some changes in the outcomes of the game when simulating multiple times the same match with the same minimax AIs
    return execute


def minimax(state, depth, alpha, beta, player, evaluate_func)->(list,int):
        if not depth: return ([],evaluate_func(state))
        if state.winner != -1: return ([],0) if state.winner == 0 else ([],float("-inf")*(-1)**state.winner)
        nextMove = []
        if player == 1:
          for move in state.available_moves:
            t=minimax(state.move(move),depth-1,alpha,beta,3-player,evaluate_func)[1]
            if t>=beta:
              return ([move],t+1)
            if t>alpha:
              alpha=t
              nextMove = [move]
            elif t== alpha:
              nextMove.append(move)
        elif player == 2:
          for move in state.available_moves:
            t=minimax(state.move(move),depth-1,alpha,beta,3-player,evaluate_func)[1]
            if t<=alpha:
              return ([move],t-1)
            if t<beta:
              nextMove = [move]
              beta=t
            elif t==beta:
              nextMove.append(move)
        return (nextMove,alpha if player==1 else beta)
"""


#minimax(State(board0,INITIAL_P1_ANIMALS,INITIAL_P2_ANIMALS),2,float("-inf"),float("inf"),1,pos_STR_heuristic)


def human_player(game):
    #print(repr(game.state))
    #print(game.state.available_moves)
    print(f"Player {game.state.player}:")
    while True:
        i = input()
        try:
            x1,y1,x2,y2 = map(int,tuple(i))
        except: pass
        if (a:=((x1,y1),(x2,y2))) in game.state.available_moves:
            break
    game.state = game.state.move(a)


players = {"Human":human_player,             #This dict will be read for choosing the players who are going to play the game
           "Random":execute_random_move,
           "AI1":execute_minimax_move(pos_STR_heuristic,4)
           }   

