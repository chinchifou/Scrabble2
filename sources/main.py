#~~~~~~~~~ MAIN ~~~~~~~~~


#~~~~~~ IMPORTS ~~~~~~

#Standard library imports
import pdb
import platform
import ctypes

from os import path
from os import makedirs

from math import floor
from random import randint, shuffle, choice

import logging


#Modules imports
import pygame


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

	def info(self, *args):
		for s in self.sprites():
			s.info(*args)

	def findByIndex(self, value):
		for l in self.sprites():
			if l.id == value :
				return l

	def findByName(self, value):
		result = []
		for s in self.sprites():
			if s.name == value :
				result.append(s)
		return result


#~~~~~~ GLOBAL VARIBLES ~~~~~~

#----- Constants -----
#define global scope for variables
global REFERENCE_TILE_SIZE, TILES_PER_LINE
#reference tile size for a 1920*1080 resolution
REFERENCE_TILE_SIZE = 60
#number of tiles on the board for each column and each row
TILES_PER_LINE = 15

global DELTA, UI_LEFT_LIMIT, UI_LEFT_INDENT, UI_TOP, UI_INTERLIGNE
#delta expressed in tiles from top left corner of the Window
DELTA = 1.5
#Left limit for text of the user interface
UI_LEFT_LIMIT = DELTA + TILES_PER_LINE + DELTA + 1.0
#Left limit with an identation in the user interface text
UI_LEFT_INDENT = UI_LEFT_LIMIT + 0.5
#Maximum for the top of the UI
UI_TOP = 1.5
#Size expressed in tile of the space between two consecutive line of text
UI_INTERLIGNE = 1.0

global PLAYERS, TURN
#all players
PLAYERS = []
# Turn number
TURN = 0

global CURSOR_IS_OPEN_HAND
CURSOR_IS_OPEN_HAND = False


global MUST_DISPLAY_POP_UP, FRAMES_BEFORE_POP_UP_DISAPPEAR, MOUSEBUTTONDOWN_DURING_POP_UP
# boolean to indicate wether to display pop_up or not
MUST_DISPLAY_POP_UP = False
# number of frames before the pop_up disappear
FRAMES_BEFORE_POP_UP_DISAPPEAR = 200
# remember that the mouse button has been press and wait for release
MOUSEBUTTONDOWN_DURING_POP_UP = False

#----- Changing a runtime -----
#class to store game variable
class GameVariable():
	def __init__(self):
		#----- Screen resolution and display -----
		self.monitor_resolution = 0
		self.window_width = 0
		self.window_height = 0
		self.window = 0.0

		self.tile_size = 0.0
		self.delta_pos_on_tile = [0.0, 0.0]

		self.hand_holder = []
		self.discard_holder = []

		#----- Letters and board -----
		self.number_of_letters_per_hand = 7

		self.bag_of_letters = []
		self.discard_holder_state = []
		self.current_board_state = [ ['?' for i in range(TILES_PER_LINE)] for j in range(TILES_PER_LINE) ]

		self.last_words_and_scores = {}
		self.predicted_score = 0		
		self.points_for_scrabble = 50

		#----- Current turn -----
		self.current_player = []

		self.current_action = 'SELECT_A_LETTER'
		self.discard_holder_displayed = False

		#----- Update display -----
		self.a_button_is_pushed = False

		self.background_empty = []
		self.background_empty_drawing = []

		self.current_background_no_text = []
		self.current_background = []



var = GameVariable()

class AllPaths():
	def __init__(self):

		self.path_log = path.abspath('../log/')
		if not path.exists(self.path_log):
			makedirs(self.path_log)

		self.path_icon = path.abspath('../materials/images/icon/')
		self.path_background = path.abspath('../materials/images/background/')

		self.path_buttons = path.abspath('../materials/images/assets/buttons/primary/') #changed later on
		self.path_buttons_french = path.abspath('../materials/images/assets/buttons/primary/french/')
		self.path_buttons_english = path.abspath('../materials/images/assets/buttons/primary/english/')
		self.path_buttons_menu = path.abspath('../materials/images/assets/buttons/side_menu/')

		self.path_letters = path.abspath('../materials/images/assets/letters/') #changed later on
		self.path_letters_french = path.abspath('../materials/images/assets/letters/french/')
		self.path_letters_english = path.abspath('../materials/images/assets/letters/english/')

		self.path_tiles = path.abspath('../materials/images/assets/tiles/')
		self.path_music = path.abspath('../materials/sounds/')

PATHS = AllPaths()

#class used to print error messages in console and log file
class ErrorPrinter():

	def not_enough_letters(self, nb_letters, nb_expected):
		logging.error('! ! ! . . . . . . . . ! ! !')
		logging.error('INITIAL SETTINGS ERROR : not enough letters at game start.')
		logging.error('%s letters available but a minium of %s letters is required.', nb_letters, nb_expected)
		logging.error('Possible solutions :')
		logging.error('  1. add more letters')
		logging.error('  2. reduce number of letters authorized per player')
		logging.error('  3. reduce the number of players')
		logging.error('! ! ! . . . . . . . . ! ! !')
		logging.error('')

		print('INITIAL SETTINGS ERROR : not enough letters at game start.')
		print('%s letters available but a minium of %s letters is required.' %(nb_letters, nb_expected))
		print('Possible solutions :')
		print('  1. add more letters')
		print('  2. reduce number of letters authorized per player')
		print('  3. reduce the number of players')
		print('')
	"""
	def typeUndefined(self, object) :
		logging.error('! ! ! . . . . . . . . ! ! !')
		logging.error('TYPE UNDEFINED : Object "%s" does not have a type.', object.name)
		logging.error('To fix this error :')
		logging.error('  - give your component a "type" attribute in its class definition')
		logging.error('! ! ! . . . . . . . . ! ! !')
		logging.error('')

		print('TYPE UNDEFINED : Object "%s" does not have a type.', object.name)
		print('To fix this error :')
		print('  - give your component a "type" attribute in its class definition')
		print('')
	"""

ERROR = ErrorPrinter()


#class used to print warning messages in console and log file
class WarningPrinter():
	pass

WARNING = WarningPrinter()
	

#class to store the different colors used in the game
class ColorPannel():
	def __init__(self):
		self.BLACK = (0,0,0)
		self.GREY_LIGHT = (143,144,138)
		self.GREY_DEEP = (39,40,34)

		self.BLUE_DEEP = (21, 109, 255)
		self.BLUE_LIGHT = (113, 201, 249)
		self.BLUE_SUPER_LIGHT = ( 124, 194, 191 )

		self.RED_DEEP = (239, 69, 86)
		self.RED_LIGHT = (249, 179, 162)

		self.GREEN = (0, 155, 151)

		self.WHITE= (255, 255, 255)

COLOR = ColorPannel()

#class used to store sounds
class Sounds():
	def __init__(self):
		self.victory = pygame.mixer.Sound(path.join(PATHS.path_music, 'tf2_achievement_unlocked_sound.ogg'))
		self.scrabble = pygame.mixer.Sound(path.join(PATHS.path_music, 'victory_fanfare.ogg'))

#class used to store line heigh used in the game
class LineHeights():
	def __init__(self):
		#size of the ui text used for title expressed in tile
		self.TITLE = 0.9
		#size of the ui text used for subtitle expressed in tile
		self.SUBTITLE = 0.7
		#size of the common ui text expressed in tile
		self.NORMAL = 0.6		
		#size for small pop up
		self.POP_UP = 0.5


LINE_HEIGHT = LineHeights()


#class to create rendering layers used for display
class Layer():
	def __init__(self):
		self.background = GroupOfSprites()		
		self.hand_holder = GroupOfSprites()

		self.tiles = GroupOfSprites()

		self.letters_on_board = GroupOfSprites()
		self.letters_just_played = GroupOfSprites()
		self.selected_letter = GroupOfSprites()

		self.buttons_on_screen = GroupOfSprites()

		self.dark_filter = GroupOfSprites()
		self.pop_up_window = GroupOfSprites()
		self.pop_up_score = GroupOfSprites()

		self.mask_text = GroupOfSprites()

		self.pop_up = GroupOfSprites()

		self.all = GroupOfSprites()

layers = Layer()

#class used to create interface text
class UIText():

	all = []

	def __init__(self, text, line_height, bold, pos_in_tiles):
		self.text = text
		self.line_height = line_height

		self.bold = int(bold)	

		self.font = pygame.font.SysFont("Calibri", floor(self.line_height*var.tile_size))
		self.font.set_bold(self.bold)

		self.pos_x, self.pos_y = pos_in_tiles[0], pos_in_tiles[1]
		self.pos_x_pix, self.pos_y_pix = pixels(self.pos_x, self.pos_y)

		self.width, self.height = tiles_tup(self.font.size(self.text))
		self.bottom_tiles = self.pos_y + self.line_height

		UIText.all.append(self)


	def resize(self):
		self.font = pygame.font.SysFont("Calibri", floor(self.line_height*var.tile_size))

		self.font.set_bold(self.bold)
		self.width, self.height = tiles_tup(self.font.size(self.text))
		self.bottom_tiles = self.pos_y + self.line_height

		self.pos_x_pix, self.pos_y_pix = pixels(self.pos_x, self.pos_y)


	def moveAtPixels(self, pos_x_pix, pos_y_pix):
		self.pos_x_pix, self.pos_y_pix = pos_x_pix, pos_y_pix
		self.pos_x, self.pos_y = tiles(self.pos_x_pix, self.pos_y_pix, to_round=True)


	def info(self):
		logging.debug("UI Text")
		logging.debug("Text : %s", self.text)
		logging.debug("Line heigh : %s", str(self.line_height))
		logging.debug("Bold : %s", str(self.bold))
		logging.debug("Font : %s", str(self.font.size))
		logging.debug("Position in tiles : %s, %s", self.pos_x, self.pos_y)
		logging.debug("Position in pixels : %s, %s", self.pos_x_pix, self.pos_y_pix)


#class used to diaply text pop up to the user
class UserInterFaceToolTip(UIText):

	def __init__(self, text, line_heigh, bold, pos_in_tiles, text_color, background_color):
		UIText.__init__(self, text, line_heigh, bold, pos_in_tiles)
		self.text_color = text_color
		self.background_color = background_color

	def drawAt(self, pixels_pos_x, pixels_pos_y):

		self.moveAtPixels(pixels_pos_x, pixels_pos_y)
		text = self.font.render(self.text, 1, self.text_color, self.background_color )
		var.window.blit( text, (self.pos_x_pix, self.pos_y_pix) )


#class storing userface interface text and displaying them
class UITextPrinter():

	def __init__(self, ui_content):

		#UI text init
		self.current_player_turn = UIText(ui_content['current_player_turn'][language_id], LINE_HEIGHT.TITLE, True, ( UI_LEFT_LIMIT, UI_TOP) ) #fix value

		self.next_player_hand_header = UIText(ui_content['next_player_hand'][language_id], LINE_HEIGHT.NORMAL, True, ( UI_LEFT_LIMIT, self.current_player_turn.bottom_tiles+0.5*UI_INTERLIGNE+1.2+2*UI_INTERLIGNE) )
		self.next_player_hand = UIText("", LINE_HEIGHT.NORMAL, False, ( UI_LEFT_INDENT, self.next_player_hand_header.bottom_tiles+0.25*UI_INTERLIGNE) )

		if display_next_player_hand :
			self.scores = UIText(ui_content['scores'][language_id], LINE_HEIGHT.NORMAL, True, ( UI_LEFT_LIMIT, self.next_player_hand.bottom_tiles+UI_INTERLIGNE) )
		else :
			self.scores = UIText(ui_content['scores'][language_id], LINE_HEIGHT.NORMAL, True, ( UI_LEFT_LIMIT, self.current_player_turn.bottom_tiles+1+UI_INTERLIGNE) )
		self.player_score = UIText(ui_content['player_score'][language_id], LINE_HEIGHT.NORMAL, False, ( UI_LEFT_INDENT, self.scores.bottom_tiles+0.25*UI_INTERLIGNE) )

		self.nothing_played = UIText( ui_content['nothing_played'][language_id], LINE_HEIGHT.NORMAL, False, (UI_LEFT_LIMIT, self.scores.bottom_tiles+(0.8*len(players_names))+UI_INTERLIGNE) )
		self.previous_turn_summary = UIText( ui_content['previous_turn_summary'][language_id], LINE_HEIGHT.NORMAL, True, ( UI_LEFT_LIMIT, self.scores.bottom_tiles+(0.8*len(players_names))+UI_INTERLIGNE ) )
		self.word_and_points = UIText ( ui_content['word_and_points'][language_id], LINE_HEIGHT.NORMAL, False, ( UI_LEFT_INDENT, self.previous_turn_summary.bottom_tiles+0.5*UI_INTERLIGNE )  )		
		self.scrabble_obtained = UIText(ui_content['scrabble_obtained'][language_id], LINE_HEIGHT.NORMAL, False, (UI_LEFT_INDENT, self.previous_turn_summary.bottom_tiles+0.5*UI_INTERLIGNE) )
		
		self.remaining_letters = UIText( ui_content['remaining_letters'][language_id], LINE_HEIGHT.NORMAL, False, (UI_LEFT_LIMIT, self.nothing_played.bottom_tiles+0.5*UI_INTERLIGNE) )
		self.remaining_letter = UIText( ui_content['remaining_letter'][language_id], LINE_HEIGHT.NORMAL, False, (UI_LEFT_LIMIT, self.nothing_played.bottom_tiles+0.5*UI_INTERLIGNE) )
		self.no_remaining_letter = UIText( ui_content['no_remaining_letter'][language_id], LINE_HEIGHT.NORMAL, False, (UI_LEFT_LIMIT, self.nothing_played.bottom_tiles+0.5*UI_INTERLIGNE) )
		
		#hardcoded help pop-up
		self.id_tile_pop_up = 0
		self.pop_up_displayed = False

		self.double_letter = UserInterFaceToolTip( ui_content['double_letter'][language_id], LINE_HEIGHT.POP_UP, False, (0, 0), COLOR.BLACK, COLOR.BLUE_LIGHT )
		self.triple_letter = UserInterFaceToolTip( ui_content['triple_letter'][language_id], LINE_HEIGHT.POP_UP, False, (0, 0), COLOR.BLACK, COLOR.BLUE_DEEP )

		self.double_word = UserInterFaceToolTip( ui_content['double_word'][language_id], LINE_HEIGHT.POP_UP, False, (0, 0), COLOR.BLACK, COLOR.RED_LIGHT )
		self.triple_word = UserInterFaceToolTip( ui_content['triple_word'][language_id], LINE_HEIGHT.POP_UP, False, (0, 0), COLOR.BLACK, COLOR.RED_DEEP )

