'''
Created on 25 Feb 2013

@author: Luis Checa
'''
import pygame , sys
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE
# it starts!
pygame.init()
# Set Clock FPS
fps = pygame.time.Clock()
# Set window to 800 by 600px
window = pygame.display.set_mode((800,600))
# Set Game window title
pygame.display.set_caption("Hangman!")
# Load main object image (cat in this case)
bg = pygame.image.load('hangman_bg.jpg').convert()
menu = pygame.image.load('hangman.jpg').convert()
# Assign colour names for ease of use
red = pygame.Color(255,0,0)
green = pygame.Color(0,255,0)
blue = pygame.Color(0,0,255)
black = pygame.Color(0,0,0)
white = pygame.Color(255,255,255)
font = pygame.font.SysFont('calibri', 30)
missed = ''
correct = ''
warning = 'Guess a letter.'
secretWord = 'birthday'
gameIsDone = False
rect_list = []

def draw_bg():
    window.blit(bg, (0,0))
    pygame.display.update()
    
def draw_menu():
    window.blit(menu,(0,0))
    draw_msg('Guess or die trying!')
    fps.tick(30)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
                
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.event.post(pygame.event.Event(QUIT))
        return
    pygame.display.update()
    
def draw_msg(msg):
    msgSurface = font.render(msg, True, white)
    msgRect = msgSurface.get_rect()
    msgRect.topleft = (10,5)
    maxRect = (0,0,600,30)
    window.blit(bg, maxRect)
    window.blit(msgSurface, msgRect)
    global rect_list
    rect_list.append(maxRect)
    
def draw_font(msg, pos, color=green):
    Surface = font.render(msg, True, color)
    Rect = Surface.get_rect()
    Rect.topleft = pos
    window.blit(Surface, Rect)
    return Rect
 
def draw_wrong():
    global missed
    msg = 'Missed letters: '
    for letter in missed:
        msg += letter.upper() + ", "
    Rect = draw_font(msg, (50, 35), red)
    global rect_list
    rect_list.append(Rect)

def draw_right():
    global correct, secretWord
    blanks = '_' * len(secretWord)

    for i in range(len(secretWord)): # replace blanks with correctly guessed letters
        if secretWord[i] in correct:
            blanks = blanks[:i] + secretWord[i] + blanks[i+1:]
    toguess= ''
    for letter in blanks: # show the secret word with spaces in between each letter
        toguess += letter
    Rect = draw_font(toguess.upper(), (50, 80))
    global rect_list
    rect_list.append(Rect)

def draw_man():
    global missed, rect_list
    parts = len(missed)
    if parts == 1:
        x,y = 430, 170
        head = pygame.draw.circle(window, white, (x, y), 30)
        pygame.draw.aaline(window,black,(x-15,y+12),(x+15,y-12))
        pygame.draw.aaline(window,black,(x-15,y-12),(x+15,y+12))
        rect_list.append(head)
    if parts >= 2:
        x,y = 430, 330
        points = [(x-15,y-135),(x-35,y),(x+35,y),(x+15,y-135)]
        body = pygame.draw.polygon(window,white,points)
        rect_list.append(body)
    if parts >= 3:
        x,y = 372, 300
        points = [(x+40,y-90),(x,y),(x+35,y-35)]
        arm = pygame.draw.polygon(window,white,points)
        rect_list.append(arm)
    if parts >= 4:
        x,y = 485, 300
        points = [(x-40,y-90),(x,y),(x-35,y-35)]
        arm1 = pygame.draw.polygon(window,white,points)
        rect_list.append(arm1)
    if parts == 5:
        x,y = 440, 380
        points = [(x-5,y+5),(x+10,y+5),(x+5,y-50),(x-5,y-50)]
        leg = pygame.draw.polygon(window,white,points)
        rect_list.append(leg)
        
        points = [x,y,20,15]
        foot = pygame.draw.ellipse(window,white,points)
        rect_list.append(foot)
    if parts == 6:
        x,y = 370, 380
        points = [(x-5,y+5),(x+10,y+5),(x+5,y-50),(x-5,y-50)]
        leg = pygame.draw.polygon(window,white,points)
        rect_list.append(leg)
        
        points = [x,y,20,15]
        foot = pygame.draw.ellipse(window,white,points)
        draw_msg('You have run out of guesses!')
        rect_list.append(foot)
def is_correct():
    global guess, correct, secretWord, gameIsDone
    if guess in secretWord:
        correct = correct + guess
        draw_right()
        # Check if the player has won
        foundAllLetters = True
        for i in range(len(secretWord)):
            if secretWord[i] not in correct:
                foundAllLetters = False
        if foundAllLetters:
            draw_msg('Yes! You won!')
            gameIsDone = True
        
    else:
        global missed
        missed = missed + guess
        draw_wrong()
        draw_man()
        # Check if player has guessed too many times and lost
        #if len(missed) == 6:
            
            #gameIsDone = True

def check_guess(guess, alreadyGuessed):
    if len(guess) != 1:
        draw_msg('Guess a single letter')
    elif guess in alreadyGuessed:
        draw_msg('Already guessed that letter, Try again.')
    elif guess not in 'abcdefghijklmnopqrstuvwxyz':
        draw_msg('Enter a LETTER.')
    else:
        draw_msg('Guess another letter')
        pygame.time.delay(50)
        return guess
    
    guess = ''
    get_input()
    return guess   
    
draw_bg()
draw_msg('Guess a letter!')
draw_wrong()
draw_right()
pygame.display.update(rect_list)
fps.tick(30)
  
def get_input():
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
                
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.event.post(pygame.event.Event(QUIT))
            guess = pygame.key.name(event.key)
            guess = check_guess(guess, missed + correct)
            return guess
    return ''
# Let the player type in a letter.
while not gameIsDone:
    rect_list = []
    guess = get_input()
    is_correct()
    pygame.display.update(rect_list)
    