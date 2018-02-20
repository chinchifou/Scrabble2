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


#~~~~~~ PYGAME CLASSES OVERRIDE ~~~~~~

#----- GroupOfSprites -----
#complete the pygame class RenderClear to allow easy resize
class GroupOfSprites(pygame.sprite.RenderClear):

	#for each sprite in this GroupOfSprites, call the resize() function
	def resize(self, *args):
		for s in self.sprites():
			s.resize(*args)

	#for each sprite in this GroupOfSprites, call the drawText() function
	def drawText(self, *args):
		for s in self.sprites():
			s.drawText(*args)


#~~~~~~ GLOBAL VARIBLES ~~~~~~

#----- Constants -----
#define global scope for variables
global REFERENCE_TILE_SIZE, TILES_PER_BOARD_COLUMN, DELTA, TITLE_LINE_HEIGHT, LINE_HEIGHT, COLOR_LIGHT_GREY, PLAYERS
#reference tile size for a 1920*1080 resolution
REFERENCE_TILE_SIZE = 60
#number of tiles on the board for each column and each row
TILES_PER_BOARD_COLUMN = 15
#delta expressed in tiles from top left corner of the Window
DELTA = 1.5
#size of the ui text used for titke expressed in tile
TITLE_LINE_HEIGHT = 0.9
#size of the common ui text expressed in tile
LINE_HEIGHT = 0.6
#color use for text rendering
COLOR_LIGHT_GREY = (143,144,138)
#all players
PLAYERS = []

#Folders' paths
path_log_folder = path.abspath('../log/')
path_icon = path.abspath('../materials/images/icon/')
path_background = path.abspath('../materials/images/background/')
path_buttons = path.abspath('../materials/images/assets/buttons/primary/')
path_buttons_menu = path.abspath('../materials/images/assets/buttons/side_menu/')
path_letters_french = path.abspath('../materials/images/assets/letters/french/')
path_letters_english = path.abspath('../materials/images/assets/letters/english/')
path_letters = path.abspath('../materials/images/assets/letters/')
path_tiles = path.abspath('../materials/images/assets/tiles/')


#----- Changing a runtime -----
#class to store game variable
class GameVariable():
	def __init__(self):
		self.monitor_resolution = 0.0

		self.tile_size = 0.0
		self.delta_pos_on_tile = 0.0

		self.bag_of_letters = []
		self.current_board_state = [ ['?' for i in range(TILES_PER_BOARD_COLUMN)] for j in range(TILES_PER_BOARD_COLUMN) ] 
		
		self.current_player = []
		self.current_action = 'SELECT_A_LETTER'

		self.background_no_letter = []

		self.current_background = []
		self.current_background_no_text = []

		self.ui_text_container = []

var = GameVariable()

#TODO to remove
"""
#class storing varaibles relative to font
class Font():
	def __init__(self):
		self.calibri = ""
		self.calibri_title = ""

	def resize(self):
		self.calibri_title = pygame.font.SysFont("Calibri", floor(TITLE_LINE_HEIGHT*var.tile_size))
		self.calibri_title.set_bold(1)
		self.calibri = pygame.font.SysFont("Calibri", floor(LINE_HEIGHT*var.tile_size))

fonts = Font()
"""

#class to create rendering layers used for display
class Layer():
	def __init__(self):
		self.background = GroupOfSprites()
		self.tiles = GroupOfSprites()
		self.hand_holder = GroupOfSprites()
		self.letters_on_board = GroupOfSprites()
		self.letters_just_played = GroupOfSprites()
		self.selected_letter = GroupOfSprites()
		self.buttons = GroupOfSprites()
		self.side_menu = GroupOfSprites()
		self.all = GroupOfSprites()

layers = Layer()

#TODO to remove
"""
#class storing user interface data
class UserInterface():
	def __init__(self):
		current_player_turn = ''
		next_player_hand = ''
		scores = ''
		player_score = ''
		previous_turn_summary = ''
		word_and_score = ''
		scrabble_obtained = ''
		nothing_played = ''
		remaining_letters_in_bag = ''
		remaining_letter_in_bag = ''
		no_remaining_letter_in_bag = ''

ui = UserInterface()
"""

#class storing user interface data
class UserInterfaceText():
	def __init__(self, text, ligne_heigh, bold, pos_in_tiles):
		self.text = text
		self.ligne_heigh = ligne_heigh
		self.bold = int(bold)	

		self.font = pygame.font.SysFont("Calibri", floor(self.ligne_heigh*var.tile_size))
		self.font.set_bold(self.bold)

		self.pos_x_tiles, self.pos_y_tiles = pos_in_tiles[0], pos_in_tiles[1]
		self.pos_x, self.pos_y = pixels(self.pos_x_tiles, self.pos_y_tiles)

	def resize(self):
		self.font = pygame.font.SysFont("Calibri", floor(self.ligne_heigh*var.tile_size))
		self.font.set_bold(self.bold)

		self.pos_x, self.pos_y = pixels(self.pos_x_tiles, self.pos_y_tiles)


