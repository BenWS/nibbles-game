import pygame
import sys 
from pygame import Rect, Surface
import math
import random

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

# initialize constants
SCREEN_DIMENSION = 10
SCREEN_HEIGHT = 100 * SCREEN_DIMENSION
SCREEN_WIDTH = 100 * SCREEN_DIMENSION
BLACK = 0,0,0

# initialize the game
pygame.init()

clock = pygame.time.Clock()
clock.tick(1)

class ProcessLog:
	def __init__(self):
		pass

	def log(self, error_message, level=None):
		if level == None:
			print('INFO: ',error_message)

# define the snake class
class Snake(pygame.sprite.Sprite):

	class Segment(pygame.sprite.Sprite):
		'''
		Individual component of the total snake. It is further 
		subclassed in order to define behavior for more specific 
		'types'	of parts.
		'''
		def __init__(self, segment_ahead=None):
				super(Snake.Segment,self).__init__()
				# draw segment
				self.width = SCREEN_DIMENSION
				self.height = SCREEN_DIMENSION
				self.surf = pygame.Surface((self.width,self.height))
				self.surf.fill((23,234,100))
				self.surf.set_colorkey((255,255,255),RLEACCEL)
				self.rect = self.surf.get_rect()

				# set the initial position and velocity
				self.velocity_prev = (0,0)
				self.velocity = (0,0)

				self._segment_ahead = self._set_segment_ahead(segment_ahead)

		def set_physical_state(self, position_int):
			'''
			Sets the position and velocity of the segment, 
			in addition to setting its position in relation to the queue
			of total segments.  
			'''
			self._segment_position = position_int
			'''
			 - get the next segment's previous velocity, i.e. this segement's current velocity
			 - place this segment where the next segment was, based on its previous velocity
			'''

		def _set_segment_ahead(self,segment):
			'''
			Sets the segment directly ahead of the current segment
			'''
			try:
					self._segment_ahead = segment
			except Exception:
				print(sys.exc_info())
				print("Error handled while adding segment to Snake...please review.")
			self._segment_ahead = segment

	class Segments():
		'''
		The full collection of all segments of the snake. 
		'''
		def __init__(self):
			# initilize empty sprite group
			self.group = pygame.sprite.Group()
			
			# initialize variables
			self.velocity_prev = (None, None)
			self._head_exists = False
				
		def __iter__(self):
			return iter(self.group.sprites())
		
		# def get_segment_ahead(self,segment):

		
		def add(self,segment=None):
			'''
			This method adds an individual segment to the total collection of segments. 
			
			It also sets properties on the segment object in order to:
			 1. Provide it awareness of the state of the segment directly ahead of it
			 2. Initialize its position and velocity 
			'''

			'''
			TODO: Create test validating that the count always increases
			by 1 with function call. 
			'''
			sprites_list = self.group.sprites()
			group_max_index = len(sprites_list) # get the segment position by total list size, thereby getting the position of the last segment assigned (i.e. this segment)

			if group_max_index == 0:
				pass # i.e. there are no segments in list and no segments ahead
			else:
				segment_ahead = self.group.sprites()[group_max_index - 1]

			if segment is not None:
				'''
				TODO: Refine logic for checking that a 'head' segment already exists - inspect the collection for object-type of head (rather than utilize flag).
				'''
				if not self._head_exists:
					self.head_exists = True
					self.group.add(segment)
				else:
					process_log.log("Head already exists. No action taken.")
			else:
				self.group.add(Snake.BodySegment(segment_ahead))	

		def get_count_segments(self):
			return len(self.group.sprites())

		def update(self):
			self.group.update()
	
	class HeadSegment(Segment):
		'''
		The first segment of the snake, 
		and has the distinct behavior of being able to 
		collide with either itself or the 'walls' of the 
		game.

		Every Snake object is instantiated with a head. 
		'''

		def __init__(self):
			super(Snake.HeadSegment,self).__init__()
			# WIP--: moving the method and property definitions below to Segments class

			# set the initial position for the head
			self.rect.right = 20 * SCREEN_DIMENSION
			self.rect.top = 10 * SCREEN_DIMENSION

			# set the initial direction and velocity
			self.speed = self.width
			self.velocity = (self.speed,0)
			

		def update(self):
			# print('Method called')
			self.rect.move_ip(self.velocity[0],self.velocity[1])
			# print(self.rect.left,self.rect.top,self.rect.width,self.rect.height)
		
		def get_velocity_prev(self):
			return self.velocity_prev

		def change_direction(self,pressed_keys):
			self.velocity_prev = self.velocity
			if pressed_keys[K_UP]:
				self.velocity = (0,-self.speed)
			if pressed_keys[K_DOWN]:
				self.velocity = (0,self.speed)
			if pressed_keys[K_LEFT]:
				self.velocity = (-self.speed,0)
			if pressed_keys[K_RIGHT]:
				self.velocity = (self.speed,0)
				
	class BodySegment(Segment):
		'''
		This class represents any segment *after* the head, 
		and has the behavior of immediately following the
		movement of the segment directly ahead of it.
		'''
		
		def __init__(self,segment_ahead=None):
			super(Snake.BodySegment,self).__init__()
			self._set_segment_ahead(segment_ahead)	
			self.velocity = self._segment_ahead.velocity


			process_log.log(self._segment_ahead.velocity)

			if isinstance(self._segment_ahead,Snake.HeadSegment):
				offset = 0
			else:
				offset = self.width

			if self._segment_ahead.velocity[0] > 0:
				# heading right
				pass
				'''
				PLANNING:

				get the position of the segment ahead
				offset new segment the surface of one dimension
				'''
				self.rect = self._segment_ahead.rect.move(-offset,0)
			if self._segment_ahead.velocity[0] < 0:
				# heading left
				self.rect = self._segment_ahead.rect.move(offset,0)
				pass
			if self._segment_ahead.velocity[1] > 0:
				# heading downwards
				self.rect = self._segment_ahead.rect.move(0,-offset)
				pass
			if self._segment_ahead.velocity[1] < 0:
				# heading upwards
				self.rect = self._segment_ahead.rect.move(0,offset)


			# self.segment_ahead = None
		
		def update(self):
			# WIP--: Logic for moving the body segment 
			'''
			Moves the current segment. The segment follows the path of the segment directly ahead of it. 
			'''

			'''
			PLANNING:

			The body segment should follow that immediately ahead of it - need more 
			generalized approach to setting inital the position and velocity and 
			having such adjusted when the head changes velocity...

			The velocity of this segment should be equal to the previous velocity 
			of the segment just ahead...
			'''
			# pass
			# print(self.segment_ahead)
			self.velocity_prev = self.velocity
			self.velocity = self._segment_ahead.velocity_prev

			self.rect.move_ip(self.velocity[0],self.velocity[1])

	'''
	TODO: 01-07-2023

	Summary: ...

	Details:
		- [ ] Method for growing the snake upon collison with an Apple object
		- [x] Method for changing the snake's direction
		- [x] Method for moving the snake
		- [ ] Strategy for managing snake segments?
	'''

	def __init__(self):
		super(Snake,self).__init__()
	
		# instantiate the segments, and add the head
		self.segments = Snake.Segments()
		self.head = Snake.HeadSegment()
		self.segments.add(self.head)

		self.head_group = pygame.sprite.Group()
		self.head_group.add(self.head)

		# self.head.rect.move_ip(-self.head.width,0)
		self.segments.add()	
		self.segments.add()	
		self.segments.add()	
		self.segments.add()	
		
		# adding first body segment 
	
	def grow(self):
		self.segments.add()
		self.segments.add()
	
	@property
	def segments_group(self):
		return self.segments.group
	
	@property
	def body_segments_group(self):
		body_segments_group = self.segments.group.copy()
		body_segments_group.remove(self.head)
		return body_segments_group

	def update(self):
		'''
		Updates all segments of the snake; different segment types may have
		a special implementation of the update method
		'''
		self.segments.update()

	def change_direction(self,pressed_keys):
		'''
		Changes the direction of the head. The direction of 
		the total snake is ultimately controlled by the direction 
		of the head
		'''
		self.head.change_direction(pressed_keys)


