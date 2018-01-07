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


#~~~~~~ GLOBAL VARIBLES ~~~~~~

TILE_SIZE = 60

#folders' paths
path_icon = path.abspath('../materials/images/icon/')
path_background = path.abspath('../materials/images/background/')
path_buttons = path.abspath('../materials/images/assets/buttons/primary/')
path_buttons_menu = path.abspath('../materials/images/assets/buttons/side_menu/')
#TODO path letters and tiles


#~~~~~~ CLASSES ~~~~~~

#----- Game window -----
class Background(pygame.sprite.Sprite):
	def __init__(self):
		#call superclass constructor
		pygame.sprite.Sprite.__init__(self)

		self.width_in_tiles = int (1920 / 60 ) #32
		self.heigh_in_tiles = int (1080 / 60 ) #18

		width = TILE_SIZE * self.width_in_tiles
		heigh = TILE_SIZE * self.heigh_in_tiles

		self.image = loadImage(path.join(path_background, 'background.png'))
		self.image = pygame.transform.smoothscale(self.image, (width, heigh))
		self.rect = pygame.Rect((0,0), (width, heigh))

	def update(self):
		#calculate new width and heigh 
		width = TILE_SIZE * self.width_in_tiles
		heigh = TILE_SIZE * self.heigh_in_tiles

		#update
		self.image = loadImage(path.join(path_background, 'background.png'))
		self.image = pygame.transform.smoothscale(self.image, (width, heigh))
		self.rect = pygame.Rect((0,0), (width, heigh))


#~~~~~~ FUNCTIONS ~~~~~~

#----- Game window creation -----
def resizeWindow(width, heigh, fullscreen, resizable, resolution_auto, custom_window_heigh, double_buffer, hardware_accelerated) :

	updateTileSize(width,heigh)

	logging.info("Window resizing")
	logging.info("New tile Size is : %s", TILE_SIZE)
	logging.info("New Window size is : %s * %s", width, heigh)

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

#----- Load image -----
def loadImage(complete_path):
	image = pygame.image.load(complete_path)
	image = image.convert()
	return image

#----- Update Tile Size to match new window size -----
def updateTileSize(width, heigh):
	ORIGINAL_TILE_SIZE = 60
	zoom_factor = min( float(width / 1920), float(heigh/1080) )
	global TILE_SIZE
	TILE_SIZE = int (floor ( ORIGINAL_TILE_SIZE*zoom_factor ) )


#~~~~~~ INITIALIAZATION ~~~~~~

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


#----- Launch Pygame -----

game_engine = pygame.init() #init() -> (numpass, numfail)
sound_engine = pygame.mixer.init() #init(frequency=22050, size=-16, channels=2, buffer=4096) -> None

#Add icon
icon_image = pygame.image.load(path.join(path_icon,'Scrabble_launcher.ico'))
icon = pygame.transform.scale(icon_image, (32, 32))
pygame.display.set_icon(icon)
pygame.display.set_caption('Scrabble')


#----- Init logger -----

path_log_folder = path.abspath('../log/')
path_log_file = path.join(path_log_folder,'scrabble.log')
logging.basicConfig(filename=path_log_file, filemode='w', level=logging.DEBUG, format='%(asctime)s  |  %(levelname)s  |  %(message)s', datefmt='%Y-%m-%d @ %I:%M:%S %p')

#logging
logging.info("INITIAL CONFIG")
logging.info("DISPLAY SETTINGS")
logging.info("Fullscreen : %s", cfg_fullscreen)
logging.info("Resizable : %s", cfg_resizable)
logging.info("Resolution auto : %s", cfg_resolution_auto)
logging.info("Custom window width : %s", cfg_custom_window_heigh * (16/9.0))
logging.info("Custom window heigh : %s", cfg_custom_window_heigh)
logging.info("Hardware accelerated : %s", cfg_hardware_accelerated)
logging.info("Double buffer : %s", cfg_double_buffer)
logging.info("GAMES RULES")
logging.info("Language : %s", language)
logging.info("Players : %s", players)
logging.info("Number of letters per_hand : %s", number_of_letters_per_hand)
logging.info("Display next player hand : %s", display_next_player_hand)
logging.info("")


#----- Window init -----

#Calculate window resolution
width=0
heigh=0
if cfg_resolution_auto :
	monitor_resolution = pygame.display.Info()
	width = monitor_resolution.current_w
	heigh = monitor_resolution.current_h
else :
	width = round (cfg_custom_window_heigh * (16/9.0) )
	heigh = cfg_custom_window_heigh


#Initialize game window
window = resizeWindow(width, heigh, cfg_fullscreen, cfg_resizable, cfg_resolution_auto, cfg_custom_window_heigh, cfg_double_buffer, cfg_hardware_accelerated)


#----- Create sprites -----

#create background
background = Background()

#create groups
#TODO

#display background
#TODO
window.blit(background.image, (0,0))
pygame.display.flip()

#Game is running
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
			
			#new width and heigh
			width = event.dict['size'][0]
			heigh = event.dict['size'][1]

			#update window
			window = resizeWindow(width, heigh, cfg_fullscreen, cfg_resizable, cfg_resolution_auto, cfg_custom_window_heigh, cfg_double_buffer, cfg_hardware_accelerated)
			
			#update assets
			background.update()

			window.blit(background.image, (0,0))
			pygame.display.flip()


		#~~~~~~ KEY PRESSED ~~~~~~			
		elif ( event_type == pygame.KEYDOWN ) :
			logging.info("Key pressed")
			key_pressed = event.key
			
			if ( key_pressed == pygame.K_ESCAPE ) :
				logging.info("ESCAPE key pressed")
				game_is_running = False #exit the game

logging.info("Game has ended properly")