#Draw UI text
	def drawText(self):

		#Current player hand
		text = self.current_player_turn.font.render( self.current_player_turn.text.replace('<CURRENT_PLAYER>',var.current_player.name), 1, COLOR.GREY_LIGHT )
		var.window.blit(text, (self.current_player_turn.pos_x_pix, self.current_player_turn.pos_y_pix))

		#display next player hand
		if display_next_player_hand :
			#Next player hand header
			text = self.next_player_hand_header.font.render( self.next_player_hand_header.text.replace('<NEXT_PLAYER>',var.current_player.next().name), 1, COLOR.GREY_LIGHT )
			var.window.blit(text, (self.next_player_hand_header.pos_x_pix, self.next_player_hand_header.pos_y_pix))

			#Next player hand content
			str_hand = ""
			for index in var.current_player.next().hand_state :
				letter_to_display = var.current_player.next().hand.findByIndex(index) 
				if letter_to_display == None :
					str_hand += ' '
				else :
					str_hand += str ( letter_to_display.name ) + "  " 

			text = self.next_player_hand.font.render( str_hand , 1, COLOR.GREY_LIGHT )
			var.window.blit(text, (self.next_player_hand.pos_x_pix, self.next_player_hand.pos_y_pix))

		#Scores header
		text = self.scores.font.render( self.scores.text, 1, COLOR.GREY_LIGHT )
		var.window.blit(text, (self.scores.pos_x_pix, self.scores.pos_y_pix))

		#score of each player
		pos_y_delta = 0
		for player in PLAYERS :
			if ( player == var.current_player ) :
				self.player_score.font.set_bold(1)
				if var.predicted_score == 0 : #move does not give points
					text = self.player_score.font.render( self.player_score.text.replace('_',' ').replace('<PLAYER>', player.name).replace('<SCORE>', str(player.score)), 1, COLOR.BLUE_SUPER_LIGHT )
				else :
					text = self.player_score.font.render( self.player_score.text.replace('_',' ').replace('<PLAYER>', player.name).replace('<SCORE>', str(player.score) + " (+" +str(var.predicted_score)) + ")" , 1, COLOR.BLUE_SUPER_LIGHT )
				self.player_score.font.set_bold(0)
				var.window.blit(text, (self.player_score.pos_x_pix, self.player_score.pos_y_pix+int(pos_y_delta*var.tile_size) ) )
			else :
				text = self.player_score.font.render( self.player_score.text.replace('_',' ').replace('<PLAYER>', player.name).replace('<SCORE>', str(player.score)), 1, COLOR.GREY_LIGHT )
				var.window.blit(text, (self.player_score.pos_x_pix, self.player_score.pos_y_pix+int(pos_y_delta*var.tile_size) ) )
			pos_y_delta += 0.8

		#previous turn summary
		if len(var.last_words_and_scores) > 0 : #something played
			#header
			text = self.previous_turn_summary.font.render( self.previous_turn_summary.text.replace('<PREVIOUS_PLAYER>',var.current_player.previous().name), 1, COLOR.GREY_LIGHT )
			var.window.blit(text, (self.previous_turn_summary.pos_x_pix, self.previous_turn_summary.pos_y_pix))

			pos_y_delta = 0
			for association in var.last_words_and_scores :
				if association[0] == "!! SCRABBLE !!" :
					text = self.scrabble_obtained.font.render( self.scrabble_obtained.text.replace('<PREVIOUS_PLAYER>',var.current_player.previous().name).replace('<SCRABBLE_POINTS>', str(var.points_for_scrabble)), 1, COLOR.RED_DEEP )
					var.window.blit(text, (self.scrabble_obtained.pos_x_pix, self.scrabble_obtained.pos_y_pix+int(pos_y_delta*var.tile_size)))
				else :		
					text = self.word_and_points.font.render( self.word_and_points.text.replace('<WORD>',association[0]).replace('<POINTS>', str(association[1])), 1, COLOR.GREY_LIGHT )
					var.window.blit(text, (self.word_and_points.pos_x_pix, self.word_and_points.pos_y_pix+int(pos_y_delta*var.tile_size)))
				pos_y_delta += 0.8

		else : #nothing played
			text = self.nothing_played.font.render( self.nothing_played.text.replace('<PREVIOUS_PLAYER>',var.current_player.previous().name), 1, COLOR.GREY_LIGHT )
			var.window.blit(text, (self.nothing_played.pos_x_pix, self.nothing_played.pos_y_pix) )

		#Remaining letters
		if len(var.bag_of_letters) == 0 :
			text = self.no_remaining_letter.font.render( self.no_remaining_letter.text, 1, COLOR.GREY_LIGHT )
		elif len(var.bag_of_letters) == 1 :
			text = self.remaining_letter.font.render( self.remaining_letter.text, 1, COLOR.GREY_LIGHT )		
		else :
			text = self.remaining_letters.font.render( self.remaining_letters.text.replace( '<LETTERS_REMAINING>', str(len(var.bag_of_letters)) ), 1, COLOR.GREY_LIGHT )

		if len(var.last_words_and_scores) > 0 : #something played
			var.window.blit(text, (self.remaining_letter.pos_x_pix, self.word_and_points.pos_y_pix+ int((pos_y_delta+UI_INTERLIGNE)*var.tile_size) ) )
		else : #nothing played
			var.window.blit(text, (self.remaining_letter.pos_x_pix, self.nothing_played.pos_y_pix+ int((0.8+UI_INTERLIGNE)*var.tile_size) ) )


	def drawHelpPopPup(self, tile, pixel_pos_x, pixel_pos_y):
		if tile.name == 'double_letter' :
			self.double_letter.drawAt(pixel_pos_x, pixel_pos_y)
		elif tile.name == 'triple_letter':
			self.triple_letter.drawAt(pixel_pos_x, pixel_pos_y)
		elif tile.name == 'double_word'or tile.name == 'start':
			self.double_word.drawAt(pixel_pos_x, pixel_pos_y)
		elif tile.name == 'triple_word':
			self.triple_word.drawAt(pixel_pos_x, pixel_pos_y)



def createPopUp(ar_texts, text_centered=True, LINE_HEIGHT=0.7, position=(0,0), bounds=(32, 18), margin_ratio=(1.0,1.0), interligne_ratio=1.5, time=4):

	# ___ Init ___
	# transform string to list of strings
	if isinstance(ar_texts, str) :
		ar_texts = ar_texts.split('\n')

	my_line_height = LINE_HEIGHT

	to_move_in_the_center = ( position == (0,0) )
	left_margin, top_margin = my_line_height*margin_ratio[0], my_line_height*margin_ratio[1]
	window_pos_x, window_pos_y = position[0], position[1]

	nb_lignes = len(ar_texts)
	interligne = interligne_ratio * my_line_height - my_line_height

	global FRAMES_BEFORE_POP_UP_DISAPPEAR
	FRAMES_BEFORE_POP_UP_DISAPPEAR = int(time * 60)


	# ___ Prevent to go out of the boundaries ___
	max_nb_letters = 0
	longest_word = ""
	for text in ar_texts :
		if len(text) > max_nb_letters :
			max_nb_letters = len(text)
			longest_word = text

	test_font = pygame.font.SysFont("Calibri", floor(my_line_height*var.tile_size))
	initial_max_width = test_font.size(longest_word)[0] / var.tile_size
	initial_total_height = my_line_height*nb_lignes + interligne*(nb_lignes - 1) 

	correction_ratio_width, correction_ratio_height = 1.0, 1.0

	if 2*left_margin + initial_max_width > bounds[0] :
		correction_ratio_width = bounds[0] / ( 2*left_margin + initial_max_width )

	if ( 2*top_margin + initial_total_height ) > bounds[1] :
		correction_ratio_height = bounds[1] / ( 2*top_margin + initial_total_height )

	correction_ratio = min( correction_ratio_width, correction_ratio_height )

	if correction_ratio < 1.0 :
		my_line_height = my_line_height * correction_ratio
		interligne = interligne_ratio * my_line_height
		left_margin, top_margin = my_line_height*margin_ratio[0], my_line_height*margin_ratio[1]


	new_total_height = 2*top_margin + my_line_height*nb_lignes + interligne*(nb_lignes - 1)

	test_font = pygame.font.SysFont("Calibri", floor(my_line_height*var.tile_size)) 
	new_max_width = test_font.size(longest_word)[0] / var.tile_size


	# ___ Window width and height ___ (rounded for for better design)
	#TODO to improve
	window_width =  ( 2*left_margin + new_max_width )
	window_height =  ( new_total_height )

	# ___ Move to the center of the center of the screen ___
	if to_move_in_the_center :
		window_pos_x =  ( (bounds[0] - window_width) / 2.0 ) 
		window_pos_y =  ( (bounds[1] - window_height) / 2.0 )

	# ___ create pop_up background surface ___
	pop_up_surface = pygame.Surface( pixels(window_width , window_height) )
	pop_up_surface.fill(COLOR.GREY_DEEP)
	pygame.draw.rect(pop_up_surface, COLOR.GREY_LIGHT, pygame.Rect( (0,0), pixels(window_width, window_height) ), 3)


	# ___ Create UI text objects ___
	ui_texts = []
	tmp_pos_x, tmp_pos_y = left_margin, top_margin
	for text in ar_texts :

		if text_centered :
			required_width = test_font.size(text)[0] / var.tile_size
			padding = ( new_max_width - required_width ) / 2.0
		else :
			padding = 0

		ui_texts.append( UIText( text, my_line_height, False, (tmp_pos_x+padding, tmp_pos_y) ) )
		tmp_pos_y += my_line_height + interligne


	# ___ Blit text to pop up ___
	for ui_text in ui_texts :
		pop_up_surface.blit( ui_text.font.render(ui_text.text, 1, COLOR.WHITE), pixels(ui_text.pos_x, ui_text.pos_y) )


	#create complete pop_up
	return UI_Surface('pop_up', window_pos_x, window_pos_y, pop_up_surface)


def displayPopUp(ar_texts, text_centered=True, LINE_HEIGHT=0.7, position=(0,0), bounds=(32, 18), margin_ratio=(1.0,1.0), interligne_ratio=1.5, time=4) :

	pygame.mouse.set_cursor(*arrow) 

	#Create pop up
	layers.pop_up.add( createPopUp(ar_texts, text_centered, LINE_HEIGHT, position, bounds, margin_ratio, interligne_ratio, time)  )
	
	# snapshot of before pop_up
	layers.buttons_on_screen.draw(var.window)
	snapshot = var.window.copy()
	
	#display pop_up
	layers.dark_filter.draw(var.window)
	layers.pop_up.draw(var.window)
	pygame.display.update()

	global MUST_DISPLAY_POP_UP
	MUST_DISPLAY_POP_UP = True
	#prepare exit image (displayed when removing pop up)
	var.window.blit(snapshot, (0,0))


#~~~~~~ CONVERTION ~~~~~~

#----- convert bewten tiles numbers and pixels -----
def tiles(value_in_pixels1, value_in_pixels2, to_round=False) :
	if to_round :
		return ( int(round( value_in_pixels1/float(var.tile_size) )), int(round( value_in_pixels2/float(var.tile_size) )) )
	else :
		return ( value_in_pixels1/float(var.tile_size), value_in_pixels2/float(var.tile_size) )

def tiles_tup(tuple, to_round=False):
	return tiles(tuple[0], tuple[1], to_round=to_round)

def in_reference_tiles(value_in_pixels1, value_in_pixels2) :
	return ( round( value_in_pixels1/float(REFERENCE_TILE_SIZE) ), round( value_in_pixels2/float(REFERENCE_TILE_SIZE) ) )

def tiles1(value_in_pixels, to_round=False) :
	if to_round :
		return int(round( value_in_pixels/float(var.tile_size) ))
	else :
		return value_in_pixels/float(var.tile_size)


def pixels(value1_in_tiles, value2_in_tiles, to_round=False) :
	if to_round :
		return ( int(round(value1_in_tiles*var.tile_size)), int(round(value2_in_tiles*var.tile_size)) )
	else :
		return ( int(value1_in_tiles*var.tile_size), int(value2_in_tiles*var.tile_size) )

def solo_pixels(value_in_tiles) :
	return ( int(value_in_tiles*var.tile_size) )



#~~~~~~ GAME CLASSES ~~~~~~


