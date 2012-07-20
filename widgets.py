import sys

import pygame
from pygame import Rect, Color

'''
Created on 22.6.2011

@author: RAdo
'''

class Box(object):
    def __init__(self,
                 screen,
                 rect,
                 bg_color,
                 border_width=0,
                 border_color = Color("white")):
        
        """
        screen: obrazovka na vykreslenie
        rect: miesto kde sa ma vykreslit
        bg_color: farba pozadia
        border_width = sirka okraja
        border_color = farba okraja
        """
        
        self.screen = screen
        self.rect = rect
        self.bg_color = bg_color
        self.border_width = border_width
        self.border_color = border_color
        
        self.in_rect = Rect(self.rect.left + self.border_width,
                        self.rect.top + self.border_width,
                        self.rect.width - (self.border_width * 2),
                        self.rect.height - (self.border_width * 2))
    def draw(self):
        pygame.draw.rect(self.screen, self.border_color, self.rect)
        pygame.draw.rect(self.screen, self.bg_color, self.in_rect)
    
    def get_internal_rect(self):
        return self.in_rect
  

        
class MsgBoard(object):
    def __init__(self, screen, rect, text, text_color,
                      bg_color, border_width=0, border_color=Color("white"),
                      font_size = 16):
        """ 
            screen: obrazovka na ktoru sa bude vykreslovat
            rect: umiestnenie a velkos
            text: skore ktore sa bude zobrazovat (x, y)
            text_color: farba fontu
            bg_color: farba pozadia
            border_width: sirka okraja
            border_color: farba okraja
        """ 
        self.screen = screen
        self.rect = rect
        self.text = text
        self.text_color = text_color
        self.bg_color = bg_color
        self.border_width = border_width
        self.border_color = border_color
        self.font_size = font_size

        
        self.font = pygame.font.Font('pismo.ttf', self.font_size) 
        
        self.box = Box(screen, rect, bg_color, border_width, border_color)
    
    def update(self, text):
        self.text = text
    
    def draw(self):          
        self.box.draw()
        
        text_sf = self.font.render(self.text, True, self.text_color, self.bg_color)
        text_rect = text_sf.get_rect()
        text_rect = text_rect.move((self.rect.centerx - int(text_rect.width / 2),
                                             self.rect.centery - int(text_rect.height / 2)))
        
        self.screen.blit(text_sf, text_rect)
        
        
    
if __name__ == '__main__':
    pygame.init()
    
    SCREEN_WIDTH, SCREEN_HEIGHT = 350, 550
    screen = pygame.display.set_mode(
                (SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    
    clock = pygame.time.Clock()
    
    b1 = Box(screen, Rect(50, 50, 100, 200), Color("blue"), 20, Color("orange"))
    
    score = MsgBoard(screen, Rect(50, 300, 200, 50),("Co to co?"), Color("green"),
                       Color("black"), 2, Color("green"))
    
    while True:
        time_passed = clock.tick(30)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
                

        b1.draw()
        
        score.draw()

        pygame.display.flip()
