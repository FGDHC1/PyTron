import pygame
import sys
import button
import pygame_gui

pygame.init()

#colors
white=(255,255,255)
black=(0,0,0)
orange=(255,90,0)
blue=(50,50,255)
grey=(127,127,127)
purple=(127,0,127)
green=(0,255,0)
red=(255,0,0)
yellow=(255,255,0)

#deathvariants
player1selfdeath=0
player2selfdeath=0
player1cutoffdeath=0
player2cutoffdeath=0
player1borderdeath=0
player2borderdeath=0

#display conditions
width, height=1000,700
display = pygame.display.set_mode((width,height))
pygame.display.set_caption('PyTron')
pygame.mouse.set_visible(True)

#highscorevariables
highscore = 0
highscorename = 'Nobody'

#debug
def toggle_debug_mode(event):
    global debug
    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[pygame.K_d] and pressed_keys[pygame.K_e] and pressed_keys[pygame.K_v]:
        debug =True
        print("Debug Mode: ON")


def debugtools(event):
    def layoutlines():
        pygame.draw.line(display, white, (width/2, 0), (width/2, height))
        pygame.draw.line(display, white, (width/3, 0), (width/3, height))
        pygame.draw.line(display, white, (width/3*2, 0), (2*width/3, height))
        pygame.draw.line(display, white, (width/4, 0), (width/4, height))
        pygame.draw.line(display, white, (width/4*3, 0), (3*width/4, height))

        # Horizontale Linie
        pygame.draw.line(display, white, (0, height/2), (width, height/2))
        pygame.draw.line(display, white, (0, height/4), (width, height/4))
        pygame.draw.line(display, white, (0, height/4*3), (width, height/4*3))

    def pointdebug(event):
        global player1score, player2score,debug
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_6:
                player1score = player1score + 1000000000000000000000000000000000000000000000000000000000000000000000000
                debug = True
            if event.key == pygame.K_7:
                player2score = player2score + 1000000000000000000000000000000000000000000000000000000000000000000000000
                debug = True
    def showvariables():
        font = pygame.font.SysFont('Arial', 15)
        #extract
        debug_text = font.render(f"Debug: {debug}", True, white)
        clock_text = font.render(f"Clock: {clock}", True, white)
        playerdeath_text = font.render(f"Death: {playerdeath}", True, white)
        no_of_rounds_text = font.render(f"No.Rounds: {no_of_rounds}", True, white)
        round_limit_text = font.render(f"RoundLimit: {round_limit}", True, white)
        roundcounting_text = font.render(f"RoundCounting: {roundcounting}", True, white)
        running_text = font.render(f"Running: {running}", True, white)
        paused_text = font.render(f"Paused: {paused}", True, white)
        start_text = font.render(f"Start: {start}", True, white)
        highscore_text = font.render(f"Highscore: {highscore}", True, white)
        highscorename_text = font.render(f"Highscorename: {highscorename}", True, white)

        #show
        display.blit(debug_text, (width-150, 0))
        display.blit(clock_text, (width-150, 20))
        display.blit(playerdeath_text, (width-150, 40))
        display.blit(no_of_rounds_text, (width-150, 60))
        display.blit(round_limit_text, (width-150, 80))
        display.blit(roundcounting_text, (width-150, 100))
        display.blit(running_text, (width-150, 120))
        display.blit(paused_text, (width-150, 140))
        display.blit(start_text, (width-150, 160))
        display.blit(highscore_text, (width-150, 180))
        display.blit(highscorename_text, (width-150, 200))

    layoutlines()
    pointdebug(event)
    showvariables()

#debug end

#FPS
clock = pygame.time.Clock()

#Debug
debug=False

#Playerstatus
player1name="Player1"
player2name="Player2"
player1score=0
player2score=0

playerwidth=10
playerspeed=10
playerdeath=False

#round limiter
no_of_rounds=0
round_limit=0
roundcounting=False

#gamestatus
paused=False
running = True
start=True

#pygame_gui manager and Textfields
manager=pygame_gui.UIManager((width,height))
Player1nameField=pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((width/4-125,height/2),(250,40)),
                                                    manager=manager, object_id="#player1name",initial_text="Player1")
