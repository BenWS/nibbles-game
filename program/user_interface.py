'''
This package is responsible for defining the screens each user sees and for loading 
and unloading graphics elements and event listeners for each screen. It defines the
overall rules of interaction between the user and the program elements (i.e. the user interface).
'''

# pygame imports
import pygame
from pygame import Rect, Surface
from pygame import font
font.init()

# python standard library
from abc import abstractmethod
import time

# local imports
from logging import ProcessLog
from graphics import Snake, Apple
from layout import Container


# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
  RLEACCEL,
  K_UP,
  K_DOWN,
  K_LEFT,
  K_RIGHT,
  K_ESCAPE,
  KEYDOWN,
  QUIT,
)

from globals import (
  SCREEN_DIMENSION,
  SCREEN_HEIGHT,
  SCREEN_WIDTH ,
  BLACK,
  WHITE,
)


# initialize the game
pygame.init()

clock = pygame.time.Clock()
clock.tick(1)

class Scene:
      '''
      A Scene is a set of event listeners and graphical elements that enable low-level graphical interaction. Think of each
      'scene' in the game runtime as a *distinct stage* (as in musical theater stage) and *distinct characters* where the
      'characters' here are graphical elements and event listeners.
      '''
      
      def __init__(self):
         self.status_codes = {
         'DEFAULT':'DEFAULT'
      }

      @abstractmethod
      def run():        
        '''
        Initilize and manage the event listeners, graphics elements,
        and elements to a particular 'scene'. 
        '''
        pass


class GameScene(Scene):
  def __init__(self,screen):
    super(GameScene, self).__init__()
    self.screen = screen

    # clear screen
    self.screen.fill(BLACK)
    pygame.display.flip()
    
  def run(self):
    # create Container object for layout
    game_container = Container(self.screen,margin=(40,40,40,40),fill_color=BLACK)
    game_surface,game_rect = game_container.render()
    

    # initialize the process log
    process_log = ProcessLog()

    # initialize snake object
    snake = Snake()
    apple = Apple()
    for entity in snake.segments:
      self.screen.blit(entity.surf,entity.rect)
      self.screen.blit(game_surface,game_rect)
    # screen.blit(snake.surf, snake.rect)
    # screen.blit(apple.surf, apple.rect)

    running = True
    # game loop
    while running:
      # self.screen.fill(BLACK)
      game_surface,game_rect = game_container.render()
      self.screen.blit(game_surface,game_rect)
      for event in pygame.event.get():
        # did the user hit a key?
        if event.type == KEYDOWN:
          # did the user hit the escape key? If so, stop the loop.
          if event.key == K_ESCAPE:
              running = False
        # did the user click the window close button? If so, stop the loop.
        elif event.type == pygame.QUIT:
            running = False
          
      # get the set of keys pressed and check for user input
      pressed_keys = pygame.key.get_pressed()
      snake.update()
      snake.change_direction(pressed_keys)

      # redraw game entities onto screen
      entity = None
      for entity in snake.segments:
        self.screen.blit(entity.surf,entity.rect)

      sprite_collided = pygame.sprite.spritecollideany(apple,snake.head_group)
      if sprite_collided is not None:
        # process_log.log("Collision detected")
        apple.relocate()
        snake.grow()

      if pygame.sprite.spritecollideany(snake.head,snake.body_segments_group):
        running=False

      def snake_exceeds_bounds(game_rect):
        return (snake.head.rect.right >= game_rect.right) \
          or (snake.head.rect.top <= game_rect.top ) \
          or (snake.head.rect.bottom >= game_rect.bottom)\
          or (snake.head.rect.left <= game_rect.left)

      if snake_exceeds_bounds(game_rect):
          running = False      

      self.screen.blit(apple.surf, apple.rect)
      # self.screen.blit(game_surface,game_rect)

      # pygame.draw.rect(screen, (0, 0, 255), (250,250,250, 250))
      pygame.display.flip()
      clock.tick(30)
    return self.status_codes['DEFAULT']


