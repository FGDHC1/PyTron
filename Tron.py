import subprocess, sys

def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

required_packages = ['pygame', 'pygame_gui']
for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        print(f"Installing {package}...")
        install_package(package)

import button, pygame, pygame_gui

pygame.init()

#Debug
debug=False #set to True if you want to enable DevMode

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
gray=(10,10,10)

#deathvariants
player1selfdeath=0
player2selfdeath=0
player1cutoffdeath=0
player2cutoffdeath=0
player1borderdeath=0
player2borderdeath=0

#who died
player1died=False
player2died=False


#speedup
speedup=True


#display conditions
width, height=1200,800
display = pygame.display.set_mode((width,height))
pygame.display.set_caption('PyTron')
pygame.mouse.set_visible(True)

#highscorevariables
highscore = 0
highscorename = 'Nobody'

#gamespeed
gamespeed=20

#FPS
clock = pygame.time.Clock()


#Playerstatus
player1name="Player1"
player2name="Player2"
player1score=0
player2score=0

playerwidth=10
playerspeed=10
playerdeath=False

#easteregg
easteregg=False
easteregg_count=0
#round limiter
no_of_rounds=0
round_limit=0
roundcounting=False

#gamestatus
paused=False
running=True
start=True
howtoplay=False
#debug

def activate_debug_mode(event):
    global debug
    if event.key == pygame.K_d and event.key == pygame.K_e and event.key == pygame.K_v or debug==True:
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

            if event.key == pygame.K_7:
                player2score = player2score + 1000000000000000000000000000000000000000000000000000000000000000000000000

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
        player1died_text = font.render(f"Player1died: {player1died}", True, white)
        player2died_text = font.render(f"Player2died: {player2died}", True, white)
        speedup_text = font.render(f"Speedup: {speedup}", True, white)
        gamespeed_text = font.render(f"Gamespeed: {gamespeed}", True, white)

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
        display.blit(highscore_text, (width-150, 340))
        display.blit(highscorename_text, (width-150, 360))
        display.blit(player1died_text, (width-150, 380))
        display.blit(player2died_text, (width - 150, 400))
        display.blit(speedup_text, (width-150, 420))
        display.blit(gamespeed_text, (width-150, 440))


    layoutlines()
    pointdebug(event)
    showvariables()

#debug end

#Backgrounds
background = pygame.Surface(display.get_size())
background = background.convert()
background.fill(black)

#pygame_gui manager and Textfields
manager=pygame_gui.UIManager((width,height))
Player1nameField=pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((width/4-125,height/2),(250,40)),
                                                    manager=manager, object_id="#player1name",initial_text="Player1")
Player2nameField=pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((((width/4)*3)-125,height/2),(250,40)),
                                                    manager=manager, object_id="#player2name",initial_text="Player2")
roundLimitField=pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((width/2-45,height/4*3),(95,40)),
                                                    manager=manager,object_id="#roundLimit",placeholder_text="Max Rounds")
speedup_button=pygame_gui.elements.UIButton(relative_rect=pygame.Rect((width/2-45,height/4*3+60),(95,40)),
                                            manager=manager,object_id="#speedup",text="Speedup: On")


#load images
start_img=pygame.image.load("png/Start_button.png").convert_alpha()
continue_img=pygame.image.load("png/Continue_button.png").convert_alpha()
quit_img=pygame.image.load("png/Quit_button.png").convert_alpha()
title_frame=pygame.image.load("png/Title_frame.png").convert_alpha()
howtoplay_img=pygame.image.load("png/HowToPlay_button_yellow.png").convert_alpha()
cross_img=pygame.image.load("png/Cross_button.png").convert_alpha()
arrowkeys_img=pygame.image.load("png/Arrowkeys.png").convert_alpha()
wasd_img=pygame.image.load("png/WASD_centered.png").convert_alpha()

#configure objects
start_button = button.Button(((width/4)*3)-125,height/4*3,start_img,1)
continue_button = button.Button(((width/4)*3)-125,height/4*3,continue_img,1)
quit_button = button.Button(width/4-125,height/4*3,quit_img, 1)
title_frame = button.Button(width/2-280,height/4-55,title_frame,1)
howtoplay_button = button.Button(width/2-96,height/4*3-100,howtoplay_img,1)
cross_button = button.Button(width-80,30,cross_img,1)
#Game background
def retrogrid (surface, gridcolor, gridsize):
    for x in range(0, width, gridsize):
        pygame.draw.line(surface, gridcolor, (x,0), (x,height))
    for y in range(0, height, gridsize):
        pygame.draw.line(surface, gridcolor, (0,y), (width,y))




def drawbackground():
    global background
    background.fill(black)
    retrogrid(background, purple, 40)


