import pygame 
from time import sleep
from sys import exit
from random import randint
from random import randrange 
from pygame.locals import * 

pygame.init()
mixer = pygame.mixer
window  = pygame.display.set_mode((640,480),0,32)
white = (255,255,255)
window.fill(white)
pygame.display.set_caption("Simple GUI game")

im3 = pygame.image.load("bakc.PNG");im3.convert()

def play(wav_path):
    mixer.init(11025) 
    sound = mixer.Sound(wav_path)
    channel = sound.play()

def displ(strin, h = 40, v =92):
    window.blit(strin, (h,v))
    pygame.display.update()
    sleep(0.081)

fontObj = pygame.font.Font('freesansbold.ttf', 24)
textSurf = fontObj.render("", True , (0,255,0),(255,0,0))
textRectObj = textSurf.get_rect()
textRectObj.center = (50,50)

def developer():
    BASICFONT = pygame.font.Font('freesansbold.ttf', 16)
    pressKeySurf = BASICFONT.render('Developer: Bereket G.', True, (255,40,0))
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (440, 450)
    window.blit(pressKeySurf, pressKeyRect)
    
def welcome_screen():
    titleFont = pygame.font.Font('freesansbold.ttf', 100)
    titleSurf1 = titleFont.render('PAMPUCH', True, (255,255,10)) 
    titleSurf11 = titleSurf1.get_rect()
    titleSurf11.center = (320,240)
    window.fill ((0,0,0))
    window.blit(titleSurf1,titleSurf11)
    developer()
    pygame.display.update()
    sleep(6)

def main():
   
    global im3, ye_1, enemy_1, ye_hor, ye_ver, ene_pos_ver, ene_pos_hor, score, white
    
    running = True
    score = 0
    hor=40 # horizotal distance coverage
    ver = 92 # vertical distance coverage
    b = 6
    direction = "horizontal"
    white = (255,255,255)
    clock = pygame.time.Clock()
    window.fill(white)

    ##### Loading Images ######
    ye_1 = pygame.image.load("ye 1.PNG").convert()
    im1 = pygame.image.load("ri 1.PNG").convert()
    im11 = pygame.image.load("ri 2.PNG").convert()
    im2 = pygame.image.load("ri 3.PNG").convert()
    im3 = pygame.image.load("bakc.PNG").convert()
    enemy_1 = pygame.image.load("ri 11.PNG").convert()
    ##### -------------  #######

    # postions of yemibelut # 
    ye_hor = randint(0,580)
    ye_ver = randint(0,450)

    # positions of enemy #
    ene_pos_hor = randint(0,550)
    ene_pos_ver = randint(0,390)

    best_scoresurf = fontObj.render("Best score: " + str(highscore) , True, (0,255,0,), (255,0,100))
    bestrect = best_scoresurf.get_rect()
    bestrect.center = (500,50)
    while running : # mian game looop
        textSurf = fontObj.render("Score " + str(score) , True , (0,255,0),(255,0,0)) # setting score to change
        window.blit(best_scoresurf, bestrect)
        window.blit(textSurf, textRectObj) # writing score 
        if direction == "horizontal":
            if hor >= 630:
                hor = 0
            if hor <= -10:
                hor = 640
            displ(im1, h = hor, v = ver) ; hor += b 
            displ(im11, h = hor, v = ver);hor += b; sleep(0.03)
            displ(im2, h = hor, v = ver) ;hor += b
            update()
        elif direction  == "vertical":
            if ver >= 470:
                ver = 0
            if ver <= -10:
                ver = 470
            displ(im1,h = hor, v = ver) ; ver += b
            displ(im11,h = hor, v = ver);ver += b; sleep(0.028)
            displ(im2,h = hor, v = ver) ;ver += b 
            update()
        if (abs(hor - ye_hor) <= 20) and (abs(ver - ye_ver) <= 20):
            play("s.wav")
            score += 100
            ye_hor = randint(0,570)
            ye_ver = randint(0,410)
            a = randrange(18,30)
            tempb = randrange(19,30)
            ene_pos_hor = ver + a
            ene_pos_ver = hor + tempb
        if (abs(hor - ene_pos_hor) <= 20) and (abs(ver - ene_pos_ver) <= 20):
            pygame.mixer.music.pause()
            play("boom.wav") # boom wav and time to game over and try to another chance
            window.blit(textSurf, textRectObj)
            running = False
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                running = False
                pygame.quit()
                exit()
            elif (event.type == pygame.KEYDOWN):
                if ( event.key == pygame.K_SPACE):
                    displ(im2, h = hor , v = ver)
                    window.blit(textSurf, textRectObj)
                    pygame.event.wait()                   
                elif (event.key == pygame.K_LEFT or event.key == pygame.K_a):
                     im1 = pygame.image.load("le 1.PNG").convert()
                     im11 = pygame.image.load("le 2.PNG").convert()
                     im2 = pygame.image.load("le 3.PNG").convert()
                     b = -6 ; direction = "horizontal"
                elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d):                                                       
                     im1 = pygame.image.load("ri 1.PNG").convert()
                     im11 = pygame.image.load("ri 2.PNG").convert()
                     im2 = pygame.image.load("ri 3.PNG").convert()
                     b = 6  ; direction = "horizontal"
                elif (event.key == pygame.K_UP or event.key == pygame.K_w):                                                        
                     im1 = pygame.image.load("up 1.PNG").convert()
                     im11 = pygame.image.load("up 2.PNG").convert()
                     im2 = pygame.image.load("up 3.PNG").convert()
                     b = -6 
                     direction = "vertical"
                elif (event.key == pygame.K_DOWN or event.key == pygame.K_s):                                                     
                     im1 = pygame.image.load("do 1.PNG").convert()
                     im11 = pygame.image.load("do 2.PNG").convert()
                     im2 = pygame.image.load("do 3.PNG").convert()
                     b = 6
                     direction = "vertical"
def update():
    displ(im3, 0,0)
    displ(ye_1, ye_hor, ye_ver)
    displ(enemy_1, ene_pos_hor, ene_pos_ver)
    pygame.display.update()

def save_score():
        global highscore
        if score > highscore:
            highscore = score
            txtfile= open("high score.txt", 'w')
            txtfile.write(str(highscore))
            BASICFONT = pygame.font.Font('freesansbold.ttf', 16)
            pressKeySurf = BASICFONT.render('Best Score: '+ str(highscore) , True, (255,5,20))
            pressKeyRect = pressKeySurf.get_rect()
            pressKeyRect.topleft = (440, 450)
            window.blit(pressKeySurf, pressKeyRect)
            pygame.display.update()

def showGameOverScreen():
    window.fill((0,0,0))
    gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
    gameSurf = gameOverFont.render('Game', True, (255,255,10))
    overSurf = gameOverFont.render('Over', True, (255,255,10))
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (320, 80)
    overRect.midtop = (320, gameRect.height + 80 + 25)
    window.blit(gameSurf, gameRect)
    window.blit(overSurf, overRect)
    save_score()
    pygame.display.update()
    sleep(2)



while True:
        # back ground muxic
        #pygame.mixer.music.load("bg.mp3")
        #pygame.mixer.music.play(-1,0.0)

        welcome_screen()
        try:
            txtfile= open("high score.txt",'r')
            highscore = int(txtfile.read())
        except:
            txtfile = open("high score.txt", 'w')
            highscore = 0
        main()
        showGameOverScreen()
        pygame.event.get()
        run = True
        while run:
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    pygame.quit()
                    exit()
                elif(event.type == pygame.KEYDOWN):
                    run = False ; break
                
                
