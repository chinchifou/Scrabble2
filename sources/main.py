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
game_engine = pygame.init()
sound_engine = pygame.mixer.init()

#Add icon
path_for_icon = path.abspath('../materials/images/icon/')
icon_image = pygame.image.load(path.join(path_for_icon,'Scrabble_launcher.ico'))
icon = pygame.transform.scale(icon_image, (32, 32))
pygame.display.set_icon(icon)
pygame.display.set_caption('Scrabble')


print('All clear Captain !')