#~~~~~~ CONVERTION ~~~~~~

#----- ResizableSprite -----
def tiles(value_in_pixels1, value_in_pixels2) :
	return ( round( value_in_pixels1/float(var.tile_size) ), round( value_in_pixels2/float(var.tile_size) ) )

def pixels(value1_in_tiles, value2_in_tiles) :
	return ( (value1_in_tiles*var.tile_size), (value2_in_tiles*var.tile_size) )

def int_pixels(value1_in_tiles, value2_in_tiles) :
	return ( round(value1_in_tiles*var.tile_size), round(value2_in_tiles*var.tile_size) )

def indexInHandHolder(cursor_pos_x):
	delta_x_hand_holder = DELTA + TILES_PER_BOARD_COLUMN + DELTA + 1
	index_in_hand = int( floor( cursor_pos_x/float(var.tile_size) ) - delta_x_hand_holder )
	#fix value on the edge
	if index_in_hand == -1:
		index_in_hand = 0
	elif index_in_hand == 7 :
		index_in_hand = 6
	return index_in_hand


#~~~~~~ GAME CLASSES ~~~~~~


#----- ResizableSprite -----
#add native capacity to be resized
class ResizableSprite(pygame.sprite.Sprite):
	nb_letters_instances = 0
	#received coordinates are expresed in tiles
	def __init__(self, name, pos_x, pos_y):
		#super class constructor
		pygame.sprite.Sprite.__init__(self, self.containers) #self.containers need to have a default container

		#name and type
		self.name = name
		#position
		self.pos_x = pos_x
		self.pos_y = pos_y

		#load image
		if self.type == "letter" or self.type == "button" :
			self.image = loadTransparentImage(path.join(self.path, self.name.replace('*','joker')+'.png'))
		else :
			self.image = loadImage(path.join(self.path, self.name+'.png'))

		#resize image
		self.image = pygame.transform.smoothscale(self.image, int_pixels(self.width, self.height) )

		#set area to be displayed
		self.rect = pygame.Rect( pixels(self.pos_x, self.pos_y), pixels(self.width, self.height) )

	def resize(self):

		#reload image
		if self.type == "letter" or self.type == "button" :
			self.image = loadTransparentImage(path.join(self.path, self.name.replace('*','joker')+'.png'))
		else :
			self.image = loadImage(path.join(self.path, self.name+'.png'))
		#resize image
		self.image = pygame.transform.smoothscale(self.image, int_pixels(self.width, self.height) )
		#set area to be displayed
		self.rect = pygame.Rect( pixels(self.pos_x, self.pos_y), pixels(self.width, self.height) )

		if self.type == "board":
			self.drawText()

	def info(self) :
		logging.debug("Sprite info :")
		logging.debug("name : %s", self.name)
		logging.debug("type : %s", self.type)
		logging.debug("at position : %s, %s", self.pos_x, self.pos_y)
		logging.debug("pixel position is : %s, %s", self.rect.x, self.rect.y)
		logging.debug("width : %s / height : %s", self.width, self.height)
		logging.debug("pixel width : %s /  pixel height : %s", self.rect.width, self.rect.height)
		logging.debug("")


#----- Sprites -----

#----- Board -----
class Board(ResizableSprite):
	def __init__(self, name, pos_x, pos_y):
		self.type = 'board'
		self.width, self.height = 32, 18
		self.path = path_background

		
		#TODO to remove
		self.text_current_player = ""
		self.pos_text_current_player = ( 0, 0 )
		
		ResizableSprite.__init__(self, name, pos_x, pos_y)

	def drawText(self):
		"""
		self.text_current_player = fonts.calibri_title.render(ui.current_player_turn.replace('<VALUE1>',var.current_player.name),1,COLOR_LIGHT_GREY)
		self.pos_text_current_player = ( (DELTA+TILES_PER_BOARD_COLUMN+DELTA+1)*var.tile_size, 2.0*var.tile_size )
		window.blit(self.text_current_player, self.pos_text_current_player)
		"""
		#TODO to improve
		text = ui_current_player_turn.font.render( ui_current_player_turn.text.replace('<VALUE1>',var.current_player.name), 1, COLOR_LIGHT_GREY )
		window.blit(text, (ui_current_player_turn.pos_x, ui_current_player_turn.pos_y))

		text = ui_next_player_hand.font.render( ui_next_player_hand.text.replace('<VALUE1>',var.current_player.next().name), 1, COLOR_LIGHT_GREY )
		window.blit(text, (ui_next_player_hand.pos_x, ui_next_player_hand.pos_y))


#----- Hand holder -----
class Hand_holder(ResizableSprite):
	def __init__(self, name, pos_x, pos_y):
		self.type = 'hand_holder'
		self.width, self.height = 7.2, 1.2
		self.path = path_background
		ResizableSprite.__init__(self, name, pos_x, pos_y)


#----- Tiles -----
class Tile(ResizableSprite):
	def __init__(self, name, pos_x, pos_y):
		self.type = 'tile'
		self.width, self.height = 1, 1
		self.path = path_tiles
		ResizableSprite.__init__(self, name, pos_x, pos_y)