#----- ResizableSprite -----
#add native capacity to be resized
class ResizableSprite(pygame.sprite.Sprite):

	#class attributes to count number of instances
	nb_created_instances = 0

	#received coordinates are expresed in tiles
	def __init__(self, name, pos_x, pos_y, tmp_path, transparent=False):

		#super class constructor
		pygame.sprite.Sprite.__init__(self, self.containers) #self.containers need to have a default container

		#unique id
		ResizableSprite.nb_created_instances += 1
		self.id = ResizableSprite.nb_created_instances

		self.name, self.pos_x, self.pos_y, self.path, self.transparent = name, pos_x, pos_y, tmp_path, transparent
		self.masks = {}

		#load image
		if self.path != None :
			if self.transparent :
				self.image = loadTransparentImage(path.join(self.path, self.name.replace('*','joker')+'.png'))
			else :
				self.image = loadImage(path.join(self.path, self.name+'.png'))

		#auto detect width and height
		if not ( hasattr(self, 'width') and hasattr(self, 'height') ) :
			self.width, self.height = in_reference_tiles(self.image.get_width(), self.image.get_height())

		#resize image
		self.image = pygame.transform.smoothscale(self.image, pixels(self.width, self.height, to_round=True ) )
		#set area to be displayed
		self.rect = pygame.Rect( pixels(self.pos_x, self.pos_y), pixels(self.width, self.height) )
		#mask for collision
		if self.transparent :
			self.mask = self.getMask(self.name+'.png')


	def resize(self):

		#reload image
		if self.path != None :
			if self.transparent :
				self.image = loadTransparentImage(path.join(self.path, self.name.replace('*','joker')+'.png'))
			else :
				self.image = loadImage(path.join(self.path, self.name+'.png'))

		#resize image
		self.image = pygame.transform.smoothscale(self.image, pixels(self.width, self.height, to_round=True) )
		#set area to be displayed
		self.rect = pygame.Rect( pixels(self.pos_x, self.pos_y), pixels(self.width, self.height) )
		#mask for collision
		if self.transparent :
			self.masks = {}
			self.mask = self.getMask(self.name+'.png')



	#move a Sprite at a given position expressed in tiles
	def moveAtTile(self, pos_x, pos_y) :

		self.rect.x, self.rect.y = pixels(pos_x, pos_y)
		self.pos_x, self.pos_y  = pos_x, pos_y


	#move a Sprite at a given position expressed in pixels
	def moveAtPixels(self, pos_x, pos_y) :

		self.rect.x, self.rect.y = pos_x, pos_y
		self.pos_x, self.pos_y  = tiles(pos_x, pos_y, to_round=True)


	def collide(self, x_pix, y_pix) :

		if self.transparent :
			collide = False
			if self.rect.collidepoint(x_pix, y_pix) :
				if self.really_collide(x_pix, y_pix) :
					collide = True
			return collide
		else :
			return self.rect.collidepoint(x_pix, y_pix)


	def really_collide(self, x_pix, y_pix) :

		x_pix_offset = x_pix - self.rect.left
		y_pix_offset = y_pix - self.rect.top

		return bool( self.mask.get_at( (x_pix_offset, y_pix_offset) ) )


	def getMask(self, name) :

		if hasattr(self, 'is_an_emoticom') :
			name = 'common'

		if (name in self.masks.keys()) :
			return self.masks[name]
		else :
			mask = pygame.mask.Mask((0,0))
			if self.transparent :
				mask = pygame.mask.from_surface(self.image)
				self.masks[name] = mask
			else :
				mask = pygame.mask.from_surface(self.image)
				mask.fill()
				self.masks[name] = mask
			return mask


	def info(self) :
		logging.debug("Sprite info :")
		logging.debug("id : %s", self.id)
		logging.debug("name : %s", self.name)
		logging.debug("at position : %s, %s", self.pos_x, self.pos_y)
		logging.debug("pixel position is : %s, %s", self.rect.x, self.rect.y)
		logging.debug("width : %s / height : %s", self.width, self.height)
		logging.debug("pixel width : %s /  pixel height : %s", self.rect.width, self.rect.height)
		logging.debug("mask width : %s /  mask height : %s", self.mask.get_size()[0], self.mask.get_size()[1])
		logging.debug("")


# ___ SUBCALSSES ___
#----- UI Surface -----
class UI_Surface(ResizableSprite):
	def __init__(self, name, pos_x, pos_y, surface):

		self.image = surface

		self.width, self.height = tiles(self.image.get_width(), self.image.get_height())

		ResizableSprite.__init__(self, name, pos_x, pos_y, None)

#----- UI Image -----
class UI_Image(ResizableSprite):
	def __init__(self, name, tmp_path, pos_x, pos_y, width=None, height=None, tmp_transparent = False):

		if ( width==None and height==None ) :
			self.image = loadImage(path.join(tmp_path, name+'.png'))
			self.width, self.height = in_reference_tiles(self.image.get_width(), self.image.get_height())
		else :
			self.width, self.height = width, height			

		self.name = name

		ResizableSprite.__init__(self, name, pos_x, pos_y, tmp_path, transparent=tmp_transparent)


# ___ SPRITES ___ 

#----- Board -----
class Board(ResizableSprite):
	def __init__(self, name, pos_x, pos_y):

		self.width, self.height = 32, 18

		ResizableSprite.__init__(self, name, pos_x, pos_y, PATHS.path_background)


#----- Hand holder -----
class Hand_holder(ResizableSprite):
	def __init__(self, name, pos_x, pos_y, max_nb_letters):

		self.width, self.height = 0.2 + var.number_of_letters_per_hand, 1.2
		self.max_nb_letters = max_nb_letters
		
		ResizableSprite.__init__(self, name, pos_x, pos_y, PATHS.path_background)

	def indexAtPos(self, cursor_pos_x):

		index_in_hand = ( int( floor( (cursor_pos_x - self.rect.left) / float(var.tile_size) ) ) )
		if index_in_hand+1 > self.max_nb_letters :
			index_in_hand -= 1

		return index_in_hand


#----- Tiles -----
class Tile(ResizableSprite):
	def __init__(self, name, pos_x, pos_y):

		ResizableSprite.__init__(self, name, pos_x, pos_y, PATHS.path_tiles)


#----- Buttons -----
class Button(ResizableSprite):
	def __init__(self, name, pos_x, pos_y, is_a_checkbox=False, is_an_emoticom=False):

		self.is_highlighted = False
		self.is_pushed = False
		self.is_enabled = True
		self.is_a_checkbox = is_a_checkbox
		self.is_an_emoticom = is_an_emoticom

		ResizableSprite.__init__(self, name, pos_x, pos_y, PATHS.path_buttons, transparent=True)

	def resize(self):
		ResizableSprite.resize(self)
		if self.is_enabled :
			self.enable()
		else :
			self.disable()

	def turnOnHighlighted(self):
		self.image = loadTransparentImage(path.join(self.path, self.name+'_highlighted.png'))
		self.image = pygame.transform.smoothscale(self.image, pixels(self.width, self.height))
		self.mask = self.getMask(self.name+'_highlighted.png')
		self.is_highlighted = True

	def turnOffHighlighted(self):
		self.image = loadTransparentImage(path.join(self.path, self.name+'.png'))
		self.image = pygame.transform.smoothscale(self.image, pixels(self.width, self.height))
		self.mask = self.getMask(self.name+'.png')
		self.is_highlighted = False

	def push(self):
		self.image = loadTransparentImage(path.join(self.path, self.name+'_pushed.png'))
		self.image = pygame.transform.smoothscale(self.image, pixels(self.width, self.height))
		self.mask = self.getMask(self.name+'_pushed.png')
		self.is_pushed = True	

	def release(self):
		self.image = loadTransparentImage(path.join(self.path, self.name+'.png'))
		self.image = pygame.transform.smoothscale(self.image, pixels(self.width, self.height))
		self.mask = self.getMask(self.name+'.png')
		self.is_pushed = False	

	def enable(self):
		self.image = loadTransparentImage(path.join(self.path, self.name+'.png'))
		self.image = pygame.transform.smoothscale(self.image, pixels(self.width, self.height))
		self.mask = self.getMask(self.name+'.png')
		self.is_enabled = True

	def disable(self):
		self.image = loadTransparentImage(path.join(self.path, self.name+'_disabled.png'))
		self.image = pygame.transform.smoothscale(self.image, pixels(self.width, self.height))
		self.mask = self.getMask(self.name+'_disabled.png')
		self.is_enabled = False


class Checkbox(Button):
	def __init__(self, name, pos_x, pos_y):
		Button.__init__(self, name, pos_x, pos_y, is_a_checkbox=True)
		self.is_filled = False

	def fill(self):
		self.name = 'filled_'+self.name
		self.is_filled = True
		self.turnOnHighlighted() #TODO - bad

	def empty(self):
		self.name = self.name.replace("filled_", "")
		self.is_filled = False
		self.turnOnHighlighted()


class Emoticom(Button):
	def __init__(self, name, pos_x, pos_y):
		self.width, self.height = 2.5, 2.5
		self.name = "selected_"+ name
		Button.__init__(self, self.name, pos_x, pos_y, is_an_emoticom=True)
		self.is_selected = True

	def select(self):
		self.name = self.name.replace("un", "")
		self.image = loadTransparentImage(path.join(self.path, self.name+'.png'))
		self.image = pygame.transform.smoothscale(self.image, pixels(self.width, self.height))
		self.mask = self.getMask(self.name+'.png')
		self.is_selected = True
		#self.turnOnHighlighted()	

	def unselect(self):
		self.name = 'un'+self.name
		self.image = loadTransparentImage(path.join(self.path, self.name+'.png'))
		self.image = pygame.transform.smoothscale(self.image, pixels(self.width, self.height))
		self.mask = self.getMask(self.name+'.png')
		self.is_selected = False
		#self.turnOnHighlighted()


#----- Letter -----
class Letter(ResizableSprite):
	def __init__(self, name, pos_x, pos_y):

		self.points = POINTS_FOR[name]

		ResizableSprite.__init__(self, name, pos_x, pos_y, PATHS.path_letters, transparent=True)


	def canMove(self, direction):

		my_index = var.hand_holder.indexAtPos(self.rect.centerx)

		wanted_index = my_index+direction
		wanted_index = max(0,wanted_index)
		wanted_index = wanted_index%( len(var.current_player.hand_state) )

		wanted_pos_id = var.current_player.hand_state[wanted_index]

		return ( wanted_pos_id == 0 )		


#----- Define sprites behavior -----

#set default groups
Board.containers = layers.all, layers.background
Hand_holder.containers = layers.all, layers.hand_holder
Tile.containers = layers.all, layers.tiles

Button.containers = layers.all
Letter.containers = layers.all
UI_Surface.containers = layers.all
UI_Image.containers = layers.all

#----- Other classes -----

#----- Player -----
class Player :

	def __init__(self, name, score, hand, hand_state) :
		self.name = name
		self.score = score
		self.hand = hand
		self.id = len(PLAYERS)
		self.hand_state = hand_state

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

	def previous(self) :
		if ( self.id - 1 >= 0 ) :
			return PLAYERS[(self.id - 1)]
		else :
			return PLAYERS[ (len(PLAYERS)-1) ]

#~~~~~~ FUNCTIONS ~~~~~~

#----- Game window creation and resize -----
def resizeWindow(width, height, fullscreen, resizable, resolution_auto, custom_window_height, double_buffer, hardware_accelerated) :
	
	logging.debug("WINDOW Creation")
	updateTileSize(width,height)

	for ui_text in UIText.all :
		ui_text.resize()

	layers.all.resize()

	width = int (1920 / REFERENCE_TILE_SIZE ) * var.tile_size
	height = int (1080 / REFERENCE_TILE_SIZE ) * var.tile_size

	var.window_width = width
	var.window_height = height

	logging.debug("Size of game window is : %s * %s", width, height)
	logging.debug("")


	if fullscreen :
		if double_buffer :
			if hardware_accelerated :
				var.window = pygame.display.set_mode( (width, height), pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE)
			else :
				var.window = pygame.display.set_mode( (width, height), pygame.FULLSCREEN | pygame.DOUBLEBUF)
		else:
			var.window = pygame.display.set_mode( (width, height), pygame.FULLSCREEN)
	else :
		if resizable :
			if double_buffer :
				if hardware_accelerated :
					var.window = pygame.display.set_mode( (width, height), pygame.RESIZABLE | pygame.DOUBLEBUF | pygame.HWSURFACE)
				else :
					var.window = pygame.display.set_mode( (width, height), pygame.RESIZABLE | pygame.DOUBLEBUF)
			else:
				var.window = pygame.display.set_mode( (width, height), pygame.RESIZABLE)
		else:
			var.window = pygame.display.set_mode( (width, height))

	pygame.event.clear(pygame.VIDEORESIZE) #remove the event pygame.VIDEORESIZE from the queue

	return var.window

#----- Resize window but do not resize Sprites -----
def resizeWindowNoSpritesUpdate(width, height, fullscreen, resizable, resolution_auto, custom_window_height, double_buffer, hardware_accelerated) :
	if fullscreen :
		if double_buffer :
			if hardware_accelerated :
				var.window = pygame.display.set_mode( (width, height), pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE)
			else :
				var.window = pygame.display.set_mode( (width, height), pygame.FULLSCREEN | pygame.DOUBLEBUF)
		else:
			var.window = pygame.display.set_mode( (width, height), pygame.FULLSCREEN)
	else :
		if resizable :
			if double_buffer :
				if hardware_accelerated :
					var.window = pygame.display.set_mode( (width, height), pygame.RESIZABLE | pygame.DOUBLEBUF | pygame.HWSURFACE)
				else :
					var.window = pygame.display.set_mode( (width, height), pygame.RESIZABLE | pygame.DOUBLEBUF)
			else:
				var.window = pygame.display.set_mode( (width, height), pygame.RESIZABLE)
		else:
			var.window = pygame.display.set_mode( (width, height))

	pygame.event.clear(pygame.VIDEORESIZE) #remove the event pygame.VIDEORESIZE from the queue

	return var.window

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
	var.tile_size = max (var.tile_size, 20) #prevent the game window of becoming to small
	logging.info("New Tile Size is : %s", var.tile_size)
	if var.current_action == "PLAY_A_LETTER" :
		var.delta_pos_on_tile
		var.delta_pos_on_tile = (var.delta_pos_on_tile[0]*zoom_factor, var.delta_pos_on_tile[1]*zoom_factor)

#Logging functions
def logPlayersInfo():
	logging.info("--- Players info ---")
	for player in PLAYERS :
		player.info()
	logging.info("")

