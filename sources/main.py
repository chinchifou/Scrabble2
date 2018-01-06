#~~~~~~~~~ MAIN ~~~~~~~~~

#~~~~~~ IMPORTS ~~~~~~

#Standard library imports
from random import randint
from math import floor
from os import path

#Modules imports
import pygame
import logging

#Other python files imports
import config_reader
import letters_and_points


#~~~~~~ FUNCTIONS ~~~~~~

#----- Game window creation -----
def refreshWindow(fullscreen, resizable, resolution_auto, custom_window_heigh, double_buffer, hardware_accelerated) :

	width = GAME_VARS['width']
	heigh = GAME_VARS['heigh']

	if fullscreen :
		if double_buffer :
			if hardware_accelerated :
				window = pygame.display.set_mode( (width, heigh), pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE)
			else :
				window = pygame.display.set_mode( (width, heigh), pygame.FULLSCREEN | pygame.DOUBLEBUF)
		else:
			window = pygame.display.set_mode( (width, heigh), pygame.FULLSCREEN)
	else :
		if resizable :
			if double_buffer :
				if hardware_accelerated :
					window = pygame.display.set_mode( (width, heigh), pygame.RESIZABLE | pygame.DOUBLEBUF | pygame.HWSURFACE)
				else :
					window = pygame.display.set_mode( (width, heigh), pygame.RESIZABLE | pygame.DOUBLEBUF)
			else:
				window = pygame.display.set_mode( (width, heigh), pygame.RESIZABLE)
		else:
			window = pygame.display.set_mode( (width, heigh))
	return window


#~~~~~~ INITIALIAZATION ~~~~~~

#Container for game variables
GAME_VARS = {}

#----- Get configuration -----
cfg_fullscreen = config_reader.h_display_params['fullscreen']
cfg_resizable = config_reader.h_display_params['resizable']
cfg_resolution_auto = config_reader.h_display_params['resolution_auto']
cfg_hardware_accelerated = config_reader.h_display_params['enable_hardware_accelerated']
cfg_double_buffer = config_reader.h_display_params['enable_double_buffer']
cfg_custom_window_heigh = config_reader.h_display_params['custom_window_heigh']

number_of_letters_per_hand = config_reader.h_rules_params['number_of_letters_per_hand']
display_next_player_hand = config_reader.h_rules_params['display_next_player_hand']
language = config_reader.h_rules_params['language']
players = config_reader.players

GAME_VARS['heigh'] = cfg_custom_window_heigh
GAME_VARS['width'] = round (cfg_custom_window_heigh * (16/9.0) )


#----- Launch Pygame -----
game_engine = pygame.init() #init() -> (numpass, numfail)
sound_engine = pygame.mixer.init() #init(frequency=22050, size=-16, channels=2, buffer=4096) -> None

#Add icon
path_for_icon = path.abspath('../materials/images/icon/')
icon_image = pygame.image.load(path.join(path_for_icon,'Scrabble_launcher.ico'))
icon = pygame.transform.scale(icon_image, (32, 32))
pygame.display.set_icon(icon)
pygame.display.set_caption('Scrabble')

#Resolution auto
if cfg_resolution_auto :
	monitor_resolution = pygame.display.Info()
	GAME_VARS['width'] = monitor_resolution.current_w
	GAME_VARS['heigh'] = monitor_resolution.current_h


#----- Init logger -----
path_log_folder = path.abspath('../log/')
path_log_file = path.join(path_log_folder,'scrabble.log')
logging.basicConfig(filename=path_log_file, filemode='w', level=logging.DEBUG, format='%(asctime)s  |  %(levelname)s  |  %(message)s', datefmt='%Y-%m-%d @ %I:%M:%S')

#logging
logging.info("INITIAL CONFIG")
logging.info("DISPLAY SETTINGS")
logging.info("Fullscreen : %s", cfg_fullscreen)
logging.info("Resizable : %s", cfg_resizable)
logging.info("Resolution auto : %s", cfg_resolution_auto)
logging.info("Custom window heigh : %s", cfg_custom_window_heigh)
logging.info("Hardware accelerated : %s", cfg_hardware_accelerated)
logging.info("Double buffer : %s", cfg_double_buffer)
logging.info("GAMES RULES")
logging.info("Language : %s", language)
logging.info("Players : %s", players)
logging.info("Number of letters per_hand : %s", number_of_letters_per_hand)
logging.info("Display next player hand : %s", display_next_player_hand)
logging.info("")


#Window init
window = refreshWindow(cfg_fullscreen, cfg_resizable, cfg_resolution_auto, cfg_custom_window_heigh, cfg_double_buffer, cfg_hardware_accelerated)
game_is_running = True
logging.info("Game is running")


#~~~~~~ MAIN LOOP ~~~~~~

while game_is_running:
	
	for event in pygame.event.get():

		event_type = event.type

		#~~~~~~ QUIT ~~~~~~
		if ( event_type == pygame.QUIT ) :
			game_is_running = False #exit the game
			logging.info("Exiting game")

		#~~~~~~ WINDOW RESIZE ~~~~~~
		elif ( event_type == pygame.VIDEORESIZE ) : #properly refresh the game window if a resize is detected
			logging.info("Window resize")
			GAME_VARS['width'] = event.dict['size'][0]
			GAME_VARS['heigh'] = event.dict['size'][1]
			window = refreshWindow(cfg_fullscreen, cfg_resizable, cfg_resolution_auto, cfg_custom_window_heigh, cfg_double_buffer, cfg_hardware_accelerated)
		
		#~~~~~~ KEY PRESSED ~~~~~~			
		elif ( event_type == pygame.KEYDOWN ) :
			logging.info("Key pressed")
			key_pressed = event.key
			
			if ( key_pressed == pygame.K_ESCAPE ) :
				logging.info("ESCAPE key pressed")
				game_is_running = False #exit the game

logging.info("Game has ended properly")
