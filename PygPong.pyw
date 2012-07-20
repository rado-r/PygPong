import sys

import pygame
from pygame.sprite import Sprite
from pygame import Rect, Color

from gamedat import Game
from widgets import MsgBoard, Box

'''
Created on 22.7.2011

@author: RAdo
'''

class Button(Sprite):
    def __init__(self, screen, rect, text,
                 button_opt, active = False):
        """
            screen: obrazovka na ktoru sa bude vykreslovat
            rect: miesto kde sa ma vykreslit button
            text: text ktory sa vypise v buttone
            button_opt: nastavenia vyzoru buttonu
                text_color: farba textu
                bg_color: farba pozadia
                border_width: sirka ramu (0 - ziadny ram)
                border_color: farba ramu
                
        """
        self.screen = screen
        self.rect = rect
        self.text = text
        
        self.button_opt_inact = button_opt
        self.button_opt_act = {"text_color": button_opt["text_color"],
                                 "bg_color": button_opt["bg_color"],
                                 "border_width": button_opt["border_width"] + 3,
                                 "border_color": button_opt["border_color"]}
        
        self.active = active
        
        self.but_active = MsgBoard(self.screen, self.rect, self.text,
                                   **self.button_opt_act)
        self.but_inactive = MsgBoard(self.screen, self.rect, self.text,
                                   **self.button_opt_inact)
        self.update()
        
    def update(self):
        if self.active:
            self.button = self.but_active
        else:
            self.button = self.but_inactive
        
    def draw(self):
        self.button.draw()
        

class Menu(object):
    def __init__(self, screen, bg_color, items,  button_opt):
        """    
            screen: obrazovka na ktoru sa bude vykraslovat
            
            bg_color: farba pozadia
            
            items: polozky ktore sa maju v menu zobrazit (n-tica)
            
            button_opt: slovnik z nastaveniamy vyzoru buttonov
                            viac v dokumentaciu Button-u
            
        """
        self.screen = screen
        self.rect = self.screen.get_rect()
        self.SCREEN_WIDTH = self.rect.width
        self.SCREEN_HEIGHT = self.rect.height
                
        self.BG_COLOR = bg_color
        
        self.items = items
        
        self.button_opt = button_opt  
        
        self.create_buttons() 
        self.active_button = 0   
        self.update(0)

        self.napis = MsgBoard(screen, Rect(220, 50, 200, 50),("PygPong"), Color("green"),
                       Color("black"), font_size = 32)
                
        self.clock = pygame.time.Clock()
        
    def update(self, move):
        self.buttons[self.active_button].active = False
        self.buttons[self.active_button].update()
        
        self.active_button += move
        if self.active_button > len(self.items):
            self.active_button = 0
            
        self.buttons[self.active_button].active = True
        self.buttons[self.active_button].update()
    
    def start(self):
        if self.active_button == 0:
            self.items[0][1]()
        
        elif self.active_button == 1:
            self.items[1][1]()
            
        elif self.active_button == 2:
            self.items[2][1]()
        
    def create_buttons(self):
        self.buttons = []
        rects = self.get_button_rects()
        
        for i in range(len(self.items)):
            self.buttons.append(Button(self.screen, rects[i], self.items[i][0],
                     self.button_opt))

    
    def get_button_rects(self):
        button_rects = []
        button_width = 200
        button_height = 50
        
        n_buttons = len(self.items)
        
        for i in range(n_buttons):
            button_rects.append(Rect((self.SCREEN_WIDTH / 2) - (button_width / 2),
                                     (self.SCREEN_HEIGHT / (n_buttons+2)) * (i+1) + 50,
                                     button_width,
                                     button_height))
        return button_rects                            
    
    def run(self):
        while True:
            time_passed = self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.update(-1)
                    elif event.key == pygame.K_DOWN:
                        self.update(1)
                    elif event.key == pygame.K_RETURN:
                        self.start()
            
            #draw
            self.screen.fill(self.BG_COLOR)
            self.napis.draw()
            for button in self.buttons:
                button.draw()
            
            pygame.display.flip()

def start_game():
    game = Game(screen, SCREEN_WIDTH, 
                            SCREEN_HEIGHT, screen.get_rect(), BG_COLOR)
    game.run()

def author():
    clock = pygame.time.Clock()

    
    row0 = MsgBoard(screen, Rect(220, 50, 200, 50),("PygPong"), Color("green"),
                       Color("black"), font_size = 32) 
    row1 = MsgBoard(screen, Rect(220, 150, 200, 50),("Python 3.1"), Color("green"),
                       Color("black"), font_size = 20)    
    row2 = MsgBoard(screen, Rect(220, 200, 200, 50),("Pygame 1.9.1"), Color("green"),
               Color("black"), font_size = 20)
    row3 = MsgBoard(screen, Rect(220, 250, 200, 50),("Author: Radoslav Rajcan"), Color("green"),
                       Color("black"))
    row4 = MsgBoard(screen, Rect(220, 300, 200, 50),("Email: radoslav.rajcan@gmail.com"), Color("green"),
                       Color("black"))
    
    while True:
        time_passed = clock.tick(30)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 0
                
        screen.fill(BG_COLOR)

        row0.draw()
        row1.draw()
        row2.draw()
        row3.draw()
        row4.draw()
        
        pygame.display.flip()
    
if __name__ == '__main__':
    SCREEN_WIDTH = 640
    SCREEN_HEIGHT = 400
    FIELD_RECT = Rect(0, 50, SCREEN_WIDTH, SCREEN_HEIGHT - 50)
    BG_COLOR = Color("black")
    
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),0, 32)
    
    menu = Menu(screen, BG_COLOR, 
                (("Start game",start_game),
                 ("About", author),
                 ("Exit", sys.exit)),
                {"text_color": Color("green"),
                 "bg_color": Color("black"),
                 "border_width": 2,
                 "border_color": Color("green")})
    menu.run()
    
    
