'''
This package is responsible for defining the screens each user sees and for loading 
and unloading graphics elements and event listeners for each screen. It defines the
overall rules of interaction between the user and the program elements (i.e. the user interface).
'''

# pygame imports
import pygame
from pygame import Rect, Surface

# python standard library
from abc import abstractmethod
import time

# local imports
from logging import ProcessLog
from graphics import Snake, Apple


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
    # initialize the process log
    process_log = ProcessLog()

    # initialize snake object
    snake = Snake()
    apple = Apple()
    for entity in snake.segments:
      self.screen.blit(entity.surf,entity.rect)
    # screen.blit(snake.surf, snake.rect)
    # screen.blit(apple.surf, apple.rect)

    running = True
    # game loop
    while running:
      self.screen.fill(BLACK)
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
      for entity in snake.segments:
        self.screen.blit(entity.surf,entity.rect)

      sprite_collided = pygame.sprite.spritecollideany(apple,snake.head_group)
      if sprite_collided is not None:
        # process_log.log("Collision detected")
        apple.relocate()
        snake.grow()

      if pygame.sprite.spritecollideany(snake.head,snake.body_segments_group):
        running=False

      def snake_exceeds_bounds():
        return (snake.head.rect.right > SCREEN_WIDTH) \
          or (snake.head.rect.top > SCREEN_HEIGHT) \
          or (snake.head.rect.bottom < 0)\
          or (snake.head.rect.left < 0)

      if snake_exceeds_bounds():
          running = False
      

      self.screen.blit(apple.surf, apple.rect)

      # pygame.draw.rect(screen, (0, 0, 255), (250,250,250, 250))
      pygame.display.flip()
      clock.tick(30)
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