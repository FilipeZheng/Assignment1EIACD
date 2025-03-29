from copy import deepcopy
class animal():
    def __init__(self,type_:str,player:int):
        self.type_ = type_
        self.player = player
        self.rank = ["Mouse","Cat","Dog","Wolf","Leopard","Tiger","Lion","Elephant"].index(type_)       #using a dictionary is perhaps better
        self.isInTrap = False
        self.isInWater = False
        self.canJump = True if type_ in ("Lion","Tiger") else False
    def __str__(self):              #currently a placeholder
        return f"{chr(-self.rank+40+self.player*32)}"

    def __le__(self,other):         #this allows operations such as animal1 <= animal2 for comparing if an animal can capture another one
        if not isinstance(other,animal):
            raise "Error"
        if self.isInTrap: return True           #in case the animal is in a trap
        if self.type_ == "Elephant" and other.type_ == "Mouse" and not other.isInWater:     #in case the comparison is between a mouse and an elephant
            return True
        if self.type_ == "Mouse" and other.type_ == "Elephant":
            return False
        return self.rank <= other.rank

    def available_moves(self,cur_pos,state)-> dict:
        def move(dir,cur_pos):          #returns None if the movement is invalid and the target pos if the movement is valid
            x,y = cur_pos
            next_pos = (x+dir[0],y+dir[1])
            if next_pos[0]<0 or next_pos[0]>=state.board.width or next_pos[1]<0 or next_pos[1]>=state.board.height: return
            if next_pos in state.animals[self.player]: return               # cannot move to a tile with an animal of the same player
            if next_pos in state.board.water:
                if self.canJump and not next_pos in state.animals[3-self.player]: # checks in case the animal can jump and whether there is a mouse in the water
                    return move(dir,next_pos)
                if self.type_ != "Mouse":
                    return
            if (a:= state.animals[3-self.player].get(next_pos)):
                if self >= a:
                    return next_pos
                return
            if next_pos in state.board.lairs[self.player]: return
            return next_pos
        moves = set()
        x,y = cur_pos
        for dir in ((1,0),(-1,0),(0,1),(0,-1)):   #the tuple contains the 4 directions an animal may move
            if (next_pos:= move(dir,cur_pos)):
                moves.add((cur_pos,next_pos))
        return moves


class board:        # used for representing the initial board, does not include the animals
    def __init__(self,empty_board:list,initial_p1_animals,initial_p2_animals):
        self.width = len(empty_board[0])
        self.height = len(empty_board)
        self.water = set()
        self.traps = {1:set(),2:set()}      # traps in 1 represent traps where player1 is vulnerable
        self.lairs = {1:set(),2:set()}      # lairs in 1 represent the goals of player2
        trans = str.maketrans("012345","._##OO")    # 1 represents water, 2: p1_traps, 3: p2_traps, 4: p1_lair, 5: p2_lair
        self.empty_board = [s.translate(trans) for s in empty_board]
        for y,row in enumerate(empty_board):
            for x,tile in enumerate(row):
                if tile != "0":
                    {"1":self.water,"2":self.traps[1],"3":self.traps[2],"4":self.lairs[1],"5":self.lairs[2]}[tile].add((x,y))

        self.animals = {1:initial_p1_animals,2:initial_p2_animals} #the choic of using a dict is for making selecting animals easier

INITIAL_P2_ANIMALS = {(0,0):animal("Lion",2),           #the dictionaries contain the coordinates of every animal and their coordinates as the keys
                    (6,0):animal("Tiger",2),            #dictionaries are useful for checking if a tile has an animal and to know where a player has animals
                    (1,1):animal("Dog",2),              #In case putting everything in an array is preffered, we can make an interpreter that creates those dictionaries by reading the array
                    (5,1):animal("Cat",2),
                    (0,2):animal("Mouse",2),
                    (2,2):animal("Leopard",2),
                    (4,2):animal("Wolf",2),
                    (6,2):animal("Elephant",2)}