class TitleScene(Scene):
   def __init__(self,screen):
      super(TitleScene,self).__init__()
      self.screen = screen
      self.screen.fill(BLACK)
      
   
   def run(self):
      running = True
      title_container = Container(self.screen,margin=(0,0,0,0))
      title_font = font.Font(None,100)
      subtitle_font = font.Font(None,50)
      title_text = title_font.render('Nibbles',True,(255,0,0))
      subtitle_text = subtitle_font.render('Press Any Key to Continue',True,(255,0,0))
      title_container.add_child(title_text)
      title_container.add_child(subtitle_text)
      title_surface,title_rect = title_container.render()
      pygame.display.flip()
      self.screen.blit(title_surface,title_rect)
      while running:
        for event in pygame.event.get():
          if event.type == pygame.QUIT:
                running = False
                
        pygame.display.flip()
      
      return self.status_codes['DEFAULT']
   
class Countdown(Scene):
   def __init__(self,screen):
      super(Countdown,self).__init__()
      self.screen = screen
      self.screen.fill(BLACK)
      self.font = font.Font(None,100)
      self.font_color = (255,0,0)
  
   def update_text(self, container, id, value):
      text_element = container.get_child(id)
      text_element.content = self.font.render(value,True,self.font_color)
   
   def render_and_flip_content(self, container):
      container_surface, container_rect = container.render()
      self.screen.blit(container_surface, container_rect)
      pygame.display.flip()

   def flip_text(self,container,id,value):
      self.update_text(container,id,value)
      self.render_and_flip_content(container)
   
   def run(self):
      title_container = Container(self.screen,margin=(0,0,0,0))
      title_text = self.font.render('',True,(255,0,0))
      title_container.add_child(title_text, id='countdown')
  
      self. flip_text(title_container,'countdown','Starting in 3...')
      time.sleep(1)
      self. flip_text(title_container,'countdown','Starting in 2...')
      time.sleep(1)
      self. flip_text(title_container,'countdown','Starting in 1...')
      time.sleep(1)
                
      pygame.display.flip()
      
      return self.status_codes['DEFAULT']
   

class GameOver(Scene):
   def __init__(self,screen):
      super(GameOver,self).__init__()
      self.screen = screen
      self.screen.fill(BLACK)
      self.font = font.Font(None,100)
      self.subtitle_font = font.Font(None,50)
      self.font_color = (255,0,0)
  
   def update_text(self, container, id, value, font=None):
      text_element = container.get_child(id)
      text_element.content = font.render(value,True,self.font_color)
   
   def render_and_flip_content(self, container):
      container_surface, container_rect = container.render()
      self.screen.blit(container_surface, container_rect)
      pygame.display.flip()

   def flip_text(self,container,id,value):
      self.update_text(container,id,value)
      self.render_and_flip_content(container)
   
   def run(self):
      running = True
      while running:
        title_container = Container(self.screen,margin=(0,0,0,0))
        title_text = self.font.render('',True,(255,0,0))
        subtitle_text = self.subtitle_font.render('',True,(255,0,0))
        title_container.add_child(title_text, id='title')
        title_container.add_child(subtitle_text, id='subtitle')
    
        self.update_text(title_container,'title','Game Over',self.font)
        self.update_text(title_container,'subtitle','Press Any Key to Exit',self.subtitle_font)
        title_surface, title_rect = title_container.render()
        self.screen.blit(title_surface, title_rect)
        pygame.display.flip()

        for event in pygame.event.get():
          if event.type == pygame.QUIT:
                running = False

      return self.status_codes['DEFAULT']

class TestScene(Scene):
  def __init__(self,screen):
    super(TestScene, self).__init__()
    self.screen = screen

    # clear screen
    self.screen.fill(BLACK)
    pygame.display.flip()

  
  def run(self):
     time.sleep(1)
     self.screen.fill(WHITE)
     pygame.display.flip()
     time.sleep(1)
     self.screen.fill(BLACK)
     pygame.display.flip()
     time.sleep(1)
     return self.status_codes['DEFAULT']