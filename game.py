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
blue = pygame.Color(0,0,255)
black = pygame.Color(0,0,0)
white = pygame.Color(255,255,255)
font = pygame.font.SysFont('calibri', 28)
missed = ''
correct = ''
guess = ''
warning = 'Guess a letter.'
secretWord = 'happy birthday'
gameIsDone = False
def draw_msg(msg):
    msgSurface = font.render(msg, True, red)
    msgRect = msgSurface.get_rect()
    msgRect.topleft = (10,10)
    window.blit(msgSurface, msgRect)

def draw_menu():
    window.blit(menu,(0,0))
    draw_msg('Guess or die trying!')
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
                
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.event.post(pygame.event.Event(QUIT))
            if event.key == K_a:
                displayBoard()
    pygame.display.update()
    fps.tick(30)
def draw_font(guess, pos):
    Surface = font.render(guess, True, green)
    Rect = Surface.get_rect()
    Rect.topleft = pos
    window.blit(Surface, Rect)
def checkGuess(alreadyGuessed):
    if len(guess) == 0:
        return False
    if len(guess) != 1:
        warning ='Please enter a single letter.'
        return False
    elif guess in alreadyGuessed:
        warning = 'You have already guessed that letter. Choose again.'
        return False
    elif guess not in 'abcdefghijklmnopqrstuvwxyz':
        warning = 'Please enter a LETTER.'
        return False
    else:
        return True
def displayBoard(missed, correct, secretWord):
    window.blit(bg, (0,0))

    msg = 'Missed letters:'
    for letter in missed:
        msg += letter + ", "
    draw_font(msg, (50, 30))

    blanks = '_' * len(secretWord)

    for i in range(len(secretWord)): # replace blanks with correctly guessed letters
        if secretWord[i] in correct:
            blanks = blanks[:i] + secretWord[i] + blanks[i+1:]
    toguess= ''
    for letter in blanks: # show the secret word with spaces in between each letter
        toguess += letter
    draw_font(toguess, (50, 80))
    draw_msg(warning)

while True:
    fps.tick(30)
    displayBoard(missed, correct, secretWord)
    pygame.display.update()
      
    # Let the player type in a letter.
    while not checkGuess(missed + correct):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                    
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.event.post(pygame.event.Event(QUIT))
                guess = pygame.key.name(event.key)
                
        draw_msg(warning)
        pygame.display.update()

    if guess in secretWord:
        correct = correct + guess

        # Check if the player has won
        foundAllLetters = True
        for i in range(len(secretWord)):
            if secretWord[i] not in correct:
                foundAllLetters = False
                break
        if foundAllLetters:
            draw_msg('Yes! The secret word is "' + secretWord + '"! You have won!')
            gameIsDone = True
    else:
        missed = missed + guess

        # Check if player has guessed too many times and lost
        if len(missed) == 6:
            displayBoard(missed, correct, secretWord)
            draw_msg('You have run out of guesses!\nAfter ' + str(len(missed)) + ' missed guesses and ' + str(len(correct)) + ' correct guesses, the word was "' + secretWord + '"')
            gameIsDone = True

    # Ask the player if they want to play again (but only if the game is done).
    if gameIsDone:
            break
    
    