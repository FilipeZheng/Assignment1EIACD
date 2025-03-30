from game import *
import random


def execute_random_move(game):      #player function
    move = random.choice(tuple(game.state.available_moves))
    game.state = game.state.move(move)

# The following dict is for heuristic funtions
strengths = {"Elephant":11,"Lion":11,"Tiger":10,"Leopard":6,"Wolf":5,"Dog":4,"Cat":3,"Mouse":2}

def Elephant_strength(state,pos,player):
    x,y = pos
    for pos1,animal in state.animals[3-player].items():
        if animal.type_ == "Mouse":
            x1,y1 = pos1
            return 9+min(5,max(abs(x1-x)+abs(y1-y),2))
    return 15

def find_strength(state,pos,player,animal):
        global strenghts
        if animal.type_ == "Elephant":
            return Elephant_strength(state,pos,player)
        else:
            return strengths[animal.type_]

def is_not_defended(state,pos,player):
    for pos1,animal in state.animals[3-player].items():
        if pos in map(lambda x: x[1],animal.available_moves(pos1,state)):
            return 0
    return 1
cache = {}

def store(func):        #decorator that stores function calls in cache
    def wrapper(*arg):
        global cache
        h = hash((func,*arg))
        if (t:=cache.get(h)): return t
        r = func(*arg)
        cache[h] = r
        return r
    return wrapper
# Maybe using decorators was a bad idea
@store
def heuristic(func):        # Add this decorator to heuristic functions to make it automatically calculate the difference between the heuristic of both players. Heuristic functions with this decorator should have at least 2 arguments: the first one being the state of the game and the last one being the player
    def wrapper(state):
        if state.winner != -1: return 0 if state.winner == 0 else float("-inf")*(-1)**state.winner
        r = func(state,player=1)-func(state,player=2)
        return r
    return wrapper

@heuristic
def number_heuristic(state,player):     #Used for valuing having animals, should be used with other heuristics to dilute the weight of STR
    return len(state.animals[player])


@heuristic
def strength_heuristic(state,player):
    global find_strength
    sum = 0
    for pos,animal in state.animals[player].items():
        strength = find_strength(state,pos,player,animal)
        sum += strength
    return sum

@heuristic
def pos_STR_heuristic(state,player):    #This heuristic weights around 0.2 times the strength one
    max_dist = state.board.height + state.board.width/2
    global find_strength
    sum = 0
    for i in state.board.lairs[3-player]: objx,objy = i
    for pos,animal in state.animals[player].items():
        strength = find_strength(state,pos,player,animal)
        x,y = pos
        dist = abs(objx-x)+abs(objy-y)
        if dist == 1: return 1000*is_not_defended(state,pos,player) 
        sum += strength*((max_dist-dist)/max_dist)
    return sum

@heuristic
def pos_STR_heuristic1(state,player):        #this heuristic function is supposed to value more moving forward pieces that are already close to the opposite lair even closer, and therefore also valuing more stopping the enemy from getting close
    global find_strength	        #This heuristic function weights on average around 0.2 times the strength one 
    max_dist = state.board.height + state.board.width/2
    sum = 0
    for i in state.board.lairs[3-player]: objx,objy = i
    for pos,animal in state.animals[player].items():
        strength = find_strength(state,pos,player,animal)
        x,y = pos
        dist = abs(objx-x)+abs(objy-y)-1
        if dist == 0: return 1000*is_not_defended(state,pos,player)
        sum += strength*(max_dist/(max_dist+dist*9))
    return sum

@heuristic
def mobility_heuristic(state,player):
    if state.player == player: return len(state.available_moves)
    return len(i for pos,animal in state.animals[3-player].items() for i in animal.available_moves(pos,state))

@heuristic
def mobility_heuristic1(state,player):   #This heuristic counts the amount of moves an animal can make and how beneficial those move are, it's a way of seeing more into the future without increasing the depth of minimax
    global find_strength	        #This heuristic function may weight on average around 0.5 times the strength one 
    max_dist = state.board.height + state.board.width/2
    sum = 0
    for i in state.board.lairs[3-player]: objx,objy = i
    for pos1,animal in state.animals[player].items():
        strength = find_strength(state,pos1,player,animal)
        for pos in animal.available_moves(pos1,state):
            x,y = pos[1]
            dist = abs(objx-x)+abs(objy-y)-1
            sum += strength*(max_dist/(max_dist+dist*9))
    return sum

@heuristic
def mobility_heuristic2(state,player):   #This heuristic values the potential to move forward rather than the amount of possible moves
    global find_strength	        #This heuristic function may weight on average around 0.2 times the strength one 
    max_dist = state.board.height + state.board.width/2
    sum = 0
    for i in state.board.lairs[3-player]: objx,objy = i
    for pos1,animal in state.animals[player].items():
        strength = find_strength(state,pos1,player,animal)
        x1,y1 = pos1
        min_dist = abs(objx-x1)+abs(objy-y1)-1
        for pos in animal.available_moves(pos1,state):
            x,y = pos[1]
            dist = abs(objx-x)+abs(objy-y)-1
            if dist == 0: sum += 100*is_not_defended(state,pos,player); break
            if dist < min_dist: min_dist = dist
        sum += strength*(max_dist/(max_dist+min_dist*9))
    return sum

@heuristic
def mobility_heuristic3(state,player):   #This heuristic values the potential to move forward rather than the amount of possible moves
    global find_strength	        #This heuristic function may weight on average around 0.2 times the strength one 
    max_dist = state.board.height + state.board.width/2
    sum = 0
    for i in state.board.lairs[3-player]: objx,objy = i
    for pos1,animal in state.animals[player].items():
        strength = find_strength(state,pos1,player,animal)
        x1,y1 = pos1
        min_dist = abs(objx-x1)+abs(objy-y1)
        for pos in animal.available_moves(pos1,state):
            x,y = pos[1]
            dist = abs(objx-x)+abs(objy-y)
            if dist < min_dist: min_dist = dist
            if dist == 1: sum += 100*is_not_defended(state,pos,player); break
        sum += strength*((max_dist-min_dist)/max_dist)
    return sum

@store
def heuristic1(state):
    return number_heuristic(state)+pos_STR_heuristic(state)*5.0 + 2.5*mobility_heuristic2(state)

@store
def heuristic2(state):
    return number_heuristic(state)*2 + strength_heuristic(state) + 5*pos_STR_heuristic1(state)

@store
def heuristic3(state):
    return strength_heuristic(state)+pos_STR_heuristic(state)*3 + 5*mobility_heuristic2(state)


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
        if not nextMove: nextMove = random.choice(tuple(state.available_moves))
        return (nextMove,alpha if player==1 else beta)


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
           "AI1":execute_minimax_move(pos_STR_heuristic,4),
           "AI2":execute_minimax_move(heuristic3,4),
           "AI3":execute_minimax_move(heuristic1,4)
           }   

