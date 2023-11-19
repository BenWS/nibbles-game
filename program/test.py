import copy
import pygame
from pygame import font
from layout import Container
from globals import RED
font.init()

    # child_union_rect = pygame.Rect.unionall(self.children)
    # child_surface_rect = self.children[0].get_rect()
    # if mode == 'center':  
    #   child_union_rect.center = (self.surface.get_width()//2,self.surface.get_height()//2)
    # if mode == 'left_middle':  
    #   child_union_rect.left = 0
    #   child_union_rect.centery = self.surface.get_height()//2
    #   child_union_rect.centery = self.surface.get_height()//2
    # if mode == 'right_middle':  
    #   child_union_rect.right = self.surface.get_width()
    #   child_union_rect.centery = self.surface.get_height()//2
    # self.surface.blit(self.children[0], child_union_rect)

screen = pygame.display.set_mode([1000,1000]) 
'''
Initialize and build the Container object and its child surfaces
'''
text_container = Container(screen, margin=(200,100,200,100))
# text_container_2 = Container(screen, margin=(10,10,10,10))
blank_container = Container(text_container,min_height=30, min_width=100)
# blank_container_2 = Container(screen,min_height=20, min_width=30)

greeting_font = font.Font(None, 60)
greeting_text = greeting_font.render('Oh hi! Taylor Swift', True, (255,0,0))
greeting_text_2 = greeting_font.render('Oh no! Bye Taylor Swift', True, (255,0,0))

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