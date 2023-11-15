from user_interface import GameScene, TestScene
import pygame
from globals import (
	SCREEN_WIDTH, SCREEN_HEIGHT, BLACK
)

'''
This module orchestrates the flow of various user interfaces based on interface exit statuses.
'''
# initialize the screen object
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
screen.fill(BLACK)

game_scene = GameScene(screen)
status_code = game_scene.run()
test_scene = TestScene(screen)
status_code = test_scene.run()