#----- Buttons -----
class Button(ResizableSprite):
	def __init__(self, name, pos_x, pos_y):
		self.type = 'button'
		self.width, self.height = 3, 1
		self.path = path_buttons
		self.is_highlighted = False
		self.is_pushed = False
		ResizableSprite.__init__(self, name, pos_x, pos_y)

	def turnOnHighlighted(self):
		self.image = loadImage(path.join(self.path, self.name+'_highlighted.png'))
		self.image = pygame.transform.smoothscale(self.image, pixels(self.width, self.height))	
		self.is_highlighted = True

	def turnOffHighlighted(self):
		self.image = loadImage(path.join(self.path, self.name+'.png'))
		self.image = pygame.transform.smoothscale(self.image, pixels(self.width, self.height))
		self.is_highlighted = False

	def push(self):
		self.image = loadImage(path.join(self.path, self.name+'_pushed.png'))
		self.image = pygame.transform.smoothscale(self.image, pixels(self.width, self.height))
		self.is_pushed = True	

	def release(self):
		self.image = loadImage(path.join(self.path, self.name+'.png'))
		self.image = pygame.transform.smoothscale(self.image, pixels(self.width, self.height))
		self.is_pushed = False		


#----- Letter -----
class Letter(ResizableSprite):
	def __init__(self, name, pos_x, pos_y):
		self.type = 'letter'
		self.width, self.height = 1, 1
		self.path = path_letters

		ResizableSprite.__init__(self, name, pos_x, pos_y)		

		#add a instance in the class counter
		ResizableSprite.nb_letters_instances += 1
		#and use it to define the id
		self.id = ResizableSprite.nb_letters_instances	

		self.points = POINTS_FOR[name]

	#move a letter at a given position expressed in tiles
	def moveAtTile(self, pos_x, pos_y) :
		self.rect.x, self.rect.y = pixels(pos_x, pos_y)
		self.pos_x, self.pos_y  = pos_x, pos_y

	#move a letter at a given position expressed in pixels
	def moveAtPixels(self, pos_x, pos_y) :
		self.rect.x, self.rect.y = pos_x, pos_y
		self.pos_x, self.pos_y  = tiles(pos_x, pos_y)

#----- Define sprites behavior -----

#set default groups
Board.containers = layers.all, layers.background
Hand_holder.containers = layers.all, layers.hand_holder
Tile.containers = layers.all, layers.tiles
Button.containers = layers.all, layers.buttons
Letter.containers = layers.all

#----- Other classes -----

#----- Player -----
class Player :

	def __init__(self, name, score, hand) :
		self.name = name
		self.score = score
		self.hand = hand
		self.id = len(PLAYERS)

		self.hand_state = []
		for i in range(number_of_letters_per_hand) :
			self.hand_state.append(0)

		index = 0
		for letter in hand :
			self.hand_state[index] = letter.id
			index += 1

	def info(self) :
		str_hand = "["
		for letter_sprite in self.hand :
			str_hand += '"' + letter_sprite.name + '"' + ' ,'
		str_hand = str_hand[:-2]
		str_hand += "]"
		logging.info("%s  :", self.name)
		logging.info("  points : %s", self.score)
		logging.info("  hand : %s", str_hand)

	def next(self) :
		return PLAYERS[(self.id + 1) % len(PLAYERS)]


#~~~~~~ FUNCTIONS ~~~~~~

#----- Game window creation -----
def resizeWindow(width, height, fullscreen, resizable, resolution_auto, custom_window_height, double_buffer, hardware_accelerated) :
	
	logging.info("WINDOW Creation")
	updateTileSize(width,height)
	#fonts.resize()
	#TODO
	for ui_text in var.ui_text_container :
		ui_text.resize()

	layers.all.resize()

	width = int (1920 / REFERENCE_TILE_SIZE ) * var.tile_size
	height = int (1080 / REFERENCE_TILE_SIZE ) * var.tile_size

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

#Load image
def loadImage(complete_path):
	image = pygame.image.load(complete_path)
	image = image.convert()
	return image

#Load transparent image
def loadTransparentImage(complete_path):
	image = pygame.image.load(complete_path)
	image = image.convert_alpha()
	return image

#Update Tile Size to match new window size
def updateTileSize(width, height):
	zoom_factor = min( float(width / 1920), float(height/1080) )
	var.tile_size = int (floor ( REFERENCE_TILE_SIZE*zoom_factor ) )	
	logging.info("New Tile Size is : %s", var.tile_size)
	if var.current_action == "PLAY_A_LETTER" :
		var.delta_pos_on_tile
		var.delta_pos_on_tile = (var.delta_pos_on_tile[0]*zoom_factor, var.delta_pos_on_tile[1]*zoom_factor)

#Logging functions
def logPlayersInfo():
	logging.info("PLAYERS INFO")
	for player in PLAYERS :
		player.info()
	logging.info("")

