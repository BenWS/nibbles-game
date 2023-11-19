from user_interface import GameScene, TestScene\
	, TitleScene, Countdown, GameOver

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

title_scene = TitleScene(screen)
status_code = title_scene.run()

countdown_scene = Countdown(screen)
status_code = countdown_scene.run()

game_scene = GameScene(screen)
status_code = game_scene.run()

game_over = GameOver(screen)
status_code = game_over.run()

# test_scene = TestScene(screen)
# status_code = test_scene.run()

