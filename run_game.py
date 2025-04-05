import pygame
from load_game import *
import os
import random
import time  # Adicionando o módulo time
pygame.init()

path = os.path.dirname(__file__)

window_x = 490
window_y = 690

dir = "Assetsfinal"
screen = pygame.display.set_mode((window_x,window_y))
pygame.display.set_caption("Jungle Chess")

# Colors
RED = (122, 22, 22)
CREAM = (255, 243, 224)
DARK_RED = (90, 15, 15)
HOVER_RED = (150, 30, 30)
SELECTED_RED = (180, 40, 40)

# Load logo
try:
    logo_img = pygame.image.load(os.path.join(path, dir, "interface", "lion_logo.png")).convert_alpha()
    # Calcular tamanho proporcional mantendo a qualidade
    logo_height = int(window_y * 0.25)  # 25% da altura da janela
    logo_width = int(logo_height * 1.2)  # Proporção um pouco mais larga que alta
    logo_img = pygame.transform.smoothscale(logo_img, (logo_width, logo_height))
    has_logo = True
except:
    has_logo = False

class Button:
    def __init__(self, x, y, width, height, text, font_size=32):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.Font(None, font_size)
        self.color = DARK_RED
        self.text_color = CREAM
        self.is_hovered = False
        self.is_selected = False
        
    def draw(self, surface):
        # Draw button background with rounded corners
        if self.is_selected:
            color = SELECTED_RED
        elif self.is_hovered:
            color = HOVER_RED
        else:
            color = self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        
        # Draw text
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
            return False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered:
                return True
        return False