#Calculate points
def calculatePoints(layer_letters_played) :

	var.current_board_state, TILES_PER_BOARD_COLUMN

	#format letters_played {'a' : (x, y)}
	letters_played = {}
	for letter in layer_letters_played :
		letters_played[(int(letter.pos_y - DELTA), int(letter.pos_x - DELTA))] = letter.name

	if len(letters_played) > 1 :
		logging.debug('%i letters played', len(letters_played))
	else :
		logging.debug('%i letter played', len(letters_played))  

	if len(letters_played) == 0 :
		logging.info('nothing played')
		logging.info('')
		return []

	else :
		#init 
		all_x = []
		all_y = []

		for tuple_pos in letters_played.keys() :
			all_x.append(tuple_pos[0])
			all_y.append(tuple_pos[1])

		min_x = min(all_x)
		max_x = max(all_x)
		min_y = min(all_y)
		max_y = max(all_y)

		delta_x = max_x - min_x
		delta_y = max_y - min_y


		words_and_scores = []

		if len(letters_played) == 7 : #is a SCRABBLE ?
			words_and_scores.append(['!! SCRABBLE !!', 50])

		if delta_x == 0 :

			#find first letter
			start_y = min_y
			while( ( (start_y - 1) >= 0) and (var.current_board_state[min_x][start_y - 1] != '?') ) :
				start_y = start_y - 1

			#find last letter
			end_y = max_y
			while( ( (end_y + 1) <= TILES_PER_BOARD_COLUMN-1) and (var.current_board_state[min_x][end_y + 1] != '?') ) :
				end_y = end_y + 1

			#words_and_scores = []

			if ( end_y > start_y ) : #prevent one letter word
				logging.debug('HORIZONTAL WORD')
				#FIRST PASSAGE
				#store word just created
				new_word = ''
				new_word_multiplier = 1
				new_word_score = 0

				for it_y in range( start_y, end_y+1 ) :
					letter = var.current_board_state[min_x][it_y]
					new_word += letter
					if ((min_x, it_y) in letters_played ): #letters just played
						#calculate points for each letter
						bonus = rules.BOARD_LAYOUT[min_x][it_y]
						if bonus == 0 : #start_tile
							new_word_multiplier *= 2
							bonus = 1
						elif bonus == 4:
							new_word_multiplier *= 2
							bonus = 1
						elif bonus == 5:
							new_word_multiplier *= 3
							bonus = 1

						new_letter_points = POINTS_FOR[letter]
						new_word_score = new_word_score + (bonus * new_letter_points)

					else : #old letters
						old_letter_points = POINTS_FOR[letter]
						new_word_score = new_word_score + old_letter_points
						
				new_word_score = new_word_score * new_word_multiplier
				words_and_scores.append([new_word, new_word_score])


			#SECOND PASSAGE
			for it_y in range( start_y, end_y+1 ) :
				#check for horizontal words
				it_x = min_x
				if (it_x, it_y) in (letters_played) : #prevent to count already existing words

					condition_1 = ( (it_x - 1) >= 0 ) and ( var.current_board_state[it_x-1][it_y] != '?' )
					condition_2 = ( (it_x + 1) <= TILES_PER_BOARD_COLUMN-1 ) and ( var.current_board_state[it_x+1][it_y] != '?' ) 

					if ( condition_1  or condition_2 ) :       
						logging.debug('VERTICAL WORD')
				
						while( ( (it_x - 1) >= 0) and (var.current_board_state[it_x-1][it_y] != '?') ) : #go to the begining of the word
							it_x = it_x - 1


						old_word = ''
						old_word_score = 0
						old_word_multiplier = 1  

						while( ( (it_x) <= TILES_PER_BOARD_COLUMN-1) and (var.current_board_state[it_x][it_y] != '?') ) : #go to the end of the word

							old_letter = var.current_board_state[it_x][it_y]
							old_word += old_letter

							if (it_x, it_y) in (letters_played) :

								bonus = rules.BOARD_LAYOUT[it_x][it_y]

								if bonus == 0 : #start_tile
									old_word_multiplier *= 2
									bonus = 1
								elif bonus == 4:
									old_word_multiplier *= 2
									bonus = 1
								elif bonus == 5:
									old_word_multiplier *= 3
									bonus = 1

								old_word_score += POINTS_FOR[old_letter] * bonus

							else :
								old_word_score += POINTS_FOR[old_letter]

							it_x = it_x + 1

						old_word_score = old_word_score * old_word_multiplier
						words_and_scores.append([old_word, old_word_score])


			total_score = 0 

			for association in words_and_scores :
				logging.info('Word %s gives %i points', association[0], association[1])
				total_score += association[1]
			
			logging.info('total_score : %i', total_score)
			logging.info('')
			return words_and_scores 


		else : 
			#find first letter
			start_x = min_x
			while( ( (start_x - 1) >= 0) and (var.current_board_state[start_x - 1][min_y] != '?') ) :
				start_x = start_x - 1

			#find last letter
			end_x = max_x
			while( ( (end_x + 1) <= TILES_PER_BOARD_COLUMN-1) and (var.current_board_state[end_x + 1][min_y] != '?') ) :
				end_x = end_x + 1

			if ( end_x > start_x ) : #prevent one letter word
				logging.debug('VERTICAL WORD')
				#FIRST PASSAGE
				#store word just created  
				new_word = ''
				new_word_multiplier = 1
				new_word_score = 0

				for it_x in range( start_x, end_x+1 ) :
					letter = var.current_board_state[it_x][min_y]
					new_word += letter
					if ((it_x, min_y) in letters_played ): #letters just played
						#calculate points for each letter
						bonus = rules.BOARD_LAYOUT[it_x][min_y]
						if bonus == 0 : #start_tile
							new_word_multiplier *= 2
							bonus = 1
						elif bonus == 4:
							new_word_multiplier *= 2
							bonus = 1
						elif bonus == 5:
							new_word_multiplier *= 3
							bonus = 1

						new_letter_points = POINTS_FOR[letter]
						new_word_score = new_word_score + (bonus * new_letter_points)

					else : #old letters
						old_letter_points = POINTS_FOR[letter]
						new_word_score = new_word_score + old_letter_points
						
				new_word_score = new_word_score * new_word_multiplier
				words_and_scores.append([new_word, new_word_score])


			#SECOND PASSAGE
			for it_x in range( start_x, end_x+1 ) :
				#check for vertical words
				it_y = min_y
				if (it_x, it_y) in (letters_played) : #prevent to count already existing words

					condition_1 = ( (it_y - 1) >= 0 ) and ( var.current_board_state[it_x][it_y-1] != '?' )
					condition_2 = ( (it_y + 1) <= TILES_PER_BOARD_COLUMN-1 ) and ( var.current_board_state[it_x][it_y+1] != '?' ) 

					if ( condition_1  or condition_2 ) :
						logging.debug('HORIZONTAL WORD')

						while( ( (it_y - 1) >= 0) and (var.current_board_state[it_x][it_y-1] != '?') ) : #go to the begining of the word
							it_y = it_y - 1


						old_word = ''
						old_word_score = 0
						old_word_multiplier = 1

						while( ( (it_y) <= TILES_PER_BOARD_COLUMN-1) and (var.current_board_state[it_x][it_y] != '?') ) : #go to the end of the word

							old_letter = var.current_board_state[it_x][it_y]
							old_word += old_letter

							if (it_x, it_y) in (letters_played) :

								bonus = rules.BOARD_LAYOUT[it_x][it_y]

								if bonus == 0 : #start_tile
									old_word_multiplier *= 2
									bonus = 1
								elif bonus == 4:
									old_word_multiplier *= 2
									bonus = 1
								elif bonus == 5:
									old_word_multiplier *= 3
									bonus = 1

								old_word_score += POINTS_FOR[old_letter] * bonus

							else :
								old_word_score += POINTS_FOR[old_letter]
							
							it_y = it_y + 1

						old_word_score = old_word_score * old_word_multiplier
						words_and_scores.append([old_word, old_word_score])

			total_score = 0 #TEMP

			for association in words_and_scores :
				logging.info('Word %s gives %i points', association[0], association[1])
				total_score += association[1]
			
			logging.info('total_score : %i', total_score)
			logging.info('')

			return words_and_scores

