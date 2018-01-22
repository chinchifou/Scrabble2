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
import letters_and_points as rules


#~~~~~~ GLOBAL VARIBLES ~~~~~~

#----- Constants -----
#reference tile size for a 1920*1080 resolution
REFERENCE_TILE_SIZE = 60
#number of tiles on the board for each column and each row
TILES_PER_BOARD_COLUMN = 15
#delta expressed in tiles from top left corner of the Window
DELTA = 1.5

#----- Changing at runtime -----
#actual tile size used to scale all assets.
TILE_SIZE = 60
#all the remaining letters in the stack
BAG_OF_LETTERS = []
#current state of the board
current_board_state = [ ['?' for i in range(TILES_PER_BOARD_COLUMN)] for j in range(TILES_PER_BOARD_COLUMN) ]
#postion of the mouse cursor on the tile
delta_pos_on_tile = [0.5*TILE_SIZE ,0.5*TILE_SIZE ]

#----- Folders' paths-----
path_log_folder = path.abspath('../log/')
path_icon = path.abspath('../materials/images/icon/')
path_background = path.abspath('../materials/images/background/')
path_buttons = path.abspath('../materials/images/assets/buttons/primary/')
path_buttons_menu = path.abspath('../materials/images/assets/buttons/side_menu/')
path_letters_french = path.abspath('../materials/images/assets/letters/french/')
path_letters_english = path.abspath('../materials/images/assets/letters/english/')
path_letters = path.abspath('../materials/images/assets/letters/')
path_tiles = path.abspath('../materials/images/assets/tiles/')


#~~~~~~ CONVERTION ~~~~~~

def tiles(value_in_pixels) :
	return round( value_in_pixels/float(TILE_SIZE) )

def pixels(value1_in_tiles, value2_in_tiles) :
	return ( round(value1_in_tiles*TILE_SIZE), round(value2_in_tiles*TILE_SIZE) )

#~~~~~~ CLASSES ~~~~~~

#----- Pygame class override -----
#specify the pygame class RenderClear to allow easy reasize
class GroupOfSprites(pygame.sprite.RenderClear):

	#call each resize function of the sprite contained in the group
    def resize(self, *args):
        for s in self.sprites():
            s.resize(*args)


#!!!!!!!!! Work in progress !!!!!!
"""
Instances variables :
	type
	name
	pos_x, pos_y #expressed in tiles
	width, height #espressed in tiles
	image
	rect
"""

class ResizableSprite(pygame.sprite.Sprite):
	#received coordinates are expresed in tiles
	def __init__(self, type, name, pos_x, pos_y):
		#super class constructor
		pygame.sprite.Sprite.__init__(self, self.containers) #self.containers need to have a default container

		#name and type
		self.name = name
		self.type = type
		#position
		self.pos_x = pos_x
		self.pos_y = pos_y

		#load image
		if self.type == "letter" or self.type == "button" :
			if self.type == "letter" :
				self.image = loadTransparentImage(path.join(path_letters, self.name.replace('*','joker')+'.png'))
				self.width, self.height = 1, 1
			elif self.type == "button" :
				self.image = loadTransparentImage(path.join(path_buttons, self.name+'.png'))
				self.width, self.height = 3, 1
		else :
			if self.type == "board" :
				self.image = loadImage(path.join(path_background, self.name+'.png'))
				self.width, self.height = 32, 18
			elif self.type == "tile" :
				self.image = loadImage(path.join(path_tiles, self.name+'.png'))
				self.width, self.height = 1, 1
			elif self.type == "hand_holder" :
				self.image = loadImage(path.join(path_background, self.name+'.png'))
				self.width, self.height = 7.2, 1.2

		#resize image
		self.image = pygame.transform.smoothscale(self.image, pixels(self.width, self.height) )

		#set area to be displayed
		self.rect = pygame.Rect( pixels(self.pos_x, self.pos_y), pixels(self.width, self.height) )

	def resize(self):

		#reload image
		if self.type == "letter" or self.type == "button" :
			if self.type == "letter" :
				self.image = loadTransparentImage(path.join(path_letters, self.name.replace('*','joker')+'.png'))
				logging.debug("resize a letter")
			elif self.type == "button" :
				self.image = loadTransparentImage(path.join(path_buttons, self.name+'.png'))
		else :
			if self.type == "board" :
				self.image = loadImage(path.join(path_background, self.name+'.png'))
			elif self.type == "tile" :
				self.image = loadImage(path.join(path_tiles, self.name+'.png'))
			elif self.type == "hand_holder" :
				self.image = loadImage(path.join(path_background, self.name+'.png'))
		#resize image
		self.image = pygame.transform.smoothscale(self.image, pixels(self.width, self.height) )
		#set area to be displayed
		self.rect = pygame.Rect( pixels(self.pos_x, self.pos_y), pixels(self.width, self.height) )

	def info(self) :
		logging.debug("Sprite info :")
		logging.debug("name : %s", self.name)
		logging.debug("type : %s", self.type)
		logging.debug("at position : %s, %s", self.pos_x, self.pos_y)
		logging.debug("pixel position is : %s, %s", self.rect.x, self.rect.y)

