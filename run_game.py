import pygame
from load_game import *
import os
pygame.init()

path = os.path.dirname(__file__)

window_x = 490
window_y = 710

dir = "Assetsfinal"
screen = pygame.display.set_mode((window_x,window_y))
pygame.display.set_caption("Jungle")

def load_assets(board_):
    global bg,a_sprites,tile_size,ldark,dark
    maxx,maxy = board_.width,board_.height
    tile_size = min(window_x//maxx,(window_y-80)//maxy)
    sprite_dimensions = (a:=tile_size-10,a)
    def load_sprite(file):
        img = pygame.image.load(os.path.join(path,dir,file))
        img = pygame.transform.scale(img,sprite_dimensions)
        return img
    animals = ("Mouse","Cat","Dog","Wolf","Leopard","Tiger","Lion","Elephant")
    a_sprites = {(rank,i):load_sprite(f"{animal}{i}.png") for rank,animal in enumerate(animals) for i in (1,2)}

    #bg = pygame.image.load(os.path.join(path,dir,"bg.png"))
    #bg = pygame.transform.scale(bg,(window_x,window_y-80))

    bg = pygame.Surface((tile_size*maxx,tile_size*maxy))


    tile_dimensions = (tile_size,tile_size)

    tile = pygame.image.load(os.path.join(path,dir,"tile.png"))
    tile = pygame.transform.scale(tile,tile_dimensions)    

    water = pygame.Surface(tile_dimensions)
    water.fill((255,44,44))

    trap = pygame.image.load(os.path.join(path,dir,"trap.png"))
    trap = pygame.transform.scale(trap,tile_dimensions)

    lair = pygame.image.load(os.path.join(path,dir,"lair.png"))
    lair = pygame.transform.scale(lair,tile_dimensions)
    
    d = {".":tile,"_":water,"#":trap,"O":lair}
    for y,row in enumerate(board_.empty_board):
        for x,tile in enumerate(row):
            bg.blit(d[tile],(x*tile_size,y*tile_size))

    dark = pygame.Surface(sprite_dimensions, pygame.SRCALPHA)
    dark.fill((0,0,0,128))
    ldark = pygame.Surface(sprite_dimensions, pygame.SRCALPHA)
    ldark.fill((0,0,0,64))


pygame.display.flip()

clock = pygame.time.Clock()

def xyblit(screen,img,xy:tuple):
    x,y = xy
    screen.blit(img,(x*tile_size+5,y*tile_size+5))

def display(state):
    global screen
    screen.fill((255,255,255))
    screen.blit(bg,(0,0))
    pos_animals = (animal for dict in state.animals.values() for animal in dict.items())
    for pos,animal in pos_animals:
        sprite = a_sprites[(animal.rank,animal.player)]
        xyblit(screen,sprite,pos)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            state.winner = 3
    pygame.display.flip()

def human_player(game): #overwrites the original function as the original one becomes unnecessary
    def select():
        nonlocal moves,selected,play
        posx,posy = pygame.mouse.get_pos()
        x,y=posx//tile_size,posy//tile_size
        if (x,y)in moves:
            game.state = game.state.move((selected,(x,y)))
            display(game.state)
            pygame.display.flip()
            play = False
            return
        moves.clear()
        display(game.state)
        xyblit(screen,ldark,(x,y))
        selected = (x,y)
        if selected in (a:=game.state.animals[game.state.player]):
            moves = a[selected].available_moves(selected,game.state)
            moves = set(map(lambda x:x[1],moves))
            for xy in moves:
                xyblit(screen,dark,xy)
        pygame.display.flip()

    
    display(game.state)
    pygame.display.flip()
    moves = {}              #this dict keeps track of the moves player may play after selecting an animal
    selected = None
    global running
    play = True
    board_y = game.state.board.height*tile_size
    while running and play:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                posx,posy = pygame.mouse.get_pos()
                if posy < board_y:
                    select()
        clock.tick(10)
    
    if not running: game.state.winner = 3
players["Human"] = human_player


"""
board0.animals[2] = {(0,0):animal("Lion",2),           
                    (6,0):animal("Tiger",2),
                    (1,1):animal("Dog",2),
                    (5,1):animal("Cat",2),
                    (0,2):animal("Mouse",2),
                    (2,2):animal("Leopard",2),
                    (4,2):animal("Wolf",2),
                    (6,2):animal("Elephant",2)},
board0.animals[1]={(0,6):animal("Elephant",1),
                    (2,6):animal("Wolf",1),
                    (4,6):animal("Leopard",1),
                    (6,6):animal("Mouse",1),
                    (1,7):animal("Cat",1),
                    (5,7):animal("Dog",1),
                    (0,8):animal("Tiger",1),
                    (6,8):animal("Lion",1)}
"""

#changing some functions in Game to make them display the game
old_play = Game.play
def new_func(self):
    old_play(self)
    display(self.state)
Game.play = new_func

old_start = Game.start
def new_func(self,*arg):
    display(self.initial_state)
    old_start(self,*arg)
Game.start = new_func

running = True

while running:
    game = Game(players["AI3"],players["AI2"],board0)
    load_assets(game.board)
    game.start(True)
    running = False
pygame.quit()