def playerreset():
    global player1dir,player2dir, player1poshistory, player2poshistory, player1pos, player2pos, playerdeath, start_time
    #P1
    player1pos = [width // 4, height // 2]
    player1dir = pygame.K_RIGHT
    player1poshistory = [player1pos.copy()]
    #p2
    player2pos = [width // 4 * 3, height // 2]
    player2dir = pygame.K_a
    player2poshistory = [player2pos.copy()]

    start_time=pygame.time.get_ticks()

    playerdeath=False


def drawplayers():
    #P1
    pygame.draw.rect(display, orange, pygame.Rect(player1pos[0],player1pos[1], playerwidth, playerwidth))
    #P2
    pygame.draw.rect(display, blue, pygame.Rect(player2pos[0], player2pos[1], playerwidth, playerwidth))


def player1movement():
    #sorce https://www.geeksforgeeks.org/snake-game-in-python-using-pygame-module/
    global player1poshistory, player1dir, player1pos
    global player2poshistory, player2dir, player2pos
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
    global no_of_rounds, player1score, player2score
    global player1cutoffdeath, player1selfdeath, player1borderdeath, player2cutoffdeath, player2selfdeath, player2borderdeath
    global player1died, player2died, playerdeath
    #player1 collision
    if player1pos in player2poshistory:
        playerdeath = True
        player1died=True
        player2score += 1
        no_of_rounds += 1
        player1cutoffdeath += 1
    if player1pos in player1poshistory[:-1]:
        playerdeath = True
        player1died=True
        player2score += 1
        no_of_rounds += 1
        player1selfdeath += 1

    # player2 collision
    if player2pos in player1poshistory:
        playerdeath = True
        player2died=True
        player1score += 1
        no_of_rounds += 1
        player2cutoffdeath += 1
    if player2pos in player2poshistory[:-1]:
        playerdeath = True
        player2died=True
        player1score += 1
        no_of_rounds += 1
        player2selfdeath += 1


    #border collision
    if player1pos[0] < 0 or player1pos[0] > width-1 or player1pos[1] < 0 or player1pos[1] > height-1 :
        playerdeath = True
        player1died=True
        player2score += 1
        no_of_rounds += 1
        player1borderdeath += 1
    if player2pos[0] < 0 or player2pos[0] > width-1 or player2pos[1] < 0 or player2pos[1] > height-1 :
        playerdeath = True
        player2died=True
        player1score += 1
        no_of_rounds += 1
        player2borderdeath += 1
    speedupfunc()


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


def numberfilter(input_string):
    global roundcounting
    filtered =''.join(filter(str.isdigit, input_string))
    if filtered=="":
        roundcounting=False
        return None
    else:
        return int(filtered)


def roundlimter():
    global roundcounting,no_of_rounds,round_limit,paused
    if roundcounting:
        if no_of_rounds < round_limit:
            pass
        else:
            paused=True


def show_roundwinner():
    global player1died, player2died
    font = pygame.font.SysFont('segoeuisemibold', 50)

    player1win_text = font.render(player1name + " made a point!", True, orange)
    textRectplayer1win = player1win_text.get_rect(center=(width / 2, height / 4))

    player2win_text = font.render(player2name + " made a point!", True, blue)
    textRectplayer2win = player2win_text.get_rect(center=(width / 2, height / 4))

    playertie_text = font.render("The round is a tie!", True, white)
    textRectplayertie = playertie_text.get_rect(center=(width / 2, height / 4))

    show_time = 1200

    if player1died != player2died:
        if player1died:
            display.blit(player2win_text, textRectplayer2win)
            pygame.display.update()
            pygame.time.delay(show_time)
        else:
            display.blit(player1win_text, textRectplayer1win)
            pygame.display.update()
            pygame.time.delay(show_time)
    elif player1died and player2died:
        display.blit(playertie_text, textRectplayertie)
        pygame.display.update()
        pygame.time.delay(show_time)
    player1died=False
    player2died=False


def toggle_speedup(event):
    global speedup
    if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == speedup_button:
        speedup = not speedup
        if speedup:
            speedup_button.set_text("Speedup: On")
            print("Speedup: On")
        else:
            speedup_button.set_text("Speedup: Off")
            print("Speedup: Off")

def speedupfunc():
    global gamespeed
    if speedup and playerdeath:
        gamespeed += 5


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

def easteregg_screen():
    global easteregg,start
    color_index=0
    rainbow_colors = [
        (255, 0, 0),
        (255, 32, 0),
        (255, 64, 0),
        (255, 96, 0),
        (255, 127, 0),
        (255, 159, 0),
        (255, 191, 0),
        (255, 223, 0),
        (255, 255, 0),
        (223, 255, 0),
        (191, 255, 0),
        (159, 255, 0),
        (127, 255, 0),
        (96, 255, 0),
        (64, 255, 0),
        (32, 255, 0),
        (0, 255, 0),
        (0, 255, 32),
        (0, 255, 64),
        (0, 255, 96),
        (0, 255, 127),
        (0, 255, 159),
        (0, 255, 191),
        (0, 255, 223),
        (0, 255, 255),
        (0, 223, 255),
        (0, 191, 255),
        (0, 159, 255),
        (0, 127, 255),
        (0, 96, 255),
        (0, 64, 255),
        (0, 32, 255),
        (0, 0, 255),
        (32, 0, 255),
        (64, 0, 255),
        (96, 0, 255),
        (127, 0, 255),
        (159, 0, 255),
        (191, 0, 255),
        (223, 0, 255),
        (255, 0, 255),
        (255, 0, 223),
        (255, 0, 191),
        (255, 0, 159),
        (255, 0, 127),
        (255, 0, 96),
        (255, 0, 64),
        (255, 0, 32),
    ]

    pygame.mouse.set_visible(True)
    display.fill(gray)
    title_font = pygame.font.SysFont('segoeuisemibold', 55)

    while easteregg:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    easteregg = False
                    start=True

            #debug
            if event.type == pygame.KEYDOWN:
                activate_debug_mode(event)
            if debug:
                debugtools(event)
            #debug end
        if color_index == len(rainbow_colors) - 1:
            color_index = 0
        else:
            color_index += 1
        eastereggtext = title_font.render("Congrats you have found an easteregg!", True, rainbow_colors[color_index])
        textRecteasteregg = eastereggtext.get_rect()
        textRecteasteregg.center = width / 2, height / 2
        pygame.time.wait(20)
        display.blit(eastereggtext, textRecteasteregg)
        if cross_button.draw(display):
            easteregg = False
            start=True
        pygame.display.update()
    pygame.mouse.set_visible(False)

def howtoplay_screen():
    global howtoplay,start
    pygame.mouse.set_visible(True)
    display.fill(gray)
    title_font = pygame.font.SysFont('segoeuisemibold', 55)
    playername_font = pygame.font.SysFont('segoeuisemibold', 30)
    text_font = pygame.font.SysFont('segoeuisemibold', 20)

    howtoplaytext = title_font.render("How to play", True, yellow)
    tutorialtext1 = text_font.render("To make a point, force your opponent to collide with your path, make them collide with themselves, ", True, white)
    tutorialtext2= text_font.render("or make them crash into the borders.", True, white)
    player1name_text = playername_font.render(player1name, True, orange)
    player2name_text = playername_font.render(player2name, True, blue)

    textRecthowtoplay = howtoplaytext.get_rect()
    textRecthowtoplay.center = width / 2, height / 8

    textRectplayer1name=player1name_text.get_rect()
    textRectplayer1name.center=width/4,height/4+120

    textRectplayer2name=player2name_text.get_rect()
    textRectplayer2name.center=width/4*3,height/4+120

    textRecttutorialtext1=tutorialtext1.get_rect()
    textRecttutorialtext1.center=width/2,height/8+75

    textRecttutorialtext2=tutorialtext2.get_rect()
    textRecttutorialtext2.center=width/2,height/8+100

    display.blit(howtoplaytext, textRecthowtoplay)
    display.blit(player1name_text, textRectplayer1name)
    display.blit(player2name_text, textRectplayer2name)
    display.blit(tutorialtext1, textRecttutorialtext1)
    display.blit(tutorialtext2, textRecttutorialtext2)

    display.blit(wasd_img,(width/4-185,height/4*2))
    display.blit(arrowkeys_img,(width/4*3-185,height/4*2))
    while howtoplay:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    howtoplay = False
                    start=True

            #debug
            if event.type == pygame.KEYDOWN:
                activate_debug_mode(event)
            if debug:
                debugtools(event)
            #debug end
        if cross_button.draw(display):
            howtoplay = False
            start=True
        pygame.display.update()
    pygame.mouse.set_visible(False)

def startscreen():
    global start,player1name,player2name,round_limit,roundcounting,debug,howtoplay,easteregg_count,easteregg
    display.fill(gray)
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
                roundcounting=True
                round_limit = numberfilter(event.text)


            #debug
            if event.type == pygame.KEYDOWN:
                activate_debug_mode(event)
            if debug:
                debugtools(event)
            #debug end

            toggle_speedup(event)

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
        if howtoplay_button.draw(display):
            start=False
            howtoplay=True
        if title_frame.draw(display):
            if easteregg_count==2:
                start=False
                easteregg=True
            else:
                easteregg_count+=1
        title_frame.draw(display)
        manager.draw_ui(display)
        pygame.display.update()
    if round_limit is not None:
        round_limit = int(round_limit)
    pygame.mouse.set_visible(False)

def pause():
    #sorce https://pythonprogramming.net/pause-game-pygame/
    global paused,debug
    pygame.mouse.set_visible(True)
    display.fill(gray)

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
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                    paused = False

            #debug
            if event.type == pygame.KEYDOWN:
                activate_debug_mode(event)
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

#main loop
retrogrid(background, purple, 40)
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
            #debug
            activate_debug_mode(event)
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

    if easteregg:
        easteregg_screen()
    if playerdeath:
        show_roundwinner()
        pygame.display.update()

    if howtoplay:
        howtoplay_screen()

    if start:
        startscreen()

    if paused:
        pause()

    if playerdeath:
        playerreset()



    pygame.display.update()
    clock.tick(gamespeed)


save_highscore()
pygame.quit()
sys.exit()



#Quelllen: Pygame documentation, Stackoverflow, Geeks for geeks, Reddit
#rhttps://www.youtube.com/watch?v=G8MYGDf_9ho
#https://youtu.be/kDSdjsdoGOY?feature=shared&t=89