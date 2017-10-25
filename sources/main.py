#~~~~~~~ MAIN ~~~~~~~~

#~~~~~~ IMPORTS ~~~~~~

#------ Standard library imports ------
from random import randint
from math import floor
from os import path

#------Modules imports -------
import pygame

#------Other python files imports -------
import config_reader
import letters_and_points


#~~~~~~ FUNCTIONS ~~~~~~

#Game window creation
def refreshWindow(fullscreen, resizable, resolution_auto, custom_window_heigh, double_buffer, hardware_accelerated) :

	if resolution_auto :
		monitor_resolution = pygame.display.Info()
		width = monitor_resolution.current_w
		heigh = monitor_resolution.current_h
	else :
		heigh = custom_window_heigh
		width = round (heigh * (16/9.0) )

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

#------ Get configuration ------
cfg_fullscreen = config_reader.h_display_params['fullscreen']
cfg_resizable = config_reader.h_display_params['resizable']
cfg_resolution_auto = config_reader.h_display_params['resolution_auto']
cfg_hardware_accelerated = config_reader.h_display_params['enable_hardware_accelerated']
cfg_double_buffer = config_reader.h_display_params['enable_double_buffer']
cfg_custom_window_heigh = config_reader.h_display_params['custom_window_heigh']

number_of_letters_per_hand = config_reader.h_rules_params['display_next_player_hand']
display_next_player_hand = config_reader.h_rules_params['language']
language = config_reader.h_rules_params['number_of_letters_per_hand']
players = config_reader.players


#------ Launch Pygame ------
game_engine = pygame.init() #init() -> (numpass, numfail)
sound_engine = pygame.mixer.init() #init(frequency=22050, size=-16, channels=2, buffer=4096) -> None

#Add icon
path_for_icon = path.abspath('../materials/images/icon/')
icon_image = pygame.image.load(path.join(path_for_icon,'Scrabble_launcher.ico'))
icon = pygame.transform.scale(icon_image, (32, 32))
pygame.display.set_icon(icon)
pygame.display.set_caption('Scrabble')

#debug in progress
print("cfg_fullscreen ", cfg_fullscreen)
print("cfg_resizable ", cfg_resizable)
print("cfg_resolution_auto ", cfg_resolution_auto)
print("cfg_hardware_accelerated ", cfg_hardware_accelerated)
print("cfg_double_buffer ", cfg_double_buffer)
print("cfg_custom_window_heigh ", cfg_custom_window_heigh)

#to debug

game_is_running = True

window = refreshWindow(cfg_fullscreen, cfg_resizable, cfg_resolution_auto, cfg_custom_window_heigh, cfg_double_buffer, cfg_hardware_accelerated)

while game_is_running:
	
	for event in pygame.event.get():

		event_type = event.type

		#~~~~~~~~~~~ QUIT ~~~~~~~~~~~
		if ( event_type == pygame.QUIT ) : #close the game window
		    game_is_running = False #exit the game        

		#~~~~~~~~~~~ WINDOW RESIZE ~~~~~~~~~~~
		elif ( event_type == pygame.VIDEORESIZE ) : #properly refresh the game window if a resize is detected
			window = refreshWindow(cfg_fullscreen, cfg_resizable, cfg_resolution_auto, cfg_custom_window_heigh, cfg_double_buffer, cfg_hardware_accelerated)


print('All clear Captain !')