Player2nameField=pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((((width/4)*3)-125,height/2),(250,40)),
                                                    manager=manager, object_id="#player2name",initial_text="Player2")
roundLimitField=pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((width/2-45,height/4*3),(95,40)),
                                                    manager=manager,object_id="#roundLimit",placeholder_text="Max Rounds")

#load Button images
start_img=pygame.image.load("png/Start_button.png").convert_alpha()
continue_img=pygame.image.load("png/Continue_button.png").convert_alpha()
quit_img=pygame.image.load("png/Quit_button.png").convert_alpha()
title_frame=pygame.image.load("png/Title_frame.png").convert_alpha()

#configure objects
start_button = button.Button(((width/4)*3)-125,height/4*3,start_img,1)
continue_button = button.Button(((width/4)*3)-125,height/4*3,continue_img,1)
quit_button = button.Button(width/4-125,height/4*3,quit_img, 1)
title_frame = button.Button(width/2-280,height/4-55,title_frame,1)

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
    #P1
    player1pos = [width // 4, height // 2]
    player1dir = pygame.K_RIGHT
    player1poshistory = [player1pos.copy()]
    #p2
    player2pos = [width // 4 * 3, height // 2]
    player2dir = pygame.K_a
    player2poshistory = [player2pos.copy()]

    playerdeath=False


def drawplayers():
    #P1
    pygame.draw.rect(display, orange, pygame.Rect(player1pos[0],player1pos[1], playerwidth, playerwidth))
    #P2
    pygame.draw.rect(display, blue, pygame.Rect(player2pos[0], player2pos[1], playerwidth, playerwidth))


def player1movement():
    global player1poshistory, player1dir, player1pos
    pressedkey = pygame.key.get_pressed()

    #Key scan
    if pressedkey[pygame.K_d] and player1dir!=pygame.K_a:
        player1dir = pygame.K_d
    elif pressedkey[pygame.K_a] and player1dir!=pygame.K_d:
        player1dir = pygame.K_a
    elif pressedkey[pygame.K_w] and player1dir!=pygame.K_s:
        player1dir = pygame.K_w
    elif pressedkey[pygame.K_s] and player1dir!=pygame.K_w:
        player1dir = pygame.K_s

    #Player Move
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

    #Key scan
    if pressedkey[pygame.K_RIGHT] and player2dir!=pygame.K_LEFT:
        player2dir = pygame.K_RIGHT
    elif pressedkey[pygame.K_LEFT] and player2dir!=pygame.K_RIGHT:
        player2dir = pygame.K_LEFT
    elif pressedkey[pygame.K_UP] and player2dir!=pygame.K_DOWN:
        player2dir = pygame.K_UP
    elif pressedkey[pygame.K_DOWN] and player2dir!=pygame.K_UP:
        player2dir = pygame.K_DOWN

    #Player Move
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
        #P1
        for pos1 in player1poshistory:
            pygame.draw.rect(display, orange, pygame.Rect(pos1[0], pos1[1], playerwidth, playerwidth))
        #P2
        for pos2 in player2poshistory:
            pygame.draw.rect(display, blue, pygame.Rect(pos2[0], pos2[1], playerwidth, playerwidth))


def playerdead():
    global playerdeath,player1score,player2score,no_of_rounds,player1cutoffdeath,player1selfdeath,player2cutoffdeath,player2selfdeath,player1borderdeath,player2borderdeath
    #player1 collision
    if player1pos in player2poshistory:
        playerdeath = True
        player2score += 1
        no_of_rounds += 1
        player1cutoffdeath += 1
    if player1pos in player1poshistory[:-1]:
        playerdeath = True
        player2score += 1
        no_of_rounds += 1
        player1selfdeath += 1

    # player2 collision
    if player2pos in player1poshistory:
        playerdeath = True
        player1score += 1
        no_of_rounds += 1
        player2cutoffdeath += 1
    if player2pos in player2poshistory[:-1]:
        playerdeath = True
        player1score += 1
        no_of_rounds += 1
        player2selfdeath += 1


    #border collision
    if player1pos[0] < 0 or player1pos[0] > width-1 or player1pos[1] < 0 or player1pos[1] > height-1 :
        playerdeath = True
        player2score += 1
        no_of_rounds += 1
        player1borderdeath += 1
    if player2pos[0] < 0 or player2pos[0] > width-1 or player2pos[1] < 0 or player2pos[1] > height-1 :
        playerdeath = True
        player1score += 1
        no_of_rounds += 1
        player2borderdeath += 1


def playernames():
    global player1name, player2name,player1score,player2score
    #Text on Scoreboard
    player1out = player1name+": "+str(player1score)
    player2out = player2name+": "+str(player2score)
    font=pygame.font.SysFont('segoeuisemibold',20)
    #player2
    textp1=font.render(player1out,True,orange)
    textRectp1=10,10
    display.blit(textp1,textRectp1)
    #player2
    textp2 = font.render(player2out, True, blue)
    textRectp2 = 10, 35
    display.blit(textp2, textRectp2)


def save_highscore():
    #determine if highscore is topped
    global player1score, player2score,player1name,player2name,highscore,highscorename
    if debug:
        pass
    else:
        if player1score>player2score and player1score>highscore:
            highscore=player1score
            highscorename=player1name
        if player2score>player1score and player2score>highscore:
            highscore=player2score
            highscorename=player2name
        #save highscore
        with open('highscore.txt', 'w') as file:
            file.write(f"{highscore},{highscorename}")

def load_highscore():
    global highscore, highscorename
    try:
        with open('highscore.txt', 'r') as file:
            line = file.readline()
            highscore_str, highscorename = line.strip().split(',')
            highscore = int(highscore_str)
    except Exception:
        highscore, highscorename = 0, 'Nobody'


def roundlimter():
    global roundcounting,no_of_rounds,round_limit,paused2
    if roundcounting:
        if no_of_rounds < round_limit:
            pass
        else:
            paused=True


def numberfilter(input_string):
    filtered =''.join(filter(str.isdigit, input_string))
    return int(filtered)


def pausestats():
    stat_font = pygame.font.SysFont('segoeuisemibold', 20)
    playername_font = pygame.font.SysFont('segoeuisemibold', 30)

    player1name_text = playername_font.render(player1name, True, orange)
    player2name_text = playername_font.render(player2name, True, blue)
    #get player1stats
    player1score_text = stat_font.render("Score: "+str(player1score), True, white)
    player1selfdeath_text = stat_font.render("Death by self-collision: "+str(player1selfdeath), True, white)
    player1cutoffdeath_text = stat_font.render("Death by opponent-collision: "+str(player1cutoffdeath), True, white)
    player1borderdeath_text = stat_font.render("Death by border-collision: "+str(player1borderdeath), True, white)
    #get player2stats
    player2score_text = stat_font.render("Score: "+str(player2score), True, white)
    player2selfdeath_text = stat_font.render("Death by self-collision: "+str(player2selfdeath), True, white)
    player2cutoffdeath_text = stat_font.render("Death by opponent-collision: "+str(player2cutoffdeath), True, white)
    player2borderdeath_text = stat_font.render("Death by border-collision: "+str(player2cutoffdeath), True, white)

    #center texts from player1
    textRectplayer1name=player1name_text.get_rect()
    textRectplayer1name.center=width/4,height/4

    textRectplayer1score=player1score_text.get_rect()
    textRectplayer1score.center=width/4,height/4+40

    textRectplayer1selfdeath=player1selfdeath_text.get_rect()
    textRectplayer1selfdeath.center=width/4,height/4+70

    textRectplayer1cutoffdeath=player1cutoffdeath_text.get_rect()
    textRectplayer1cutoffdeath.center=width/4,height/4+100

    textRectplayer1borderdeath=player1borderdeath_text.get_rect()
    textRectplayer1borderdeath.center=width/4,height/4+130

    #center texts from player2
    textRectplayer2name=player2name_text.get_rect()
    textRectplayer2name.center=width/4*3,height/4

    textRectplayer2score=player2score_text.get_rect()
    textRectplayer2score.center=width/4*3,height/4+40

    textRectplayer2selfdeath=player2selfdeath_text.get_rect()
    textRectplayer2selfdeath.center=width/4*3,height/4+70

    textRectplayer2cutoffdeath=player2cutoffdeath_text.get_rect()
    textRectplayer2cutoffdeath.center=width/4*3,height/4+100

    textRectplayer2borderdeath=player2borderdeath_text.get_rect()
    textRectplayer2borderdeath.center=width/4*3,height/4+130



    #show names
    display.blit(player1name_text, textRectplayer1name)
    display.blit(player2name_text, textRectplayer2name)

    #show player1 stats
    display.blit(player1score_text, textRectplayer1score)
    display.blit(player1selfdeath_text, textRectplayer1selfdeath)
    display.blit(player1cutoffdeath_text, textRectplayer1cutoffdeath)
    display.blit(player1borderdeath_text, textRectplayer1borderdeath)
    #show player2 stats
    display.blit(player2score_text, textRectplayer2score)
    display.blit(player2selfdeath_text, textRectplayer2selfdeath)
    display.blit(player2cutoffdeath_text, textRectplayer2cutoffdeath)
    display.blit(player2borderdeath_text, textRectplayer2borderdeath)


def startscreen():
    global start,player1name,player2name,round_limit,roundcounting,debug
    display.fill(black)
    pygame.mouse.set_visible(True)

    title_font = pygame.font.SysFont('segoeuisemibold', 65)
    starttext = title_font.render("PyTron", True, yellow)
    textRectstart = starttext.get_rect()
    textRectstart.center = width / 2, height / 4-10
    display.blit(starttext, textRectstart)

    while start:
        UIRefreshRate=clock.tick(20)/1200
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_highscore()
                pygame.quit()
                sys.exit()
            #getnames
            if event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED and event.ui_element == Player1nameField:
                player1name = event.text
            if event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED and event.ui_element == Player2nameField:
                player2name = event.text
            #roundlimiting
            if event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED and event.ui_element == roundLimitField:
                round_limit = numberfilter(event.text)
                roundcounting=True

            #debug
            if event.type == pygame.KEYDOWN:
                toggle_debug_mode(event)
            if debug:
                debugtools(event)
            #debug end


            manager.process_events(event)
        manager.update(UIRefreshRate)

        highscore_font = pygame.font.SysFont('segoeuisemibold', 20)
        highscoretext = highscore_font.render(f"Highscore: {highscore} from {highscorename}", True, white)
        textRecthighscore = highscoretext.get_rect()
        textRecthighscore.center = width/2,height/4+70
        display.blit(highscoretext, textRecthighscore)

        if start_button.draw(display):
            start=False
        if quit_button.draw(display):
            save_highscore()
            pygame.quit()
            sys.exit()
        title_frame.draw(display)
        manager.draw_ui(display)
        pygame.display.update()
    round_limit = int(round_limit)
    pygame.mouse.set_visible(False)


def pause():
    global paused,debug
    pygame.mouse.set_visible(True)
    display.fill(black)

    title_font = pygame.font.SysFont('segoeuisemibold', 65)
    pausetext=title_font.render("Paused",True,yellow)
    textRectpause=pausetext.get_rect()
    textRectpause.center=width/2,height/4-10
    display.blit(pausetext,textRectpause)

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_highscore()
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_0:
                    paused = False

            #debug
            if event.type == pygame.KEYDOWN:
                toggle_debug_mode(event)
            if debug:
                debugtools(event)
            #debug end

        if continue_button.draw(display):
            paused=False
        if quit_button.draw(display):
            save_highscore()
            pygame.quit()
            sys.exit()
        pausestats()
        pygame.display.update()
    pygame.mouse.set_visible(False)


load_highscore()
startscreen()
playerreset()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                paused=True
                pause()
            #debug
            toggle_debug_mode(event)
        if debug:
            debugtools(event)
            #debug end
    display.blit(background, (0, 0))
    drawplayers()
    drawbackground()
    player1movement()
    player2movement()
    drawpath()
    playerdead() 
    playernames()
    roundlimter()


    if playerdeath:
        playerreset()



    pygame.display.update()
    clock.tick(20)


save_highscore()
pygame.quit()
sys.exit()

#Quelllen: Pygame documentation, Stackoverflow, Geeks for geeks, thepythoncode.com, Reddit
#https://www.youtube.com/watch?v=G8MYGDf_9ho&t=162s
#https://youtu.be/kDSdjsdoGOY?feature=shared&t=219