#Calculate points
def calculatePoints(layer_letters_played) :

	#format 'letters_played' {(x, y) : 'a' }
	# 'x' and 'y' will then be swapped when accessing 'board_state' as it is a matrix
	# eg : m =[[a, b], [c, d]] -> to get 'b' you need to access : m[1][2] which for the UI would be m(2, 1)
	letters_played = {}
	for letter in layer_letters_played :
		letters_played[(int(letter.pos_x - DELTA), int(letter.pos_y - DELTA))] = letter.name

	#___ LOGGER ___	
	if len(letters_played) > 1 :
		logging.debug('%i letters played : %s', len(letters_played), letters_played)
		logging.info('')
	else :
		logging.debug('%i letter played : %s', len(letters_played), letters_played)
		logging.info('') 


	#store the cause of invladity for help pop-up
	invalid_move_cause = ''

	#___ First turn valid move conditions ___
	if len( layers.letters_on_board.sprites() ) == 0 : #first turn

		if var.current_board_state[7][7] == '?' : #not on the start tile
			logging.info('INVALID MOVE - Did not play on the start tile')
			invalid_move_cause = 'not_on_start_tile'

		if len(letters_played) == 1 : #one letter played
			logging.info('INVALID MOVE - Only played one letter on first turn')
			invalid_move_cause = 'first_turn_one_letter'

		if invalid_move_cause != '' :
			return [ [], invalid_move_cause ]


	#___ Nothing played ___
	if len(letters_played) == 0 :
		logging.info('Nothing played')
		logging.info('')
		return [ [], '' ]


	#___ SOMETHING PLAYED ___
	else :

		#___ INITIALISATION ___
		words_and_scores = []
		all_x, all_y = [], []
		is_valid_move = True

		for tuple_pos in letters_played.keys() :
			all_x.append(tuple_pos[0])
			all_y.append(tuple_pos[1])

		min_x, max_x, delta_x = min(all_x), max(all_x), max(all_x)-min(all_x)
		min_y, max_y, delta_y = min(all_y), max(all_y), max(all_y)-min(all_y)

		logging.debug("delat x : %s, delta y : %s", delta_x, delta_y)

		# played in diagonal ?
		if (delta_x != 0 and delta_y != 0) :
			#TODO display error message
			logging.info("INVALID MOVE - Played in diagonal")
			invalid_move_cause = 'play_in_diagonal'
			is_valid_move = False
			return [ [], invalid_move_cause]


		#___ VERTICAL WORD PLAYED ___
		if delta_x == 0 :
			logging.debug('Vertical word possible')

			start_y, end_y = min_y, max_y
			#find first letter
			while( ( (start_y - 1) >= 0) and (var.current_board_state[start_y - 1][min_x] != '?') ) :
				start_y = start_y - 1
			#find last letter
			while( ( (end_y + 1) < TILES_PER_LINE) and (var.current_board_state[end_y + 1][min_x] != '?') ) :
				end_y = end_y + 1


			#------ Is valid move ? ------

			#supposed INVALID until the opposite is proven
			away_vertically, away_horizontally, contains_holes = True, True, True

			#away from older letters ? (above or below)
			if (start_y == min_y and end_y == max_y and len( layers.letters_on_board.sprites() ) > 0):
				logging.debug("  Not played close to another word - vertically")	
			else :
				away_vertically = False

			#contains hole with just the letters played ?
			if (delta_y+1 > len(letters_played) ) :
				logging.debug("  There is a hole in the word if using only letters played")
			else :
				contains_holes = False

			if away_vertically or contains_holes :
				#browse all letters
				it_y = start_y
				while( ( it_y < TILES_PER_LINE) and (var.current_board_state[it_y][min_x] != '?') ) :
					#left
					if min_x > 0 :
						if var.current_board_state[it_y][min_x-1] != '?' :
							away_horizontally = False
					#right
					if min_x + 1 < TILES_PER_LINE :
						if var.current_board_state[it_y][min_x+1] != '?' :
							away_horizontally = False

					it_y = it_y + 1

				it_y = it_y - 1 #back to last letter

				if ( (it_y-start_y) != (end_y-start_y) ) :
					logging.debug("    There is a hole in the word if using all available letters")
				else :
					contains_holes = False

			#------ Conclude on validity ------
			if away_vertically and away_horizontally :
				logging.info("INVALID MOVE - Not played close to an existing word")
				is_valid_move = False
				invalid_move_cause = 'not_reusing_letters'

			if contains_holes :
				logging.info("INVALID MOVE - Contains holes")
				is_valid_move = False
				invalid_move_cause = 'hole_in_word'	


			#----- VALID MOVE -----

			if is_valid_move :

				#___ SCRABBLE ___
				if len(letters_played) == 7 : #is a SCRABBLE ?
					words_and_scores.append(['!! SCRABBLE !!', var.points_for_scrabble])
					logging.info('Scrabble obtained')
					SOUNDS.victory.play()
			
				# prevent one letter word to be counted
				if end_y == start_y  : 
					logging.debug('  Vertical one letter word ignored')

				else:
					logging.info('Vertical word played')
					new_word, new_word_multiplier, new_word_score = '', 1, 0

					#___ FIRST PASSAGE : calculate points for word just created ___
					for it_y in range( start_y, end_y+1 ) :

						letter = var.current_board_state[it_y][min_x]
						new_word += letter

						#letters just played
						if ((min_x, it_y) in letters_played ): 

							# get corresponding multipliers for this tile
							bonus = rules.BOARD_LAYOUT[it_y][min_x]
							tile_letter_multiplier, tile_word_multiplier = rules.MULTIPLIERS[bonus][0], rules.MULTIPLIERS[bonus][1]

							# increment score and calculate the global multipier
							new_word_score += POINTS_FOR[letter] * tile_letter_multiplier
							new_word_multiplier *= tile_word_multiplier

						# letters already on board
						else : 
							old_letter_points = POINTS_FOR[letter]
							new_word_score = new_word_score + old_letter_points
							
					# total score for this word		
					new_word_score = new_word_score * new_word_multiplier
					words_and_scores.append([new_word, new_word_score])


				#___ SECOND PASSAGE : calculate points for words already on board and completed by the new word ___
				for it_y in range( start_y, end_y+1 ) :

					#check for old words complete by this new played word
					it_x = min_x
					if (it_x, it_y) in (letters_played) : #prevent to count already existing words

						condition_1 = ( (it_x - 1) >= 0 ) and ( var.current_board_state[it_y][it_x-1] != '?' )
						condition_2 = ( (it_x + 1) < TILES_PER_LINE ) and ( var.current_board_state[it_y][it_x+1] != '?' ) 

						if ( condition_1  or condition_2 ) :       
							logging.debug('Horizontal word played')

							#___ PREPARE ITERATION : go to the begining of the word ___
							while( ( (it_x - 1) >= 0) and (var.current_board_state[it_y][it_x-1] != '?') ) : 
								it_x = it_x - 1

							old_word, old_word_score, old_word_multiplier = '', 0, 1
							#___ ITERATE ON THE LETTER OF THE WORD (go to the end of the word) ___
							while( ( (it_x) < TILES_PER_LINE) and (var.current_board_state[it_y][it_x] != '?') ) :

								old_letter = var.current_board_state[it_y][it_x]
								old_word += old_letter

								#letters just played
								if (it_x, it_y) in (letters_played) :

									# get corresponding multipliers for this tile
									bonus = rules.BOARD_LAYOUT[it_y][it_x]
									tile_letter_multiplier, tile_word_multiplier = rules.MULTIPLIERS[bonus][0], rules.MULTIPLIERS[bonus][1]

									# increment score and calculate the global multipier
									old_word_score += POINTS_FOR[old_letter] * tile_letter_multiplier
									old_word_multiplier *= tile_word_multiplier

								else :
									old_word_score += POINTS_FOR[old_letter]

								it_x = it_x + 1

							old_word_score = old_word_score * old_word_multiplier
							words_and_scores.append([old_word, old_word_score])

			#----- INVALID MOVE -----
			else :
				return[ [], invalid_move_cause ]


		#___ HORIZONTAL WORD PLAYED ___
		elif delta_y == 0 : 
			logging.debug('Horizontal word possible')

			start_x, end_x = min_x, max_x
			#find first letter
			while( ( (start_x - 1) >= 0) and (var.current_board_state[min_y][start_x - 1] != '?') ) :
				start_x = start_x - 1
			#find last letter
			while( ( (end_x + 1) < TILES_PER_LINE) and (var.current_board_state[min_y][end_x + 1] != '?') ) :
				end_x = end_x + 1


			#------ Is valid move ? ------

			#supposed INVALID until the opposite is proven
			away_vertically, away_horizontally, contains_holes = True, True, True

			#away from older letters (left or right)
			if (start_x == min_x and end_x == max_x and len( layers.letters_on_board.sprites() ) > 0):
				logging.debug("  Not played close to another word - horizontally")	
			else :
				away_horizontally = False

			#contains hole with just the letters played ?
			if (delta_x+1 > len(letters_played) ) :
				logging.debug("  There is a hole between letters played")
			else :
				contains_holes = False

			if away_horizontally or contains_holes :
				#browse all letters
				it_x = start_x
				while( ( it_x < TILES_PER_LINE) and (var.current_board_state[min_y][it_x] != '?') ) :
					#up
					if min_y > 0 :
						if var.current_board_state[min_y - 1][it_x] != '?':
							away_vertically = False
					#down
					if min_y + 1 < TILES_PER_LINE :
						if var.current_board_state[min_y + 1][it_x] != '?':
							away_vertically = False						

					it_x = it_x + 1

				it_x = it_x - 1 #back to last letter

				if ( (it_x-start_x) != (end_x-start_x) ) :
					logging.debug("    There is a hole in the word if using all available letters")
				else :
					contains_holes = False

			#------ Conclude on validity ------
			if away_vertically and away_horizontally :
				logging.info("INVALID MOVE - Not played close to an existing word")
				is_valid_move = False
				invalid_move_cause = 'not_reusing_letters'

			if contains_holes :
				logging.info("INVALID MOVE - Contains holes")
				is_valid_move = False
				invalid_move_cause = 'hole_in_word'


			#----- VALID MOVE -----

			if is_valid_move :
				#___ SCRABBLE ___
				if len(letters_played) == 7 : #is a SCRABBLE ?

					#TODO do not add a scrabble if invalid move
					words_and_scores.append(['!! SCRABBLE !!', var.points_for_scrabble])
					logging.info('Scrabble obtained')
					SOUNDS.victory.play()

				#Do not count one letter word
				if  end_x == start_x :
					logging.debug('  Horizontal one letter word ignored')

				else : 
					logging.debug('Horizontal word played')
					new_word, new_word_multiplier, new_word_score= '', 1, 0

					#___ FIRST PASSAGE : calculate points for word just created ___
					for it_x in range( start_x, end_x+1 ) :

						letter = var.current_board_state[min_y][it_x]
						new_word += letter

						#letters just played
						if ((it_x, min_y) in letters_played ): 

							# get corresponding multipliers for this tile
							bonus = rules.BOARD_LAYOUT[min_y][it_x]
							tile_letter_multiplier, tile_word_multiplier = rules.MULTIPLIERS[bonus][0], rules.MULTIPLIERS[bonus][1]

							# increment score and calculate the global multipier
							new_word_score += POINTS_FOR[letter] * tile_letter_multiplier
							new_word_multiplier *= tile_word_multiplier

						# letters already on board
						else : 
							old_letter_points = POINTS_FOR[letter]
							new_word_score = new_word_score + old_letter_points
							
					# total score for this word		
					new_word_score = new_word_score * new_word_multiplier
					words_and_scores.append([new_word, new_word_score])


				#___ SECOND PASSAGE : calculate points for words already on board and completed by the new word ___
				for it_x in range( start_x, end_x+1 ) :

					#check for old words complete by this new played word
					it_y = min_y
					if (it_x, it_y) in (letters_played) : #prevent to count already existing words

						condition_1 = ( (it_y - 1) >= 0 ) and ( var.current_board_state[it_y-1][it_x] != '?' )
						condition_2 = ( (it_y + 1) < TILES_PER_LINE ) and ( var.current_board_state[it_y+1][it_x] != '?' ) 

						if ( condition_1  or condition_2 ) :
							logging.debug('Vertical word played')

							#___ PREPARE ITERATION : go to the begining of the word ___
							while( ( (it_y - 1) >= 0) and (var.current_board_state[it_y-1][it_x] != '?') ) : #go to the begining of the word
								it_y = it_y - 1

							old_word, old_word_score, old_word_multiplier= '', 0, 1
							#___ ITERATE ON THE LETTER OF THE WORD (go to the end of the word) ___
							while( ( (it_y) < TILES_PER_LINE) and (var.current_board_state[it_y][it_x] != '?') ) :

								old_letter = var.current_board_state[it_y][it_x]
								old_word += old_letter

								#letters just played
								if (it_x, it_y) in (letters_played) :

									# get corresponding multipliers for this tile
									bonus = rules.BOARD_LAYOUT[it_y][it_x]
									tile_letter_multiplier, tile_word_multiplier = rules.MULTIPLIERS[bonus][0], rules.MULTIPLIERS[bonus][1]

									# increment score and calculate the global multipier
									old_word_score += POINTS_FOR[old_letter] * tile_letter_multiplier
									old_word_multiplier *= tile_word_multiplier

								else :
									old_word_score += POINTS_FOR[old_letter]
								
								it_y = it_y + 1

							old_word_score = old_word_score * old_word_multiplier
							words_and_scores.append([old_word, old_word_score])

			#----- INVALID MOVE -----
			else :
				return[ [], invalid_move_cause ]


		#----- Calculate scores -----
		total_score = 0 #TEMP

		for association in words_and_scores :
			logging.info("Word '%s' gives %i points", association[0], association[1])
			total_score += association[1]
		
		logging.info('Total score this turn : %i', total_score)
		logging.info('')

		return [ words_and_scores, '' ]


#increment predicted score in real time
def incrementPredictedScore():
	var.predicted_score = 0
	a_words_points, move_is_valid = calculatePoints(layers.letters_just_played)
	if move_is_valid:
		for h_word_point in a_words_points :
			var.predicted_score = var.predicted_score + h_word_point[1]


#~~~~~~ LOAD CONFIGURATION ~~~~~~

#----- Init logger -----

log_file = path.join(PATHS.path_log,'scrabble.log')
# levels : NOTSET < DEBUG < INFO < WARNING < ERROR < CRITICAL
logging.basicConfig(filename=log_file, filemode='w', level=logging.DEBUG, format='%(asctime)s.%(msecs)03d  |  %(levelname)s  |  %(message)s', datefmt='%Y-%m-%d  %p %I:%M:%S')
logging.info("_________START OF LOG___________")
logging.info("")

#----- OS verification -----
os_name = platform.system()
os_version = platform.release()
logging.debug("Platform : %s %s", os_name, os_version)
logging.debug("")

#----- Get configuration -----

#Display settings
display_settings = config_reader.h_display_params
cfg_fullscreen = display_settings['fullscreen']
cfg_resizable = display_settings['resizable']
cfg_resolution_auto = display_settings['resolution_auto']
cfg_custom_window_height = display_settings['custom_window_height']
cfg_enable_windows_ten_upscaling = display_settings['enable_windows_ten_upscaling']
cfg_hardware_accelerated = display_settings['enable_hardware_accelerated']
cfg_double_buffer = display_settings['enable_double_buffer']
cfg_max_fps = display_settings['max_fps']