#~~~~~~ LOAD CONFIGURATION ~~~~~~

#----- Init logger -----

path_log_file = path.join(path_log_folder,'scrabble.log')
logging.basicConfig(filename=path_log_file, filemode='w', level=logging.DEBUG, format='%(asctime)s.%(msecs)03d  |  %(levelname)s  |  %(message)s', datefmt='%Y-%m-%d %p %I:%M:%S')
logging.info("_________START OF LOG___________")
logging.info("")

#----- Get configuration -----

#Display settings
display_settings = config_reader.h_display_params
cfg_fullscreen = display_settings['fullscreen']
cfg_resizable = display_settings['resizable']
cfg_resolution_auto = display_settings['resolution_auto']
cfg_hardware_accelerated = display_settings['enable_hardware_accelerated']
cfg_double_buffer = display_settings['enable_double_buffer']
cfg_custom_window_height = display_settings['custom_window_height']
cfg_max_fps = display_settings['max_fps']

#Game settings
game_settings = config_reader.h_rules_params
number_of_letters_per_hand = game_settings['number_of_letters_per_hand']
display_next_player_hand = game_settings['display_next_player_hand']
LETTERS_LANGUAGE = game_settings['letters_language']
UI_LANGUAGE = game_settings['ui_language']
players_names = config_reader.players

#Letters and points
if LETTERS_LANGUAGE == 'english' :
	var.bag_of_letters = rules.letters_english
	POINTS_FOR = rules.points_english
	path_letters = path_letters_english
elif LETTERS_LANGUAGE == 'french':
	var.bag_of_letters = rules.letters_french
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
logging.info("Language : %s", LETTERS_LANGUAGE)
logging.info("Players : %s", players_names)
logging.info("Number of letters per_hand : %s", number_of_letters_per_hand)
logging.info("Display next player hand : %s", display_next_player_hand)
logging.info("")


