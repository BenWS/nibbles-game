# WIP: 2023_09_02_1

# Simple pygame program


'''
TODO: 2023_09_09_1 - Design Class for Screen Element Management

I should create a framework for UI element management akin to HTML
and the DOM tree where I can position child elements with respect
to the parents and position element size in terms of percentages,
versus absolute size in pixels.

Let's coin the term 'Screen Object Model' or SOM to indicate kinship with
the concept of DOM.

- 09-09-2023: 
  - Trying to understand how to create an abstract class
    (or similar construct) through which I can manage UI containers without
    coupling too closely with low-level sprites
  - Will I need recursive 'blitting' to render the full SOM tree?
'''

# Import and initialize the pygame library
import pygame
from pygame import font, surface
pygame.init()	

class GreetingScreen:
    def __init__(self,parent_surface):
        self.parent_surface = parent_surface
        self.my_font = font.Font(None,100)
        self.text = self.my_font.render('Greetings!', True, (255,0,0))
        self.primary_rect = self.text.get_rect()
        
    def get_text(self):
         return self.text
    
    def set_position(self,mode):
        if mode == 'center':  
          self.primary_rect.center = (self.parent_surface.get_width()//2,self.parent_surface.get_height()//2)   
        if mode == 'left_middle':  
          self.primary_rect.left = 0
          self.primary_rect.centery = self.parent_surface.get_height()//2
        if mode == 'right_middle':  
          self.primary_rect.right = self.parent_surface.get_width()
          self.primary_rect.centery = self.parent_surface.get_height()//2
    
    def blit(self):
        self.parent_surface.blit(self.text,self.primary_rect)

    
# Set up the drawing window
screen = pygame.display.set_mode([1000, 1000])

# Run until the user asks to quit
running = True
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with white
    screen.fill((255, 255, 255))

    # initialize game screen
    greeting_screen = GreetingScreen(screen)
    greeting_screen.set_position('center')
    greeting_screen.blit()

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()