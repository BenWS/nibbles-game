import copy
import pygame
from pygame import font
from layout import Container
from globals import RED
font.init()


screen = pygame.display.set_mode([1000,1000]) 
'''
Initialize and build the Container object and its child surfaces
'''
text_container = Container(screen, margin=(200,100,200,100),border_enabled=True)
blank_container = Container(text_container,min_height=30, min_width=100,border_enabled=True)

greeting_font = font.Font(None, 60)
greeting_text = greeting_font.render('Oh hi!', True, (255,0,0))
greeting_text_2 = greeting_font.render('Oh no!', True, (255,0,0))

'''
TODO: 2023_11_16_1

Refactor code to match the desired interface
'''

text_container.add_child(greeting_text)
text_container.add_child(blank_container,id='my_container')
text_container.add_child(greeting_text)
text_container.add_child(greeting_text)
text_container.add_child(blank_container)
text_container.add_child(greeting_text)
text_surface,text_rect = text_container.render()
screen.blit(text_surface, text_rect)

element = text_container.get_child(id='my_container')
print(element.vertical_offset)
# blank_container.render()
# greeting_screen.blit()


# Run until the user asks to quit
running = True
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()