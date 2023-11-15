# WIP: 2023_09_02_1

# Simple pygame program


'''
TODO: 2023_09_09_1 - Design Class for Screen Element Management

 - Determine whether any class related to Screen Element Management should be a member of the user_interface or the graphics package (or another)
  - (One way to frame the above question may be to think of such in context of how the `main` sequence will interact with such)

---------------------------------------

Additional notes and context:

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
        self.my_font = font.Font(None,size=12) # create new font
        self.text = self.my_font.render('Greetings!', True, (255,0,0)) # create new surface (image) from the font
        self.text_rect = self.text.get_rect() # create rectangle from the text surface
        
    def get_text(self):
         return self.text
    
    def set_position(self,mode):
        if mode == 'center':  
          self.text_rect.center = (self.parent_surface.get_width()//2,self.parent_surface.get_height()//2)   
        if mode == 'left_middle':  
          self.text_rect.left = 0
          self.text_rect.centery = self.parent_surface.get_height()//2
        if mode == 'right_middle':  
          self.text_rect.right = self.parent_surface.get_width()
          self.text_rect.centery = self.parent_surface.get_height()//2
    
    def blit(self):
        self.parent_surface.blit(self.text,self.text_rect)



class Element:
    def __init__(self):
        self.width = None
        self.height = None
        self.surface = None
        
class Container:
  '''
  TODO: 11-11-2023

   - The container class should be able to position its child elements in either a vertical or horizontal layout
   - Recursive containers should be allowed - i.e. we should be able to make a container the child of another container
   - We should be able to specific element position relative to the container in terms of percentages *and* pixels
   - If positioning is specified in terms of percentages, exceeding 100% should not throw an error, but render such as 1.5x bigger than the parent if the total percentage is 150% (as an example)
   - If the parent container moves, the children should move in reference to the parent
  '''
  def __init__(self,surface):
    super(Container,self).__init__()
    # self.parent = None
    self.surface = surface
    self.children = [] 

  def add_child(self,surface):
    # surface.parent = self
    self.children.append(surface)

  def set_position(self,mode):
    '''
    This method sets the position of all the children elements of this container object. 
    The 'union' of the child surfaces is what effectively gets positioned.
    '''
    
    # get vertical center
    def get_total_height():
      total_height = 0
      for child in self.children:
        total_height += child.get_rect().height
      return total_height

    def get_total_width():
      '''
      If layout is vertical, then knowing the total width can be inferred
      based on the maximum width rectangle
      '''
      max_width = 0
      for child in self.children:
        if child.get_rect().width > max_width:
          max_width = child.get_rect().width
      
      return max_width
      

    def get_vertical_offset(child_index):
      '''
      Get vertical offset from center for a specific element
      '''
      vertical_offset = 0
      upper_index_limit = child_index
      for index,child in enumerate(self.children):
          if index < upper_index_limit:
              vertical_offset += child.get_rect().height
          
          if index == upper_index_limit:
              vertical_offset += child.get_rect().centery
              return vertical_offset
            
          if index > upper_index_limit:
              return vertical_offset
    
    def get_horizontal_offset(child_index):
        '''
        Get horizontal offset from center for given child element
        '''
        child = self.children[child_index]
        return get_total_width()//2 - child.get_rect().centerx
        # return get_total_width()*1.0/2
          
    def get_center_movement():
      # get the movement required for center
      screen_center_y = self.surface.get_rect().centery
      screen_center_x = self.surface.get_rect().centerx
      center_movement_x = screen_center_x - get_total_width()//2
      center_movement_y = screen_center_y - get_total_height()//2
      return (center_movement_x,center_movement_y)


    # set the position of the elements
    for index, child in enumerate(self.children):
    # get the position of each element and compare against center
        vertical_offset = get_vertical_offset(index)
        horizontal_offset = get_horizontal_offset(index)
        center_movement_x,center_movement_y = get_center_movement()
        child_rect = child.get_rect()
        child_rect.move_ip(horizontal_offset + center_movement_x, vertical_offset + center_movement_y)
        self.surface.blit(child,child_rect)


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
    
# Set up the drawing window
screen = pygame.display.set_mode([1000, 1000])

# Fill the background with white
screen.fill((0, 0, 0))


# initialize game screen

# text_font = font.Font(None, 100)
# text_surface = text_font.render('Oh hi! Taylor Swift', True, (255,0,0))


# text_subsurface_1 = screen.subsurface(text_surface.get_rect())
# text_subsurface_1.blit(text_surface, text_surface.get_rect())

# text_subsurface_2 = screen.subsurface(text_surface.get_rect())
# text_subsurface_2.blit(text_surface, text_surface.get_rect())

# width = text_subsurface_2.get_rect().width
# height = text_subsurface_2.get_rect().height
# blank_surface = pygame.Surface((width, height))
# blank_surface_rect = blank_surface.get_rect()
# blank_surface_rect.move_ip(0,text_subsurface_1.get_rect().height)
# screen.blit(blank_surface, blank_surface_rect)
# text_subsurface_2_rect = pygame.Rect(200,200,200,200)
# text_subsurface_1_height = text_subsurface_1.get_rect().height
# text_subsurface_2_rect.move_ip(0,text_subsurface_1_height)
# screen.blit(text_subsurface_2,(300,300))

# greeting_screen = GreetingScreen(screen)
screen_container = Container(screen)
greeting_font = font.Font(None, 30)
greeting_text = greeting_font.render('Oh hi! Taylor Swift', True, (255,0,0))
greeting_text_2 = greeting_font.render('Oh no! Bye Taylor Swift', True, (255,0,0))

screen_container.add_child(greeting_text)
screen_container.add_child(greeting_text)
# screen_container.add_child(greeting_text)
# screen_container.add_child(greeting_text)
screen_container.set_position('right_middle')
# greeting_screen.blit()


# Run until the user asks to quit
running = True
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    



    # screen_container = Container(screen)
    
    # red_surface = pygame.Surface((0,0))
    # red_surface.fill((255,0,0))
    
    # blue_surface = pygame.Surface((0,0))
    # blue_surface.fill((255,0,0))
    
    # screen_container.add([red_surface,blue_surface])

    
    # surface = pygame.Surface((0,0))
    # surface.fill((255,0,0))
    # screen.blit(surface,(0,0))


    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()