#logging configuration
logging.debug("--- Display settings ---")
logging.debug("  Fullscreen : %s", cfg_fullscreen)
logging.debug("  Resizable : %s", cfg_resizable)
logging.debug("  Resolution auto : %s", cfg_resolution_auto)
logging.debug("  Enable Windows 10 upscaling : %s", cfg_enable_windows_ten_upscaling)
logging.debug("  Custom window width : %s", int ( cfg_custom_window_height * (16/9.0)) )
logging.debug("  Custom window height : %s", cfg_custom_window_height)
logging.debug("  Hardware accelerated : %s", cfg_hardware_accelerated)
logging.debug("  Double buffer : %s", cfg_double_buffer)
logging.debug("")

#----- DPI scaling -----
if cfg_enable_windows_ten_upscaling == False :
	if ( os_name == "Windows" and os_version == "10" ):
		# Query DPI Awareness (Windows 10 and 8)
		awareness = ctypes.c_int()
		errorCode = ctypes.windll.shcore.GetProcessDpiAwareness(0, ctypes.addressof(awareness))

		if awareness.value == 0 :
			# Set DPI Awareness  (Windows 10 and 8)
			errorCode = ctypes.windll.shcore.SetProcessDpiAwareness(2)
			if errorCode != 0:
				errorCode = ctypes.windll.shcore.SetProcessDpiAwareness(1)
			if errorCode == 0 :
				logging.debug("Pygame's window resolution handled by itself")
			else :
				logging.debug("  DPI scaling failed with Eror code : %s", errorCode)
			logging.debug("")

#Game settings
game_settings = config_reader.h_rules_params
var.number_of_letters_per_hand = game_settings['number_of_letters_per_hand']
display_next_player_hand = game_settings['display_next_player_hand']
enable_shuffle_letter = game_settings['enable_shuffle_letter']
LETTERS_LANGUAGE = game_settings['letters_language']
UI_LANGUAGE = game_settings['ui_language']
players_names = config_reader.players
display_type_of_tile_on_hoovering = game_settings['display_type_of_tile_on_hoovering']
display_new_score_in_real_time = game_settings['display_new_score_in_real_time']

#Letters and points
if LETTERS_LANGUAGE == 'english' :
	var.bag_of_letters = rules.letters_english
	POINTS_FOR = rules.points_english
	PATHS.path_letters = PATHS.path_letters_english
elif LETTERS_LANGUAGE == 'french':
	var.bag_of_letters = rules.letters_french
	POINTS_FOR = rules.points_french
	PATHS.path_letters = PATHS.path_letters_french

#Data validation
forced = ""
if var.number_of_letters_per_hand < 5:
	var.number_of_letters_per_hand = 5
	forced = 'forced to '
elif var.number_of_letters_per_hand > 9 :
	var.number_of_letters_per_hand = 9
	forced = 'forced to '

#initialize discard holder state
var.discard_holder_state = [ 0 for i in range (0, var.number_of_letters_per_hand) ]

logging.debug("--- Game Rules ---")
logging.debug("  Language : %s", LETTERS_LANGUAGE)
logging.info("  Players : %s", players_names)
logging.debug("  Number of letters per_hand %s: %s", forced, var.number_of_letters_per_hand)
logging.debug("  Display next player hand : %s", display_next_player_hand)
logging.debug("  Enable shuffle letters : %s", enable_shuffle_letter)
logging.debug("")


#~~~~~~ GAME INITIALIAZATION ~~~~~~


#----- Launch Pygame -----


game_engine = pygame.init() #init() -> (numpass, numfail)
sound_engine = pygame.mixer.init() #init(frequency=22050, size=-16, channels=2, buffer=4096) -> None
game_is_running = True

fps_clock = pygame.time.Clock()
clic_clock = pygame.time.Clock()
logging.debug("--- Initialization ---")
logging.debug("  %s pygame modules were launched and %s failed", game_engine[0], game_engine[1])
logging.debug("  Pygame started")
logging.debug("")
logging.info("-------------------")
logging.info("GAME STARTED")
logging.info("-------------------")
logging.info("")

#----- Load Sounds -----
SOUNDS = Sounds()
logging.debug("SOUNDS loaded")
logging.debug("")



#___ CUSTOM POINTERS ___
#SMALL

arrow_strings = ( #sized 24x24
  "X                       ",
  "XX                      ",
  "X.X                     ",
  "X..X                    ",
  "X...X                   ",
  "X....X                  ",
  "X.....X                 ",
  "X......X                ",
  "X.......X               ",
  "X........X              ",
  "X.........X             ",
  "X..........X            ",
  "X......XXXXXX           ",
  "X...X..X                ",
  "X..XX..X                ",
  "X.X  X..X               ",
  "XX   X..X               ",
  "X     X..X              ",
  "      X..X              ",
  "       XXX              ",
  "                        ",
  "                        ",
  "                        ",
  "                        ",
)
arrow=((24,24),(0,0))+pygame.cursors.compile(arrow_strings,"X",".")

hand_strings = ( #sized 24x24
  "                        ",
  "     XX                 ",
  "    X..X                ",
  "    X..X                ",
  "    X..X                ",
  "    X..X                ",
  "    X..XXX              ",
  "    X..X..XXX           ",
  "    X..X..X..XX         ",
  "    X..X..X..X.X        ",
  "XXX X..X..X..X..X       ",
  "X..XX........X..X       ",
  "X...X...........X       ",
  " X..X...........X       ",
  "  X.X...........X       ",
  "  X.............X       ",
  "   X............X       ",
  "   X...........X        ",
  "    X..........X        ",
  "    X..........X        ",
  "     X........X         ",
  "     X........X         ",
  "     XXXXXXXXXX         ",
  "                        ",
)
hand=((24,24),(6,1))+pygame.cursors.compile(hand_strings,"X",".")

hand_strings = ( #sized 24x24
  "         XX             ",
  "      XXX..XXX          ",
  "     X..X..X..X         ",
  "     X..X..X..X         ",
  "     X..X..X..X         ",
  "     X..X..X..XX        ",
  "     X..X..X..X.X       ",
  "     X..X..X..X..X      ",
  "     X..X..X..X..X      ",
  "     X..X..X..X..X      ",
  " XXX X..X..X..X..X      ",
  " X..XX........X..X      ",
  " X...X...........X      ",
  "  X..X...........X      ",
  "   X.X...........X      ",
  "   X.............X      ",
  "    X............X      ",
  "    X...........X       ",
  "     X..........X       ",
  "     X..........X       ",
  "      X........X        ",
  "      X........X        ",
  "      XXXXXXXXXX        ",
  "                        ",
)
open_hand=((24,24),(10,4))+pygame.cursors.compile(hand_strings,"X",".")

hand_strings = ( #sized 24x24
  "                        ",
  "                        ",
  "                        ",
  "                        ",
  "        XXXXXX          ",
  "     XXXX..X..XX        ",
  "     X..X..X..X.X       ",
  "     X..X..X..X..X      ",
  "     X..X..X..X..X      ",
  "     X..X..X..X..X      ",
  "    XX..X..X..X..X      ",
  "   X.X........X..X      ",
  "   X.X...........X      ",
  "   X.X...........X      ",
  "   X.X...........X      ",
  "   X.............X      ",
  "    X............X      ",
  "    X...........X       ",
  "     X..........X       ",
  "     X..........X       ",
  "      X........X        ",
  "      X........X        ",
  "      XXXXXXXXXX        ",
  "                        ",
)
close_hand=((24,24),(10,4))+pygame.cursors.compile(hand_strings,"X",".")

hand_clic_strings = ( #sized 24x24
  "                        ",
  "                        ",
  "                        ",
  "                        ",
  "                        ",
  "    XXX                 ",
  "    X..XXX              ",
  "    X..X..XXX           ",
  "    X..X..X..XX         ",
  "    X..X..X..X.X        ",
  "XXX X..X..X..X..X       ",
  "X..XX........X..X       ",
  "X...X...........X       ",
  " X..X...........X       ",
  "  X.X...........X       ",
  "  X.............X       ",
  "   X............X       ",
  "   X...........X        ",
  "    X..........X        ",
  "    X..........X        ",
  "     X........X         ",
  "     X........X         ",
  "     XXXXXXXXXX         ",
  "                        ",
)
hand_clic=((24,24),(6,1))+pygame.cursors.compile(hand_clic_strings,"X",".")

"""
#BIG
#TODO3 to debug:

	arrow_strings = ( #sized 24x24
	  "            X                                   ",
	  "            XX                                  ",
	  "            X.X                                 ",
	  "            X..X                                ",
	  "            X...X                               ",
	  "            X....X                              ",
	  "            X.....X                             ",
	  "            X......X                            ",
	  "            X.......X                           ",
	  "            X........X                          ",
	  "            X.........X                         ",
	  "            X..........X                        ",
	  "            X...........X                       ",
	  "            X............X                      ",
	  "            X.............X                     ",
	  "            X..............X                    ",
	  "            X...............X                   ",
	  "            X................X                  ",
	  "            X.................X                 ",
	  "            X..................X                ",
	  "            X...................X               ",
	  "            X....................X              ",
	  "            X.....................X             ",
	  "            X......................X            ",  
	  "            X.......................X           ",
	  "            X........................X          ",
	  "            X.............XXXXXXXXXXXXX         ",
	  "            X.......X.....X                     ",
	  "            X......XX.....X                     ",
	  "            X.....X  X.....X                    ",
	  "            X....X   X.....X                    ",
	  "            X...X    X.....X                    ",
	  "            X  X      X.....X                   ",
	  "            X X       X.....X                   ",
	  "            XX         X.....X                  ",
	  "            X          X.....X                  ",
	  "                        X.....X                 ",
	  "                        X.....X                 ",
	  "                         X.....X                ",
	  "                         X.....X                ",
	  "                          XXXXXX                ",
	  "                                                ",
	  "                                                ",
	  "                                                ",
	  "                                                ",
	  "                                                ",
	  "                                                ",
	  "                                                ",
	)
	arrow=((48,48),(13,1))+pygame.cursors.compile(arrow_strings,"X",".")

	hand_strings = ( #sized 24x24
	  "                                                ",
	  "                  XX                            ",
	  "                 X..X                           ",
	  "                X....X                          ",
	  "                X....X                          ",
	  "                X....X                          ",
	  "                X....X                          ",
	  "                X....X                          ",
	  "                X....X                          ",
	  "                X....X                          ",
	  "                X....X                          ",
	  "                X....XXXXX                      ",
	  "                X....X....X                     ",
	  "                X....X....XXXXX                 ",
	  "       XXXX     X....X....X....X                ",
	  "       X...X    X....X....X....X                ",
	  "      X.....X   X....X....X....XXXX             ",
	  "      X......X  X....X....X....X...X            ",
	  "       X.....X  X....X....X....X...X            ",
	  "       X......X X....X....X.... ...X            ",
	  "        X.....X X..................X            ",  
	  "         X.....XX..................X            ",
	  "          X.....X..................X            ",
	  "          X.....X..................X            ",
	  "           X.......................X            ",
	  "           X.......................X            ",
	  "            X......................X            ",
	  "            X......................X            ",
	  "             X.....................X            ",
	  "             X.....................X            ",
	  "             X.....................X            ",
	  "              X....................X            ",
	  "              X...................X             ",
	  "               X..................X             ",
	  "               X.................X              ",
	  "                X................X              ",  
	  "                X...............X               ",
	  "                 X..............X               ",
	  "                  XXXXXXXXXXXXXX                ",
	  "                                                ",
	  "                                                ",
	  "                                                ",
	  "                                                ",
	  "                                                ",
	  "                                                ",
	  "                                                ",
	  "                                                ",
	  "                                                ",
	)
	hand=((48,48),(20,2))+pygame.cursors.compile(hand_strings,"X",".")

	hand_strings = ( #sized 24x24
	  "                                                ",
	  "                                                ",
	  "                                                ",
	  "                       XX                       ",
	  "                      X..X                      ",
	  "                     X....X                     ",	
	  "                  XX X....X XX                  ",
	  "                 X..XX....XX..X                 ",
	  "                X....X....X....X                ",
	  "                X....X....X....X                ",
	  "                X....X....X....X                ",
	  "                X....X....X....X                ",
	  "                X....X....X....X                ",
	  "                X....X....X....X                ",
	  "                X....X....X....XXX              ",
	  "                X....X....X....X..X             ",
	  "                X....X....X....X...X            ",
	  "                X....X....X....X...X            ",
	  "        XXXX    X....X....X....X...X            ",
	  "        X...X   X....X....X....X...X            ",
	  "       X.....X  X....X....X....X...X            ",
	  "       X......X X....X....X....X...X            ",
	  "        X.....X X....X....X....X...X            ",
	  "        X......XX....X....X....X...X            ",
	  "         X.....XX..................X            ",  
	  "          X.....X..................X            ",
	  "          X.....X..................X            ",
	  "           X.......................X            ",
	  "           X.......................X            ",
	  "           X.......................X            ",
	  "            X......................X            ",
	  "            X......................X            ",
	  "             X.....................X            ",
	  "             X.....................X            ",
	  "             X.....................X            ",
	  "              X....................X            ",
	  "              X...................X             ",
	  "               X..................X             ",
	  "               X.................X              ",
	  "                X................X              ",  
	  "                X...............X               ",
	  "                 X..............X               ",
	  "                  XXXXXXXXXXXXXX                ",
	  "                                                ",
	  "                                                ",
	  "                                                ", 
	  "                                                ",
	  "                                                ",
	)
	open_hand=((48,48),(24,14))+pygame.cursors.compile(hand_strings,"X",".")

	hand_strings = ( #sized 24x24
	  "                                                ",
	  "                                                ",
	  "                                                ",
	  "                                                ",
	  "                                                ",
	  "                                                ", 
	  "                                                ",
	  "                                                ",
	  "                                                ",
	  "                                                ",
	  "                                                ", 
	  "                      XXXX                      ",
	  "                 XXXXX....XXXXX                 ",
	  "                X....X....X....X                ",
	  "                X....X....X....X                ",
	  "                X....X....X....X                ",
	  "                X....X....X....XXX              ",
	  "                X....X....X....X..X             ",
	  "             XXXX....X....X....X...X            ",
	  "            X...X....X....X....X...X            ",
	  "           X....X....X....X....X...X            ",
	  "          X.....X....X....X....X...X            ",
	  "          X.....X....X....X....X...X            ",
	  "           X...XX....X....X....X...X            ",
	  "           X.......................X            ",  
	  "            X......................X            ",
	  "             X.....................X            ",
	  "             X.....................X            ",
	  "              X....................X            ",
	  "              X....................X            ",
	  "              X....................X            ",
	  "              X....................X            ",
	  "              X....................X            ",
	  "              X....................X            ",
	  "              X....................X            ",
	  "              X....................X            ",
	  "              X...................X             ",
	  "               X..................X             ",
	  "               X.................X              ",
	  "                X................X              ",  
	  "                X...............X               ",
	  "                 X..............X               ",
	  "                  XXXXXXXXXXXXXX                ",
	  "                                                ",
	  "                                                ",
	  "                                                ", 
	  "                                                ",
	  "                                                ",
	)
	close_hand=((48,48),(24,14))+pygame.cursors.compile(hand_strings,"X",".")
"""