"""
#test children class
class TestClass(ResizableSprite):
	def __init__(self, name, pos_x, pos_y):
		self.type = 'letter'
		ResizableSprite.__init__(self, self.type, name, pos_x, pos_y)
"""
#!!!!!!!!! Work in progress !!!!!!



#----- Board -----
class Board(ResizableSprite):
	def __init__(self, name, pos_x, pos_y):
		self.type = 'board'
		ResizableSprite.__init__(self, self.type, name, pos_x, pos_y)


#----- Hand holder -----
class Hand_holder(ResizableSprite):
	def __init__(self, name, pos_x, pos_y):
		self.type = 'hand_holder'
		ResizableSprite.__init__(self, self.type, name, pos_x, pos_y)


#----- Tiles -----
class Tile(pygame.sprite.Sprite):
	def __init__(self, tile_name, pos_x_in_tiles, pos_y_in_tiles):
		#call superclass constructor
		pygame.sprite.Sprite.__init__(self, self.containers)

		#name
		self.name = tile_name

		#width and height
		self.width_in_tiles = 1
		self.height_in_tiles = 1

		self.width = TILE_SIZE * self.width_in_tiles
		self.height = TILE_SIZE * self.height_in_tiles

		#position
		self.pos_x_in_tiles = pos_x_in_tiles
		self.pos_y_in_tiles = pos_y_in_tiles	

		self.pos_x = TILE_SIZE * self.pos_x_in_tiles
		self.pos_y = TILE_SIZE * self.pos_y_in_tiles

		#TODO add self.pos_x_on_board

		#image
		self.image = loadImage(path.join(path_tiles, self.name+'.png'))
		self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))
		self.rect = pygame.Rect((self.pos_x,self.pos_y), (self.width, self.height))

	def resize(self):
		#calculate new width and height 
		self.width = TILE_SIZE * self.width_in_tiles
		self.height = TILE_SIZE * self.height_in_tiles

		self.pos_x = TILE_SIZE * self.pos_x_in_tiles
		self.pos_y = TILE_SIZE * self.pos_y_in_tiles

		#update
		self.image = loadImage(path.join(path_tiles, self.name+'.png'))
		self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))
		self.rect = pygame.Rect((self.pos_x,self.pos_y), (self.width, self.height))


