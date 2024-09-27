import pygame
import sys
import button



pygame.init()

white=(255,255,255)
black=(0,0,0)
orange=(255,90,0)
blue=(50,50,255)
grey=(127,127,127)
purple=(127,0,127)
green=(0,255,0)
red=(255,0,0)
yellow=(255,255,0)


width, height=800,500

display = pygame.display.set_mode((width,height))
pygame.display.set_caption('PyTron')
pygame.mouse.set_visible(True)

clock = pygame.time.Clock()

player1name="player1"
player2name="player2"
player1score=0
player2score=0

playerwidth=10
playerspeed=10
playerdeath=False
paused=False
#load Button images
start_img=pygame.image.load("Start_button.png").convert_alpha()
continue_img=pygame.image.load("Continue_button.png").convert_alpha()
quit_img=pygame.image.load("Quit_button.png").convert_alpha()



start_button = button.Button(width/10*6,height/4*3,start_img)
continue_button = button.Button(width/10*6,height/4*3,continue_img)
quit_button = button.Button(width/10,height/4*3,quit_img)

running = True
start=True

#Game background
def retrogrid (surface, gridcolor, gridsize):
    for x in range(0, width, gridsize):
        pygame.draw.line(surface, gridcolor, (x,0), (x,height))
    for y in range(0, height, gridsize):
        pygame.draw.line(surface, gridcolor, (0,y), (width,y))

background = pygame.Surface(display.get_size())
background = background.convert()
background.fill(black)
retrogrid(background, purple, 40)

def drawbackground():
    global background
    background.fill(black)
    retrogrid(background, purple, 40)

def playerreset():
    global player1dir,player2dir, player1poshistory, player2poshistory, player1pos, player2pos, playerdeath
    player1pos = [width // 4, height // 2]
    player1dir = pygame.K_RIGHT
    player1poshistory = [player1pos.copy()]

    player2pos = [width // 4 * 3, height // 2]
    player2dir = pygame.K_a
    player2poshistory = [player2pos.copy()]

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


    if len(player1poshistory) == 1 and player1pos == player1poshistory[0]:
        pass
    else:
        player1poshistory.append(player1pos.copy())

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

    if len(player2poshistory) == 1 and player2pos == player2poshistory[0]:
        pass
    else:
        player2poshistory.append(player2pos.copy())
def drawpath():
        for pos1 in player1poshistory:
            pygame.draw.rect(display, orange, pygame.Rect(pos1[0], pos1[1], playerwidth, playerwidth))
        for pos2 in player2poshistory:
            pygame.draw.rect(display, blue, pygame.Rect(pos2[0], pos2[1], playerwidth, playerwidth))

def playerdead():
    global playerdeath,player1score,player2score
    #player collision
    if player1pos in player2poshistory:
        playerdeath = True
        player2score += 1
    if player1pos in player1poshistory[:-1]:
        playerdeath = True
        player2score += 1


    if player2pos in player2poshistory[:-1]:
        playerdeath = True
        player1score += 1
    if player2pos in player1poshistory:
        playerdeath = True
        player1score += 1


    #border collision
    if player1pos[0] < 0 or player1pos[0] > width-1 or player1pos[1] < 0 or player1pos[1] > height-1 :
        playerdeath = True
        player2score += 1
    if player2pos[0] < 0 or player2pos[0] > width-1 or player2pos[1] < 0 or player2pos[1] > height-1 :
        playerdeath = True
        player1score += 1

def playernames():
    global player1name, player2name,player1score,player2score
    player1out = player1name+": "+str(player1score)
    player2out = player2name+": "+str(player2score)
    font=pygame.font.SysFont('Aptos',30)
    #player2
    textp1=font.render(player1out,True,orange)
    textRectp1=textp1.get_rect()
    textRectp1.center=50,15
    display.blit(textp1,textRectp1)
    #player2
    textp2 = font.render(player2out, True, blue)
    textRectp2 = textp2.get_rect()
    textRectp2.center = 50, 40
    display.blit(textp2, textRectp2)

def startscreen():
    global start
    display.fill(black)

    font = pygame.font.SysFont('Aptos', 80)
    starttext = font.render("PyTron", True, yellow)
    textRectstart = starttext.get_rect()
    textRectstart.center = width / 2, height / 4
    display.blit(starttext, textRectstart)

    while start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if start_button.draw(display):
            start=False
        if quit_button.draw(display):
            pygame.quit()
            sys.exit()
        pygame.display.update()



def pause():
    global paused
    display.fill(black)

    font = pygame.font.SysFont('Aptos', 80)
    pausetext=font.render("Paused",True,yellow)
    textRectpause=pausetext.get_rect()
    textRectpause.center=width/2,height/4
    display.blit(pausetext,textRectpause)

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = False

        if continue_button.draw(display):
            paused=False
        if quit_button.draw(display):
            pygame.quit()
            sys.exit()



        pygame.display.update()
startscreen()
playerreset()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                paused=True
                pause()

    display.blit(background, (0, 0))
    drawplayers()
    drawbackground()
    player1movement()
    player2movement()
    drawpath()
    playerdead() 
    playernames()


    if playerdeath:
        playerreset()



    pygame.display.update()
    clock.tick(20)

pygame.quit()
sys.exit()

#Quelllen: Pygame documentation, Stackoverflow, Geeks for geeks, thepythoncode.com,
#https://www.youtube.com/watch?v=G8MYGDf_9ho&t=162s
#https://youtu.be/kDSdjsdoGOY?feature=shared&t=219