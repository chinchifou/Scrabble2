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

#----- Constants -----
#reference tile size for a 1920*1080 resolution
REFERENCE_TILE_SIZE = 60

#----- CHANGING AT RUNTIME -----
#actual tile size used to scale all assets.
TILE_SIZE = 60
#all the remaining letters in the stack
BAG_OF_LETTERS = []

#folders' paths
path_log_folder = path.abspath('../log/')
path_icon = path.abspath('../materials/images/icon/')
path_background = path.abspath('../materials/images/background/')
path_buttons = path.abspath('../materials/images/assets/buttons/primary/')
path_buttons_menu = path.abspath('../materials/images/assets/buttons/side_menu/')
path_letters_french = path.abspath('../materials/images/assets/letters/french/')
path_letters_english = path.abspath('../materials/images/assets/letters/english/')


#~~~~~~ CLASSES ~~~~~~

#----- Pygame class override -----
#specify the pygame class RenderClear to allow easy reasize
class GroupOfSprites(pygame.sprite.RenderClear):

	#call each resize function of the sprite contained in the group
    def resize(self, *args):
        for s in self.sprites():
            s.resize(*args)


#----- Board -----
class Board(pygame.sprite.Sprite):
	def __init__(self):
		#call superclass constructor
		pygame.sprite.Sprite.__init__(self, self.containers)

		self.width_in_tiles = int (1920 / REFERENCE_TILE_SIZE ) #32
		self.height_in_tiles = int (1080 / REFERENCE_TILE_SIZE ) #18

		width = TILE_SIZE * self.width_in_tiles
		height = TILE_SIZE * self.height_in_tiles

		self.image = loadImage(path.join(path_background, 'empty_background.png'))
		self.image = pygame.transform.smoothscale(self.image, (width, height))
		self.rect = pygame.Rect((0,0), (width, height))

	def resize(self):
		#calculate new width and height 
		width = TILE_SIZE * self.width_in_tiles
		height = TILE_SIZE * self.height_in_tiles

		#update
		self.image = loadImage(path.join(path_background, 'empty_background.png'))
		self.image = pygame.transform.smoothscale(self.image, (width, height))
		self.rect = pygame.Rect((0,0), (width, height))


#----- Buttons -----
class Button(pygame.sprite.Sprite):
	def __init__(self, button_name):
		#call superclass constructor
		pygame.sprite.Sprite.__init__(self, self.containers)

		self.button_name = button_name

		self.width_in_tiles = 3
		self.height_in_tiles = 1

		self.pos_x_in_tiles = 27
		self.pos_y_in_tiles = 3.5

		width = TILE_SIZE * self.width_in_tiles
		height = TILE_SIZE * self.height_in_tiles

		self.pos_x = TILE_SIZE * self.pos_x_in_tiles
		self.pos_y = TILE_SIZE * self.pos_y_in_tiles

		self.image = loadImage(path.join(path_buttons, self.button_name+'.png'))
		self.image = pygame.transform.smoothscale(self.image, (width, height))
		self.rect = pygame.Rect((self.pos_x,self.pos_y), (width, height))

	def resize(self):
		#calculate new width and height 
		width = TILE_SIZE * self.width_in_tiles
		height = TILE_SIZE * self.height_in_tiles

		self.pos_x = TILE_SIZE * self.pos_x_in_tiles
		self.pos_y = TILE_SIZE * self.pos_y_in_tiles

		#update
		self.image = loadImage(path.join(path_buttons, self.button_name+'.png'))
		self.image = pygame.transform.smoothscale(self.image, (width, height))
		self.rect = pygame.Rect((self.pos_x,self.pos_y), (width, height))


#----- Letter -----
class Letter(pygame.sprite.Sprite):
	def __init__(self, letter):
		#call superclass constructor
		pygame.sprite.Sprite.__init__(self, self.containers)

		self.letter = letter

		size = TILE_SIZE

		self.image = loadTransparentImage(path.join(path_letters_french, letter+'.png'))
		self.image = pygame.transform.smoothscale(self.image, (size, size))

		pos = pygame.mouse.get_pos()		
		self.rect = pygame.Rect(pos, (size, size))

	def resize(self):
		#calculate new width and height 
		size = TILE_SIZE

		self.image = loadTransparentImage(path.join(path_letters_french, self.letter+'.png'))
		self.image = pygame.transform.smoothscale(self.image, (size, size))

		pos = pygame.mouse.get_pos()		
		self.rect = pygame.Rect(pos, (size, size))