# define the apple class
class Apple():
	'''
	TODO: 01-07-2023

	- Method for growing the snake upon collison with an Apple object
	- Method for changing the snake's direction
	- Method for moving the snake
	'''
	def __init__(self):
		super(Apple,self).__init__()
		# self.surf = pygame.image.load("Assets/jetfighter.png").convert()
		self.surf = pygame.Surface((SCREEN_DIMENSION,SCREEN_DIMENSION))
		self.surf.fill((255,0,0))
		# self.surf = pygame.transform.scale(self.surf, (100,100))
		self.surf.set_colorkey((255,255,255),RLEACCEL)
		self.rect = self.surf.get_rect()
		self.rect.left = 300
		self.rect.top = 650

	def relocate(self):
		'''
		TODO:
		
		- Apple should not be placed at 'edge' of screen - should have an upper and lower-bound as buffer
		- Apple should not be placed directly ahead of snake head on relocation
		'''
		x_coord = SCREEN_DIMENSION * math.floor(random.random() * 100)
		y_coord = SCREEN_DIMENSION * math.floor(random.random() * 100)
		apple.rect.top = y_coord
		apple.rect.left= x_coord

# initialize the process log
process_log = ProcessLog()

# initialize the screen object
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
screen.fill(BLACK)

# initialize snake object
snake = Snake()
apple = Apple()
for entity in snake.segments:
	screen.blit(entity.surf,entity.rect)
# screen.blit(snake.surf, snake.rect)
# screen.blit(apple.surf, apple.rect)

running = True
# game loop
while running:
	screen.fill(BLACK)
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
		screen.blit(entity.surf,entity.rect)

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
	

	screen.blit(apple.surf, apple.rect)

	# pygame.draw.rect(screen, (0, 0, 255), (250,250,250, 250))
	pygame.display.flip()
	clock.tick(30)

'''
TODO: General

 - [ ] Working on method for initially placing the body segment directly after the head
 - [ ] The snake coordinates should be 'square' with the apple coordinates - determine way to better keep to requirement in light of potential future program modifications
 - [ ] Initial display rules and display
'''


'''
WIP: Outline

 - [ ] Prevent direction change for snake if such would result in immediate collison with its own segment 
 - [ ] Setting initial direction to negative value reverses input 
 - [ ] Initially document methods and classes
'''

