import pygame
from pygame.locals import *
import random
import time
import os

pygame.init()
pygame.font.init()

#Game Info
display_x = 800
display_y = 600

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)

myfont = pygame.font.SysFont(None, 30)
bigfont = pygame.font.SysFont(None,80)
textsurface = myfont.render('Score', False, (255,255,255))

GameDisplay = pygame.display.set_mode((display_x,display_y))

pygame.display.set_caption('Space Invaders')

clock = pygame.time.Clock()
#Gane Images
spaceship1 = pygame.image.load('ship.png')
blocker1 = pygame.image.load('blocker.png')
laserimg = pygame.image.load('laser.png')
purpleenemy = pygame.image.load('purple1.png')
purpleenemy2 = pygame.image.load('purple2.png')
blueenemy = pygame.image.load('blue1.png')
blueenemy2 = pygame.image.load('blue2.png')
greenenemy = pygame.image.load('green1.png')
greenenemy2 = pygame.image.load('green2.png')
bigship1 = pygame.image.load('bigship.png')
biggreen1 = pygame.image.load('biggreen.png')
bigblue1 = pygame.image.load('bigblue.png')
bigpurple1 = pygame.image.load('bigpurple.png')
littleship1 = pygame.image.load('littleship.png')
enemybul = pygame.image.load('enemybullet.png')

def spaceship(x,y):
    GameDisplay.blit(spaceship1,(x,y))
def draw_bullet(x,y):
    GameDisplay.blit(laserimg,(x,y))
def draw_enemy(x,y,colour):
    if index == 1:
        colourmap = {
            'purple': purpleenemy,
            'blue': blueenemy,
            'green': greenenemy,
    }
    if index == 2:
        colourmap = {
            'purple': purpleenemy2,
            'blue': blueenemy2,
            'green': greenenemy2,
    }
        
    GameDisplay.blit(colourmap[colour],(x,y))
def draw_enemybul(x,y):
    GameDisplay.blit(enemybul,(x,y))
def populate_enemies():
    for i in range(10):
        global enemy_x, enemy_dir
        enemy_x=0
        enemy_dir = 10
        enemies.append({'x':70*i + 20,'y':90, 'colour':'purple'})
        enemies.append({'x':70*i + 20,'y':150,'colour':'blue'})
        enemies.append({'x':70*i + 20,'y':210,'colour':'green'})
        enemies.append({'x':70*i + 20,'y':270,'colour':'green'})

def enemy_bullets():
    if len(enemybullet) < 5:
        length = len(enemies)
        ran = random.randint(0,length)
        i = 0
        for enemy in enemies:
            if i == ran:
                enemybullet.append({'x':enemies[ran]['x']+25,'y':enemies[ran]['y']+20})
                            
            i+=1

def titlescreen():
    intro = True
    while intro == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    intro = False
        GameDisplay.fill(black)
        title = bigfont.render("Space Invaders",True, (255,255, 255))
        enter = myfont.render("Press enter to continue",True,(255,255,255))
        GameDisplay.blit(title,(200,200))
        GameDisplay.blit(enter,(285,300))
        GameDisplay.blit(bigship1,(200,300))
        GameDisplay.blit(bigpurple1,(510,300))
        GameDisplay.blit(biggreen1, (510,400))
        GameDisplay.blit(bigblue1, (200,400))
        pygame.display.update()

spaceship_width = 50
enemies = []
enemybullet = []
enemy_x = 0
enemy_dir = 10
enemy_speed = 10
populate_enemies()
index = 2
frames = 0    
#enemyresets = 1