#TODO - to change for normal letters
	def update(self):
		size = TILE_SIZE
		pos = pygame.mouse.get_pos()		
		self.rect = pygame.Rect(pos, (size, size))


#----- Player -----
class Player :

    def __init__(self, name, points, hand) :
        self.name = name
        self.points = points
        self.hand = hand

    def info(self) :
        logging.info('name : %s', self.name)
        logging.info('points : %s', self.points)
        logging.info('hand : %s', self.hand)


#~~~~~~ FUNCTIONS ~~~~~~

#----- Game window creation -----
def resizeWindow(width, height, fullscreen, resizable, resolution_auto, custom_window_height, double_buffer, hardware_accelerated) :

	updateTileSize(width,height)

	width = int (1920 / REFERENCE_TILE_SIZE ) * TILE_SIZE
	height = int (1080 / REFERENCE_TILE_SIZE ) * TILE_SIZE

	logging.info("Window resizing")
	logging.info("New tile Size is : %s", TILE_SIZE)
	logging.info("New Window size is : %s * %s", width, height)

	if fullscreen :
		if double_buffer :
			if hardware_accelerated :
				window = pygame.display.set_mode( (width, height), pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE)
			else :
				window = pygame.display.set_mode( (width, height), pygame.FULLSCREEN | pygame.DOUBLEBUF)
		else:
			window = pygame.display.set_mode( (width, height), pygame.FULLSCREEN)
	else :
		if resizable :
			if double_buffer :
				if hardware_accelerated :
					window = pygame.display.set_mode( (width, height), pygame.RESIZABLE | pygame.DOUBLEBUF | pygame.HWSURFACE)
				else :
					window = pygame.display.set_mode( (width, height), pygame.RESIZABLE | pygame.DOUBLEBUF)
			else:
				window = pygame.display.set_mode( (width, height), pygame.RESIZABLE)
		else:
			window = pygame.display.set_mode( (width, height))
	return window

#----- Load image -----
def loadImage(complete_path):
	image = pygame.image.load(complete_path)
	image = image.convert()
	return image

#----- Load transparent image -----
def loadTransparentImage(complete_path):
	image = pygame.image.load(complete_path)
	image = image.convert_alpha()
	return image

#----- Update Tile Size to match new window size -----
def updateTileSize(width, height):
	zoom_factor = min( float(width / 1920), float(height/1080) )
	global TILE_SIZE
	TILE_SIZE = int (floor ( REFERENCE_TILE_SIZE*zoom_factor ) )


#~~~~~~ INITIALIAZATION ~~~~~~

#----- Init logger -----
path_log_file = path.join(path_log_folder,'scrabble.log')
logging.basicConfig(filename=path_log_file, filemode='w', level=logging.DEBUG, format='%(asctime)s  |  %(levelname)s  |  %(message)s', datefmt='%Y-%m-%d @ %I:%M:%S %p')
logging.info("_________START OF LOG___________")

#----- Get configuration -----
#Display settings
cfg_fullscreen = config_reader.h_display_params['fullscreen']
cfg_resizable = config_reader.h_display_params['resizable']
cfg_resolution_auto = config_reader.h_display_params['resolution_auto']
cfg_hardware_accelerated = config_reader.h_display_params['enable_hardware_accelerated']
cfg_double_buffer = config_reader.h_display_params['enable_double_buffer']
cfg_custom_window_height = config_reader.h_display_params['custom_window_height']

#Game rules
number_of_letters_per_hand = config_reader.h_rules_params['number_of_letters_per_hand']
display_next_player_hand = config_reader.h_rules_params['display_next_player_hand']
language = config_reader.h_rules_params['language']
players = config_reader.players