INITIAL_P1_ANIMALS  ={(0,6):animal("Elephant",1),
                    (2,6):animal("Wolf",1),
                    (4,6):animal("Leopard",1),
                    (6,6):animal("Mouse",1),
                    (1,7):animal("Cat",1),
                    (5,7):animal("Dog",1),
                    (0,8):animal("Tiger",1),
                    (6,8):animal("Lion",1)}


board0 = board(["0025200",
                "0002000",
                "0000000",
                "0110110",
                "0110110",
                "0110110",
                "0000000",
                "0003000",
                "0034300"
                ], INITIAL_P1_ANIMALS,INITIAL_P2_ANIMALS)

board1 = board(["02520",
                "00200",
                "01010",
                "00300",
                "03430"
                ],
                {(4,4):animal("Lion",1),
                (0,4):animal("Tiger",1),
                (3,3):animal("Elephant",1),
                (1,3):animal("Mouse",1)
                }
               ,
               {(0,0):animal("Lion",2),
                (4,0):animal("Tiger",2),
                (1,1):animal("Elephant",2),
                (3,1):animal("Mouse",2)}
               )

"""                                 # Old program
EMPTY_BOARD = ["..#0#..",              #The way I thought about displaying the board is by getting the empty board and pasting all the animals on it
                "...#...",            #This board is independent from how the game works, its only purpose is to act as the background
                ".......",
                ".__.__.",
                ".__.__.",
                ".__.__.",
                ".......",
                "...#...",
                "..#0#.."]

WATER = {(1,3),(2,3),(4,3),(5,3),           
        (1,4),(2,4),(4,4),(5,4),
        (1,5),(2,5),(4,5),(5,5)}

TRAPS = {1:{(2,0),(4,0),(3,1)},
        2:{(2,8),(4,8),(3,7)}}

LAIRS = {2:(3,0),1:(3,8)}
"""



class State():              #object with one state of the game
    def __init__(self,board_):
        self.board = board_
        self.animals = self.board.animals   #made for selecting animals easier as the animals weren't originally stored in the board
        self.player = 1                 # player refers to the player who's going to make the next play
        self.available_moves = set()    # the format of the moves in the set is (start,dest)
        self.update_available_moves()   #func that is defined below
        self.winner = -1
        self.turns_since_last_capture = 0

    def update_available_moves(self):                   #adds the elements to the dict
        self.available_moves.clear()
        for pos,ani in self.animals[self.player].items():
            moves = ani.available_moves(pos,self)           
            self.available_moves.update(moves)              # Another way of programming this would've been making the animals update the dict directly, but having the animals creating a seperate dict helps for seeing the available moves a specific animal has

    def update_winner(self):
        if self.turns_since_last_capture >= 100:
            self.winner = 0
        if not self.available_moves:
            self.winner = 3-self.player
        for lair in self.board.lairs[self.player]:
            if lair in self.animals[3-self.player]:
                self.winner = 3-self.player

    def __repr__(self):                 #used for converting into a string using the repr() function, may delete this because the code isn't very readable, a display function should do the trick
        return "\n".join("".join(str(a[(x,y)]) if (x,y) in (a:=self.animals[1]) else str(a[(x,y)]) if (x,y) in (a:=self.animals[2]) else self.board.empty_board[y][x] for x in range(self.board.width)) for y in range(self.board.height))


    def move(self,move):
        new_state = deepcopy(self)
        start,dest = move
        p_animals = new_state.animals[self.player]
        p_animals[dest] = p_animals[start]
        p_animals[dest].isInTrap = True if dest in self.board.traps[self.player] else False
        p_animals[dest].isInWater = True if dest in self.board.water else False

        del p_animals[start]
        if dest in (o_animals := new_state.animals[3-self.player]):
            del o_animals[dest]
            new_state.turns_since_last_capture = 0
        else: new_state.turns_since_last_capture += 1
        new_state.player = 3-self.player
        new_state.update_available_moves()
        new_state.update_winner()
        return new_state