#----- Buttons -----
class Button(pygame.sprite.Sprite):
	def __init__(self, button_name, pos_x_in_tiles, pos_y_in_tiles):
		#call superclass constructor
		pygame.sprite.Sprite.__init__(self, self.containers)

		self.name = button_name
		
		#width and height
		self.width_in_tiles = 3
		self.height_in_tiles = 1

		self.width = TILE_SIZE * self.width_in_tiles
		self.height = TILE_SIZE * self.height_in_tiles

		self.is_highlighted = False
		self.is_pushed = False

		#position
		self.pos_x_in_tiles = pos_x_in_tiles
		self.pos_y_in_tiles = pos_y_in_tiles

		self.pos_x = TILE_SIZE * self.pos_x_in_tiles
		self.pos_y = TILE_SIZE * self.pos_y_in_tiles

		self.image = loadImage(path.join(path_buttons, self.name+'.png'))
		self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))
		self.rect = pygame.Rect((self.pos_x,self.pos_y), (self.width, self.height))

	def resize(self):
		#calculate new width and height 
		self.width = TILE_SIZE * self.width_in_tiles
		self.height = TILE_SIZE * self.height_in_tiles

		self.pos_x = TILE_SIZE * self.pos_x_in_tiles
		self.pos_y = TILE_SIZE * self.pos_y_in_tiles

		#update
		self.image = loadImage(path.join(path_buttons, self.name+'.png'))
		self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))
		self.rect = pygame.Rect((self.pos_x,self.pos_y), (self.width, self.height))

	def turnOnHighlighted(self):
		self.image = loadImage(path.join(path_buttons, self.name+'_highlighted.png'))
		self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))
		self.is_highlighted = True

	def turnOffHighlighted(self):
		self.image = loadImage(path.join(path_buttons, self.name+'.png'))
		self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))
		self.is_highlighted = False

	def push(self):
		self.image = loadImage(path.join(path_buttons, self.name+'_pushed.png'))
		self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))
		self.is_pushed = True	

	def release(self):
		self.image = loadImage(path.join(path_buttons, self.name+'.png'))
		self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))
		self.is_pushed = False		


#----- Letter -----
class Letter(pygame.sprite.Sprite):
	def __init__(self, letter, pos_x_in_tiles, pos_y_in_tiles):
		#call superclass constructor
		pygame.sprite.Sprite.__init__(self, self.containers)

		self.letter = letter
		self.points = POINTS_FOR[letter]

		self.pos_x_in_tiles = pos_x_in_tiles
		self.pos_y_in_tiles = pos_y_in_tiles

		self.pos_x = TILE_SIZE * self.pos_x_in_tiles
		self.pos_y = TILE_SIZE * self.pos_y_in_tiles

		self.size = TILE_SIZE

		if self.letter == '*':
			self.image = loadTransparentImage(path.join(path_letters, 'joker.png'))
		else :
			self.image = loadTransparentImage(path.join(path_letters, self.letter+'.png'))

		self.image = pygame.transform.smoothscale(self.image, (self.size, self.size))		
		self.rect = pygame.Rect((self.pos_x, self.pos_y), (self.size, self.size))

	def resize(self): 
		self.size = TILE_SIZE

		self.pos_x = TILE_SIZE * self.pos_x_in_tiles
		self.pos_y = TILE_SIZE * self.pos_y_in_tiles

		if self.letter == '*':
			self.image = loadTransparentImage(path.join(path_letters, 'joker.png'))
		else :
			self.image = loadTransparentImage(path.join(path_letters, self.letter+'.png'))

		self.image = pygame.transform.smoothscale(self.image, (self.size, self.size))
		self.rect = pygame.Rect((self.pos_x, self.pos_y), (self.size, self.size))

	#move a letter at a given position expressed in pixels
	def moveAt(self, pos_x, pos_y) :
		self.rect.x = pos_x
		self.rect.y = pos_y

		self.pos_x = pos_x
		self.pos_y = pos_y

		self.pos_x_in_tiles = pos_x / float(TILE_SIZE)
		self.pos_y_in_tiles = pos_y / float(TILE_SIZE)