#logging configuration
logging.info("INITIAL CONFIG")
logging.info("")
logging.info("DISPLAY SETTINGS")
logging.info("Fullscreen : %s", cfg_fullscreen)
logging.info("Resizable : %s", cfg_resizable)
logging.info("Resolution auto : %s", cfg_resolution_auto)
logging.info("Custom window width : %s", int ( cfg_custom_window_height * (16/9.0)) )
logging.info("Custom window height : %s", cfg_custom_window_height)
logging.info("Hardware accelerated : %s", cfg_hardware_accelerated)
logging.info("Double buffer : %s", cfg_double_buffer)
logging.info("")
logging.info("GAMES RULES")
logging.info("Language : %s", language)
logging.info("Players : %s", players)
logging.info("Number of letters per_hand : %s", number_of_letters_per_hand)
logging.info("Display next player hand : %s", display_next_player_hand)
logging.info("")

#Launch Pygame
game_engine = pygame.init() #init() -> (numpass, numfail)
sound_engine = pygame.mixer.init() #init(frequency=22050, size=-16, channels=2, buffer=4096) -> None
logging.info("%s pygame modules were launched and %s failed", game_engine[0], game_engine[1])
logging.info("Pygame started")

#Add icon
icon_image = pygame.image.load(path.join(path_icon,'Scrabble_launcher.ico'))
icon = pygame.transform.scale(icon_image, (32, 32))
pygame.display.set_icon(icon)
pygame.display.set_caption('Scrabble')


#----- Window init -----

#Calculate window resolution
width=0
height=0
if cfg_resolution_auto :
	monitor_resolution = pygame.display.Info()
	width = monitor_resolution.current_w
	height = monitor_resolution.current_h
else :
	width = round (cfg_custom_window_height * (16/9.0) )
	height = cfg_custom_window_height

#Initialize game window
window = resizeWindow(width, height, cfg_fullscreen, cfg_resizable, cfg_resolution_auto, cfg_custom_window_height, cfg_double_buffer, cfg_hardware_accelerated)


#----- Create sprites -----

#create sprite groups
layer_background = GroupOfSprites()
layer_scores_and_buttons = GroupOfSprites()
layer_hand_letters = GroupOfSprites()
layer_side_menu = GroupOfSprites()
layer_all = GroupOfSprites()

#set default groups
Board.containers = layer_all, layer_background
Button.containers = layer_all, layer_scores_and_buttons
Letter.containers = layer_all, layer_hand_letters

#create background
board = Board()
layer_background.draw(window)
pygame.display.flip()
current_backgroud = window.copy()

#create a test letter
letter_k = Letter('K')

#create a test button
button = Button("draw")

#Game is running
game_is_running = True
logging.info("-------------------")
logging.info("GAME STARTED")
logging.info("-------------------")


#~~~~~~ MAIN LOOP ~~~~~~

while game_is_running:
	
	for event in pygame.event.get():

		event_type = event.type

		#~~~~~~ QUIT ~~~~~~
		if ( event_type == pygame.QUIT ) :
			game_is_running = False #exit the game
			logging.info("-------------------")
			logging.info("Exiting game")
			logging.info("-------------------")

		#~~~~~~ WINDOW RESIZE ~~~~~~
		elif ( event_type == pygame.VIDEORESIZE ) : #properly refresh the game window if a resize is detected
			
			#new width and height
			width = event.dict['size'][0]
			height = event.dict['size'][1]

			#update window
			window = resizeWindow(width, height, cfg_fullscreen, cfg_resizable, cfg_resolution_auto, cfg_custom_window_height, cfg_double_buffer, cfg_hardware_accelerated)
			
			layer_all.resize()
			layer_background.draw(window)
			layer_scores_and_buttons.draw(window)
			
			current_backgroud = window.copy()

			layer_hand_letters.draw(window)
			pygame.display.flip()


		#~~~~~~ KEY PRESSED ~~~~~~			
		elif ( event_type == pygame.KEYDOWN ) :
			logging.info("Key pressed")
			key_pressed = event.key
			
			if ( key_pressed == pygame.K_ESCAPE ) :
				logging.info("ESCAPE key pressed")
				game_is_running = False #exit the game

		elif(event_type == pygame.MOUSEMOTION ):

			#TODO to remove
			pos = pygame.mouse.get_pos()
			x = pos[0]
			y = pos[1]	

			if ( ( 0 <= x <= board.rect.width ) and ( 0 <= y <= board.rect.height )  ):
				
				layer_hand_letters.clear(window, current_backgroud)
				layer_hand_letters.update()
				content = layer_hand_letters.draw(window)
				pygame.display.flip()
				

logging.info("Game has ended")
logging.info("_________END OF LOG___________")