#~~~~~~ GAME INITIALIAZATION ~~~~~~

#----- Launch Pygame -----

game_engine = pygame.init() #init() -> (numpass, numfail)
sound_engine = pygame.mixer.init() #init(frequency=22050, size=-16, channels=2, buffer=4096) -> None
fps_clock = pygame.time.Clock()
clic_clock = pygame.time.Clock() #TODO to use
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

#----- Initializing User Interface texts -----
#TODO to remove
"""
#create specific fonts
fonts.calibri_title = pygame.font.SysFont("Calibri", floor(TITLE_LINE_HEIGHT*var.tile_size))
fonts.calibri_title.set_bold(1)
fonts.calibri = pygame.font.SysFont("Calibri", floor(LINE_HEIGHT*var.tile_size))
"""
#User interface language
if UI_LANGUAGE == 'english' :
	language_id = 0
elif UI_LANGUAGE == 'french' :
	language_id = 1
else :
	language_id = 0

#User interface content
ui_content = config_reader.h_ui_params

#TODO to refactor
"""
#ui.current_player_turn = ui_content['current_player_turn'][language_id]
#ui.next_player_hand = ui_content['next_player_hand'][language_id]
ui.scores = ui_content['scores'][language_id]
ui.player_score = ui_content['player_score'][language_id]
ui.previous_turn_summary = ui_content['previous_turn_summary'][language_id]
ui.word_and_score = ui_content['word_and_score'][language_id]
ui.scrabble_obtained = ui_content['scrabble_obtained'][language_id]
ui.nothing_played = ui_content['nothing_played'][language_id]
ui.remaining_letters_in_bag = ui_content['remaining_letters'][language_id]
ui.remaining_letter_in_bag = ui_content['remaining_letter'][language_id]
ui.no_remaining_letter_in_bag = ui_content['no_remaining_letter'][language_id]
"""

ui_current_player_turn = UserInterfaceText(ui_content['current_player_turn'][language_id], TITLE_LINE_HEIGHT, True, ( (DELTA+TILES_PER_BOARD_COLUMN+DELTA+1), 2.0) )
var.ui_text_container.append(ui_current_player_turn)
#TODO find a better way to store instance
ui_next_player_hand = UserInterfaceText(ui_content['next_player_hand'][language_id], LINE_HEIGHT, False, ( (DELTA+TILES_PER_BOARD_COLUMN+DELTA+1), 6.0) )
var.ui_text_container.append(ui_next_player_hand )

#----- Window init -----

#Calculate window resolution
width=0
height=0
if cfg_resolution_auto :
	var.monitor_resolution = pygame.display.Info()
	width = var.monitor_resolution.current_w
	height = var.monitor_resolution.current_h
else :
	width = round (cfg_custom_window_height * (16/9.0) )
	height = cfg_custom_window_height

#Initialize game window
window = resizeWindow(width, height, cfg_fullscreen, cfg_resizable, cfg_resolution_auto, cfg_custom_window_height, cfg_double_buffer, cfg_hardware_accelerated)

#----- Create players -----

for player_name in players_names :
	start_hand = GroupOfSprites()
	pos_x = (TILES_PER_BOARD_COLUMN+4)
	pos_y = 3.5
	for i in range(number_of_letters_per_hand) :
		random_int = randint(0,len(var.bag_of_letters)-1)
		start_hand.add(Letter(var.bag_of_letters[random_int], pos_x, pos_y))
		del(var.bag_of_letters[random_int])
		pos_x = pos_x+1

	PLAYERS.append(Player(player_name,0,start_hand))

logPlayersInfo()

var.current_player = PLAYERS[0]
var.current_player.info()

#----- Create board game -----

#create background
board = Board("empty_background", 0, 0) #automatically stored in the corresponding layer
#create hand_holder
hand_holder = Hand_holder("hand_holder", 18.9, 3.4)#automatically stored in the corresponding layer

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

#create button END TURN
button_end_turn = Button("end_turn", 27, 3.5)

#first image
layers.background.draw(window)
layers.tiles.draw(window)
layers.hand_holder.draw(window)
layers.buttons.draw(window)

var.background_no_letter = window.copy()

var.current_player.hand.draw(window)
var.current_background_no_text = window.copy()

layers.background.drawText()
var.current_background = window.copy()

pygame.display.update()


#~~~~~~ MAIN  ~~~~~~

#----- Start -----

#Game is running
game_is_running = True