class PlayerSelector:
    def __init__(self, player_num):
        self.player_num = player_num
        button_width = 180
        button_height = 50
        spacing = 20
        start_y = window_y // 2 - 50

        # Criar botões para cada opção
        self.buttons = []
        options = ["Human", "Easy AI", "Medium AI", "Hard AI", "Random AI"]
        for i, text in enumerate(options):
            x = window_x//2 - button_width//2
            y = start_y + (button_height + spacing) * i
            self.buttons.append(Button(x, y, button_width, button_height, text, 36))
        
        self.selected = None

    def draw(self, surface):
        # Desenhar título
        title_font = pygame.font.Font(None, 48)
        title_text = title_font.render(f"Select Player {self.player_num}", True, CREAM)
        title_rect = title_text.get_rect(centerx=window_x//2, y=window_y//4)
        surface.blit(title_text, title_rect)

        # Desenhar botões
        for button in self.buttons:
            button.draw(surface)

    def handle_event(self, event):
        for i, button in enumerate(self.buttons):
            if button.handle_event(event):
                # Desselecionar todos os outros botões
                for b in self.buttons:
                    b.is_selected = False
                button.is_selected = True
                self.selected = i
                return True
        return False

def draw_start_screen():
    screen.fill(RED)
    
    # Draw logo text
    logo_font = pygame.font.Font(None, 80)
    logo_text = logo_font.render("JUNGLE", True, CREAM)
    chess_text = logo_font.render("CHESS", True, CREAM)
    
    # Calculate positions for better layout
    if has_logo:
        # Centralizar o texto
        text_y = window_y // 4
        logo_rect = logo_text.get_rect(centerx=window_x//2, centery=text_y)
        chess_rect = chess_text.get_rect(centerx=window_x//2, centery=text_y + 70)
        
        # Posicionar o leão abaixo do texto
        logo_x = (window_x - logo_img.get_width()) // 2
        logo_y = text_y + 120  # Espaço abaixo do texto "CHESS"
        screen.blit(logo_img, (logo_x, logo_y))
    else:
        logo_rect = logo_text.get_rect(centerx=window_x//2, centery=window_y//3)
        chess_rect = chess_text.get_rect(centerx=window_x//2, centery=window_y//3 + 70)
    
    screen.blit(logo_text, logo_rect)
    screen.blit(chess_text, chess_rect)
    
    # Create start button with better positioning
    button_width = 220
    button_height = 60
    button_x = window_x//2 - button_width//2
    button_y = window_y - 180 if has_logo else window_y - 150
    start_button = Button(button_x, button_y, button_width, button_height, "START GAME", 45)
    
    return start_button

def start_screen():
    start_button = draw_start_screen()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if start_button.handle_event(event):
                waiting = False
                return True
        
        # Redraw screen
        screen.fill(RED)
        # Draw logo text and lion
        logo_font = pygame.font.Font(None, 80)
        logo_text = logo_font.render("JUNGLE", True, CREAM)
        chess_text = logo_font.render("CHESS", True, CREAM)
        
        if has_logo:
            # Centralizar o texto
            text_y = window_y // 4
            logo_rect = logo_text.get_rect(centerx=window_x//2, centery=text_y)
            chess_rect = chess_text.get_rect(centerx=window_x//2, centery=text_y + 70)
            
            # Posicionar o leão abaixo do texto
            logo_x = (window_x - logo_img.get_width()) // 2
            logo_y = text_y + 120  # Espaço abaixo do texto "CHESS"
            screen.blit(logo_img, (logo_x, logo_y))
        else:
            logo_rect = logo_text.get_rect(centerx=window_x//2, centery=window_y//3)
            chess_rect = chess_text.get_rect(centerx=window_x//2, centery=window_y//3 + 70)
        
        screen.blit(logo_text, logo_rect)
        screen.blit(chess_text, chess_rect)
        
        # Draw button
        start_button.draw(screen)
        pygame.display.flip()
        clock.tick(60)
    return True

def load_assets(board_):
    global bg,a_sprites,tile_size,ldark,dark
    maxx,maxy = board_.width,board_.height
    tile_size = min(window_x//maxx,(window_y-60)//maxy)
    sprite_dimensions = (a:=tile_size-10,a)
    def load_sprite(file):
        img = pygame.image.load(os.path.join(path,dir,file)).convert_alpha()
        img = pygame.transform.smoothscale(img,sprite_dimensions)
        return img
    animals = ("Mouse","Cat","Dog","Wolf","Leopard","Tiger","Lion","Elephant")
    a_sprites = {(rank,i):load_sprite(f"{animal}{i}.png") for rank,animal in enumerate(animals) for i in (1,2)}

    bg = pygame.Surface((tile_size*maxx,tile_size*maxy))

    tile_dimensions = (tile_size,tile_size)

    # Melhorar qualidade dos tiles do tabuleiro
    tile = pygame.image.load(os.path.join(path,dir,"tile.png")).convert_alpha()
    tile = pygame.transform.smoothscale(tile,tile_dimensions)    

    water = pygame.Surface(tile_dimensions)
    water.fill((255,44,44))

    trap = pygame.image.load(os.path.join(path,dir,"trap.png")).convert_alpha()
    trap = pygame.transform.smoothscale(trap,tile_dimensions)

    lair = pygame.image.load(os.path.join(path,dir,"lair.png")).convert_alpha()
    lair = pygame.transform.smoothscale(lair,tile_dimensions)
    
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

font = pygame.font.Font(None, 50)

def display(state,turn = None):
    global screen,running,font,window_y,window_x
    screen.fill((122,22,22))
    screen.blit(bg,(0,0))
    pos_animals = (animal for dict in state.animals.values() for animal in dict.items())
    for pos,animal in pos_animals:
        sprite = a_sprites[(animal.rank,animal.player)]
        xyblit(screen,sprite,pos)
        
    if state.winner == -1:
        player_text = font.render(f"Player {state.player}", True, (255, 255, 255))
    else:
        if state.winner == 0:
            player_text = font.render(f"Draw !!!", True, (255, 255, 255))
        else:
            player_text = font.render(f"Winner: {3-state.player}!", True, (255, 255, 255))
    screen.blit(player_text,(10,window_y-50))
    
    if turn!=None:
        turn_text = font.render(f"Turn   {turn+1:{" "}>3} ",True,(255,255,255))
        screen.blit(turn_text,(window_x-180,window_y-50))
    
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
            display(game.state,game.turns)
            pygame.display.flip()
            play = False
            return
        moves.clear()
        display(game.state,game.turns)
        xyblit(screen,ldark,(x,y))
        selected = (x,y)
        if selected in (a:=game.state.animals[game.state.player]):
            moves = a[selected].available_moves(selected,game.state)
            moves = set(map(lambda x:x[1],moves))
            for xy in moves:
                xyblit(screen,dark,xy)
        pygame.display.flip()

    
    display(game.state,game.turns)
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
                    (6,2):animal("Elephant",2)}

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
    display(self.state,self.turns)
Game.play = new_func

old_start = Game.start
def new_func(self,*arg):
    display(self.state,self.turns)
    old_start(self,*arg)
Game.start = new_func

running = True

def post_game(game):
    def display1(state,turns):
        global display,font,screen,window_x,window_y
        display(state,turns)
        text = font.render("-      +",True,(255,255,255))
        screen.blit(text,(window_x-95,window_y-52))
        pygame.display.flip()
    global running
    def click():
        nonlocal board_y,turn,notExit
        posx,posy = pygame.mouse.get_pos()
        if posy > board_y:
            if posx > window_x-60:
                turn = (turn+1)%game.turns
            elif posx > window_x-120:
                turn = (turn-1)%game.turns
            elif posx < window_x-180:
                notExit = 0
            display1(game.log[turn],turn)
    display1(game.state,game.turns)

    turn = game.turns
    game.turns += 1	# game.turns will now act as the upper bound for turn
    board_y = game.state.board.height*tile_size
    notExit = 1
    while running and notExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click()
    clock.tick(10)

def select_players():
    selectors = [PlayerSelector(1), PlayerSelector(2)]
    current_selector = 0
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None, None
            
            if selectors[current_selector].handle_event(event):
                if current_selector == 0:
                    current_selector = 1
                else:
                    # Ambos os jogadores foram selecionados
                    selections = [s.selected for s in selectors]
                    if None not in selections:
                        return get_players(selections[0]), get_players(selections[1])
        
        # Desenhar tela
        screen.fill(RED)
        selectors[current_selector].draw(screen)
        pygame.display.flip()
        clock.tick(60)

def get_players(selection):
    if selection == 0:  # Human
        return players["Human"]
    elif selection == 1:  # Easy AI
        return players["AI1"]
    elif selection == 2:  # Medium AI
        return players["AI2"]
    elif selection == 3:  # Hard AI
        return players["AI3"]
    else:  # Random AI
        return players["Random"]  # Agora usa o execute_random_move

def game_loop(game):
    global running,screen,window_x,window_y,font
    while running and game.state.winner == -1:
        display(game.state)
        pygame.display.flip()
        if game.state.player == 1:
            game.p1.play(game)
        else:
            game.p2.play(game)
            
while running:
    # Show start screen first
    if not start_screen():
        break
    
    # Select players
    player1, player2 = select_players()
    if player1 is None or player2 is None:  # User closed the window
        break
        
    game = Game(player1, player2, board0)
    load_assets(game.board)
    game.start(True)
    post_game(game)
pygame.quit()