def gameloop():
    global enemy_x,enemy_dir,enemies,enemy_speed,index,frames,enemyresets
    x = (display_x * 0.45)
    y = (display_y * 0.9)
    x_change = 0
    score = 0
    enemyresets = 1
    lives = 3
    blockercheck1 = True
    blockercheck2 = True
    blockercheck3 = True

        
    gameover = False

    keys = [False, False, False] # left, right, space

    bullet = None

    while not gameover:
         
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
               pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    keys[0]=True
                elif event.key == pygame.K_RIGHT:
                    keys[1]=True
                elif event.key == pygame.K_SPACE:
                    keys[2] = True
                    
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    keys[0]=False
                elif event.key == pygame.K_RIGHT:
                    keys[1]=False
                elif event.key == pygame.K_SPACE:
                    keys[2]=False
        
        x_change = 0
        if keys[0] and not keys[1]:
            x_change = 0 if x < 0 else -5
            
        elif keys[1] and not keys[0]:
            x_change = 0 if x > display_x - spaceship_width else 5

        x += x_change
        if bullet:
            bullet = (bullet[0], bullet[1]-8)
            if bullet[1] < 0:
                bullet = None
        else:
            if keys[2]:
                bullet = (x+23,y-18)

        
        
        if frames == int(40/enemyresets):
            enemy_x += enemy_dir

            movedown=False
            if enemy_x>80:
                enemy_dir = -1*enemy_speed
                movedown = True
            if enemy_x <10:
                enemy_dir = 1*enemy_speed
                movedown = True

            for enemy in enemies:
                enemy['x'] += enemy_dir
                if movedown:
                    enemy['y'] += 10
                     
                    
                    
            if len(enemies) == 0: 
                enemyresets += 1
                populate_enemies()
                enemy_speed += 1
            index = 3-index
            frames = 0
        
            
        for enemy in enemies:
            if bullet and enemy['x'] < bullet[0] + 2.5 < enemy['x'] + 50 and enemy['y'] < bullet[1] < enemy['y'] + 60:
                enemies.remove(enemy)
                bullet = None
            if enemy['x'] < x <enemy['x']+45 and enemy['y']< y < enemy['y']+45:
                gameover = True
            if enemy['y'] > 600:
                gameover = True
        for i in range(3):
            for enemy in enemies:
                if 80+200*i < enemy['x'] < 180+200*i and enemy['y'] > 410:
                    if i == 0:
                        blockercheck1 = False
                    elif i == 1:
                        blockercheck2 = False
                    else:
                        blockercheck3 = False
        

        for i in range(3):
            if i == 0 and blockercheck1:
                if bullet and 133 < bullet[0]-200*i < 233 and 450 < bullet[1] < 500:
                    bullet = None
            if i == 1 and blockercheck2:
                if bullet and 133 < bullet[0]-200*i < 233 and 450 < bullet[1] < 500:
                    bullet = None
            if i == 2 and blockercheck3:
                if bullet and 133 < bullet[0]-200*i < 233 and 450 < bullet[1] < 500:
                    bullet = None
        enemy_bullets()
        for i in range(len(enemybullet)):
            if enemybullet[i]['y']>600:
                del enemybullet[i]
                break

        
        for i in range(3):
            for j in range(len(enemybullet)):
                if i==0 and blockercheck1:
                    if 133<enemybullet[j]['x']-200*i<233 and 440<enemybullet[j]['y']<500:
                        del enemybullet[j]
                        break
                if i==1 and blockercheck2:
                     if 133<enemybullet[j]['x']-200*i<233 and 440<enemybullet[j]['y']<500:
                        del enemybullet[j]
                        break
                if i==2 and blockercheck3:
                    if 133<enemybullet[j]['x']-200*i<233 and 440<enemybullet[j]['y']<500:
                        del enemybullet[j]
                        break
        for i in range(len(enemybullet)):
            if x < enemybullet[i]['x']+2.5 <x+50 and y<enemybullet[i]['y']<y+50:
                lives -=1
                del enemybullet[i]
                break
        for enemybul1 in enemybullet:
            enemybul1['y'] += 3

        if lives == 0:
            #lives = 3
            gameover = True
            #endscreen(enemyresets)
        frames += 1
        # Render time!!!!!
        GameDisplay.fill(black)

        for i in range(3):
            if i == 0 and blockercheck1:
                GameDisplay.blit(blocker1,(133+200*i,450))
            if i == 1 and blockercheck2:
                GameDisplay.blit(blocker1,(133+200*i,450))
            if i ==2 and blockercheck3:
                GameDisplay.blit(blocker1,(133+200*i,450))
 
        for j in range(lives):
            GameDisplay.blit(littleship1,(625+40*j,0))


        for enemy in enemies:
            draw_enemy(enemy['x'],enemy['y'],enemy['colour'])

        for enbullet in enemybullet:
            draw_enemybul(enbullet['x'],enbullet['y'])

        if bullet:
            draw_bullet(bullet[0],bullet[1])
        
            
        spaceship(x,y)
        textsurface = myfont.render('Score: {}'.format(40-len(enemies) + 40*enemyresets-40), True, (255,255,255))
        livestext = myfont.render('Lives:',True,(255,255,255))
        #texty = myfont.render('{}    {}      {}   {}'.format(x,enemy['x'],y,enemy['y']),True,(255,255,255))
        #GameDisplay.blit(texty,(100,0))
        GameDisplay.blit(livestext,(550,0))
        GameDisplay.blit(textsurface,(0,0)) 
        pygame.display.update()

        clock.tick(60)
        
def endscreen(enemyresets):
    end = True
    while end:
        time.sleep(1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    end = False
        GameDisplay.fill(black)
        gameovertext = bigfont.render("Game Over",True,(255,255,255))
        scoretext = myfont.render("Your score was: {}".format(40-len(enemies) + 40*enemyresets-40),True,(255,255,255))
        enter = myfont.render("Press enter to return to main screen",True,(255,255,255))
        GameDisplay.blit(gameovertext,(240,200))
        GameDisplay.blit(scoretext,(295,280))
        GameDisplay.blit(enter,(220,350))
        
        pygame.display.update()
gameExit = False         
while not gameExit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            gameExit = True
    x = (display_x * 0.45)
    y = (display_y * 0.9)
    x_change = 0
    score = 0
    enemyresets = 1
    lives = 3
    blockercheck1 = True
    blockercheck2 = True
    blockercheck3 = True
    enemies.clear()
    populate_enemies()
    enemybullet.clear()
    enemy_x = 0
    enemy_dir = 10
    enemy_speed = 10
    index = 2
    frames = 0 
    
        
    gameover = False

    keys = [False, False, False] # left, right, space

    bullet = None
    
    titlescreen()
    gameloop()
    endscreen(enemyresets)
#Exits pygame
pygame.quit()

quit()


