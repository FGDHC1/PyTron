import pygame
import sys
from time import sleep


pygame.init()

white=(255,255,255)
black=(0,0,0)
orange=(255,90,0)
blue=(50,50,255)
grey=(127,127,127)
purple=(127,0,127)

width, height=800,500

display = pygame.display.set_mode((width,height))
pygame.display.set_caption('PyTron')
pygame.mouse.set_visible(False)

clock = pygame.time.Clock()

def retrogrid (surface, gridcolor, gridsize):
    for x in range(0, width, gridsize):
        pygame.draw.line(surface, gridcolor, (x,0), (x,height))
    for y in range(0, height, gridsize):
        pygame.draw.line(surface, gridcolor, (0,y), (width,y))

background = pygame.Surface(display.get_size())
background = background.convert()
background.fill(black)
retrogrid(background, purple, 40)

playerwidth=10
playerspeed=10
playerdeath=False


def playerreset():
    global player1dir,player2dir, player1poshistory, player2poshistory, player1pos, player2pos, playerdeath
    player1pos = [width // 4, height // 2]
    player1dir = pygame.K_RIGHT
    player1poshistory = [player1pos[:]]

    player2pos = [width // 4 * 3, height // 2]
    player2dir = pygame.K_a
    player2poshistory = [player2pos[:]]

    playerdeath=False

def drawplayers():
    pygame.draw.rect(display, orange, pygame.Rect(player1pos[0],player1pos[1], playerwidth, playerwidth))
    pygame.draw.rect(display, blue, pygame.Rect(player2pos[0], player2pos[1], playerwidth, playerwidth))

def player1movement():
    global player1poshistory, player1dir, player1pos
    pressedkey = pygame.key.get_pressed()

    if pressedkey[pygame.K_d] and player1dir!=pygame.K_a:
        player1dir = pygame.K_d
    elif pressedkey[pygame.K_a] and player1dir!=pygame.K_d:
        player1dir = pygame.K_a
    elif pressedkey[pygame.K_w] and player1dir!=pygame.K_s:
        player1dir = pygame.K_w
    elif pressedkey[pygame.K_s] and player1dir!=pygame.K_w:
        player1dir = pygame.K_s

    if player1dir==pygame.K_d:
        player1pos[0] += playerspeed
    elif player1dir==pygame.K_a:
        player1pos[0] -= playerspeed
    elif player1dir==pygame.K_w:
        player1pos[1] -= playerspeed
    elif player1dir==pygame.K_s:
        player1pos[1] += playerspeed


    if len(player1poshistory) > 2 and player1pos[:] == player1poshistory[0]:
        break
    else:
        player1poshistory.append(player1pos[:])

def player2movement():
    global player2poshistory, player2dir, player2pos
    pressedkey = pygame.key.get_pressed()

    if pressedkey[pygame.K_RIGHT] and player2dir!=pygame.K_LEFT:
        player2dir = pygame.K_RIGHT
    elif pressedkey[pygame.K_LEFT] and player2dir!=pygame.K_RIGHT:
        player2dir = pygame.K_LEFT
    elif pressedkey[pygame.K_UP] and player2dir!=pygame.K_DOWN:
        player2dir = pygame.K_UP
    elif pressedkey[pygame.K_DOWN] and player2dir!=pygame.K_UP:
        player2dir = pygame.K_DOWN

    if player2dir==pygame.K_RIGHT:
        player2pos[0] += playerspeed
    elif player2dir==pygame.K_LEFT:
        player2pos[0] -= playerspeed
    elif player2dir==pygame.K_UP:
        player2pos[1] -= playerspeed
    elif player2dir==pygame.K_DOWN:
        player2pos[1] += playerspeed

    if len(player2poshistory) > 2 and player2pos[:] == player2poshistory[0]:
        break
    else:
        player2poshistory.append(player2pos[:])
def drawpath():
        for pos in player1poshistory:
            pygame.draw.rect(display, orange, pygame.Rect(pos[0], pos[1], playerwidth, playerwidth))
        for pos in player2poshistory:
            pygame.draw.rect(display, blue, pygame.Rect(pos[0], pos[1], playerwidth, playerwidth))

def playerdead():
    global playerdeath
    if player1pos


playerreset()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False

    display.blit(background, (0, 0))
    drawplayers()
    player1movement()
    player2movement()
    drawpath()
    playerdead()

    # if playerdeath:
    #     playerreset()



    pygame.display.update()
    clock.tick(15)

pygame.quit()
sys.exit()