#Set custom cursor
pygame.mouse.set_cursor(*arrow)


#----- Window init -----

#Add icon to the window
icon_image = pygame.image.load(path.join(PATHS.path_icon,'Scrabble_launcher.ico'))
icon = pygame.transform.scale(icon_image, (32, 32))
pygame.display.set_icon(icon)
pygame.display.set_caption('Scrabble')

#Calculate window resolution
if cfg_resolution_auto :
	var.monitor_resolution = pygame.display.Info()
	var.window_width = var.monitor_resolution.current_w
	var.window_height = var.monitor_resolution.current_h
else :
	var.window_width = round (cfg_custom_window_height * (16/9.0) )
	var.window_height = cfg_custom_window_height
	var.monitor_resolution = pygame.display.Info()

#Initialize game window
var.window = resizeWindow(var.window_width, var.window_height, cfg_fullscreen, cfg_resizable, cfg_resolution_auto, cfg_custom_window_height, cfg_double_buffer, cfg_hardware_accelerated)

#----- Variables init -----

#Define UI scaling
if 1 <= len(players_names) <= 2 :
	UI_INTERLIGNE = 1.25
if 3 <= len(players_names) <= 4 :
	UI_INTERLIGNE = 1.0
if 5 <= len(players_names) <= 6 :
	UI_TOP = 1.0
	UI_INTERLIGNE = 0.8
	LINE_HEIGHT.TITLE = 0.8
	LINE_HEIGHT.SUBTITLE = 0.6
elif 6 < len(players_names) :
	UI_TOP = 0.75
	UI_INTERLIGNE = 0.7
	LINE_HEIGHT.TITLE = 0.7
	LINE_HEIGHT.SUBTITLE = 0.6


#----- Create board game -----

#create background
board = Board("empty_background", 0, 0) #automatically stored in the corresponding layer

#create hand_holder
var.hand_holder = Hand_holder("hand_holder", UI_LEFT_LIMIT - 0.1, UI_TOP+LINE_HEIGHT.TITLE+0.5*UI_INTERLIGNE-0.1, var.number_of_letters_per_hand)#automatically stored in the corresponding layer

#create discard holder
var.discard_holder = Hand_holder("discard_holder", UI_LEFT_LIMIT - 0.1, UI_TOP+LINE_HEIGHT.TITLE+ 1.75*UI_INTERLIGNE-0.1, var.number_of_letters_per_hand)#automatically stored in the corresponding layer
var.discard_holder.remove(layers.hand_holder) #remove from layer


#User interface language
if UI_LANGUAGE == 'english' :
	language_id = 0
	PATHS.path_buttons = PATHS.path_buttons_english
elif UI_LANGUAGE == 'french' :
	language_id = 1
	PATHS.path_buttons = PATHS.path_buttons_french
else :
	language_id = 0
	PATHS.path_buttons = PATHS.path_buttons_english

#User interface content
ui_content = config_reader.h_ui_params

#User interface pop up content
ui_pop_up_content = config_reader.h_pop_up_params

#Initialize userface texts
ui_text = UITextPrinter(ui_content)


#----- Create players -----
enough_letters = len(players_names)*var.number_of_letters_per_hand <= len(var.bag_of_letters)

if enough_letters :

	for player_name in players_names :
		start_hand = GroupOfSprites()
		hand_state = []
		pos_x = (UI_LEFT_LIMIT)
		pos_y = ui_text.current_player_turn.bottom_tiles+0.5*UI_INTERLIGNE

		for i in range(var.number_of_letters_per_hand) :
			if len(var.bag_of_letters) > 0 :
				random_int = randint(0,len(var.bag_of_letters)-1)
				letter = Letter(var.bag_of_letters[random_int], pos_x, pos_y)
				start_hand.add(letter)
				hand_state.append(letter.id)
				del(var.bag_of_letters[random_int])
				pos_x = pos_x+1

		PLAYERS.append(Player(player_name, 0, start_hand, hand_state))

	logPlayersInfo()

	var.current_player = PLAYERS[0]
	var.current_player.info()

else :
	game_is_running = False
	ERROR.not_enough_letters( len(var.bag_of_letters), len(players_names)*var.number_of_letters_per_hand )


#~~~~~~ CREATE SPRITES ~~~~~~

#create tiles
DELTA = 1.5
x_pos = 0 + DELTA
y_pos = 0 + DELTA
for row in range(0,TILES_PER_LINE) :
	for column in range(0, TILES_PER_LINE) :
		if rules.BOARD_LAYOUT[row][column] == 0 :
			Tile('start', x_pos, y_pos)
		elif rules.BOARD_LAYOUT[row][column] == 1 :
			Tile('normal', x_pos, y_pos)
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

# ------- CREATES BUTTONS --------

button_shuffle = Button("shuffle", tiles1(var.hand_holder.rect.x)+var.number_of_letters_per_hand + 0.2 + 0.75, layers.hand_holder.sprites()[0].pos_y + 0.1 )
button_draw = Button("draw", button_shuffle.pos_x, UI_TOP+LINE_HEIGHT.TITLE+ 1.75*UI_INTERLIGNE)
button_cancel = Button("cancel", button_shuffle.pos_x, UI_TOP+LINE_HEIGHT.TITLE+ 1.75*UI_INTERLIGNE)
button_end_turn = Button("end_turn", button_draw.pos_x, button_draw.pos_y + 1 + 0.2)
button_confirm = Button("confirm", button_draw.pos_x, button_draw.pos_y + 1 + 0.2)


layers.buttons_on_screen.add(button_end_turn)
layers.buttons_on_screen.add(button_shuffle)
layers.buttons_on_screen.add(button_draw)

#create dark_filter
mask_surface = pygame.Surface((var.window_width, var.window_height))
mask_surface.fill(COLOR.BLACK)
mask_surface.set_alpha(230)
mask_surface = mask_surface.convert_alpha()
dark_filter = UI_Surface('dark_filter', 0, 0, mask_surface)
layers.dark_filter.add(dark_filter)



# ___ FIRST IMAGE ___

if game_is_running :

	layers.background.draw(var.window)
	layers.tiles.draw(var.window)
	layers.hand_holder.draw(var.window)
	var.background_empty = var.window.copy() #emtpy background

	discard_holder = layers.all.findByName("discard_holder")
	layers.hand_holder.add(discard_holder)
	layers.hand_holder.draw(var.window)
	var.background_empty_drawing = var.window.copy() #empty background with two holders
	layers.hand_holder.remove(discard_holder)
	layers.hand_holder.clear(var.window, var.background_empty)

	layers.buttons_on_screen.draw(var.window)
	var.current_player.hand.draw(var.window)
	var.current_background_no_text = var.window.copy() #full_background without text
	ui_text.drawText()

	var.current_background = var.window.copy() #current background
	pygame.display.update()