#----- Player -----
class Player :

    def __init__(self, name, score, hand) :
        self.name = name
        self.score = score
        self.hand = hand
        self.id = len(PLAYERS)

    def info(self) :
    	str_hand = "["
    	for letter_sprite in self.hand :
    		str_hand += '"' + letter_sprite.letter + '"' + ' ,'
    	str_hand = str_hand[:-2]
    	str_hand += "]"
    	logging.info("%s has %s points and the following hand : %s", self.name, self.score, str_hand)

    def next(self) :
    	return PLAYERS[(self.id + 1) % len(PLAYERS)]


#~~~~~~ FUNCTIONS ~~~~~~

#----- Game window creation -----
def resizeWindow(width, height, fullscreen, resizable, resolution_auto, custom_window_height, double_buffer, hardware_accelerated) :
	
	logging.info("WINDOW Creation")
	updateTileSize(width,height)

	width = int (1920 / REFERENCE_TILE_SIZE ) * TILE_SIZE
	height = int (1080 / REFERENCE_TILE_SIZE ) * TILE_SIZE

	logging.info("Size of game window is : %s * %s", width, height)
	logging.info("")

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

	pygame.event.clear(pygame.VIDEORESIZE) #remove the event pygame.VIDEORESIZE from the queue

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
	logging.info("New Tile Size is : %s", TILE_SIZE)

#----- Logging functions -----
def logPlayersInfo():
	logging.info("PLAYERS INFO")
	for player in PLAYERS :
		player.info()
	logging.info("")


#~~~~~~ LOAD CONFIGURATION ~~~~~~

#----- Init logger -----
path_log_file = path.join(path_log_folder,'scrabble.log')
logging.basicConfig(filename=path_log_file, filemode='w', level=logging.DEBUG, format='%(asctime)s.%(msecs)03d  |  %(levelname)s  |  %(message)s', datefmt='%Y-%m-%d %p %I:%M:%S')
logging.info("_________START OF LOG___________")
logging.info("")

#----- Get configuration -----
#Display settings
cfg_fullscreen = config_reader.h_display_params['fullscreen']
cfg_resizable = config_reader.h_display_params['resizable']
cfg_resolution_auto = config_reader.h_display_params['resolution_auto']
cfg_hardware_accelerated = config_reader.h_display_params['enable_hardware_accelerated']
cfg_double_buffer = config_reader.h_display_params['enable_double_buffer']
cfg_custom_window_height = config_reader.h_display_params['custom_window_height']

#Game settings
number_of_letters_per_hand = config_reader.h_rules_params['number_of_letters_per_hand']
display_next_player_hand = config_reader.h_rules_params['display_next_player_hand']
LANGUAGE = config_reader.h_rules_params['language']
players_names = config_reader.players

#Letters and points
if LANGUAGE == 'english' :
	BAG_OF_LETTERS = rules.letters_english
	POINTS_FOR = rules.points_english
	path_letters = path_letters_english
elif LANGUAGE == 'french':
	BAG_OF_LETTERS = rules.letters_french
	POINTS_FOR = rules.points_french
	path_letters = path_letters_french

#logging configuration
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
logging.info("Language : %s", LANGUAGE)
logging.info("Players : %s", players_names)
logging.info("Number of letters per_hand : %s", number_of_letters_per_hand)
logging.info("Display next player hand : %s", display_next_player_hand)
logging.info("")


#~~~~~~ GAME INITIALIAZATION ~~~~~~

#----- Launch Pygame -----
game_engine = pygame.init() #init() -> (numpass, numfail)
sound_engine = pygame.mixer.init() #init(frequency=22050, size=-16, channels=2, buffer=4096) -> None
clock = pygame.time.Clock()
logging.info("INITIALIZATION")
logging.info("%s pygame modules were launched and %s failed", game_engine[0], game_engine[1])
logging.info("Pygame started")
logging.info("")
logging.info("-------------------")
logging.info("GAME STARTED")
logging.info("-------------------")
logging.info("")

#Add icon to the window
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
layer_tiles = GroupOfSprites()
layer_letters_on_board = GroupOfSprites()
layer_letters_just_played = GroupOfSprites()
layer_buttons = GroupOfSprites()
layer_side_menu = GroupOfSprites()
layer_all = GroupOfSprites()

