'''
Created on 25 Feb 2013

@author: Luis Checa
'''
import pygame , sys
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE,K_a
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
#blue = pygame.Color(0,0,255)
#black = pygame.Color(0,0,0)
#white = pygame.Color(255,255,255)
font = pygame.font.SysFont('calibri', 30)
missed = ''
correct = ''
warning = 'Guess a letter.'
secretWord = 'happy birthday'
gameIsDone = False
rect_list = []
is_valid = False

def draw_bg():
    window.blit(bg, (0,0))
    pygame.display.update()
    
def draw_menu():
    window.blit(menu,(0,0))
    draw_msg('Guess or die trying!', menu)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
                
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.event.post(pygame.event.Event(QUIT))
            if event.key == K_a:
                return
    fps.tick(30)
    pygame.display.update()
    
def draw_msg(msg, bg):
    msgSurface = font.render(msg, True, red)
    msgRect = msgSurface.get_rect()
    msgRect.topleft = (10,5)
    window.blit(bg,msgRect.topleft,msgRect)
    window.blit(msgSurface, msgRect)
    global rect_list
    rect_list.append(msgRect)
    
def draw_font(guess, pos):
    Surface = font.render(guess, True, green)
    Rect = Surface.get_rect()
    Rect.topleft = pos
    window.blit(Surface, Rect)
    return Rect
 
def draw_wrong(missed):
    msg = 'Missed letters:'
    for letter in missed:
        msg += letter + ", "
    Rect = draw_font(msg, (50, 35))
    global rect_list
    rect_list.append(Rect)

def draw_word(secretWord, correct):
    blanks = '_' * len(secretWord)

    for i in range(len(secretWord)): # replace blanks with correctly guessed letters
        if secretWord[i] in correct:
            blanks = blanks[:i] + secretWord[i] + blanks[i+1:]
    toguess= ''
    for letter in blanks: # show the secret word with spaces in between each letter
        toguess += letter
    Rect = draw_font(toguess, (50, 80))
    global rect_list
    rect_list.append(Rect)

def check_guess(guess, alreadyGuessed):
    if len(guess) != 1:
        draw_msg('Please guess a letter'. bg)
    elif guess in alreadyGuessed:
        draw_msg('You have already guessed that letter. Choose again.', bg)
    elif guess not in 'abcdefghijklmnopqrstuvwxyz':
        draw_msg('Please enter a LETTER.', bg)
    else:
        draw_msg('Please guess another letter', bg)
        pygame.time.delay(50)
        return guess
    
    guess = ''
    get_input()
    return guess

def is_correct(guess,correct):
    if guess in secretWord:
        correct = correct + guess
        draw_word(secretWord, correct)
        # Check if the player has won
        foundAllLetters = True
        for i in range(len(secretWord)):
            if secretWord[i] not in correct:
                foundAllLetters = False
        if foundAllLetters:
            draw_msg('Yes! The secret word is "' + secretWord + '"! You have won!', bg)
            gameIsDone = True
        
    else:
        global missed
        missed = missed + guess
        draw_wrong(missed)
        # Check if player has guessed too many times and lost
        if len(missed) == 6:
            draw_msg('You have run out of guesses!', bg)
            gameIsDone = True
        
def display_board(missed, correct, secretWord):
    draw_wrong(missed)
    draw_word(secretWord, correct)
    
draw_bg()
display_board(missed, correct, secretWord)
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
    is_correct(guess, correct)
    pygame.display.update(rect_list)
    