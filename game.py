import pygame 
from time import sleep
from sys import exit
from random import randint
from random import randrange 
from pygame.locals import * 
from enum import Enum
from collections import namedtuple
import numpy as np



pygame.init()
fontObj = pygame.font.Font('freesansbold.ttf', 24)

Point = namedtuple('Point', 'x, y')
# reset
# reward
# play(action) -> direction
# game_iteration
# is_collision

class SpriteGame:
    def __init__(self, w=640,h=480):
        self.w = w
        self.h = h
        self.mixer = pygame.mixer
        self.window =  pygame.display.set_mode((self.w, self.h))
        white = (255,255,255)
        self.window.fill(white)
        pygame.display.set_caption("Simple GUI game")
        self.im3 = pygame.image.load("bakc.PNG")
        self.im3.convert()
        self.reset()
        
    #mixer = pygame.mixer
    #window  = pygame.display.set_mode((640,480),0,32)
    #white = (255,255,255)
    #window.fill(white)
    #pygame.display.set_caption("Simple GUI game")

    #im3 = pygame.image.load("bakc.PNG");im3.convert()

    def play(self,wav_path):
        self.mixer.init(11025) 
        self.sound = self.mixer.Sound(wav_path)
        self.channel = self.sound.play()

    def displ(self,strin, h = 40, v =92):
        self.window.blit(strin, (h,v))
        pygame.display.update()
        sleep(0.081)

    def reset(self):
        
        self.textSurf = fontObj.render("", True , (0,255,0),(255,0,0))
        self.textRectObj = self.textSurf.get_rect()
        self.textRectObj.center = (50,50)
        self.frame_iteration = 0
        self.welcome_screen()
        try:
            txtfile= open("high score.txt",'r')
            self.highscore = int(txtfile.read())
        except:
            txtfile = open("high score.txt", 'w')
            self.highscore = 0
        self.main()
    # fontObj = pygame.font.Font('freesansbold.ttf', 24)
    # textSurf = fontObj.render("", True , (0,255,0),(255,0,0))
    # textRectObj = textSurf.get_rect()
    # textRectObj.center = (50,50)
    
    
    def developer(self):
        BASICFONT = pygame.font.Font('freesansbold.ttf', 16)
        pressKeySurf = BASICFONT.render('Developer: Bereket G.', True, (255,40,0))
        pressKeyRect = pressKeySurf.get_rect()
        pressKeyRect.topleft = (440, 450)
        self.window.blit(pressKeySurf, pressKeyRect)
        
    def welcome_screen(self):
        titleFont = pygame.font.Font('freesansbold.ttf', 100)
        titleSurf1 = titleFont.render('PAMPUCH', True, (255,255,10)) 
        titleSurf11 = titleSurf1.get_rect()
        titleSurf11.center = (320,240)
        self.window.fill ((0,0,0))
        self.window.blit(titleSurf1,titleSurf11)
        self.developer()
        pygame.display.update()
        sleep(6)

    def move(self):
        if self.direction == "horizontal":
            if self.hor >= 630:
                self.hor = 0
            if self.hor <= -10:
                self.hor = 640
            self.displ(self.im1, h = self.hor, v = self.ver)
            self.hor += self.b 
            self.displ(self.im11, h = self.hor, v = self.ver)
            self.hor += self.b
            sleep(0.03)
            self.displ(self.im2, h = self.hor, v = self.ver)
            self.hor += self.b
            self.update()
        elif self.direction  == "vertical":
            if self.ver >= 470:
                self.ver = 0
            if self.ver <= -10:
                self.ver = 470
            self.displ(self.im1,h = self.hor, v = self.ver)
            self.ver += self.b
            self.displ(self.im11,h = self.hor, v = self.ver)
            self.ver += self.b
            sleep(0.028)
            self.displ(self.im2,h = self.hor, v = self.ver)
            self.ver += self.b 
            self.update()
        
        
    
    def is_enemy(self, pt=None):
        
        if (abs(pt.x - self.ene_pos_hor) <= 20) or (abs(pt.y - self.ene_pos_ver) <= 20):
            return True
        return False
    def play_step(self, action):
        self.frame_iteration += 1
        # my score board
        self.textSurf = fontObj.render("Score " + str(self.score) , True , (0,255,0),(255,0,0)) # setting score to change
        self.window.blit(self.best_scoresurf, self.bestrect)
        self.window.blit(self.textSurf, self.textRectObj) # writing score 
        
        # 1. Collect User Input
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                self.running = False
                pygame.quit()
                exit()
        
        # 2. move
        self.move()
        
        # 3. check if game over
        reward = 0
        game_over = False 
        
        if (abs(self.hor - self.ene_pos_hor) <= 20) and (abs(self.ver - self.ene_pos_ver) <= 20):
            pygame.mixer.music.pause()
            self.play("boom.wav") # boom wav and time to game over and try to another chance
            self.window.blit(self.textSurf, self.textRectObj)
            self.running = False
            game_over = True
            reward = -10
            return reward, game_over, self.score
            #if self.frame_iteration > 100*len(self.snake):
            
        # 4. eat food
        
        if (abs(self.hor - self.ye_hor) <= 20) and (abs(self.ver - self.ye_ver) <= 20):
            self.play("s.wav")
            self.score += 100
            self.ye_hor = randint(0,570)
            self.ye_ver = randint(0,410)
            self.a = randrange(18,30)
            self.tempb = randrange(19,30)
            self.ene_pos_hor = self.ver + self.a
            self.ene_pos_ver = self.hor + self.tempb
            
            reward  = 10
            
        # action
        # up
        if np.array_equal(action, [1, 0, 0, 0]):
            self.im1 = pygame.image.load("up 1.PNG").convert()
            self.im11 = pygame.image.load("up 2.PNG").convert()
            self.im2 = pygame.image.load("up 3.PNG").convert()
            self.b = -6 
            self.direction = "vertical"
        # right
        elif np.array_equal(action, [0, 1, 0, 0]):
            self.im1 = pygame.image.load("ri 1.PNG").convert()
            self.im11 = pygame.image.load("ri 2.PNG").convert()
            self.im2 = pygame.image.load("ri 3.PNG").convert()
            self.b = 6  
            self.direction = "horizontal"
        # left
        elif np.array_equal(action, [0, 0, 1, 0]):
            self.im1 = pygame.image.load("le 1.PNG").convert()
            self.im11 = pygame.image.load("le 2.PNG").convert()
            self.im2 = pygame.image.load("le 3.PNG").convert()
            self.b = -6 
            self.direction = "horizontal"
        else: # [0, 0, 0, 1]
            self.im1 = pygame.image.load("do 1.PNG").convert()
            self.im11 = pygame.image.load("do 2.PNG").convert()
            self.im2 = pygame.image.load("do 3.PNG").convert()
            self.b = 6
            self.direction = "vertical"
        
        return reward, game_over, self.score    
    def main(self):
        global im3, ye_1, enemy_1, ye_hor, ye_ver, ene_pos_ver, ene_pos_hor, score, white
        
        # [straight, right, left, back]
        
        #clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        
        
        self.running = True
        self.score = 0
        self.hor = 40 # horizotal distance coverage
        self.ver = 92 # vertical distance coverage
        self.b = 6 # 6=forward -6=backward
        self.direction = "horizontal"
        white = (255,255,255)
        clock = pygame.time.Clock()
        self.window.fill(white)

        ##### Loading Images ######
        self.ye_1 = pygame.image.load("ye 1.PNG").convert() # food
        self.im1 = pygame.image.load("ri 1.PNG").convert() # actor motion1
        self.im11 = pygame.image.load("ri 2.PNG").convert() # actor motion2
        self.im2 = pygame.image.load("ri 3.PNG").convert() # actor motion2
        self.im3 = pygame.image.load("bakc.PNG").convert() # background
        self.enemy_1 = pygame.image.load("ri 11.PNG").convert() # enemy
        ##### -------------  #######

        # positions of food # 
        self.ye_hor = randint(0,580)
        self.ye_ver = randint(0,450)

        # positions of enemy #
        self.ene_pos_hor = randint(0,550)
        self.ene_pos_ver = randint(0,390)

        # score board
        self.best_scoresurf = fontObj.render("Best score: " + str(self.highscore) , True, (0,255,0,), (255,0,100))
        self.bestrect = self.best_scoresurf.get_rect()
        self.bestrect.center = (500,50)
        
        # main game loop
        #while self.running : 
        
    def update(self):
        self.displ(self.im3, 0,0)
        self.displ(self.ye_1, self.ye_hor, self.ye_ver)
        self.displ(self.enemy_1, self.ene_pos_hor, self.ene_pos_ver)
        pygame.display.update()

    def save_score(self):
        #global highscore
        if self.score > self.highscore:
            self.highscore = self.score
            txtfile= open("high score.txt", 'w')
            txtfile.write(str(self.highscore))
            BASICFONT = pygame.font.Font('freesansbold.ttf', 16)
            pressKeySurf = BASICFONT.render('Best Score: '+ str(self.highscore) , True, (255,5,20))
            pressKeyRect = pressKeySurf.get_rect()
            pressKeyRect.topleft = (440, 450)
            self.window.blit(pressKeySurf, pressKeyRect)
            pygame.display.update()

    def showGameOverScreen(self):
        self.window.fill((0,0,0))
        gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
        gameSurf = gameOverFont.render('Game', True, (255,255,10))
        overSurf = gameOverFont.render('Over', True, (255,255,10))
        gameRect = gameSurf.get_rect()
        overRect = overSurf.get_rect()
        gameRect.midtop = (320, 80)
        overRect.midtop = (320, gameRect.height + 80 + 25)
        self.window.blit(gameSurf, gameRect)
        self.window.blit(overSurf, overRect)
        self.save_score()
        pygame.display.update()
        sleep(2)


if __name__ == '__main__':
    game = SpriteGame()
    
    # game loop
    while True:
        reward, game_over, score = game.play_step([1, 0, 0, 0])
        if game_over == True:
            game.showGameOverScreen()
            break
        
    
                    
                    
