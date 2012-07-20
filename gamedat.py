import sys

import pygame
from pygame.sprite import Sprite
from pygame import Rect, Color

from vec2d import vec2d

from widgets import MsgBoard

'''
Created on 21.6.2011

@author: RAdo
'''

class Bat(Sprite):
    def __init__(self, screen, field, game, image, side):
        """
            screen: obrazovka na ktoru sa bude vykraslovat
            
            field: rect v ktorom sa odohrava hra
            
            game: objekt hry
            
            image: ibrazok pre palku
            
            side: (left / right) urcuje na ktorej strane je palka
        """
        Sprite.__init__(self)
        
        self.screen = screen
        self.game = game
        self.field = field
        self.side = side
        self.speed = 5
        self.movement = 0
        
        self.image = image
        self.rect = image.get_rect()
        self.lives = 3
        
        if side == "left":
            self.pos = [self.field.left + 10, self.field.centery]
        else:
            self.pos = [(self.field.width - 10 - self.rect.width),
                        self.field.centery]
            
        self.rect = self.rect.move(self.pos)
        
        
    def update(self):
        self.rect = self.rect.move(0, self.movement)
        if self.rect.top < self.field.top:
            self.rect.top = self.field.top
        elif self.rect.bottom > self.field.bottom:
            self.rect.bottom = self.field.bottom
            
    def draw(self):
        self.screen.blit(self.image, self.rect)
    
    def move_up(self):
        self.movement -= self.speed
    
    def move_down(self):
        self.movement += self.speed
    
    def stop(self):
        self.movement = 0

class Ball(Sprite):  
    def __init__(self, screen, field, game,
                  image, init_pos, init_direction):
        """
            screen: obrazovka na ktoru sa bude vykraslovat
            
            field: rect v ktorom sa odohrava hra
            
            game: objekt hry
            
            image: ibrazok pre loptu
            
            init_direction = smer lopty na zaciatku
        """
        Sprite.__init__(self)
        
        self.screen = screen
        self.field = field
        self.game = game
        self.image = image
        self.pos = vec2d(init_pos)
        self.direction = vec2d(init_direction).normalized()

        self.speed = 0.35
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        
    def update(self, time_passed):
        
        displacement = vec2d(    
                self.direction.x * self.speed * time_passed,
                self.direction.y * self.speed * time_passed)
        self.pos += displacement
        self.rect.center = self.pos
                
        if self.rect.top < self.field.top or self.rect.bottom > self.field.bottom:
            self.direction[1] = -self.direction[1]
        
        if (self.rect.colliderect(self.game.bat_r.rect.inflate(-7, 0))):
            # otaca smerovy vektor podla toho ako zasiahla lopta palku
            # ak na kraji uhol je vacsi ak v strede uhol sa nemeni
            self.direction.rotate((self.rect.centery - self.game.bat_r.rect.centery) * 2)
            self.direction[0] = -self.direction[0]
            
        elif(self.rect.colliderect(self.game.bat_l.rect.inflate(-7, 0))):
            # otaca smerovy vektor podla toho ako zasiahla lopta palku
            # ak na kraji uhol je vacsi ak v strede uhol sa nemeni
            self.direction.rotate(-(self.rect.centery - self.game.bat_l.rect.centery) * 2)
            self.direction[0] = -self.direction[0]
        
        # Ak lopta prejde za obrazovku odcita zivot
        if self.rect.left < (self.field.left - 10):
            self.game.bat_l.lives -= 1
            self.game.new_ball()
            self.kill()
            self.game.paused = not self.game.paused
        
        elif self.rect.right > (self.field.right + 10):
            self.game.bat_r.lives -= 1
            self.game.new_ball()
            self.kill()
            self.game.paused = not self.game.paused
            
            
            
    def draw(self):
        self.screen.blit(self.image, self.rect)

class Game(object):

    def __init__(self, screen, screen_width, screen_height,
                 fiel_rect, bg_color):
        
        self.SCREEN_WIDTH = screen_width
        self.SCREEN_HEIGHT = screen_height
        self.FIELD_RECT = Rect(0, 50, self.SCREEN_WIDTH,
                                self.SCREEN_HEIGHT - 50)
        self.BG_COLOR = bg_color
        
        self.screen = screen
        
        self.bat_image = pygame.image.load("images/bat.png").convert_alpha()
        self.ball_image = pygame.image.load("images/ball.png").convert_alpha()
        
        self.bat_l = Bat(self.screen, self.FIELD_RECT, self, self.bat_image, "left")
        self.bat_r = Bat(self.screen, self.FIELD_RECT, self, self.bat_image, "right")        
        
        self.score = (self.bat_l.lives, self.bat_r.lives)
        self.score_board = MsgBoard(self.screen, Rect(0, 0, self.SCREEN_WIDTH, 50),
                                      "{0} : {1}".format(*self.score),
                                      Color("green"),Color("black"),
                                       2, Color("green"))
        
        self.fps_board = MsgBoard(self.screen, Rect(0, 0, 150, 50), "0", Color("green"),
                       Color("black"), 2, Color("green"))

        self.new_ball()
        
        self.clock = pygame.time.Clock()
        
        self.paused = False
        
    def new_ball(self):
        self.ball = Ball(self.screen, self.FIELD_RECT, self,
                         self.ball_image, (100, 100),(5, 3) )
    
    def win_check(self):
        if self.score[0] <= 0 or self.score[1] <= 0:
            win_text = "Left player win!"
            if self.score[0] <= 0:
                win_text = "Right player win!"
            
            win_msg = MsgBoard(self.screen, self.FIELD_RECT, win_text, 
                               Color("green"), Color("black"),
                               2, Color("green"))
            win_msg.draw()
            self.paused = True
            
            
    
    def run(self):
        
        while True:
            time_passed = self.clock.tick(100)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.bat_r.move_up()
                    elif event.key == pygame.K_DOWN:
                        self.bat_r.move_down()
                    elif event.key == pygame.K_w:
                        self.bat_l.move_up()
                    elif event.key == pygame.K_s:
                        self.bat_l.move_down()
                    elif event.key == pygame.K_SPACE:
                        self.paused = not self.paused
                    elif event.key == pygame.K_ESCAPE:
                        return 0
                elif event.type == pygame.KEYUP:
                    if (event.key == pygame.K_UP) or (event.key == pygame.K_DOWN):
                        self.bat_r.stop()
                    elif (event.key == pygame.K_w) or (event.key == pygame.K_s):
                        self.bat_l.stop()
            
            if not self.paused:
                
                # update
                self.bat_l.update()
                self.bat_r.update()
            
                self.ball.update(time_passed)
                
                self.score = (self.bat_l.lives, self.bat_r.lives)            
                self.score_board.update("{0} : {1}".format(*self.score))
                self.fps_board.update(str(int(self.clock.get_fps())))
            
                # draw
                self.screen.fill(self.BG_COLOR)
            
                self.score_board.draw()
                self.fps_board.draw()
            
                self.bat_l.draw()
                self.bat_r.draw()
            
                self.ball.draw()
                
                self.win_check()            
            
                pygame.display.flip()
                
                        

            
"""
if __name__ == '__main__':
    SCREEN_WIDTH = 640
    SCREEN_HEIGHT = 400
    FIELD_RECT = Rect(0, 50, SCREEN_WIDTH, SCREEN_HEIGHT - 50)
    BG_COLOR = Color("black")
    
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),0, 32)
    
    game = Game(screen, SCREEN_WIDTH, SCREEN_HEIGHT, FIELD_RECT, BG_COLOR)
    game.run()
"""