#~~~~~~ MAIN  ~~~~~~

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

		#~~~~~~ KEY PRESSED - ESCAPE GAME ~~~~~~			
		elif ( event_type == pygame.KEYDOWN ) and ( event.key == pygame.K_ESCAPE ) :
			logging.info("ESCAPE key pressed")
			game_is_running = False #exit the game

		#~~~~~~ KEY PRESSED - RESTART GAME ~~~~~~			
		elif ( event_type == pygame.KEYDOWN ) and ( event.key == pygame.K_SPACE ) :
			logging.info("SPACE key pressed")
			pass


		#~~~~~~ WINDOW RESIZE ~~~~~~
		#TODO create a specific function ?
		elif ( event_type == pygame.VIDEORESIZE ) : #properly refresh the game window if a resize is detected
			
			#new width and height
			width = event.dict['size'][0]
			height = event.dict['size'][1]

			#create a fullscreen image fully black to prevent later artefacts
			var.window = resizeWindowNoSpritesUpdate(var.monitor_resolution.current_w, var.monitor_resolution.current_h, cfg_fullscreen, cfg_resizable, cfg_resolution_auto, cfg_custom_window_height, cfg_double_buffer, cfg_hardware_accelerated)
			pygame.draw.rect(var.window, COLOR.BLACK, ( (0,0), (var.monitor_resolution.current_w, var.monitor_resolution.current_h) ) )
			pygame.display.update()

			var.window = resizeWindow(width, height, cfg_fullscreen, cfg_resizable, cfg_resolution_auto, cfg_custom_window_height, cfg_double_buffer, cfg_hardware_accelerated)

			#return to normal config even if drawing letters
			layers.hand_holder.remove(discard_holder)

			layers.background.draw(var.window)
			layers.tiles.draw(var.window)
			layers.hand_holder.draw(var.window)
			var.background_empty = var.window.copy()

			discard_holder = layers.all.findByName("discard_holder")
			layers.hand_holder.add(discard_holder)
			layers.hand_holder.draw(var.window)
			var.background_empty_drawing = var.window.copy()
			
			if var.discard_holder_displayed == False :
				layers.hand_holder.remove(discard_holder)
				layers.hand_holder.clear(var.window, var.background_empty)

			layers.buttons_on_screen.draw(var.window)
			layers.letters_on_board.draw(var.window)
			layers.letters_just_played.draw(var.window)
			var.current_player.hand.draw(var.window)

			var.current_background_no_text = var.window.copy()
			ui_text.drawText()

			var.current_background = var.window.copy()
			layers.selected_letter.draw(var.window)

			if MUST_DISPLAY_POP_UP :
				# snapshot of before pop_up
				snapshot = var.window.copy()

				#display pop_up
				layers.dark_filter.draw(var.window)
				layers.pop_up.draw(var.window)
				pygame.display.update()

				#prepare exit image (displayed when removing pop up)
				var.window.blit(snapshot, (0,0))

			else :
				pygame.display.update()
			

		# NORMAL EVENTS
		else :
			# //////// POP UP DISPLAYED ////////
			if MUST_DISPLAY_POP_UP :
				if (event_type == pygame.MOUSEBUTTONDOWN and event.button == 1 ):
					MOUSEBUTTONDOWN_DURING_POP_UP = True
				if ( event_type == pygame.MOUSEBUTTONUP and event.button == 1 and MOUSEBUTTONDOWN_DURING_POP_UP ) :
					FRAMES_BEFORE_POP_UP_DISAPPEAR = 0
					MOUSEBUTTONDOWN_DURING_POP_UP = False

			# //////// WINDOW DISPLAYED ////////
			elif (var.current_action == "WINDOW_DISPLAYED") :
				pass


			# //////// MAIN GAME SCREEN ////////

			else : 
				#~~~~~~~~~~~ MOUSE BUTTONS ~~~~~~~~~~~
				if ( ( (event_type == pygame.MOUSEBUTTONDOWN) or (event_type == pygame.MOUSEBUTTONUP) ) and event.button == 1 ) :

					timer = clic_clock.tick()

					#~~~~~~~~~~~ PRESS LEFT CLIC ~~~~~~~~~~~
					if ( event_type == pygame.MOUSEBUTTONDOWN ) :

						cursor_pos_x, cursor_pos_y = event.pos[0], event.pos[1]

						#------ SELECT A LETTER -------
						if var.current_action == 'SELECT_A_LETTER' :

							#------ Clic on the Hand Holder ? -------
							if var.hand_holder.collide(cursor_pos_x, cursor_pos_y) :

								#------ Clic on a letter in the Hand Holder ? -------
								for letter_from_hand in var.current_player.hand :

									if letter_from_hand.collide(cursor_pos_x, cursor_pos_y) :

										#TODO8 to debug
										pygame.mouse.set_cursor(*close_hand)

										var.delta_pos_on_tile = ( cursor_pos_x - letter_from_hand.rect.x , cursor_pos_y - letter_from_hand.rect.y)
										layers.selected_letter.add(letter_from_hand)
											
										#remove letter from hand
										var.current_player.hand.remove(letter_from_hand)
										hand_state_index = var.current_player.hand_state.index(letter_from_hand.id)
										var.current_player.hand_state[hand_state_index] = 0

										#refresh screen
										var.current_player.hand.clear(var.window, var.background_empty_drawing) #needed when drawing letters
										var.current_player.hand.draw(var.window)

										var.current_background = var.window.copy()									
										layers.selected_letter.draw(var.window)
										pygame.display.update()

										var.current_action = "PLAY_A_LETTER"


							#------ Clic on the Discard Holder ? -------
							elif var.discard_holder_displayed and var.discard_holder.collide(cursor_pos_x, cursor_pos_y) :

								#------ Clic on a letter in the Discard Holder ? -------
								for letter_from_hand in var.current_player.hand :

									if letter_from_hand.collide(cursor_pos_x, cursor_pos_y) :

										pygame.mouse.set_cursor(*close_hand)

										var.delta_pos_on_tile = ( cursor_pos_x - letter_from_hand.rect.x , cursor_pos_y - letter_from_hand.rect.y)
										layers.selected_letter.add(letter_from_hand)

										#remove letter from hand
										var.current_player.hand.remove(letter_from_hand)
										index_discard_holder = var.discard_holder_state.index(letter_from_hand.id)
										var.discard_holder_state[index_discard_holder] = 0

										if var.discard_holder_state == [0 for i in range (0, var.number_of_letters_per_hand)] :
											button_confirm.disable()

										#refresh screen
										#TODO9 refresh not OK
										var.current_player.hand.clear(var.window, var.background_empty_drawing)
										var.current_player.hand.draw(var.window)

										layers.buttons_on_screen.draw(var.window)

										var.current_background = var.window.copy()									
										layers.selected_letter.draw(var.window)
										pygame.display.update()

										pygame.mouse.set_cursor(*close_hand)
										var.current_action = "PLAY_A_LETTER"


							#------ CLIC ON A LETTER JUST PLAYED ? -------
							else :
								for letter_from_board in layers.letters_just_played :

									if letter_from_board.collide(cursor_pos_x, cursor_pos_y) :

										pygame.mouse.set_cursor(*close_hand)

										var.delta_pos_on_tile = ( cursor_pos_x - letter_from_board.rect.x , cursor_pos_y - letter_from_board.rect.y)

										tile_x_on_board = int(letter_from_board.pos_x - DELTA)
										tile_y_on_board = int(letter_from_board.pos_y - DELTA)

										var.current_board_state[tile_y_on_board][tile_x_on_board] = '?'

										layers.letters_just_played.remove(letter_from_board)
										layers.selected_letter.add(letter_from_board)

										#refresh screen
										layers.letters_just_played.clear(var.window, var.background_empty)
										layers.letters_just_played.draw(var.window)

										var.current_background = var.window.copy()									
										layers.selected_letter.draw(var.window)
										pygame.display.update()

										pygame.mouse.set_cursor(*close_hand)
										var.current_action = "PLAY_A_LETTER"
							

							#------ CLIC ON BUTTONS (VISUAL) -------
							for button in layers.buttons_on_screen :
								if button.is_enabled :
									if button.collide(cursor_pos_x, cursor_pos_y) == True :
										#change button state
										button.is_highlighted = False
										button.push()
										var.a_button_is_pushed = True
										layers.buttons_on_screen.clear(var.window, var.background_empty)
										layers.buttons_on_screen.draw(var.window) 
							pygame.display.update()



						#------ PLAY A LETTER -------
						elif var.current_action == 'PLAY_A_LETTER' :

							#------ A LETTER IS SELECTED -------
							if len(layers.selected_letter) == 1 : 

								selected_letter = layers.selected_letter.sprites()[0]
								letter_center_x, letter_center_y = selected_letter.rect.centerx, selected_letter.rect.centery
								
								move_my_letter = False


								#------ CLIC ON THE HAND HOLDER ? -------
								if var.hand_holder.collide(letter_center_x, letter_center_y) :

									index_in_hand = var.hand_holder.indexAtPos(letter_center_x)
									delta_x, delta_y = layers.hand_holder.sprites()[0].pos_x + 0.1, layers.hand_holder.sprites()[0].pos_y + 0.1

									#------ EMPTY SPOT ? -------
									if var.current_player.hand_state[index_in_hand] == 0 :
										move_my_letter = True

									#----------------------NOT AN EMPTY SLOT--------------------	
									else :
										#TODO1 to improve

										letter_id = var.current_player.hand_state[index_in_hand]
										old_letter = var.current_player.hand.findByIndex(letter_id)

										offset_x = selected_letter.rect.centerx - old_letter.rect.centerx
										if offset_x >= 0 : #want to push to the left
											direction = -1
										else :
											direction = +1

										if old_letter.canMove(direction) : #no need to push other letters

											old_letter.moveAtTile( delta_x + index_in_hand + direction, delta_y )
											var.current_player.hand_state[index_in_hand+direction] = old_letter.id
											var.current_player.hand_state[index_in_hand] = 0

											move_my_letter = True


										else : #need to push
											#try backward
											if old_letter.canMove(-direction) :

												old_letter.moveAtTile( delta_x + index_in_hand - direction, delta_y )
												var.current_player.hand_state[index_in_hand-direction] = old_letter.id
												var.current_player.hand_state[index_in_hand] = 0

												move_my_letter = True
											else :
												pass


									if move_my_letter == True :
									
										selected_letter.moveAtTile( delta_x + index_in_hand, delta_y )
										var.current_player.hand_state[index_in_hand] = selected_letter.id

										#change letter from layers
										var.current_player.hand.add(selected_letter)
										layers.selected_letter.remove(selected_letter)

										#refresh screen
										layers.selected_letter.clear(var.window, var.current_background)
										var.current_player.hand.draw(var.window)

										if display_new_score_in_real_time :
											incrementPredictedScore()
											layers.mask_text.draw(var.window)

										var.current_background = var.window.copy()

										pygame.mouse.set_cursor(*open_hand)
										CURSOR_IS_OPEN_HAND = True

										pygame.display.update()											

										var.current_action = "SELECT_A_LETTER"


								#------ Clic on the discard holder ? -------
								if var.discard_holder_displayed and var.discard_holder.collide(letter_center_x, letter_center_y) :

									index_in_hand = var.discard_holder.indexAtPos(letter_center_x)
									delta_x, delta_y = var.discard_holder.pos_x + 0.1, var.discard_holder.pos_y + 0.1

									#------ EMPTY SPOT ? -------
									if var.discard_holder_state[index_in_hand] == 0 :
										move_my_letter = True

									else :
										#TODO push letters
										pass

									if move_my_letter == True :
										button_confirm.enable()	
									
										selected_letter.moveAtTile( delta_x + index_in_hand, delta_y )
										var.discard_holder_state[index_in_hand] = selected_letter.id

										#change letter from layers
										var.current_player.hand.add(selected_letter)
										layers.selected_letter.remove(selected_letter)

										#refresh screen
										layers.selected_letter.clear(var.window, var.current_background)
										var.current_player.hand.draw(var.window)

										layers.buttons_on_screen.draw(var.window)

										var.current_background = var.window.copy()

										pygame.mouse.set_cursor(*open_hand)
										CURSOR_IS_OPEN_HAND = True

										pygame.display.update()											

										var.current_action = "SELECT_A_LETTER"


								#------ CLIC ON A TILE ON THE BOARD ? -------
								for tile in layers.tiles :

									if tile.collide(letter_center_x, letter_center_y) == True :

										logging.debug("Tile center pos : %i, %i", tile.rect.centerx, tile.rect.centery)

										tile_x_on_board = int( tile.pos_x - DELTA )
										tile_y_on_board = int( tile.pos_y - DELTA )

										#------ EMPTY TILE ? -------
										if var.current_board_state[tile_y_on_board][tile_x_on_board] == '?':

											if var.discard_holder_displayed == False :

												selected_letter = layers.selected_letter.sprites()[0]

												selected_letter.moveAtTile( (tile_x_on_board + DELTA), (tile_y_on_board + DELTA) )
												var.current_board_state[tile_y_on_board][tile_x_on_board] = selected_letter.name

												layers.letters_just_played.add(selected_letter)								
												layers.selected_letter.remove(selected_letter)

												layers.selected_letter.clear(var.window, var.current_background)	
												layers.letters_just_played.draw(var.window)


												if display_new_score_in_real_time :
													incrementPredictedScore()
													layers.mask_text.draw(var.window)

												#TODO REFRESH TEXT
												var.current_background = var.window.copy()

												pygame.mouse.set_cursor(*open_hand)
												CURSOR_IS_OPEN_HAND = True

												pygame.display.update()

												var.current_action = "SELECT_A_LETTER"

											elif var.discard_holder_displayed :

												#TODO 7 in other languages
												displayPopUp("You cannot play here") 



					#~~~~~~~~~~~ RELEASE LEFT CLIC ~~~~~~~~~~~
					elif ( event_type == pygame.MOUSEBUTTONUP ) :

						var.a_button_is_pushed = False

						#------ SELECT A LETTER -------
						if ( var.current_action == 'SELECT_A_LETTER' ) :

							need_update = False


							#------ RELEASE CLIC ON END TURN BUTTON -------
							if ( (button_end_turn.collide(cursor_pos_x, cursor_pos_y) == True) and (button_end_turn.is_pushed) ):

								button_end_turn.release()

								#calculate score
								var.last_words_and_scores, invalid_move_cause = calculatePoints(layers.letters_just_played)

								words = []
								for association in var.last_words_and_scores :
									var.current_player.score += association[1]
									words.append(association[0])


								#------ CHECK IF VALID MOVE ------
								valid_move = True
								text_pop_up = []

								if ( len( layers.letters_just_played.sprites() ) > 0) :
									if invalid_move_cause != '' : #invalid move
										valid_move = False
										text_pop_up = ui_pop_up_content[invalid_move_cause][language_id].split('<NEWLINE>')
							

								#------ INVALID MOVE -> Display Pop Up ------		
								if valid_move == False :

									need_update = False
									displayPopUp(text_pop_up, interligne_ratio=1.6, margin_ratio=(2.0,1.5), time = 8)  
								

								#------ VALID MOVE -> Draw letters and next player ------
								else :

									#letters
									for letter in layers.letters_just_played :
										layers.letters_on_board.add(letter)

									layers.letters_just_played.empty()
									layers.letters_just_played.clear(var.window, var.background_empty)

									#redraw letters
									index_hand = 0
									while len(var.bag_of_letters) > 0 and index_hand < var.number_of_letters_per_hand :
										if var.current_player.hand_state[index_hand] == 0 :
											random_int = randint(0,len(var.bag_of_letters)-1)
											drawn_letter = Letter(var.bag_of_letters[random_int], 0, 0)
											del(var.bag_of_letters[random_int])	

											var.current_player.hand_state[index_hand] = drawn_letter.id
											delta_x, delta_y = UI_LEFT_LIMIT, ui_text.current_player_turn.bottom_tiles+0.5*UI_INTERLIGNE
											drawn_letter.moveAtTile( delta_x + index_hand, delta_y )
											var.current_player.hand.add(drawn_letter)

										index_hand += 1

									var.current_player = var.current_player.next()
									var.current_player.info()

									#display
									var.window.blit(var.background_empty, (0,0))

									layers.letters_on_board.draw(var.window)
									#TODO ? draw hand_holder ?
									var.current_player.hand.draw(var.window)
									layers.buttons_on_screen.draw(var.window)

									var.current_background_no_text = var.window.copy()
									ui_text.drawText()

									var.current_background = var.window.copy()

									TURN += 1

									need_update = True



							#------ RELEASE CLIC ON CONFIRM BUTTON -------
							if ( (button_confirm.collide(cursor_pos_x, cursor_pos_y) == True) and (button_confirm.is_pushed) and (button_confirm.is_enabled)):
								
								layers.buttons_on_screen.add(button_end_turn)
								layers.buttons_on_screen.remove(button_confirm)
								button_confirm.release()

								layers.buttons_on_screen.add(button_draw)
								layers.buttons_on_screen.remove(button_cancel)
								button_cancel.release()

								need_update = True



								var.discard_holder_displayed = False
								discarded_letters = []

								for index in var.discard_holder_state :
									if index != 0 :

										letter = var.current_player.hand.findByIndex(index)
										var.current_player.hand.remove(letter)
										discarded_letters.append(letter)

										logging.info("%s has discarded letter %s", var.current_player.name, letter.name)
										
								var.discard_holder_state = [0 for i in range (0, var.number_of_letters_per_hand)]

								#redraw letters
								index_hand = 0
								while len(var.bag_of_letters) > 0 and index_hand < var.number_of_letters_per_hand :
									if var.current_player.hand_state[index_hand] == 0 :
										random_int = randint(0,len(var.bag_of_letters)-1)
										drawn_letter = Letter(var.bag_of_letters[random_int], 0, 0)
										del(var.bag_of_letters[random_int])	

										var.current_player.hand_state[index_hand] = drawn_letter.id
										delta_x, delta_y = UI_LEFT_LIMIT, ui_text.current_player_turn.bottom_tiles+0.5*UI_INTERLIGNE
										drawn_letter.moveAtTile( delta_x + index_hand, delta_y )
										var.current_player.hand.add(drawn_letter)
										logging.info("%s has drawn letter %s", var.current_player.name, drawn_letter.name)

									index_hand += 1

								#put discarded letters in the bag of letters
								for letter in discarded_letters :
									var.bag_of_letters.append(letter.name)


								#create UI info pop up
								#TODO 7
								pop_up_text = ""
								if len(discarded_letters) == 1 :
									pop_up_text = var.current_player.name + " has discarded letter "
								else :
									pop_up_text = var.current_player.name + " has discarded letters "

								for letter in discarded_letters :
									if len(discarded_letters) > 1 : #more than one element
										if letter != discarded_letters[0] : #not first
											if letter != discarded_letters[-1] : #not last
												pop_up_text = pop_up_text+" , "
											else :
												pop_up_text = pop_up_text+" and "
												#TODO 7
									pop_up_text = pop_up_text+letter.name
								pop_up_text = pop_up_text+"."

								discarded_letters = []
								
								var.current_player = var.current_player.next()
								var.current_player.info()

								#display
								var.window.blit(var.background_empty, (0,0))

								layers.letters_on_board.draw(var.window)
								var.current_player.hand.draw(var.window)
								layers.buttons_on_screen.draw(var.window)

								var.current_background_no_text = var.window.copy()
								ui_text.drawText()

								var.current_background = var.window.copy()

								TURN += 1

								displayPopUp(pop_up_text)

								need_update = False



							#------ RELEASE CLIC ON SHUFFLE BUTTON -------

							#TODO : check if works properly

							elif ( enable_shuffle_letter and (button_shuffle.collide(cursor_pos_x, cursor_pos_y) == True) and (button_shuffle.is_pushed) ):
									button_shuffle.release()

									layers.buttons_on_screen.clear(var.window, var.background_empty)
									layers.buttons_on_screen.draw(var.window)
									need_update = True

									# ___ SHUFFLE ___

									pos_x = (UI_LEFT_LIMIT)
									pos_y = layers.hand_holder.sprites()[0].pos_y + 0.1

									shuffle(var.current_player.hand_state)


									pos_x = (UI_LEFT_LIMIT)
									pos_y = pos_y = layers.hand_holder.sprites()[0].pos_y + 0.1

									hand_state = []
									for index in var.current_player.hand_state :

										if index != 0:
											var.current_player.hand.findByIndex(index).moveAtTile(pos_x, pos_y)
										pos_x = pos_x + 1

									# ___ UPDATE DISPLAY ___
									var.current_player.hand.clear(var.window, var.background_empty)
									var.current_player.hand.draw(var.window)	

									need_update = True


							#------ RELEASE CLIC ON DRAW BUTTON -------
							elif ( ( (button_draw.collide(cursor_pos_x, cursor_pos_y) == True) and (button_draw.is_pushed) ) or ( (button_cancel.collide(cursor_pos_x, cursor_pos_y) == True) and (button_cancel.is_pushed) ) ):

								#discard holder not displayed yet
								if var.discard_holder_displayed == False :

									#not enough letters remaining
									if len(var.bag_of_letters) < var.number_of_letters_per_hand :

										button_draw.release()
										displayPopUp("Not enough remaining letters")

									else:										
										button_draw.release()
										layers.buttons_on_screen.remove(button_draw)	

										layers.buttons_on_screen.add(button_cancel)
										button_cancel.turnOnHighlighted()

										layers.buttons_on_screen.add(button_confirm)
										button_confirm.disable()

										layers.buttons_on_screen.remove(button_end_turn)


										#TODO9 - create a snapsot for later screen refresh ??? 
										discard_holder = layers.all.findByName("discard_holder")
										layers.hand_holder.add(discard_holder)

										#display
										layers.buttons_on_screen.draw(var.window)
										layers.hand_holder.draw(var.window)
										var.current_player.hand.draw(var.window)

										var.current_background = var.window.copy()
										var.discard_holder_displayed = True

										need_update = True

								#Discard holde already displayed
								elif var.discard_holder_displayed == True :

									if var.discard_holder_state == [0 for i in range (0, var.number_of_letters_per_hand)] :

										layers.buttons_on_screen.remove(button_cancel)
										layers.buttons_on_screen.add(button_draw)

										layers.buttons_on_screen.remove(button_confirm)
										layers.buttons_on_screen.add(button_end_turn)

										button_cancel.release()
										button_draw.turnOnHighlighted()

										discard_holder = layers.all.findByName("discard_holder")
										layers.hand_holder.remove(discard_holder)
										layers.hand_holder.clear(var.window, var.background_empty)

										#update
										layers.buttons_on_screen.draw(var.window)
										layers.hand_holder.draw(var.window)
										var.current_player.hand.draw(var.window)
										var.current_background = var.window.copy()

										var.discard_holder_displayed = False
										need_update = True


									else :
										#TODO7 in different languages
										button_cancel.release()
										displayPopUp("Attention lettres dans la pioche")


							#------ RELEASE CLIC AWAY FROM BUTTON (VISUAL) -------
							else :
								if not CURSOR_IS_OPEN_HAND == True :
									pygame.mouse.set_cursor(*arrow)
								#force update of mouse pointer
								#pygame.event.post(pygame.event.Event(pygame.MOUSEMOTION))
								
								for button in layers.buttons_on_screen :
									if button.is_pushed :
										button.release() #release all pushed buttons
										if button.collide(cursor_pos_x, cursor_pos_y) :
											button.turnOnHighlighted()
										else :
											button.turnOffHighlighted()

										layers.buttons_on_screen.clear(var.window, var.background_empty)
										layers.buttons_on_screen.draw(var.window)
										need_update = True										

							if need_update :
								#pygame.event.post(pygame.event.Event(pygame.MOUSEMOTION))
								pygame.display.update()
							

						#------ PLAY A SELECTED LETTER-------
						if var.current_action == 'PLAY_A_LETTER' and len(layers.selected_letter) == 1 :

							#TODO to improve based on "is a mouse" or "is a touchescreen"
							#not a simple fast clic
							if ( timer > 200 )  :

								selected_letter = layers.selected_letter.sprites()[0]
								letter_center_x, letter_center_y = selected_letter.rect.centerx, selected_letter.rect.centery 

								move_my_letter = False

								#------ CLIC ON THE HAND HOLDER ? -------
								if var.hand_holder.collide(letter_center_x, letter_center_y) :

									index_in_hand = var.hand_holder.indexAtPos(letter_center_x)
									delta_x, delta_y = var.hand_holder.pos_x + 0.1, var.hand_holder.pos_y + 0.1


									#------ EMPTY SPOT ? -------
									if var.current_player.hand_state[index_in_hand] == 0 :
										move_my_letter = True

									#----------------------NOT AN EMPTY SLOT--------------------	
									else :

										letter_id = var.current_player.hand_state[index_in_hand]
										old_letter = var.current_player.hand.findByIndex(letter_id)

										offset_x = selected_letter.rect.centerx - old_letter.rect.centerx
										if offset_x >= 0 : #want to push to the left
											direction = -1
										else :
											direction = +1

										if old_letter.canMove(direction) : #no need to push other letters

											old_letter.moveAtTile( delta_x + index_in_hand + direction, delta_y )
											var.current_player.hand_state[index_in_hand+direction] = old_letter.id
											var.current_player.hand_state[index_in_hand] = 0

											move_my_letter = True


										else : #need to push
											#try backward
											if old_letter.canMove(-direction) :

												old_letter.moveAtTile( delta_x + index_in_hand - direction, delta_y )
												var.current_player.hand_state[index_in_hand-direction] = old_letter.id
												var.current_player.hand_state[index_in_hand] = 0

												move_my_letter = True
											else :
												pass


									if move_my_letter == True :
									
										selected_letter.moveAtTile( delta_x + index_in_hand, delta_y )
										var.current_player.hand_state[index_in_hand] = selected_letter.id

										#change letter from layers
										var.current_player.hand.add(selected_letter)
										layers.selected_letter.remove(selected_letter)

										#refresh screen
										layers.selected_letter.clear(var.window, var.current_background)

										var.current_player.hand.clear(var.window, var.current_background)
										var.current_player.hand.draw(var.window)

										if display_new_score_in_real_time :
											incrementPredictedScore()
											layers.mask_text.draw(var.window)
											#TODO4 display predicted score

										var.current_background = var.window.copy()

										pygame.mouse.set_cursor(*open_hand)
										CURSOR_IS_OPEN_HAND = True

										pygame.display.update()											

										var.current_action = "SELECT_A_LETTER"


								#------ Clic on the discard holder ? -------
								if var.discard_holder_displayed and var.discard_holder.collide(letter_center_x, letter_center_y) :

									index_in_hand = var.discard_holder.indexAtPos(letter_center_x)
									delta_x, delta_y = var.discard_holder.pos_x + 0.1, var.discard_holder.pos_y + 0.1

									#------ EMPTY SPOT ? -------
									if var.discard_holder_state[index_in_hand] == 0 :
										move_my_letter = True
										
									else :
										#TODO1 push letters
										pass

									if move_my_letter == True :
										button_confirm.enable()
									
										selected_letter.moveAtTile( delta_x + index_in_hand, delta_y )
										var.discard_holder_state[index_in_hand] = selected_letter.id

										#change letter from layers
										var.current_player.hand.add(selected_letter)
										layers.selected_letter.remove(selected_letter)

										#refresh screen
										layers.selected_letter.clear(var.window, var.current_background)

										var.current_player.hand.clear(var.window, var.current_background)
										var.current_player.hand.draw(var.window)

										layers.buttons_on_screen.draw(var.window)

										var.current_background = var.window.copy()

										pygame.mouse.set_cursor(*open_hand)
										CURSOR_IS_OPEN_HAND = True

										pygame.display.update()											

										var.current_action = "SELECT_A_LETTER"


								#------ CLIC ON A TILE ON THE BOARD ? -------
								for tile in layers.tiles :

									if tile.collide(letter_center_x, letter_center_y) == True :

										if not var.discard_holder_displayed :
											tile_x_on_board = int( tile.pos_x - DELTA )
											tile_y_on_board = int( tile.pos_y - DELTA )

											#------ EMPTY TILE ? -------
											if var.current_board_state[tile_y_on_board][tile_x_on_board] == '?':

												selected_letter = layers.selected_letter.sprites()[0]

												selected_letter.moveAtTile( (tile_x_on_board + DELTA), (tile_y_on_board + DELTA) )
												var.current_board_state[tile_y_on_board][tile_x_on_board] = selected_letter.name

												layers.letters_just_played.add(selected_letter)								
												layers.selected_letter.remove(selected_letter)

												layers.selected_letter.clear(var.window, var.current_background)	
												layers.letters_just_played.draw(var.window)

												if display_new_score_in_real_time :
													incrementPredictedScore()
													layers.mask_text.draw(var.window)	
													#TODO4 display predicted score						

												pygame.mouse.set_cursor(*open_hand)
												CURSOR_IS_OPEN_HAND = True

												pygame.display.update()

												var.current_action = "SELECT_A_LETTER"

										elif var.discard_holder_displayed :
											#TODO 7 in other languages
											displayPopUp("You cannot play here")


		#~~~~~~ MOUSE MOTION ~~~~~~	
		if(event_type == pygame.MOUSEMOTION ):

			if not MUST_DISPLAY_POP_UP :

				mouse_pos = pygame.mouse.get_pos()
				cursor_pos_x = mouse_pos[0]
				cursor_pos_y = mouse_pos[1]

				#------ SELECT A LETTER ------ 
				if ( not var.a_button_is_pushed ) and var.current_action == 'SELECT_A_LETTER' :

					#------ CHANGE APPEARANCE OF BUTTONS (VISUAL) ------
					buttons_changed = False
					#TODO restrict area to boost performance
					for button in layers.buttons_on_screen :
						if button.is_enabled :
							if ( button.collide(cursor_pos_x, cursor_pos_y) == True ) and ( not button.is_highlighted ) and (not button.is_pushed ) :
								button.turnOnHighlighted()
								pygame.mouse.set_cursor(*hand)
								buttons_changed = True
							elif ( button.collide(cursor_pos_x, cursor_pos_y) == False ) and ( button.is_highlighted ) and (not button.is_pushed ):
								button.turnOffHighlighted()
								pygame.mouse.set_cursor(*arrow)
								buttons_changed = True

					if buttons_changed :
						layers.buttons_on_screen.clear(var.window, var.background_empty)
						layers.buttons_on_screen.draw(var.window)
						pygame.display.update()

					collide = False
					for letter in layers.letters_just_played.sprites() :
						if letter.collide(cursor_pos_x, cursor_pos_y) :
							collide = True
							pygame.mouse.set_cursor(*open_hand)
							CURSOR_IS_OPEN_HAND = True		
					for letter in var.current_player.hand :
						if letter.collide(cursor_pos_x, cursor_pos_y) :
							collide = True
							pygame.mouse.set_cursor(*open_hand)
							CURSOR_IS_OPEN_HAND = True

					#TODO
					if CURSOR_IS_OPEN_HAND == True and collide == False:
						pygame.mouse.set_cursor(*arrow)
						CURSOR_IS_OPEN_HAND = False


				#------ MOVE SELECTED LETTER ------ 
				if len(layers.selected_letter) == 1 :

					layers.selected_letter.sprites()[0].moveAtPixels(cursor_pos_x - var.delta_pos_on_tile[0], cursor_pos_y - var.delta_pos_on_tile[1])

					#TODO8 possible display problem to solve (flickering around other letters when moving a letter)
					layers.selected_letter.clear(var.window, var.current_background)
					layers.selected_letter.draw(var.window)

					pygame.display.update()


				#------ INFO ABOUT HOVERED TILE ------
				#TODO improve logic for better performance
				if display_type_of_tile_on_hoovering :
					if var.current_action == 'SELECT_A_LETTER' or var.current_action == 'PLAY_A_LETTER':
						cursor_on_a_special_tile = False

						#Is cursor on a special tile ?
						for tile in layers.tiles :
							if tile.collide(cursor_pos_x, cursor_pos_y) :
								if  ( tile.name != 'normal' ) :
									cursor_on_a_special_tile = True

									#TODO using layers
									#pop up not already displayed for this tile
									if tile.id != ui_text.id_tile_pop_up :

										#remove previously displayed text
										layers.background.draw(var.window)
										layers.tiles.draw(var.window)
										layers.hand_holder.draw(var.window)

										layers.buttons_on_screen.draw(var.window)
										layers.letters_on_board.draw(var.window)
										layers.letters_just_played.draw(var.window)
										var.current_player.hand.draw(var.window)

										var.current_background_no_text = var.window.copy()
										ui_text.drawText()

										ui_text.drawHelpPopPup(tile, tile.rect.x+int((2/60.0)*var.tile_size), tile.rect.y+var.tile_size-int((2/60.0)*(var.tile_size)))

										var.current_background = var.window.copy()
										layers.selected_letter.draw(var.window)
										pygame.display.update()

										ui_text.id_tile_pop_up = tile.id
										ui_text.pop_up_displayed = True
										break

						#If cursor on a normal tile
						if ( not cursor_on_a_special_tile and ui_text.pop_up_displayed ):
							#remove previously displayed text
							layers.background.draw(var.window)
							layers.tiles.draw(var.window)
							layers.hand_holder.draw(var.window)

							layers.buttons_on_screen.draw(var.window)
							layers.letters_on_board.draw(var.window)
							layers.letters_just_played.draw(var.window)
							var.current_player.hand.draw(var.window)

							var.current_background_no_text = var.window.copy()
							ui_text.drawText()
							
							var.current_background = var.window.copy()
							layers.selected_letter.draw(var.window)
							pygame.display.update()

							ui_text.id_tile_pop_up = 0
							ui_text.pop_up_displayed = False



	#display fps
	#logging.debug('fps : %s', str(fps_clock.get_fps() ) )

	if MUST_DISPLAY_POP_UP :
		if FRAMES_BEFORE_POP_UP_DISAPPEAR > 0 :
			FRAMES_BEFORE_POP_UP_DISAPPEAR -= 1
		else :
			MUST_DISPLAY_POP_UP = False
			FRAMES_BEFORE_POP_UP_DISAPPEAR = 200
			layers.pop_up.empty()
			#force update of  mouse pointer
			if len(layers.selected_letter) == 1 :
				pygame.mouse.set_cursor(*open_hand)
			pygame.event.post(pygame.event.Event(pygame.MOUSEMOTION))
			pygame.display.update()

logging.info("")
logging.info("Game has ended")
logging.info("")
logging.info("_________END OF LOG___________")
