from os import path
import pygame
from random import randint
pygame.init()
#---------------------------------------------------------------
win = pygame.display.set_mode((960,780))
run = True
pygame.display.set_caption('ALEN INVASION')
pygame.display.set_icon(pygame.image.load('stuff/icon.png'))
space_ship = pygame.image.load('stuff/spaceship.png')
space_ship = pygame.transform.scale(space_ship,(90,95))
space_ship_x = 355
space_ship_y = 679
space_ship_x_change = 0
background = pygame.image.load('stuff/wall.jpg')
font = pygame.font.Font('freesansbold.ttf',22)
score = 0
border = pygame.Rect(810,0,10,900)
text_x = 830
text_y = 10

#----------------------------------------------------------------
enemy = []
enemy_x = []
enemy_y= []
enemy_y_change= []
enemy_x_change= []
nums_of_enemies= 5
for i in range(nums_of_enemies):
    # enemy.append(pygame.image.load('enemy2.png'))
    enemy.append(pygame.transform.scale(pygame.image.load('stuff/enemy2.png'),(70,35)))
    enemy_x.append(randint(4,725))
    enemy_y.append(10) 
    enemy_y_change.append(30)
    enemy_x_change.append(1)
#----------------------------------------------------------------
bullet = pygame.image.load('stuff/bullet.png')
bullet = pygame.transform.scale(bullet,(30,40))
bullet = pygame.transform.rotate(bullet,(90))
bullet_x = 0
bullet_y = 679
bullet_y_change = 3
bullet_state = 'ready'
bullet_sound = pygame.mixer.Sound(path.join('stuff/laser.wav'))
music = pygame.mixer.Sound(path.join('stuff/background.wav'))
music.play(-1)
explode = pygame.mixer.Sound(path.join('stuff/explosion.wav'))
game_over_font = pygame.font.Font('freesansbold.ttf',100)
#-----------------------------------------------------------------
def game_over_text():
    gameover = game_over_font.render('GAME OVER',True,(0,0,255))
    win.blit(gameover,(75,360))
    
def border_show():
    pygame.draw.rect(win,(255,255,255),border)

def show_text(x,y):
    score_text = font.render('Score :'+str(score),True,(255,255,255))
    win.blit(score_text,(x,y))
    
def player(x,y):
    win.blit(space_ship,(x,y))

def enemyf(x,y,i):
    win.blit(enemy[i],(x,y))

def bulletf(x,y):
    global bullet_state
    bullet_state = 'fire'
    win.blit(bullet,(x+25,y+17))

def iscollision(enemy_x,enemy_y,bullet_x,bullet_y):
    distance = ((bullet_x - enemy_x)**2 + (bullet_y - enemy_y)**2)**0.5
    if distance <38:
        return True
    else:
        return False

#------------------------------------------------------------------
while run:
    win.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                space_ship_x_change = 2
            if event.key == pygame.K_LEFT:
                space_ship_x_change = -2
            if event.key == pygame.K_SPACE:
                if bullet_state is 'ready':
                    bullet_sound.play()
                    bullet_x = space_ship_x
                    bulletf(bullet_x,bullet_y)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT  or event.key == pygame.K_LEFT:
                space_ship_x_change = 0
    space_ship_x += space_ship_x_change
#---------------------------------------------------------------------
    for i in range(nums_of_enemies):
        if enemy_y[i]> 610:
            for j in range(nums_of_enemies):
                enemy_y[i] = 1000
            game_over_text()
            break
        enemy_x[i] += enemy_x_change[i]
        if enemy_x[i] <= 0:
            enemy_x_change[i] = 1.6
            enemy_y[i] += enemy_y_change[i]
        elif enemy_x[i] > 730:
            enemy_x_change[i] = -1.6
            enemy_y[i] += enemy_y_change[i]

        colide = iscollision(enemy_x[i],enemy_y[i],bullet_x,bullet_y)
        if colide:
            explode.play()
            score += 1
            bullet_y = 679
            bullet_state = 'ready'
            enemy_x[i] = randint(4,725)
            enemy_y[i] = 10
        enemyf(enemy_x[i],enemy_y[i],i)
#---------------------------------------------------------------------
    if space_ship_x <= 0:
        space_ship_x =0
    elif space_ship_x > 710:
        space_ship_x = 710
    if bullet_y <= 0:
        bullet_y = 679
        bullet_state = 'ready'
 
    if bullet_state is 'fire':
        bulletf(bullet_x,bullet_y)
        bullet_y -= bullet_y_change
    player(space_ship_x,space_ship_y)
    show_text(text_x,text_y)
    border_show()
    pygame.display.update()

