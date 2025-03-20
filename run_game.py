import pygame
from load_game import *
import os
pygame.init()

path = os.path.dirname(__file__)

window_x = 490
window_y = 710

dir = "assets"
screen = pygame.display.set_mode((window_x,window_y))
pygame.display.set_caption("Jungle")

def load_assets(board_):
    global bg,a_sprites,tile_size,ldark,dark
    maxx,maxy = board_.length,board_.height
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

running = True

def xyblit(screen,img,xy:tuple):
    x,y = xy
    screen.blit(img,(x*tile_size+5,y*tile_size+5))

def display(state):
    screen.blit(bg,(0,0))
    pos_animals = (animal for dict in state.animals.values() for animal in dict.items())
    for pos,animal in pos_animals:
        sprite = a_sprites[(animal.rank,animal.player)]
        xyblit(screen,sprite,pos)
def player(game):
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
    while running and play:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                select()
        clock.tick(10)
    
    if not running: game.state.winner = 3



while running:
    game = Game(player,player)
    load_assets(game.board)
    game.start(True)
    running = False
pygame.quit()