#set default groups
Board.containers = layer_all, layer_background
Hand_holder.containers = layer_all, layer_background
Button.containers = layer_all, layer_buttons
Letter.containers = layer_all
Tile.containers = layer_all, layer_tiles


#----- Create board game -----

#create background
board = Board("empty_background", 0, 0)
hand_holder = Hand_holder("hand_holder", 18.9, 3.4)

#create tiles
DELTA = 1.5
x_pos = 0 + DELTA
y_pos = 0 + DELTA
for row in range(0,TILES_PER_BOARD_COLUMN) :
	for column in range(0, TILES_PER_BOARD_COLUMN) :
		if rules.BOARD_LAYOUT[row][column] == 0 :
			Tile('start', x_pos, y_pos)
		elif rules.BOARD_LAYOUT[row][column] == 1 :
			Tile('empty', x_pos, y_pos)
		elif rules.BOARD_LAYOUT[row][column] == 2 :
			Tile('double_letter', x_pos, y_pos)
		elif rules.BOARD_LAYOUT[row][column] == 3 :
			Tile('triple_letter', x_pos, y_pos)
		elif rules.BOARD_LAYOUT[row][column] == 4 :
			Tile('double_word', x_pos, y_pos)
		elif rules.BOARD_LAYOUT[row][column] == 5 :
			Tile('triple_word', x_pos, y_pos)
		x_pos += 1
	x_pos = 0 + DELTA
	y_pos += 1

#create a test button
button_end_turn = Button("end_turn", 27, 3.5)


#----- Create players -----

PLAYERS = []

for player_name in players_names :
	start_hand = GroupOfSprites()
	pos_x = (TILES_PER_BOARD_COLUMN+4)
	pos_y = 3.5
	for i in range(number_of_letters_per_hand) :
		random_int = randint(0,len(BAG_OF_LETTERS)-1)
		start_hand.add(Letter(BAG_OF_LETTERS[random_int], pos_x, pos_y))
		del(BAG_OF_LETTERS[random_int])
		pos_x = pos_x+1

	PLAYERS.append(Player(player_name,0,start_hand))

logPlayersInfo()

id_current_player = 0
current_player = PLAYERS[id_current_player]

#///// Test Values /////
#layer_letters_just_played.add(Letter("J",3+DELTA, 5+DELTA))
"""
TestClass.containers = layer_all
test_letter = TestClass('a', 5, 5)
layer_letters_just_played.add(test_letter)
"""
#///////////////////////


#----- First image -----

for sprite in layer_background :
	sprite.info()


BLACK_BACKGROUND = window.copy()

layer_background.draw(window)
layer_tiles.draw(window)
layer_buttons.draw(window)

current_background = window.copy()	

layer_letters_just_played.draw(window) #TODO TEMP ?

pygame.display.update()

#----- Initial game state -----

current_action = 'SELECT_A_LETTER'
NO_LETTER = Letter('A',0,0)
selected_letter = NO_LETTER


#~~~~~~ MAIN  ~~~~~~

#----- Start -----

#Game is running
game_is_running = True