#Main loop
while game_is_running:

	fps_clock.tick(cfg_max_fps) #force the game to run slower than the specified max frames per second

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
		#TODO create a specific function ?
		elif ( event_type == pygame.VIDEORESIZE ) : #properly refresh the game window if a resize is detected
			
			#new width and height
			width = event.dict['size'][0]
			height = event.dict['size'][1]

			#create a fullscreen fully black to prevent later artefacts
			window = resizeWindow(var.monitor_resolution.current_w, var.monitor_resolution.current_h, cfg_fullscreen, cfg_resizable, cfg_resolution_auto, cfg_custom_window_height, cfg_double_buffer, cfg_hardware_accelerated)
			pygame.draw.rect(window, (0,0,0), ( (0,0), (var.monitor_resolution.current_w, var.monitor_resolution.current_h) ) )
			pygame.display.update()

			window = resizeWindow(width, height, cfg_fullscreen, cfg_resizable, cfg_resolution_auto, cfg_custom_window_height, cfg_double_buffer, cfg_hardware_accelerated)

			layers.background.draw(window)
			layers.tiles.draw(window)
			layers.hand_holder.draw(window)
			layers.buttons.draw(window)
			var.background_no_letter = window.copy()
			layers.letters_on_board.draw(window)
			layers.letters_just_played.draw(window)
			var.current_player.hand.draw(window)
			var.current_background_no_text = window.copy()
			layers.background.drawText()
			var.current_background = window.copy()
			layers.selected_letter.draw(window)
			
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

			timer = clic_clock.tick() #TODO to use ?

			#~~~~~~~~~~~ PRESS LEFT CLIC ~~~~~~~~~~~
			if ( event_type == pygame.MOUSEBUTTONDOWN ) :

				cursor_pos_x, cursor_pos_y = event.pos[0], event.pos[1]

				#------ SELECT A LETTER -------
				if var.current_action == 'SELECT_A_LETTER' :

					#------ CLIC ON A LETTER IN HAND ? -------
					for letter_from_hand in var.current_player.hand :

						if letter_from_hand.rect.collidepoint(cursor_pos_x, cursor_pos_y) == True :

							var.delta_pos_on_tile = ( cursor_pos_x - letter_from_hand.rect.x , cursor_pos_y - letter_from_hand.rect.y)
							layers.selected_letter.add(letter_from_hand)
							
							var.current_player.hand.remove(letter_from_hand)
							hand_state_index = var.current_player.hand_state.index(letter_from_hand.id)
							var.current_player.hand_state[hand_state_index] = 0
							var.current_player.hand.clear(window, var.background_no_letter)
							var.current_player.hand.draw(window)

							var.current_background = window.copy()
							layers.selected_letter.draw(window)

							pygame.display.update()

							var.current_action = "PLAY_A_LETTER"


					#------ CLIC ON A LETTER JUST PLAYED ? -------
					for letter_from_board in layers.letters_just_played :

						if letter_from_board.rect.collidepoint(cursor_pos_x, cursor_pos_y) == True :

							var.delta_pos_on_tile = ( cursor_pos_x - letter_from_board.rect.x , cursor_pos_y - letter_from_board.rect.y)

							tile_x_on_board = int(letter_from_board.pos_x - DELTA)
							tile_y_on_board = int(letter_from_board.pos_y - DELTA)

							var.current_board_state[tile_y_on_board][tile_x_on_board] = '?'

							layers.letters_just_played.remove(letter_from_board)
							layers.selected_letter.add(letter_from_board)

							layers.letters_just_played.clear(window, var.background_no_letter)

							var.current_background = window.copy()
							layers.letters_just_played.draw(window)
							layers.selected_letter.draw(window)

							pygame.display.update()

							var.current_action = "PLAY_A_LETTER"

					#------ CLIC ON END TURN -------
					if button_end_turn.rect.collidepoint(cursor_pos_x, cursor_pos_y) == True :
						#change button state
						button_end_turn.is_highlighted = False
						button_end_turn.push()
						layers.buttons.clear(window, var.current_background)
						layers.buttons.draw(window)

						var.current_background = window.copy()
						pygame.display.update()


				#------ PLAY A LETTER -------
				elif var.current_action == 'PLAY_A_LETTER' :

					#------ A LETTER IS SELECTED -------
					if len(layers.selected_letter) == 1 : 

						#------ CLIC ON THE HAND HOLDER ? -------
						for hand_holder in layers.hand_holder :

							if hand_holder.rect.collidepoint(cursor_pos_x, cursor_pos_y) == True :

								index_in_hand = indexInHandHolder(cursor_pos_x)

								#------ EMPTY SPOT ? -------
								if var.current_player.hand_state[index_in_hand] == 0 :

									selected_letter = layers.selected_letter.sprites()[0]
									
									delta_x, delta_y = DELTA + TILES_PER_BOARD_COLUMN + DELTA + 1, DELTA + 2
									selected_letter.moveAtTile( delta_x + index_in_hand, delta_y )
									var.current_player.hand_state[index_in_hand] = selected_letter.id

									var.current_player.hand.add(selected_letter)
									layers.selected_letter.remove(selected_letter)

									layers.selected_letter.clear(window, var.current_background)
									var.current_player.hand.draw(window)

									var.current_background = window.copy()	
									pygame.display.update()

									var.current_action = "SELECT_A_LETTER"


						#------ CLIC ON A TILE ON THE BOARD ? -------
						for tile in layers.tiles :

							if tile.rect.collidepoint(cursor_pos_x, cursor_pos_y) == True :

								tile_x_on_board = int( tile.pos_x - DELTA )
								tile_y_on_board = int( tile.pos_y - DELTA )

								#------ EMPTY TILE ? -------
								if var.current_board_state[tile_y_on_board][tile_x_on_board] == '?':

									selected_letter = layers.selected_letter.sprites()[0]

									selected_letter.moveAtTile( (tile_x_on_board + DELTA), (tile_y_on_board + DELTA) )
									var.current_board_state[tile_y_on_board][tile_x_on_board] = selected_letter.name

									layers.letters_just_played.add(selected_letter)								
									layers.selected_letter.remove(selected_letter)

									layers.selected_letter.clear(window, var.current_background)	
									layers.letters_just_played.draw(window)

									var.current_background = window.copy()	
									pygame.display.update()

									var.current_action = "SELECT_A_LETTER"


			#~~~~~~~~~~~ RELEASE LEFT CLIC ~~~~~~~~~~~
			elif ( event_type == pygame.MOUSEBUTTONUP ) :

				#------ SELECT A LETTER -------
				if var.current_action == 'SELECT_A_LETTER' :

					#------ RELEASE CLIC ON END TURN BUTTON -------
					if button_end_turn.rect.collidepoint(cursor_pos_x, cursor_pos_y) == True :
						button_end_turn.turnOnHighlighted()
						layers.buttons.clear(window, var.current_background)
						layers.buttons.draw(window)

						last_words_and_scores = calculatePoints(layers.letters_just_played)

						for association in last_words_and_scores :
							var.current_player.score +=  association[1]

						for letter in layers.letters_just_played :
							layers.letters_on_board.add(letter)

						layers.letters_just_played.empty()
						window.blit(var.current_background_no_text, (0,0))
						var.current_player.hand.clear(window, var.background_no_letter)

						#redraw letters
						index_hand = 0
						while len(var.bag_of_letters) > 0 and index_hand < number_of_letters_per_hand :
							if var.current_player.hand_state[index_hand] == 0 :
								random_int = randint(0,len(var.bag_of_letters)-1)
								drawn_letter = Letter(var.bag_of_letters[random_int], 0, 0)
								var.current_player.hand_state[index_hand] = drawn_letter.id
								delta_x, delta_y = DELTA + TILES_PER_BOARD_COLUMN + DELTA + 1, DELTA + 2
								drawn_letter.moveAtTile( delta_x + index_hand, delta_y )
								var.current_player.hand.add(drawn_letter)								
							index_hand += 1

						var.current_player = var.current_player.next()
						var.current_player.info()

						layers.letters_just_played.clear(window, var.current_background_no_text)
						layers.letters_on_board.draw(window)

						var.current_player.hand.draw(window)
						var.current_background_no_text = window.copy()
						layers.background.drawText()
						var.current_background = window.copy()

						pygame.display.update()

				#------ RELEASE CLIC AWAY FROM BUTTON -------
				for button in layers.buttons :
					if button.is_pushed :
						button.release() #release all pushed buttons
						if button.rect.collidepoint(cursor_pos_x, cursor_pos_y) :
							button.turnOnHighlighted()
						else :
							button.turnOffHighlighted()
						layers.buttons.clear(window, var.current_background)
						layers.buttons.draw(window)

						#TO DO - prevent artefact

						layers.selected_letter.clear(window, var.current_background)
						var.current_background = window.copy()
						layers.selected_letter.draw(window)

						pygame.display.update()


		#~~~~~~ MOUSE MOTION ~~~~~~	
		elif(event_type == pygame.MOUSEMOTION ):

			mouse_pos = pygame.mouse.get_pos()
			cursor_pos_x = mouse_pos[0]
			cursor_pos_y = mouse_pos[1]

			#change appearance of button
			if var.current_action == 'SELECT_A_LETTER' :
				buttons_changed = False
				for button in layers.buttons :
					if ( button.rect.collidepoint(cursor_pos_x, cursor_pos_y) == True ) and ( not button.is_highlighted ) and (not button.is_pushed ) :
						button.turnOnHighlighted()
						buttons_changed = True
					elif ( button.rect.collidepoint(cursor_pos_x, cursor_pos_y) == False ) and ( button.is_highlighted ):
						button_end_turn.turnOffHighlighted()
						buttons_changed = True
				if buttons_changed :
					layers.buttons.clear(window, var.current_background)
					layers.buttons.draw(window)

					pygame.display.update()

			if len(layers.selected_letter) == 1 :
				layers.selected_letter.sprites()[0].moveAtPixels(cursor_pos_x - var.delta_pos_on_tile[0], cursor_pos_y - var.delta_pos_on_tile[1])

				layers.selected_letter.clear(window, var.current_background)
				var.current_background = window.copy()
				layers.selected_letter.draw(window)

				pygame.display.update()
			

logging.info("Game has ended")
logging.info("")
logging.info("_________END OF LOG___________")