#Main loop
while game_is_running:
	
	for event in pygame.event.get():

		event_type = event.type

		#~~~~~~ QUIT ~~~~~~
		if ( event_type == pygame.QUIT ) :
			game_is_running = False #exit the game
			logging.info("-------------------")
			logging.info("Exiting game")
			logging.info("-------------------")
			logging.info("")

		#~~~~~~ WINDOW RESIZE ~~~~~~
		elif ( event_type == pygame.VIDEORESIZE ) : #properly refresh the game window if a resize is detected
			
			#new width and height
			width = event.dict['size'][0]
			height = event.dict['size'][1]

			#TODO to improve
			BLACK_BACKGROUND = window.fill((0,0,0))
			pygame.display.update()

			window = resizeWindow(width, height, cfg_fullscreen, cfg_resizable, cfg_resolution_auto, cfg_custom_window_height, cfg_double_buffer, cfg_hardware_accelerated)

			#To IMPROVE ?
			BLACK_BACKGROUND = window.fill((0,0,0))
			pygame.display.update()
			layer_all.resize()

			layer_background.draw(window)
			layer_tiles.draw(window)
			layer_letters_on_board.draw(window)
			layer_buttons.draw(window)
			layer_letters_just_played.draw(window)
			
			current_background = window.copy()
			
			pygame.display.update()
			
		#~~~~~~ KEY PRESSED ~~~~~~			
		elif ( event_type == pygame.KEYDOWN ) :
			logging.info("Key pressed")
			key_pressed = event.key
			
			if ( key_pressed == pygame.K_ESCAPE ) :
				logging.info("ESCAPE key pressed")
				game_is_running = False #exit the game
			

		#~~~~~~~~~~~ MOUSE BUTTONS ~~~~~~~~~~~
		elif ( ( (event_type == pygame.MOUSEBUTTONDOWN) or (event_type == pygame.MOUSEBUTTONUP) ) and event.button == 1 ) :

			timer = clock.tick()            
			#~~~~~~~~~~~ PRESS LEFT CLIC ~~~~~~~~~~~
			if ( event_type == pygame.MOUSEBUTTONDOWN ) :

				cursor_pos_x, cursor_pos_y = event.pos[0], event.pos[1]

				#------ SELECT A LETTER -------
				if current_action == 'SELECT_A_LETTER' :
					#TODO rename tile in letter
					#click on a letter in hand ?
					for tile_in_hand in current_player.hand :

						if tile_in_hand.rect.collidepoint(cursor_pos_x, cursor_pos_y) == True :

							selected_letter = tile_in_hand
							delta_pos_on_tile = ( cursor_pos_x - tile_in_hand.rect.x , cursor_pos_y - tile_in_hand.rect.y)
							current_action = "PLAY_A_LETTER"

					#click on a letter just played ?
					for tile_in_hand in layer_letters_just_played :

						if tile_in_hand.rect.collidepoint(cursor_pos_x, cursor_pos_y) == True :

							selected_letter = tile_in_hand
							delta_pos_on_tile = ( cursor_pos_x - tile_in_hand.pos_x , cursor_pos_y - tile_in_hand.pos_y)

							tile_x_on_board = int( tile_in_hand.pos_x_in_tiles - DELTA)
							tile_y_on_board = int(tile_in_hand.pos_y_in_tiles - DELTA)

							current_board_state[tile_y_on_board][tile_x_on_board] = '?'

							layer_letters_just_played.remove(selected_letter)
							current_player.hand.add(selected_letter)

							layer_letters_just_played.clear(window, current_background)
							layer_letters_just_played.draw(window)

							current_player.hand.clear(window, current_background)	
							current_player.hand.draw(window)

							pygame.display.update()

							current_action = "PLAY_A_LETTER"


				#------ PLAY A LETTER -------
				elif current_action == 'PLAY_A_LETTER' :

					#click on a tile ?
					for tile in layer_tiles :

						if tile.rect.collidepoint(cursor_pos_x, cursor_pos_y) == True :

							tile_x_on_board = int( tile.pos_x_in_tiles - DELTA )
							tile_y_on_board = int( tile.pos_y_in_tiles - DELTA )

							#Tile is empty
							if current_board_state[tile_y_on_board][tile_x_on_board] == '?':

								#letter from hand
								if current_player.hand.has(selected_letter) : 

									selected_letter.moveAt( (tile_x_on_board + DELTA) * TILE_SIZE , (tile_y_on_board + DELTA) * TILE_SIZE )
									current_board_state[tile_y_on_board][tile_x_on_board] = selected_letter.letter

									current_player.hand.remove(selected_letter)
									current_player.hand.remove(selected_letter)
									layer_letters_just_played.add(selected_letter)

									selected_letter = NO_LETTER

									current_player.hand.clear(window, current_background)								
									current_player.hand.draw(window)

									layer_letters_just_played.clear(window, current_background)	
									layer_letters_just_played.draw(window)

									pygame.display.update()

									current_action = "SELECT_A_LETTER"

								#letter from board
								elif layer_letters_just_played.has(selected_letter) :

									selected_letter.moveAt( (tile_x_on_board + DELTA) * TILE_SIZE , (tile_y_on_board + DELTA) * TILE_SIZE )
									current_board_state[tile_y_on_board][tile_x_on_board] = selected_letter.letter

									selected_letter = NO_LETTER

									layer_letters_just_played.clear(window, current_background)	
									layer_letters_just_played.draw(window)

									pygame.display.update()


									logging.debug("board state")
									logging.debug("%s", current_board_state)

									current_action = "SELECT_A_LETTER"

				#start next player tunnel
				if button_end_turn.rect.collidepoint(cursor_pos_x, cursor_pos_y) == True :
					#change button state
					button_end_turn.push()
					button_end_turn.is_highlighted = False
					layer_buttons.clear(window, current_background)
					layer_buttons.draw(window)
					pygame.display.update()


			elif ( event_type == pygame.MOUSEBUTTONUP ) :

				#next player
				if button_end_turn.rect.collidepoint(cursor_pos_x, cursor_pos_y) == True :
					#change button state
					button_end_turn.push()
					button_end_turn.is_highlighted = False
					layer_buttons.clear(window, current_background)
					layer_buttons.draw(window)
					pygame.display.update()

					#TODO calculate score

					for letter in layer_letters_just_played :
						layer_letters_on_board.add(letter)

					layer_letters_just_played.empty()

					current_player.hand.clear(window, current_background)
					current_player = current_player.next()

					current_player.info()

					layer_letters_on_board.clear(window, current_background)
					layer_letters_just_played.clear(window, current_background)

					layer_letters_on_board.draw(window)

					current_background = window.copy()

					current_player.hand.draw(window)

					pygame.display.update()

				#relase pushed buttons
				for button in layer_buttons :
					if button.is_pushed :
						button.release()
						if button.rect.collidepoint(cursor_pos_x, cursor_pos_y) :
							button.turnOnHighlighted()
						else :
							button.turnOffHighlighted()
						layer_buttons.clear(window, current_background)
						layer_buttons.draw(window)

						#TO DO - prevent artefact

						pygame.display.update()


		#~~~~~~ MOUSE MOTION ~~~~~~	
		elif(event_type == pygame.MOUSEMOTION ):

			mouse_pos = pygame.mouse.get_pos()
			cursor_pos_x = mouse_pos[0]
			cursor_pos_y = mouse_pos[1]

			#change appearance of button
			if current_action == 'SELECT_A_LETTER' :
				buttons_changed = False
				for button in layer_buttons :
					if ( button.rect.collidepoint(cursor_pos_x, cursor_pos_y) == True ) and ( not button.is_highlighted ) and (not button.is_pushed ) :
						button.turnOnHighlighted()
						buttons_changed = True
					elif ( button.rect.collidepoint(cursor_pos_x, cursor_pos_y) == False ) and ( button.is_highlighted ):
						button_end_turn.turnOffHighlighted()
						buttons_changed = True

				if buttons_changed :
					layer_buttons.clear(window, current_background)
					layer_buttons.draw(window)
					pygame.display.update()


			selected_letter.moveAt(cursor_pos_x - delta_pos_on_tile[0], cursor_pos_y - delta_pos_on_tile[1])

			current_player.hand.clear(window, current_background)								
			current_player.hand.draw(window)

			layer_letters_just_played.clear(window, current_background)	
			layer_letters_just_played.draw(window)

			pygame.display.update()
			

logging.info("Game has ended")
logging.info("")
logging.info("_________END OF LOG___________")

