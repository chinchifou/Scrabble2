#~~~~~~~~~ MAIN ~~~~~~~~~


#~~~~~~ IMPORTS ~~~~~~

#Standard library imports
from os import path
from os import makedirs

from math import floor
from random import randint, shuffle, choice

import platform

import ctypes

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

global DELTA, UI_LEFT_LIMIT, UI_LEFT_INDENT, UI_INTERLIGNE
#delta expressed in tiles from top left corner of the Window
DELTA = 1.5
#Left limit for text of the user interface
UI_LEFT_LIMIT = DELTA + TILES_PER_LINE + DELTA + 1.0
#Left limit with an identation in the user interface text
UI_LEFT_INDENT = UI_LEFT_LIMIT + 0.5
#Size expressed in tile of the space between two consecutive line of text
UI_INTERLIGNE = 1.0

global PLAYERS, STEP, MAPING_STEP_MAX_SCORE
#all players
PLAYERS = []
# Turn number
STEP = 0
#for a step give the corresponding max number of points
MAPING_STEP_MAX_SCORE = {
3 : 16,
6 : 34,
9: 26
}

global CURSOR_IS_OPEN_HAND
CURSOR_IS_OPEN_HAND = False


global MUST_DIPSLAY_POP_UP, FRAMES_BEFORE_POP_UP_DISAPPEAR
# boolean to indicate wether to display pop_up or not
MUST_DIPSLAY_POP_UP = False
# number of frames before the pop_up disappear
FRAMES_BEFORE_POP_UP_DISAPPEAR = 200

#Folders' paths
path_log = path.abspath('../log/')
if not path.exists(path_log):
	makedirs(path_log)

path_icon = path.abspath('../materials/images/icon/')
path_background = path.abspath('../materials/images/background/')

path_buttons = path.abspath('../materials/images/assets/buttons/primary/') #changed later on
path_buttons_french = path.abspath('../materials/images/assets/buttons/primary/french/')
path_buttons_english = path.abspath('../materials/images/assets/buttons/primary/english/')
path_buttons_menu = path.abspath('../materials/images/assets/buttons/side_menu/')

path_letters = path.abspath('../materials/images/assets/letters/') #changed later on
path_letters_french = path.abspath('../materials/images/assets/letters/french/')
path_letters_english = path.abspath('../materials/images/assets/letters/english/')

path_tiles = path.abspath('../materials/images/assets/tiles/')
path_music = path.abspath('../materials/sounds/')


#----- Changing a runtime -----
#class to store game variable
class GameVariable():
	def __init__(self):
		self.monitor_resolution = 0
		self.window_width = 0
		self.window_height = 0

		self.tile_size = 0.0
		self.delta_pos_on_tile = 0.0

		self.number_of_letters_per_hand = 7

		self.bag_of_letters = []
		self.current_board_state = [ ['?' for i in range(TILES_PER_LINE)] for j in range(TILES_PER_LINE) ]

		self.last_words_and_scores = {}
		self.predicted_score = 0
		
		self.current_player = []

		self.current_action = 'SELECT_A_LETTER'

		self.background_empty = []
		self.background_no_letter = []
		self.current_background = []
		self.background_empty = []
		self.background_pop_up_empty = []
		self.current_background_no_text = []

		self.points_for_scrabble = 50

var = GameVariable()

#class used to print error messages in console and log file
class ErrorPrinter():

	def not_enough_letters(self):
		logging.error('! ! ! . . . . . . . . ! ! !')
		logging.error('INITIAL SETTINGS ERROR : not enough letters at game start.')
		logging.error('Some player has less letters than the others.')
		logging.error('Possible solutions :')
		logging.error('  1. add more letters')
		logging.error('  2. reduce number of letters authorized per player')
		logging.error('  3. reduce the number of players')
		logging.error('! ! ! . . . . . . . . ! ! !')
		logging.error('')

		print('INITIAL SETTINGS ERROR : not enough letters at game start.')
		print('Some player has less letters than the others.')
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
		self.victory = pygame.mixer.Sound(path.join(path_music, 'tf2_achievement_unlocked_sound.ogg'))
		self.scrabble = pygame.mixer.Sound(path.join(path_music, 'victory_fanfare.ogg'))

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
		#size for the progress bar text
		self.PROGRESS_BAR = 0.46

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

		self.progress_bar = GroupOfSprites()
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
class UserInterFacePopUp(UIText):

	def __init__(self, text, line_heigh, bold, pos_in_tiles, text_color, background_color):
		UIText.__init__(self, text, line_heigh, bold, pos_in_tiles)
		self.text_color = text_color
		self.background_color = background_color

	def drawAt(self, pixels_pos_x, pixels_pos_y):

		self.moveAtPixels(pixels_pos_x, pixels_pos_y)
		text = self.font.render(self.text, 1, self.text_color, self.background_color )
		window.blit( text, (self.pos_x_pix, self.pos_y_pix) )


#class storing userface interface text and displaying them
class UITextPrinter():

	def __init__(self, ui_content):

		"""		
		#UI text init
		self.current_player_turn = UIText(ui_content['current_player_turn'][language_id], 1.0, False, ( UI_LEFT_LIMIT, 3*UI_INTERLIGNE) )

		self.next_player_hand_header = UIText(ui_content['next_player_hand'][language_id], LINE_HEIGHT.NORMAL, True, ( UI_LEFT_LIMIT, self.current_player_turn.bottom_tiles+1.2+1*UI_INTERLIGNE) )

		self.next_player_hand = UIText("", LINE_HEIGHT.NORMAL, False, ( UI_LEFT_INDENT, self.next_player_hand_header.pos_y+1) )

		if display_next_player_hand :
			self.scores = UIText(ui_content['scores'][language_id], 1.0, True, ( UI_LEFT_LIMIT, self.next_player_hand.bottom_tiles+UI_INTERLIGNE) )
		else :
			self.scores = UIText(ui_content['scores'][language_id], LINE_HEIGHT.SUBTITLE, False, ( UI_LEFT_LIMIT, self.current_player_turn.bottom_tiles+2+UI_INTERLIGNE) )

		self.player_score = UIText(ui_content['player_score'][language_id], LINE_HEIGHT.NORMAL, False, ( UI_LEFT_INDENT, self.scores.bottom_tiles) )

		#previous turn summary
		if False :
			self.previous_turn_summary = UIText( ui_content['previous_turn_summary'][language_id], LINE_HEIGHT.NORMAL, True, ( UI_LEFT_LIMIT, self.scores.bottom_tiles+(0.8*len(players_names))+UI_INTERLIGNE ) )

		self.word_and_points = UIText ( ui_content['word_and_points'][language_id], LINE_HEIGHT.NORMAL, False, ( UI_LEFT_INDENT, self.player_score.bottom_tiles )  )		

		self.nothing_played = UIText( ui_content['nothing_played'][language_id], LINE_HEIGHT.NORMAL, False, (UI_LEFT_LIMIT, self.scores.bottom_tiles+(0.8*len(players_names))+UI_INTERLIGNE) )

		#Scrabble obtained
		if False :
			self.scrabble_obtained = UIText(ui_content['scrabble_obtained'][language_id], LINE_HEIGHT.NORMAL, False, (UI_LEFT_INDENT, self.previous_turn_summary.bottom_tiles) )
		
		#remaining letters
		if False :
			self.remaining_letters = UIText( ui_content['remaining_letters'][language_id], LINE_HEIGHT.NORMAL, False, (UI_LEFT_LIMIT, self.previous_turn_summary.bottom_tiles) )

			self.remaining_letter = UIText( ui_content['remaining_letter'][language_id], LINE_HEIGHT.NORMAL, False, (UI_LEFT_LIMIT, self.previous_turn_summary.bottom_tiles) )
		
			self.no_remaining_letter = UIText( ui_content['no_remaining_letter'][language_id], LINE_HEIGHT.NORMAL, False, (UI_LEFT_LIMIT, self.previous_turn_summary.bottom_tiles) )
		"""
		#hardcoded help pop-up
		self.id_tile_pop_up = 0
		self.pop_up_displayed = False

		self.double_letter = UserInterFacePopUp( ui_content['double_letter'][language_id], LINE_HEIGHT.NORMAL, False, (0, 0), COLOR.BLACK, COLOR.BLUE_LIGHT )
		self.triple_letter = UserInterFacePopUp( ui_content['triple_letter'][language_id], LINE_HEIGHT.NORMAL, False, (0, 0), COLOR.BLACK, COLOR.BLUE_DEEP )

		self.double_word = UserInterFacePopUp( ui_content['double_word'][language_id], LINE_HEIGHT.NORMAL, False, (0, 0), COLOR.BLACK, COLOR.RED_LIGHT )
		self.triple_word = UserInterFacePopUp( ui_content['triple_word'][language_id], LINE_HEIGHT.NORMAL, False, (0, 0), COLOR.BLACK, COLOR.RED_DEEP )

		hand_holder = layers.hand_holder.sprites()[0]

		# ___ UI TEXT init ___
		self.header = UIText("Marquez le plus de points possible.", LINE_HEIGHT.SUBTITLE, False, ( UI_LEFT_LIMIT, hand_holder.pos_y - 1.0) )
		
		self.max_score = UIText("Score maximal atteignable : ", LINE_HEIGHT.NORMAL, False, ( UI_LEFT_LIMIT, hand_holder.pos_y + 1.2 + 1.25 + 1) )	

		self.score_header = UIText("Score prévisionnel : ", LINE_HEIGHT.NORMAL, False, ( UI_LEFT_LIMIT, self.max_score.bottom_tiles + 0.75) )
		self.score = UIText("99", LINE_HEIGHT.SUBTITLE, False, ( UI_LEFT_LIMIT + self.score_header.width, self.score_header.pos_y-0.05) )

		self.texts_suggest_word =[
		UIText("Mots suggérés : ", LINE_HEIGHT.NORMAL, False, ( UI_LEFT_LIMIT, self.score.bottom_tiles + 1.5) ),
		UIText("NAVIR[E] - RAVIN[E] - AV[E]NIR", LINE_HEIGHT.NORMAL, False, ( UI_LEFT_LIMIT + 0.5, self.score.bottom_tiles + 1.5 + 1.25) )
		]


	#Custom UI text
	def drawText(self, step):

		hand_holder = layers.hand_holder.sprites()[0]

		# ___ DISPLAY ON SCREEN ___
		#Header
		text = self.header.font.render( self.header.text, 1, COLOR.WHITE )
		window.blit(text, (self.header.pos_x_pix, self.header.pos_y_pix))

		pygame.draw.aaline(window, COLOR.GREY_LIGHT, (UI_LEFT_LIMIT*var.tile_size, (hand_holder.pos_y +1.2+1.25+0.5)*var.tile_size), ( (UI_LEFT_LIMIT+hand_holder.width)*var.tile_size, (hand_holder.pos_y +1.2+1.25+0.5)*var.tile_size) )

		text = self.max_score.font.render( self.max_score.text + str(MAPING_STEP_MAX_SCORE[step]), 1, COLOR.WHITE )
		window.blit(text, (self.max_score.pos_x_pix, self.max_score.pos_y_pix))

		#Scores header
		if display_new_score_in_real_time :	
			text = self.score_header.font.render(self.score_header.text, 1, COLOR.WHITE )
			window.blit(text, (self.score_header.pos_x_pix, self.score_header.pos_y_pix))

			if var.predicted_score > 0 :
				self.score.font.set_bold(1)
				text = self.score.font.render(str(var.predicted_score), 1, COLOR.BLUE_LIGHT )
				self.score.font.set_bold(0)
			else :
				text = self.score.font.render(str(var.predicted_score), 1, COLOR.WHITE )
			window.blit(text, (self.score.pos_x_pix, self.score.pos_y_pix) )

			pygame.draw.aaline(window, COLOR.GREY_LIGHT, (UI_LEFT_LIMIT*var.tile_size, (self.score.bottom_tiles + 0.5)*var.tile_size), ( (UI_LEFT_LIMIT+hand_holder.width)*var.tile_size, (self.score.bottom_tiles + 0.5)*var.tile_size ) )

		if suggest_word :
			for text_it in self.texts_suggest_word :
				window.blit( text_it.font.render(text_it.text, 1, COLOR.WHITE), (text_it.pos_x_pix, text_it.pos_y_pix) )



	"""
	#Draw UI text
	def drawText(self, *args):

		custom_color = COLOR.WHITE
		for arg in args:
			custom_color = arg

		#Current player hand
		text = self.current_player_turn.font.render( self.current_player_turn.text.replace('<CURRENT_PLAYER>',var.current_player.name), 1, COLOR.GREY_LIGHT )
		window.blit(text, (self.current_player_turn.pos_x_pix, self.current_player_turn.pos_y_pix))		

		
		#display next player hand
		if display_next_player_hand :
			#Next player hand header
			text = self.next_player_hand_header.font.render( self.next_player_hand_header.text.replace('<NEXT_PLAYER>',var.current_player.next().name), 1, COLOR.GREY_LIGHT )
			window.blit(text, (self.next_player_hand_header.pos_x_pix, self.next_player_hand_header.pos_y_pix))

			#Next player hand content
			str_hand = ""
			for index in var.current_player.next().hand_state :
				letter_to_display = var.current_player.next().hand.findByIndex(index) 
				if letter_to_display == None :
					str_hand += ' '
				else :
					str_hand += str ( letter_to_display.name ) + "  " 

			text = self.next_player_hand.font.render( str_hand , 1, COLOR.GREY_LIGHT )
			window.blit(text, (self.next_player_hand.pos_x_pix, self.next_player_hand.pos_y_pix))

		#Scores header
		if display_new_score_in_real_time :
			text = self.scores.font.render( self.scores.text, 1, COLOR.GREY_LIGHT )
			window.blit(text, (self.scores.pos_x_pix, self.scores.pos_y_pix))		

			#text = self.player_score.font.render( self.player_score.text.replace('<SCORE>', str(var.current_player.score) ), 1, COLOR.GREY_LIGHT )
			#window.blit(text, (self.player_score.pos_x_pix, self.player_score.pos_y_pix))

			#score of each player
			pos_y_delta = 0
			for player in PLAYERS :
				if ( player == var.current_player ) :
					self.player_score.font.set_bold(1)
					if var.predicted_score == 0 : #move does not give points
						text = self.player_score.font.render( self.player_score.text.replace('_',' ').replace('<PLAYER>', player.name).replace('<SCORE>', str(player.score)), 1, custom_color )
					else :
						text = self.player_score.font.render( self.player_score.text.replace('_',' ').replace('<PLAYER>', player.name).replace('<SCORE>', str(player.score) + " (+" +str(var.predicted_score)) + ")" , 1, custom_color )
					self.player_score.font.set_bold(0)
					window.blit(text, (self.player_score.pos_x_pix+(( pos_y_delta+0.2)*var.tile_size), self.player_score.pos_y_pix+(( pos_y_delta+0.4)*var.tile_size) ) )
				else :
					text = self.player_score.font.render( self.player_score.text.replace('_',' ').replace('<PLAYER>', player.name).replace('<SCORE>', str(player.score)), 1, COLOR.GREY_LIGHT )
					window.blit(text, (self.player_score.pos_x_pix, self.player_score.pos_y_pix+(pos_y_delta*var.tile_size) ) )
				pos_y_delta += 0.8

		#previous turn summary
		if False :
			if len(var.last_words_and_scores) > 0 :

				#header
				text = self.previous_turn_summary.font.render( self.previous_turn_summary.text.replace('<PREVIOUS_PLAYER>',var.current_player.previous().name), 1, COLOR.GREY_LIGHT )
				window.blit(text, (self.previous_turn_summary.pos_x_pix, self.previous_turn_summary.pos_y_pix))

				pos_y_delta = 0
				for association in var.last_words_and_scores :
					if association[0] == "!! SCRABBLE !!" :
						text = self.scrabble_obtained.font.render( self.scrabble_obtained.text.replace('<PREVIOUS_PLAYER>',var.current_player.previous().name).replace('<SCRABBLE_POINTS>', str(var.points_for_scrabble)), 1, COLOR.RED_DEEP )
						window.blit(text, (self.scrabble_obtained.pos_x_pix, self.scrabble_obtained.pos_y_pix+(pos_y_delta*var.tile_size)))
					else :		
						text = self.word_and_points.font.render( self.word_and_points.text.replace('<WORD>',association[0]).replace('<POINTS>', str(association[1])), 1, COLOR.GREY_LIGHT )
						window.blit(text, (self.word_and_points.pos_x_pix, self.word_and_points.pos_y_pix+(pos_y_delta*var.tile_size)))
					pos_y_delta += 0.8

			else :
				#nothing played
				text = self.nothing_played.font.render( self.nothing_played.text.replace('<PREVIOUS_PLAYER>',var.current_player.previous().name), 1, COLOR.GREY_LIGHT )
				window.blit(text, (self.nothing_played.pos_x_pix, self.nothing_played.pos_y_pix) )

		#remaining_letters
		if False :

			if len(var.bag_of_letters) == 0 :
				text = self.no_remaining_letter.font.render( self.no_remaining_letter.text, 1, COLOR.GREY_LIGHT )
					
				if len(var.last_words_and_scores) > 0 :
					window.blit(text, (self.no_remaining_letter.pos_x_pix, self.no_remaining_letter.pos_y_pix+ (pos_y_delta+UI_INTERLIGNE)*var.tile_size ) )
				else :
					window.blit(text, (self.no_remaining_letter.pos_x_pix, self.nothing_played.pos_y_pix+ (2*UI_INTERLIGNE)*var.tile_size ) )

			elif len(var.bag_of_letters) == 1 :
				text = self.remaining_letter.font.render( self.remaining_letter.text, 1, COLOR.GREY_LIGHT )
					
				if len(var.last_words_and_scores) > 0 :
					window.blit(text, (self.remaining_letter.pos_x_pix, self.remaining_letter.pos_y_pix+ (pos_y_delta+UI_INTERLIGNE)*var.tile_size ) )
				else :
					window.blit(text, (self.remaining_letter.pos_x_pix, self.nothing_played.pos_y_pix+ (2*UI_INTERLIGNE)*var.tile_size ) )

			else :
				text = self.remaining_letters.font.render( self.remaining_letters.text.replace( '<LETTERS_REMAINING>', str(len(var.bag_of_letters)) ), 1, COLOR.GREY_LIGHT )

				if len(var.last_words_and_scores) > 0 :
					window.blit(text, (self.remaining_letters.pos_x_pix, self.remaining_letters.pos_y_pix+ (pos_y_delta+UI_INTERLIGNE)*var.tile_size ) )
				else :
					window.blit(text, (self.remaining_letters.pos_x_pix, self.nothing_played.pos_y_pix+ (2*UI_INTERLIGNE)*var.tile_size ) )
			"""


	def drawTextPopUp(self, step):

		pop_up_window = layers.pop_up_window.sprites()[0]
		limit_left = tiles1( pop_up_window.rect.left )
		limit_top = tiles1( pop_up_window.rect.top )

		if step == 1 :
			all_texts = [
			UIText( "Bonjour !", LINE_HEIGHT.TITLE, True, (limit_left+1, limit_top+2) ),
			UIText( "Je suis votre ergonome virtuelle.", LINE_HEIGHT.TITLE, True, (limit_left+1, limit_top+4) ),
			UIText( "Pouvez-vous m'aider à améliorer ce logiciel ?", LINE_HEIGHT.TITLE, True, (limit_left+1, limit_top+6) )
			]
			"""
			buble_points = [
			pixels(2.5, 2.5),
			pixels(23.5, 2.5),
			pixels(23.5, 10.5),
			pixels(24.5, 11.25), <-Mouse
			pixels(23.5, 11.1),
			pixels(23.5, 14),
			pixels(2.5, 14)
			]
			"""
			buble_points = [
			pixels(2.5, 3.5),
			pixels(23.5, 3.5),
			pixels(23.5, 7.5),
			pixels(24.5, 10.25),
			pixels(23.5, 8.5),
			pixels(23.5, 9.5),
			pixels(2.5, 9.5)
			]		

		elif step == 2 :
			all_texts = [
			UIText( "Votre objectif :", LINE_HEIGHT.TITLE, True, (limit_left+1, limit_top+2) ),
			UIText( "Marquer le plus de points possibles en plaçant un mot", LINE_HEIGHT.TITLE, False, (limit_top+1, limit_top+3.5) ),
			UIText( "sur le plateau.", LINE_HEIGHT.TITLE, False, (limit_top+1, limit_top+4.5) ),
			UIText( "Astuce :", LINE_HEIGHT.TITLE, True, (limit_left+1, limit_top+6.5) ),
			UIText( "Les cases bonus rapportent plus de points.", LINE_HEIGHT.TITLE, False, (limit_left+1, limit_top+8) )
			]
			buble_points = [
			pixels(2.5, 3.5),
			pixels(23.5, 3.5),
			pixels(23.5, 8.5),
			pixels(24.5, 10.25),
			pixels(23.5, 9.1),
			pixels(23.5, 11.5),
			pixels(2.5, 11.5)
			]

		elif step == 4 :
			all_texts = [
			UIText( "Alors, comment cela vous a t'il paru ? Je pense que l'on peut faire mieux ...", LINE_HEIGHT.NORMAL, False, (limit_left+1, limit_top+0.5) ),
			UIText( "Aidez moi à améliorer l'ergonomie de ce logiciel en répondant à ces questions.", LINE_HEIGHT.NORMAL, False, (limit_left+1, limit_top+1.5) ),
			UIText( "Marquer des points vous a paru :", LINE_HEIGHT.NORMAL, True, (limit_left+1, limit_top+3) ),

			UIText( "Facile", LINE_HEIGHT.NORMAL, False, (limit_left+2.75+0.75, limit_top+7.25) ),			
			UIText( "Normal", LINE_HEIGHT.NORMAL, False, (limit_left+2.75+4+0.6, limit_top+7.25) ),
			UIText( "Difficile", LINE_HEIGHT.NORMAL, False, (limit_left+2.75+8+0.5, limit_top+7.25) ),


			UIText( "Cochez ce qui vous a posé problème :", LINE_HEIGHT.NORMAL, True, (limit_left+1, limit_top+8.25) ),
			UIText( "Réussir à composer un mot", LINE_HEIGHT.NORMAL, False, (limit_left+2.75, limit_top+9.75) ),
			UIText( "Marquer le plus de points possible", LINE_HEIGHT.NORMAL, False, (limit_left+2.75, limit_top+11.25) )
			]
			buble_points = [
			pixels(2.25, 2.25),
			pixels(23.5, 2.25),
			pixels(23.5, 8.5),
			pixels(24.5, 10.25),
			pixels(23.5, 9.1),
			pixels(23.5, 14.3),
			pixels(2.25, 14.3)
			]
		elif step == 5 :
			all_texts = [
			UIText( "J'ai pris en compte vos remarques.", LINE_HEIGHT.NORMAL, True, (limit_left+1, limit_top+1.5) ),
			UIText( "Voici une nouvelle version dans laquelle j'ai apporté quelques améliorations.", LINE_HEIGHT.NORMAL, False, (limit_left+1, limit_top+2.5) ),
			UIText( "Améliorations :", LINE_HEIGHT.NORMAL, True, (limit_left+1, limit_top+4.5) ),
			UIText( "Pour composer un mot :", LINE_HEIGHT.NORMAL, False, (limit_left+2, limit_top+5.5) ),
			UIText( "> Pouvoir réorganiser mes lettres", LINE_HEIGHT.NORMAL, False, (limit_left+4, limit_top+6.75) ),
			UIText( "Pour marquer le plus de points possible :", LINE_HEIGHT.NORMAL, False, (limit_left+2, limit_top+8.25) ),
			UIText( "> Afficher l'effet des cases bonus au survol", LINE_HEIGHT.NORMAL, False, (limit_left+4, limit_top+9.5) )
			]
			buble_points = [
			pixels(2.5, 3.25),
			pixels(23.5, 3.25),
			pixels(23.5, 8.5),
			pixels(24.5, 10.25),
			pixels(23.5, 9.1),
			pixels(23.5, 12.5),
			pixels(2.5, 12.5)
			]
		elif step == 7 :
			all_texts = [
			UIText( "Alors, comment vous a paru cette nouvelle version ?", LINE_HEIGHT.NORMAL, True, (limit_top+1, limit_top+1.5) ),
			UIText( "Marquer des points vous a paru :", LINE_HEIGHT.NORMAL, True, (limit_left+1, limit_top+3) ),

			UIText( "Facile", LINE_HEIGHT.NORMAL, False, (limit_left+2.75+0.75, limit_top+7.25) ),			
			UIText( "Normal", LINE_HEIGHT.NORMAL, False, (limit_left+2.75+4+0.6, limit_top+7.25) ),
			UIText( "Difficile", LINE_HEIGHT.NORMAL, False, (limit_left+2.75+8+0.5, limit_top+7.25) ),

			UIText( "Cochez ce qui vous a posé problème :", LINE_HEIGHT.NORMAL, True, (limit_left+1, limit_top+8) ),
			UIText( "Réussir à composer un mot", LINE_HEIGHT.NORMAL, False, (limit_left+2.75, limit_top+9.25) ),
			UIText( "Marquer le plus de points possible", LINE_HEIGHT.NORMAL, False, (limit_left+2.75, limit_top+10.75) )
			]
			buble_points = [
			pixels(2.25, 3.25),
			pixels(23.5, 3.25),
			pixels(23.5, 8.5),
			pixels(24.5, 10.25),
			pixels(23.5, 9.1),
			pixels(23.5, 14),
			pixels(2.25, 14)
			]
		elif step == 8 :
			"""
			all_texts = [
			UIText( "J'ai pris en compte ces nouvelles remarques.", LINE_HEIGHT.NORMAL, True, (limit_left+1, limit_top+0.5) ),
			UIText( "Voici une dernière version dans laquelle j'ai apporté quelques améliorations.", LINE_HEIGHT.NORMAL, False, (limit_top+1, limit_top+1.5) ),
			UIText( "Améliorations :", LINE_HEIGHT.NORMAL, True, (limit_left+1, limit_top+3) ),
			UIText( "Pour composer un mot :", LINE_HEIGHT.NORMAL, False, (limit_left+2, limit_top+4.25) ),
			UIText( "Pouvoir réorganiser mes lettres", LINE_HEIGHT.NORMAL, False, (limit_left+4.25, limit_top+5.75) ),
			UIText( "Me proposer des mots possibles", LINE_HEIGHT.NORMAL, False, (limit_left+4.25, limit_top+7.25) ),
			UIText( "Pour marquer le plus de points possible :", LINE_HEIGHT.NORMAL, False, (limit_left+2, limit_top+8.75) ),
			UIText( "Afficher l'effet des cases bonus au survol", LINE_HEIGHT.NORMAL, False, (limit_left+4.25, limit_top+10.25) ),
			UIText( "Afficher mon score en temps réel", LINE_HEIGHT.NORMAL, False, (limit_left+4.25, limit_top+11.5) )
			]
			"""
			all_texts = [
			UIText( "J'ai pris en compte ces nouvelles remarques.", LINE_HEIGHT.NORMAL, True, (limit_left+1, limit_top+1.5) ),
			UIText( "Voici une dernière version dans laquelle j'ai apporté de nouvelles améliorations.", LINE_HEIGHT.NORMAL, False, (limit_top+1, limit_top+2.5) ),
			UIText( "Nouvelles améliorations :", LINE_HEIGHT.NORMAL, True, (limit_left+1, limit_top+4) ),
			UIText( "Pour composer un mot :", LINE_HEIGHT.NORMAL, False, (limit_left+2, limit_top+5.25) ),
			UIText( "> Me proposer des mots possibles", LINE_HEIGHT.NORMAL, False, (limit_left+4, limit_top+6.75) ),
			UIText( "Pour marquer le plus de points possible :", LINE_HEIGHT.NORMAL, False, (limit_left+2, limit_top+8.25) ),
			UIText( "> Afficher mon score en temps réel", LINE_HEIGHT.NORMAL, False, (limit_left+4, limit_top+9.75) )
			]
			buble_points = [
			pixels(2.5, 3.25),
			pixels(23.5, 3.25),
			pixels(23.5, 8.5),
			pixels(24.5, 10.25),
			pixels(23.5, 9.1),
			pixels(23.5, 13.3),
			pixels(2.5, 13.3)
			]
		elif step == 10 :			
			all_texts = [
			UIText( "Notre travail est maintenant terminé.", LINE_HEIGHT.SUBTITLE, False, (limit_left+1, limit_top+4) ),
			UIText( "Ensemble nous avons améliorer l'ergonomie de ce logiciel.", LINE_HEIGHT.SUBTITLE, False, (limit_left+1, limit_top+6) ),
			UIText( "Merci de votre participation !", LINE_HEIGHT.SUBTITLE, False, (limit_left+1, limit_top+7) ),
			UIText( "Un récapitulatif concernant l'ergonomie vous attend à la page suivante.", LINE_HEIGHT.SUBTITLE, False, (limit_left+1, limit_top+9) )
			]
			buble_points = [
			pixels(2.5, 5.5),
			pixels(23.5, 5.5),
			pixels(23.5, 10.5),
			pixels(24.5, 11.25),
			pixels(23.5, 11.1),
			pixels(23.5, 12.25),
			pixels(2.5, 12.25)
			]
		elif step == 11 :
			custom_height = 0.65
			all_texts = [
			UIText( "Comme nous venons de le voir, l'ergonomie c'est :", custom_height, False, (limit_left+1, limit_top+1) ),
			UIText( "> Ecouter et observer l'utilisateur pour cerner son besoin", custom_height, False, (limit_left+2, limit_top+2.75) ),
			UIText( "> Une science avec des méthodes pour concevoir et améliorer le logiciel", custom_height, False, (limit_left+2, limit_top+4) ),
			UIText( "> Recommencer et améliorer jusqu'à satisfaire l'utilisateur", custom_height, False, (limit_left+2, limit_top+5.25) ),
			UIText( "En fait, l'ergonomie c'est l'avenir !", custom_height, False, (limit_left+1, limit_left+7.5) ),
			UIText( "Apprenez-en plus en regardant notre vidéo de présentation.", custom_height, False, (limit_left+1, limit_top+9) ),
			UIText( "A bientôt !", custom_height, True, (limit_left+12.25, limit_top+11) ),
			]
			buble_points = [
			pixels(2.5, 2.5),
			pixels(23.5, 2.5),
			pixels(23.5, 10.5),
			pixels(24.5, 11.25),
			pixels(23.5, 11.1),
			pixels(23.5, 14),
			pixels(2.5, 14)
			]		

		for text_it in all_texts :
			window.blit( text_it.font.render(text_it.text, 1, COLOR.WHITE), (text_it.pos_x_pix, text_it.pos_y_pix) )

		pygame.draw.aalines( window, COLOR.GREY_LIGHT, True, buble_points, 1 )	

	"""
	def drawPopUpScore2(self, word):

		if len(word) > 0 :
			text = "Vous avez marqué "+str(var.current_player.score)+" points."
			ui_text = UIText( text, LINE_HEIGHT.SUBTITLE, False, (12, 9) )

		else :
			if ( len( layers.letters_just_played.sprites() ) > 0) :
				text = "Vous n'avez pas marqué de points."
				ui_text = UIText( text, LINE_HEIGHT.SUBTITLE, False, (12, 9) )
			else :
				text = "Déposer des lettres sur le plateau pour marquer des points."
				ui_text = UIText( text, LINE_HEIGHT.SUBTITLE, False, (12, 9) )


		ui_text.pos_x = 16 - round(ui_text.width / 2.0)
		ui_text.pos_y = 8 - round(ui_text.height / 2.0)
		ui_text.pos_x_pix, ui_text.pos_y_pix = pixels(ui_text.pos_x, ui_text.pos_y)


		layers.pop_up_score.sprites()[0].pos_x = ui_text.pos_x - 1
		layers.pop_up_score.sprites()[0].pos_y = ui_text.pos_y - 0.5

		layers.pop_up_score.sprites()[0].width = ui_text.width + 2
		layers.pop_up_score.sprites()[0].height = ui_text.height + 1

		layers.pop_up_score.sprites()[0].resize()


		layers.dark_filter.draw(window)
		layers.pop_up_score.draw(window)

		window.blit( ui_text.font.render(text, 1, COLOR.WHITE), (ui_text.pos_x_pix, ui_text.pos_y_pix) )
	"""

	def drawHelpPopPup(self, tile, pixel_pos_x, pixel_pos_y):
		if tile.name == 'double_letter' :
			self.double_letter.drawAt(pixel_pos_x, pixel_pos_y)
		elif tile.name == 'triple_letter':
			self.triple_letter.drawAt(pixel_pos_x, pixel_pos_y)
		elif tile.name == 'double_word'or tile.name == 'start':
			self.double_word.drawAt(pixel_pos_x, pixel_pos_y)
		elif tile.name == 'triple_word':
			self.triple_word.drawAt(pixel_pos_x, pixel_pos_y)



def createPopUp(ar_texts, position=(0,0), bounds=(32, 18), LINE_HEIGHT=0.7, margin_ratio=(1.0,1.0), interligne_ratio=0.5, time = 4000):

	# ___ Init ___
	FRAMES_BEFORE_POP_UP_DISAPPEAR = int(time / 20.0)

	nb_lignes = len(ar_texts)
	my_line_height = LINE_HEIGHT

	interligne = interligne_ratio * my_line_height

	left_margin, top_margin = my_line_height*margin_ratio[0], my_line_height*margin_ratio[1]
	window_pos_x, window_pos_y = position[0], position[1]

	to_move_in_the_center = ( position == (0,0) )


	# ___ Prevent to go out of the boudary ___
	max_nb_letters = 0
	longest_word = ""
	for text in ar_texts :
		if len(text) > max_nb_letters :
			max_nb_letters = len(text)
			longest_word = text

	test_font = pygame.font.SysFont("Calibri", floor(my_line_height*var.tile_size))
	initial_max_width = test_font.size(text)[0] / var.tile_size


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

		window_pos_x = (32 - window_width) / 2.0 
		window_pos_y = (18 - window_height) / 2.0


	# ___ create pop_up background surface ___
	pop_up_surface = pygame.Surface( pixels(window_width , window_height) )
	pop_up_surface.fill(COLOR.GREY_DEEP)
	pygame.draw.rect(pop_up_surface, COLOR.GREY_LIGHT, pygame.Rect( (0,0), pixels(window_width, window_height) ), 3)


	# ___ Create UI text objects ___
	ui_texts = []
	tmp_pos_x, tmp_pos_y = window_pos_x + left_margin, window_pos_y + top_margin
	for text in ar_texts :
		ui_texts.append( UIText( text, my_line_height, False, (tmp_pos_x, tmp_pos_y) ) )
		tmp_pos_y += my_line_height + interligne


	# ___ add text ___
	tmp_pos_y = top_margin
	for ui_text in ui_texts :
		pop_up_surface.blit( ui_text.font.render(ui_text.text, 1, COLOR.WHITE), pixels(left_margin, tmp_pos_y) )
		tmp_pos_y = tmp_pos_y + my_line_height + interligne


	#create complete pop_up
	return UI_Surface('pop_up', window_pos_x, window_pos_y, pop_up_surface)



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
	return ( (value_in_tiles*var.tile_size) )



#~~~~~~ GAME CLASSES ~~~~~~


#----- ResizableSprite -----
#add native capacity to be resized
class ResizableSprite(pygame.sprite.Sprite):

	#class attributes to count number of instances
	nb_created_instances = 0

	#received coordinates are expresed in tiles
	def __init__(self, name, pos_x, pos_y, transparent=False):

		#super class constructor
		pygame.sprite.Sprite.__init__(self, self.containers) #self.containers need to have a default container

		#unique id
		ResizableSprite.nb_created_instances += 1
		self.id = ResizableSprite.nb_created_instances

		self.name, self.pos_x, self.pos_y, self.transparent = name, pos_x, pos_y, transparent

		#load image
		if self.path != None :
			if self.transparent :
				self.image = loadTransparentImage(path.join(self.path, self.name.replace('*','joker')+'.png'))
			else :
				self.image = loadImage(path.join(self.path, self.name+'.png'))

		#auto detect width and height
		if not ( hasattr(self, 'width') and hasattr(self, 'height') ) :
			self.width, self.height = in_reference_tiles(self.image.get_width(), self.image.get_height())

		self.center = (pos_x + self.width/2, pos_y + self.height / 2)
		self.center_pix = pixels(self.center[0], self.center[1])

		#resize image
		self.image = pygame.transform.smoothscale(self.image, pixels(self.width, self.height, to_round=True ) )
		#set area to be displayed
		self.rect = pygame.Rect( pixels(self.pos_x, self.pos_y), pixels(self.width, self.height) )


	def resize(self):

		self.center_pix = pixels(self.center[0], self.center[1])
		#TODO to use for better collide detection

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


	def info(self) :
		logging.debug("Sprite info :")
		logging.debug("id : %s", self.id)
		logging.debug("name : %s", self.name)
		logging.debug("at position : %s, %s", self.pos_x, self.pos_y)
		logging.debug("pixel position is : %s, %s", self.rect.x, self.rect.y)
		logging.debug("width : %s / height : %s", self.width, self.height)
		logging.debug("pixel width : %s /  pixel height : %s", self.rect.width, self.rect.height)
		logging.debug("")

# ___ SUBCALSSES ___
#----- UI Surface -----
class UI_Surface(ResizableSprite):
	def __init__(self, name, pos_x, pos_y, surface):
		self.path = None
		self.image = surface

		ResizableSprite.__init__(self, name, pos_x, pos_y)

#----- UI Image -----
class UI_Image(ResizableSprite):
	def __init__(self, name, path, pos_x, pos_y, width, height):

		self.path = path
		self.name = name
		self.width, self.height = width, height

		ResizableSprite.__init__(self, name, pos_x, pos_y, transparent=True)


# ___ SPRITES ___ 

#----- Board -----
class Board(ResizableSprite):
	def __init__(self, name, pos_x, pos_y):

		self.path = path_background
		self.width, self.height = 32, 18

		ResizableSprite.__init__(self, name, pos_x, pos_y)


#----- Hand holder -----
class Hand_holder(ResizableSprite):
	def __init__(self, name, pos_x, pos_y, max_nb_letters):

		self.path = path_background
		self.width, self.height = 0.2 + var.number_of_letters_per_hand, 1.2
		self.max_nb_letters = max_nb_letters
		
		ResizableSprite.__init__(self, name, pos_x, pos_y)

	def indexAtPos(self, cursor_pos_x):

		index_in_hand = ( int( floor( (cursor_pos_x - self.rect.left) / float(var.tile_size) ) ) )
		if index_in_hand+1 > self.max_nb_letters :
			index_in_hand -= 1

		return index_in_hand


#----- Tiles -----
class Tile(ResizableSprite):
	def __init__(self, name, pos_x, pos_y):

		self.path = path_tiles

		ResizableSprite.__init__(self, name, pos_x, pos_y)


#----- Buttons -----
class Button(ResizableSprite):
	def __init__(self, name, pos_x, pos_y, is_a_checkbox=False, is_an_emoticom=False):

		self.path = path_buttons
		self.is_highlighted = False
		self.is_pushed = False
		self.is_a_checkbox = is_a_checkbox
		self.is_an_emoticom = is_an_emoticom

		ResizableSprite.__init__(self, name, pos_x, pos_y, transparent=True)

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
		self.is_selected = True
		#self.turnOnHighlighted()	

	def unselect(self):
		self.name = 'un'+self.name
		self.image = loadTransparentImage(path.join(self.path, self.name+'.png'))
		self.image = pygame.transform.smoothscale(self.image, pixels(self.width, self.height))
		self.is_selected = False
		#self.turnOnHighlighted()


#----- Letter -----
class Letter(ResizableSprite):
	def __init__(self, name, pos_x, pos_y):

		self.path = path_letters
		self.points = POINTS_FOR[name]

		ResizableSprite.__init__(self, name, pos_x, pos_y, transparent=True)		

	#move a letter at a given position expressed in tiles
	def moveAtTile(self, pos_x, pos_y) :
		self.rect.x, self.rect.y = pixels(pos_x, pos_y)
		self.pos_x, self.pos_y  = pos_x, pos_y

	#move a letter at a given position expressed in pixels
	def moveAtPixels(self, pos_x, pos_y) :
		self.rect.x, self.rect.y = pos_x, pos_y
		self.pos_x, self.pos_y  = tiles(pos_x, pos_y, to_round=True)


##----- Progress Bar -----
class ProgressBar():
	def __init__(self, pos_x, pos_y, width, height, nb_state):

		#create progress bar
		self.progress_bar_bck = UI_Image('progress_bar_background', path_background, pos_x, pos_y, width, height)
		layers.progress_bar.add(self.progress_bar_bck)

		#filling of the progress bar
		self.progress_bar_filling = UI_Image('progress_bar_tile', path_background, pos_x, pos_y, 0, height)
		layers.progress_bar.add(self.progress_bar_filling)

		#reinit progress bar
		self.button_reinit = Button("reinit", pos_x-1.25, pos_y-0.56)
		#self.button_reinit.width, self.button_reinit.height = height, height
		#self.button_reinit.resize()
		#layers.progress_bar.add(self.button_reinit)

 		#diggerent states of the progress bar
		self.state = 0
		self.nb_state = nb_state
		self.ratio_width = width/float(nb_state-1)

	def draw(self):

		layers.progress_bar.draw(window)

		text = UIText( "Etape : "+str(self.state)+" / "+str(self.nb_state-1), LINE_HEIGHT.PROGRESS_BAR, False, (28.6-7/3.0, 14.4) )
		if self.state in (0,1,2,3,4,5) :
			text = UIText( "Etape : 1 / 3", LINE_HEIGHT.PROGRESS_BAR, False, (28.6-7/3.0, 14.4) )
		elif self.state in (6,7,8) :
			text = UIText( "Etape : 2 / 3", LINE_HEIGHT.PROGRESS_BAR, False, (28.6-7/3.0, 14.4) )
		else :
			text = UIText( "Etape : 3 / 3", LINE_HEIGHT.PROGRESS_BAR, False, (28.6-7/3.0, 14.4) )

		window.blit( text.font.render(text.text, 1, COLOR.GREY_LIGHT), (text.pos_x_pix, text.pos_y_pix) )

	def fill(self):

		self.state = (self.state+1)%(self.nb_state)

		self.progress_bar_filling.width = self.state * self.ratio_width
		self.progress_bar_filling.resize()

	def empty(self):

		self.state = 0

		self.progress_bar_filling.width = self.state * self.ratio_width
		self.progress_bar_filling.resize()


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
	
	logging.info("WINDOW Creation")
	updateTileSize(width,height)

	for ui_text in UIText.all :
		ui_text.resize()

	layers.all.resize()

	width = int (1920 / REFERENCE_TILE_SIZE ) * var.tile_size
	height = int (1080 / REFERENCE_TILE_SIZE ) * var.tile_size

	var.window_width = width
	var.window_height = height

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

#----- Resize window but do not resize Sprites -----
def resizeWindowNoSpritesUpdate(width, height, fullscreen, resizable, resolution_auto, custom_window_height, double_buffer, hardware_accelerated) :
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

	#format 'letters_played' {(x, y) : 'a' }
	# 'x' and 'y' will then be swapped when accessing 'board_state' it is a matrix
	# eg : m =[[a, b], [c, d]] -> to get 'b' you need to access : m[1][2] which for the UI would be m(2, 1)
	letters_played = {}
	for letter in layer_letters_played :
		letters_played[(int(letter.pos_x - DELTA), int(letter.pos_y - DELTA))] = letter.name

	#___ LOGGER ___	
	logging.debug("letters played : %s", letters_played)

	if len(letters_played) > 1 :
		logging.debug('%i letters played', len(letters_played))
	else :
		logging.debug('%i letter played', len(letters_played)) 

	#___ NOTHING PLAYED ___
	if len(letters_played) == 0 :
		logging.info('nothing played')
		logging.info('')
		return []

	#___ SOMETHING PLAYED ___
	else :

		#___ SCRABBLE ___
		if len(letters_played) == 7 : #is a SCRABBLE ?
			pass
			"""
			#TODO do not add a scrabble if invalid move
			words_and_scores.append(['!! SCRABBLE !!', var.points_for_scrabble])
			SOUNDS.victory.play()
			"""

		#___ INITIALISATION ___
		words_and_scores = []
		all_x, all_y = [], []

		for tuple_pos in letters_played.keys() :
			all_x.append(tuple_pos[0])
			all_y.append(tuple_pos[1])

		min_x, max_x, delta_x = min(all_x), max(all_x), min(all_x)-max(all_x)
		min_y, max_y, delta_y = min(all_y), max(all_y), min(all_y)-max(all_y)


		#___ ERROR CHECKING ___	
		# played in diagonal ?
		if (delta_x != 0 and delta_y != 0) :
			#TODO display error message
			logging.debug("played in diagonal")
			return []


		#___ VERTICAL WORD PLAYED ___
		if delta_x == 0 :

			start_y, end_y = min_y, max_y

			#find first letter
			while( ( (start_y - 1) >= 0) and (var.current_board_state[start_y - 1][min_x] != '?') ) :
				start_y = start_y - 1

			#find last letter
			while( ( (end_y + 1) <= TILES_PER_LINE-1) and (var.current_board_state[end_y + 1][min_x] != '?') ) :
				end_y = end_y + 1


			#away from older letters (above or below)
			if (start_y == min_y and end_y == max_y and len( layers.letters_on_board.sprites() ) > 0):
				logging.debug("not played close to another word")


			if (delta_y+1 != len(letters_played) ) :
				logging.debug("there is a hole between letters played")
				#browse all letters
				it_y = start_y
				while( ( (it_y + 1) <= TILES_PER_LINE-1) and (var.current_board_state[it_y + 1][min_x] != '?') ) :
					it_y = it_y + 1
				if ( (it_y-start_y) != (end_y-start_y) ) :
					logging.debug("there is a hole between letters played - even using old letters")
					return []
				"""
				logging.debug("min_y : %i, max_y : %i, start_y : %i, end_y : %i", min_y, max_y, start_y, end_y)

				if not ( (end_y - start_y == max_y - start_y) or (end_y - start_y == end_y - min_y) ):
					logging.debug("there is a hole in the word - even using old letters")
					return []
				"""		


			#TODO : do not allow one letter in first turn
			# prevent one letter word
			if ( end_y > start_y ) : 

				logging.debug('VERTICAL WORD')
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
					condition_2 = ( (it_x + 1) <= TILES_PER_LINE-1 ) and ( var.current_board_state[it_y][it_x+1] != '?' ) 

					if ( condition_1  or condition_2 ) :       
						logging.debug('HORIZONTAL WORD')

						#___ PREPARE ITERATION : go to the begining of the word ___
						while( ( (it_x - 1) >= 0) and (var.current_board_state[it_y][it_x-1] != '?') ) : 
							it_x = it_x - 1

						old_word, old_word_score, old_word_multiplier = '', 0, 1
						#___ ITERATE ON THE LETTER OF THE WORD (go to the end of the word) ___
						while( ( (it_x) <= TILES_PER_LINE-1) and (var.current_board_state[it_y][it_x] != '?') ) :

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

			total_score = 0 

			for association in words_and_scores :
				logging.info('Word %s gives %i points', association[0], association[1])
				total_score += association[1]
			
			logging.info('total_score : %i', total_score)
			logging.info('')
			return words_and_scores 

		#___ HORIZONTAL WORD PLAYED ___
		elif delta_y == 0 : 

			start_x, end_x = min_x, max_x

			#find first letter
			while( ( (start_x - 1) >= 0) and (var.current_board_state[min_y][start_x - 1] != '?') ) :
				start_x = start_x - 1

			#find last letter
			while( ( (end_x + 1) <= TILES_PER_LINE-1) and (var.current_board_state[min_y][end_x + 1] != '?') ) :
				end_x = end_x + 1


			#away from older letters (left or right)
			if (start_x == min_x and end_x == max_x and len( layers.letters_on_board.sprites() ) > 0):
				logging.debug("not played close to another word")


			if (delta_x+1 != len(letters_played) ) :
				logging.debug("there is a hole between letters played")
				#browse all letters
				it_x = start_x
				while( ( (it_x + 1) <= TILES_PER_LINE-1) and (var.current_board_state[min_y][it_x + 1] != '?') ) :
					it_x = it_x + 1

				logging.debug("it_x : %i, start_x : %i, end_x : %i", it_x, start_x, end_x)
				if ( (it_x-start_x) != (end_x-start_x) ) :
					logging.debug("there is a hole between letters played - even using old letters")
					return []

			#TODO : do not allow one letter in first turn
			#prevent one letter word
			if ( end_x > start_x ) : 

				logging.debug('HORIZONTAL WORD')
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
					condition_2 = ( (it_y + 1) <= TILES_PER_LINE-1 ) and ( var.current_board_state[it_y+1][it_x] != '?' ) 

					if ( condition_1  or condition_2 ) :
						logging.debug('VERTICAL WORD')

						#___ PREPARE ITERATION : go to the begining of the word ___
						while( ( (it_y - 1) >= 0) and (var.current_board_state[it_y-1][it_x] != '?') ) : #go to the begining of the word
							it_y = it_y - 1

						old_word, old_word_score, old_word_multiplier= '', 0, 1
						#___ ITERATE ON THE LETTER OF THE WORD (go to the end of the word) ___
						while( ( (it_y) <= TILES_PER_LINE-1) and (var.current_board_state[it_y][it_x] != '?') ) :

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

			total_score = 0 #TEMP

			for association in words_and_scores :
				logging.info('Word %s gives %i points', association[0], association[1])
				total_score += association[1]
			
			logging.info('total_score : %i', total_score)
			logging.info('')

			return words_and_scores


#increment predicted score in real time
def incrementPredictedScore():
	var.predicted_score = 0
	for h_word_point in calculatePoints(layers.letters_just_played) :
		var.predicted_score = var.predicted_score + h_word_point[1]


#~~~~~~ LOAD CONFIGURATION ~~~~~~

#----- Init logger -----

path_log_file = path.join(path_log,'scrabble.log')
# levels : NOTSET < DEBUG < INFO < WARNING < ERROR < CRITICAL
logging.basicConfig(filename=path_log_file, filemode='w', level=logging.DEBUG, format='%(asctime)s.%(msecs)03d  |  %(levelname)s  |  %(message)s', datefmt='%Y-%m-%d %p %I:%M:%S')
logging.info("_________START OF LOG___________")
logging.info("")

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
logging.debug("DISPLAY SETTINGS")
logging.debug("Fullscreen : %s", cfg_fullscreen)
logging.debug("Resizable : %s", cfg_resizable)
logging.debug("Resolution auto : %s", cfg_resolution_auto)
logging.debug("Enable Windows 10 upscaling : %s", cfg_enable_windows_ten_upscaling)
logging.debug("Custom window width : %s", int ( cfg_custom_window_height * (16/9.0)) )
logging.debug("Custom window height : %s", cfg_custom_window_height)
logging.debug("Hardware accelerated : %s", cfg_hardware_accelerated)
logging.debug("Double buffer : %s", cfg_double_buffer)
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

#dirty
suggest_word = False

#Letters and points
if LETTERS_LANGUAGE == 'english' :
	var.bag_of_letters = rules.letters_english
	POINTS_FOR = rules.points_english
	path_letters = path_letters_english
elif LETTERS_LANGUAGE == 'french':
	var.bag_of_letters = rules.letters_french
	POINTS_FOR = rules.points_french
	path_letters = path_letters_french

#Data validation
forced = ""
if var.number_of_letters_per_hand < 5:
	var.number_of_letters_per_hand = 5
	forced = 'forced to '
elif var.number_of_letters_per_hand > 9 :
	var.number_of_letters_per_hand = 9
	forced = 'forced to '

logging.debug("GAMES RULES")
logging.debug("Language : %s", LETTERS_LANGUAGE)
logging.debug("Players : %s", players_names)
logging.debug("Number of letters per_hand %s: %s", forced, var.number_of_letters_per_hand)
logging.debug("Display next player hand : %s", display_next_player_hand)
logging.debug("Enable shuffle letters : %s", enable_shuffle_letter)
logging.debug("")


#~~~~~~ GAME INITIALIAZATION ~~~~~~


#----- OS verification and DPI scaling -----


os_name = platform.system()
os_version = platform.release()

if cfg_enable_windows_ten_upscaling == False :
	if ( os_name == "Windows" and os_version == "10" ):
		# Query DPI Awareness (Windows 10 and 8)
		awareness = ctypes.c_int()
		errorCode = ctypes.windll.shcore.GetProcessDpiAwareness(0, ctypes.addressof(awareness))

		if awareness.value == 0 :
			logging.debug("DPI scaling")
			logging.debug("Applications' resolutions are overriden by Windows 10")
			logging.debug("Changing this behaviour for this pygame app instance ...")

			# Set DPI Awareness  (Windows 10 and 8)
			errorCode = ctypes.windll.shcore.SetProcessDpiAwareness(2)
			logging.debug("Pygame's window resolution is now handled by itself")
			logging.debug("")


#----- Launch Pygame -----


game_engine = pygame.init() #init() -> (numpass, numfail)
"""
sound_engine = pygame.mixer.init() #init(frequency=22050, size=-16, channels=2, buffer=4096) -> None
"""
game_is_running = True


#Create custom pointer

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
hand=((24,24),(5,0))+pygame.cursors.compile(hand_strings,"X",".")

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
open_hand=((24,24),(5,0))+pygame.cursors.compile(hand_strings,"X",".")

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
close_hand=((24,24),(5,0))+pygame.cursors.compile(hand_strings,"X",".")

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
hand_clic=((24,24),(5,0))+pygame.cursors.compile(hand_clic_strings,"X",".")

pygame.mouse.set_cursor(*arrow)



fps_clock = pygame.time.Clock()
clic_clock = pygame.time.Clock()
logging.debug("INITIALIZATION")
logging.debug("%s pygame modules were launched and %s failed", game_engine[0], game_engine[1])
logging.debug("Pygame started")
logging.debug("")
logging.info("-------------------")
logging.info("GAME STARTED")
logging.info("-------------------")
logging.info("")

"""
#----- Load Sounds -----
SOUNDS = Sounds()
logging.debug("SOUNDS loaded")
logging.debug("")
"""

#----- Window init -----

#Add icon to the window
icon_image = pygame.image.load(path.join(path_icon,'Scrabble_launcher.ico'))
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
window = resizeWindow(var.window_width, var.window_height, cfg_fullscreen, cfg_resizable, cfg_resolution_auto, cfg_custom_window_height, cfg_double_buffer, cfg_hardware_accelerated)

#----- Initializing User Interface texts -----

#----- Create board game -----

#create background
board = Board("empty_background", 0, 0) #automatically stored in the corresponding layer

#create hand_holder
hand_holder = Hand_holder("hand_holder", UI_LEFT_LIMIT - 0.1, 1.5*UI_INTERLIGNE+1.4, var.number_of_letters_per_hand)#automatically stored in the corresponding layer


#User interface language
if UI_LANGUAGE == 'english' :
	language_id = 0
	path_buttons = path_buttons_english
elif UI_LANGUAGE == 'french' :
	language_id = 1
	path_buttons = path_buttons_french
else :
	language_id = 0
	path_buttons = path_buttons_english

#User interface content
ui_content = config_reader.h_ui_params

#Initialize userface texts
ui_text = UITextPrinter(ui_content)


#~~~~~~ PLAYERS LETTERS ~~~~~~

#tmp_first_hand = ['B','E','S','O','I', 'N']
#tmp_second_hand = ['S','Y','S','T','E','M','E']
#tmp_third_hand = ['U','T','I','L','I','S','A']
#tmp_second_hand = ['S','E','T','E','S','M','Y']
#tmp_third_hand = ['U','A','S','L','I','T','I']

tmp_first_hand = ['O',0,'S','B',0,'E','N']

tmp_second_hand = ['C','I',0,'C','N','E','S']
tmp_second_hand2 = ['S','C',0,'I','N','C','E']

tmp_third_hand = ['N','I','V',0,'A','R']
tmp_third_hand2 = ['A','V','I',0,'N','R']


start_hand = GroupOfSprites()
hand_state = []
pos_x = (UI_LEFT_LIMIT)
pos_y = layers.hand_holder.sprites()[0].pos_y + 0.1

for tmp_letter in tmp_first_hand :
	if tmp_letter != 0 :
		letter = Letter(tmp_letter, pos_x, pos_y)
		start_hand.add(letter)
		hand_state.append(letter.id)
	else :
		hand_state.append(0)
	pos_x = pos_x+1


#~~~~~~ CREATE PLAYER ~~~~~~

PLAYERS.append(Player(players_names[0], 0, start_hand, hand_state))

var.current_player = PLAYERS[0]

'''

#----- Create players -----
enough_letters = len(players_names)*var.number_of_letters_per_hand < len(var.bag_of_letters)

if enough_letters :

	for player_name in players_names :
		start_hand = GroupOfSprites()
		hand_state = []
		pos_x = (UI_LEFT_LIMIT)
		pos_y = ui_text.current_player_turn.pos_y+1

		for i in range(var.number_of_letters_per_hand) :
			if len(var.bag_of_letters) > 0 :
				letter = Letter(var.bag_of_letters[0], pos_x, pos_y)
				start_hand.add(letter)
				hand_state.append(letter.id)
				del(var.bag_of_letters[0])
				pos_x = pos_x+1

		PLAYERS.append(Player(player_name, 0, start_hand, hand_state))

	logPlayersInfo()

	var.current_player = PLAYERS[0]
	var.current_player.info()


else :
	game_is_running = False
	ERROR.not_enough_letters()
'''

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


# //////// Add letters on Board ///////////
x, y = 4, 2
for letter in "METHODES" :
	layers.letters_on_board.add( Letter(letter,DELTA+x,DELTA+y) )
	y += 1

x, y = 3, 4
for letter in "UTILISATEUR" :
	if (x, y) != (4,4) :
		layers.letters_on_board.add( Letter(letter,DELTA+x,DELTA+y) )
	x += 1

x, y = 4, 8
for letter in "ERGONOMIE" :
	if (x, y) != (4,8) :
		layers.letters_on_board.add( Letter(letter,DELTA+x,DELTA+y) )
	x += 1

# ------- CREATES BUTTONS --------
button_ok = Button("ok", 32/2.0 - 1, 14.5 )
#button_ok2 = Button("ok", 32/2.0 - 5, 14.5 )

button_end_turn = Button("end_turn", tiles1(hand_holder.rect.x)+var.number_of_letters_per_hand + 0.2 + 0.75, layers.hand_holder.sprites()[0].pos_y + 0.1)

button_shuffle = Button("shuffle", tiles1(hand_holder.rect.x)+var.number_of_letters_per_hand + 0.2 + 0.75, button_end_turn.pos_y + 1.25)

#button_play = Button("play", 32/2.0 + 6, 8.5)
button_play = Button("play", 32/2.0 + 6, 7.5)


# ------- CHECKBOXES --------
# STEP 4
"""
checkbox_facile = Checkbox("checkbox", 3.5, 6 )
checkbox_moyen = Checkbox("checkbox", 3.5, 7.5 )
checkbox_difficile = Checkbox("checkbox", 3.5, 9 )
"""
checkbox_function_shuffle = Checkbox("checkbox", 3.5, 11.5 )
checkbox_function_display_bonus = Checkbox("checkbox", 3.5, 13 )
#checkbox_function_score = Checkbox("checkbox", 3, 16 )

# STEP 5
checkbox_find_word = Checkbox("checkbox", 5, 8.5 )
checkbox_bonus_cases = Checkbox("checkbox", 5, 11.25 )

# STEP 7
checkbox_facile2 = Checkbox("checkbox", 3.5, 5 )
checkbox_moyen2 = Checkbox("checkbox", 3.5, 6.5 )
checkbox_difficile2 = Checkbox("checkbox", 3.5, 8 )

checkbox_function_shuffle2 = Checkbox("checkbox", 3.5, 11 )
checkbox_function_display_bonus2 = Checkbox("checkbox", 3.5, 12.50 )
checkbox_function_score2 = Checkbox("checkbox", 3.5, 14 )

#STEP 8
checkbox_find_word2 = Checkbox("checkbox", 5, 7.5)
checkbox_suggest_word2 = Checkbox("checkbox", 5, 9)

checkbox_bonus_cases2 = Checkbox("checkbox", 5, 12 )
checkbox_calculate_score2 = Checkbox("checkbox", 5, 13.25 )


# ------- EMOTICOM --------
happy = Emoticom("happy", 5, 6.5)
neutral = Emoticom("neutral", 9, 6.5)
sad = Emoticom("sad", 13, 6.5)

all_emoticoms = [happy, neutral, sad]


#create dark_filter
mask_surface = pygame.Surface((var.window_width, var.window_height))
mask_surface.fill(COLOR.BLACK)
#mask_surface.set_alpha(180)
mask_surface.set_alpha(230)
mask_surface = mask_surface.convert_alpha()
dark_filter = UI_Surface('dark_filter', 0, 0, mask_surface)
layers.dark_filter.add(dark_filter)

#create window_pop_up
pop_up_window_surface = pygame.Surface((28*var.tile_size, 14*var.tile_size))
pop_up_window_surface.fill(COLOR.GREY_DEEP)
pygame.draw.rect( pop_up_window_surface, COLOR.GREY_LIGHT, pygame.Rect((0, 0), pixels(28, 14, to_round=False)), 3 )
buble_points = [
pixels(0.5, 0.5),
pixels(21.5, 0.5),
pixels(21.5, 8.6),
pixels(22.5, 9.25),
pixels(21.5, 9.1),
pixels(21.5, 12),
pixels(0.5, 12)
]	
#pygame.draw.aalines( pop_up_window_surface, COLOR.GREY_LIGHT, True, buble_points, 1 )			
pop_up_window = UI_Surface('pop_up_window', 2, 2, pop_up_window_surface)
layers.pop_up_window.add(pop_up_window)

#create score window_pop_up
pop_up_score_surface = pygame.Surface((11*var.tile_size, 3.5*var.tile_size))
pop_up_score_surface.fill(COLOR.GREY_DEEP)				
pop_up_score = UI_Surface('score_pop_up', 11, 7.25, pop_up_score_surface)
layers.pop_up_score.add(pop_up_score)

#create mask for text
surf_mask_text = pygame.Surface( (ui_text.score.width*var.tile_size, ui_text.score.height*var.tile_size) )
logging.debug("Mask surface width : %i, height : %i", round(ui_text.score.width*2*var.tile_size), round(ui_text.score.height*var.tile_size) )
surf_mask_text.fill(COLOR.GREY_DEEP)				
mask_text_score = UI_Surface('mask_text_score', ui_text.score.pos_x, ui_text.score.pos_y, surf_mask_text)
layers.mask_text.add(mask_text_score)

#create avatar
#ui_avatar = UI_Image('ergonome', path_background, 22, 2.84, 6, 6) #Screen 32*18
#ui_avatar = UI_Image('ergonome', path_background, 24, 3.84, 5, 5) #Screen 32*18
ui_avatar = UI_Image('ergonome', path_background, 24, 9, 5, 5) #Screen 32*18

layers.pop_up_window.add(ui_avatar)

#create progress bar
progress_bar = ProgressBar(28.6-7/3.0, 15, 7/3.0, 1.2/3.0, 12)



# ___ SNAPSHOT FOR LATER EASY REFRESH ___
layers.buttons_on_screen.add(button_end_turn)

layers.background.draw(window)
layers.tiles.draw(window)
layers.hand_holder.draw(window)
var.background_empty = window.copy()

layers.buttons_on_screen.draw(window)
var.background_no_letter = window.copy()

layers.dark_filter.draw(window)
layers.pop_up_window.draw(window)
layers.background_pop_up_empty = window.copy()


# ___ FIRST IMAGE ___
layers.buttons_on_screen.remove(button_end_turn)
layers.buttons_on_screen.add(button_play)

layers.background.draw(window)
layers.tiles.draw(window)

layers.buttons_on_screen.draw(window)

layers.letters_on_board.draw(window)
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
			STEP = 0
			progress_bar.empty()

			# Reset conf
			enable_shuffle_letter = False
			display_type_of_tile_on_hoovering = False
			display_new_score_in_real_time = False
			suggest_word = False

			# Reset Board
			var.current_board_state = [ ['?' for i in range(TILES_PER_LINE)] for j in range(TILES_PER_LINE) ]

			# Reset letters
			for letter in layers.letters_on_board :
				letter.kill()
			
			for letter in layers.letters_just_played :
				letter.kill()

			for letter in var.current_player.hand :
				letter.kill()

			x, y = 4, 2
			for letter in "METHODES" :
				layers.letters_on_board.add( Letter(letter,DELTA+x,DELTA+y) )
				y += 1

			x, y = 3, 4
			for letter in "UTILISATEUR" :
				if (x, y) != (4,4) :
					layers.letters_on_board.add( Letter(letter,DELTA+x,DELTA+y) )
				x += 1

			x, y = 4, 8
			for letter in "ERGONOMIE" :
				if (x, y) != (4,8) :
					layers.letters_on_board.add( Letter(letter,DELTA+x,DELTA+y) )
				x += 1

			# ___ CHECKBOXES ___
			checkbox_find_word.empty()
			checkbox_bonus_cases.empty()
			checkbox_function_shuffle2.empty()
			checkbox_function_display_bonus2.empty()

			layers.buttons_on_screen.empty()
			layers.buttons_on_screen.add(button_play)

			# Reset player
			var.current_player.score = 0

			pos_x = (UI_LEFT_LIMIT)
			pos_y = layers.hand_holder.sprites()[0].pos_y + 0.1

			hand_state = []
			for tmp_letter in tmp_first_hand :
				if tmp_letter != 0 :
					letter = Letter(tmp_letter, pos_x, pos_y)
					start_hand.add(letter)
					hand_state.append(letter.id)
				else :
					hand_state.append(0)
				pos_x = pos_x+1
			PLAYERS[0].hand_state = hand_state


			# ___ SNAPSHOT FOR LATER EASY REFRESH ___
			layers.buttons_on_screen.add(button_end_turn)

			layers.background.draw(window)
			layers.tiles.draw(window)
			layers.hand_holder.draw(window)
			var.background_empty = window.copy()

			layers.buttons_on_screen.draw(window)
			var.background_no_letter = window.copy()

			layers.dark_filter.draw(window)
			layers.pop_up_window.draw(window)
			layers.background_pop_up_empty = window.copy()


			# ___ FIRST IMAGE ___
			layers.buttons_on_screen.remove(button_end_turn)
			layers.buttons_on_screen.add(button_play)

			layers.background.draw(window)
			layers.tiles.draw(window)

			layers.buttons_on_screen.draw(window)

			layers.letters_on_board.draw(window)
			pygame.display.update()

			var.current_action = "SELECT_A_LETTER"		
			



		#~~~~~~ WINDOW RESIZE ~~~~~~
		#TODO create a specific function ?
		elif ( event_type == pygame.VIDEORESIZE ) : #properly refresh the game window if a resize is detected
			
			#new width and height
			width = event.dict['size'][0]
			height = event.dict['size'][1]

			#create a fullscreen image fully black to prevent later artefacts
			window = resizeWindowNoSpritesUpdate(var.monitor_resolution.current_w, var.monitor_resolution.current_h, cfg_fullscreen, cfg_resizable, cfg_resolution_auto, cfg_custom_window_height, cfg_double_buffer, cfg_hardware_accelerated)
			pygame.draw.rect(window, COLOR.BLACK, ( (0,0), (var.monitor_resolution.current_w, var.monitor_resolution.current_h) ) )
			pygame.display.update()

			window = resizeWindow(width, height, cfg_fullscreen, cfg_resizable, cfg_resolution_auto, cfg_custom_window_height, cfg_double_buffer, cfg_hardware_accelerated)

			layers.background.draw(window)
			layers.tiles.draw(window)
			layers.hand_holder.draw(window)
			var.background_empty = window.copy()

			layers.buttons_on_screen.draw(window)
			var.background_no_letter = window.copy()

			layers.letters_on_board.draw(window)
			layers.letters_just_played.draw(window)
			var.current_player.hand.draw(window)
			var.current_background_no_text = window.copy()

			progress_bar.draw()
			if STEP in (3,6,9):
				ui_text.drawText(STEP)
			var.current_background = window.copy()

			layers.selected_letter.draw(window)


			if var.current_action == "WINDOW_DISPLAYED":
				layers.dark_filter.draw(window)
				layers.pop_up_window.draw(window)
				layers.background_pop_up_empty = window.copy()
				layers.buttons_on_screen.draw(window)
				progress_bar.draw()
				ui_text.drawTextPopUp(STEP)	
			else :
				layers.dark_filter.draw(window)
				layers.pop_up_window.draw(window)
				layers.background_pop_up_empty = window.copy()
				window.blit(var.current_background, (0,0))

			# ///// DIRTY PATCH /////
			if STEP == 0 :
				layers.background.draw(window)
				layers.tiles.draw(window)
				layers.buttons_on_screen.draw(window)
				layers.letters_on_board.draw(window)

			pygame.display.update()
			

		# NORMAL EVENTS
		else :
			# //////// POP UP DISPLAYED ////////
			if MUST_DIPSLAY_POP_UP :
				if ( event_type == pygame.MOUSEBUTTONUP  and event.button == 1 ) :
					FRAMES_BEFORE_POP_UP_DISAPPEAR = 0

			# //////// WINDOW DISPLAYED ////////
			elif (var.current_action == "WINDOW_DISPLAYED") :

				need_refresh_buttons_on_screen = False

				#~~~~~~~~~~~ MOUSE BUTTONS ~~~~~~~~~~~
				if ( ( (event_type == pygame.MOUSEBUTTONDOWN) or (event_type == pygame.MOUSEBUTTONUP) ) and event.button == 1 ) :

					timer = clic_clock.tick()

					#~~~~~~~~~~~ PRESS LEFT CLIC ~~~~~~~~~~~
					if ( event_type == pygame.MOUSEBUTTONDOWN ) :

						cursor_pos_x, cursor_pos_y = event.pos[0], event.pos[1]

						#------ CLIC ON BUTTONS (VISUAL) -------
						for button in layers.buttons_on_screen :
							if button.rect.collidepoint(cursor_pos_x, cursor_pos_y) == True :
								#change button state
								button.is_highlighted = False
								button.push()
								need_refresh_buttons_on_screen = True

					#~~~~~~~~~~~ RELEASE LEFT CLIC ~~~~~~~~~~~
					elif ( event_type == pygame.MOUSEBUTTONUP ) :

						#~~~~~~~~~~~ EMOTICOMS ~~~~~~~~~~~ 
						if ( (happy.rect.collidepoint(cursor_pos_x, cursor_pos_y) == True) and (happy.is_pushed) ):
							happy.release()

							if happy.is_selected :
								if neutral.is_selected :
									neutral.unselect()
								if sad.is_selected :
									sad.unselect()
								need_refresh_buttons_on_screen = True
							else :
								happy.select()
								if neutral.is_selected :
									neutral.unselect()
								if sad.is_selected :
									sad.unselect()
								need_refresh_buttons_on_screen = True

						if ( (neutral.rect.collidepoint(cursor_pos_x, cursor_pos_y) == True) and (neutral.is_pushed) ):
							neutral.release()

							if neutral.is_selected :
								if happy.is_selected :
									happy.unselect()
								if sad.is_selected :
									sad.unselect()
								need_refresh_buttons_on_screen = True
							else :
								neutral.select()
								if happy.is_selected :
									happy.unselect()
								if sad.is_selected :
									sad.unselect()
								need_refresh_buttons_on_screen = True


						if ( (sad.rect.collidepoint(cursor_pos_x, cursor_pos_y) == True) and (sad.is_pushed) ):
							sad.release()

							if sad.is_selected :
								if neutral.is_selected :
									neutral.unselect()
								if happy.is_selected :
									happy.unselect()
								need_refresh_buttons_on_screen = True
							else :
								sad.select()
								if neutral.is_selected :
									neutral.unselect()
								if happy.is_selected :
									happy.unselect()
								need_refresh_buttons_on_screen = True

						#~~~~~~~~~~~ BUTTON OK ~~~~~~~~~~~
						if ( (button_ok.rect.collidepoint(cursor_pos_x, cursor_pos_y) == True) and (button_ok.is_pushed) ):

							button_ok.release()
							layers.buttons_on_screen.clear(window, var.background_pop_up_empty)
							layers.buttons_on_screen.draw(window)

							if STEP in (2,5,6) :
								pygame.mouse.set_cursor(*arrow)


							if STEP == 1 :

								# ___ NEXT STEP ___
								STEP = STEP + 1
								progress_bar.fill()

								# ___ DRAW WINDOW ___
								window.blit(var.background_pop_up_empty, (0,0))

								layers.buttons_on_screen.draw(window)
								progress_bar.draw()
								ui_text.drawTextPopUp(STEP)

								pygame.display.update()


							elif STEP == 4 :

								move_on = True
								nb_selected = 0
								for emo in all_emoticoms :
									if emo.is_selected :
										nb_selected += 1
								if nb_selected > 1 :
									move_on = False

									#creeate pop up
									layers.pop_up.add( createPopUp(["Donnez votre avis en cliquant sur un emoticône svp."], LINE_HEIGHT=LINE_HEIGHT.SUBTITLE)  )

									# snapshot of before pop_up
									snapshot = window.copy()

									#display pop_up
									layers.dark_filter.draw(window)
									layers.pop_up.draw(window)
									pygame.display.update()

									MUST_DIPSLAY_POP_UP = True

									#prepare exit image (displayed when removing pop up)
									window.blit(snapshot, (0,0))


								if move_on :

									# ___ CHANGE CONF ___
									if checkbox_function_shuffle.is_filled :
										enable_shuffle_letter = True
										layers.buttons_on_screen.add(button_shuffle)
									if checkbox_function_display_bonus.is_filled :
										display_type_of_tile_on_hoovering = True

									# Reset checkboxes
									for button in layers.buttons_on_screen :
										if button.is_a_checkbox :
											button.empty()
										if button.is_an_emoticom :
											button.select()

									# ___ DRAW BOARD ___
									"""
									layers.background.draw(window)
									layers.tiles.draw(window)
									layers.hand_holder.draw(window)
									layers.buttons_on_screen.draw(window)
									var.background_no_letter = window.copy()
									layers.letters_on_board.draw(window)
									layers.letters_just_played.draw(window)
									var.current_player.hand.draw(window)
									var.current_background_no_text = window.copy()
									ui_text.drawText(STEP)
									var.current_background = window.copy()
									layers.selected_letter.draw(window)
									"""

									# ___ NEXT STEP ___
									STEP = STEP + 1
									progress_bar.fill()


									# ___ ADD BUTTONS 
									layers.buttons_on_screen.empty()
									layers.buttons_on_screen.add(button_ok)

									#layers.buttons_on_screen.add(checkbox_find_word)
									checkbox_find_word.fill()
									#layers.buttons_on_screen.add(checkbox_bonus_cases)
									#if display_type_of_tile_on_hoovering :
									checkbox_bonus_cases.fill()

									# ___ DRAW WINDOW ___
									window.blit(var.background_pop_up_empty, (0,0))

									layers.buttons_on_screen.draw(window)
									progress_bar.draw()
									ui_text.drawTextPopUp(STEP)

									pygame.display.update()
									#TODO based on selected checkboxes


							elif STEP == 7 :

								move_on = True
								nb_selected = 0
								for emo in all_emoticoms :
									if emo.is_selected :
										nb_selected += 1
								if nb_selected > 1 :
									move_on = False

									#creeate pop up
									layers.pop_up.add( createPopUp(["Donner votre avis en cliquant sur un emoticôme svp."], LINE_HEIGHT=LINE_HEIGHT.SUBTITLE)  )

									# snapshot of before pop_up
									snapshot = window.copy()

									#display pop_up
									layers.dark_filter.draw(window)
									layers.pop_up.draw(window)
									pygame.display.update()

									MUST_DIPSLAY_POP_UP = True

									#prepare exit image (displayed when removing pop up)
									window.blit(snapshot, (0,0))

								if move_on :

									STEP = STEP + 1
									progress_bar.fill()

									# Keep track of choice
									tmp_enable_shuffle, tmp_display_pop_up, tmp_display_score = False, False, False

									if checkbox_function_shuffle2.is_filled or enable_shuffle_letter :
										tmp_enable_shuffle = True
									if checkbox_function_display_bonus2.is_filled or display_type_of_tile_on_hoovering :
										tmp_display_pop_up = True
									#if checkbox_function_score2.is_filled :
									tmp_display_score = True
									tmp_suggest_word = True

									#TODO NO CHECKBOX

									# Reset
									for button in layers.buttons_on_screen :
										if button.is_a_checkbox :
											button.empty()
										if button.is_an_emoticom :
											button.select()

									layers.buttons_on_screen.empty()

									"""
									layers.background.draw(window)
									layers.tiles.draw(window)
									layers.hand_holder.draw(window)
									layers.buttons_on_screen.draw(window)
									var.background_no_letter = window.copy()

									layers.letters_on_board.draw(window)
									layers.letters_just_played.draw(window)
									var.current_player.hand.draw(window)
									var.current_background_no_text = window.copy()
									
									progress_bar.draw()
									ui_text.drawText(STEP)
									var.current_background = window.copy()
									layers.selected_letter.draw(window)
									"""

									window.blit(var.background_pop_up_empty, (0,0))

									layers.dark_filter.draw(window)
									layers.pop_up_window.draw(window)

									layers.buttons_on_screen.add(button_ok)
									#layers.buttons_on_screen.add(progress_bar.button_reinit)

									#layers.buttons_on_screen.add(checkbox_find_word2)
									#layers.buttons_on_screen.add(checkbox_bonus_cases2)
									#layers.buttons_on_screen.add(checkbox_calculate_score2)
									#layers.buttons_on_screen.add(checkbox_suggest_word2)

									if tmp_enable_shuffle :
										checkbox_find_word2.fill()
										checkbox_find_word2.turnOffHighlighted()
									if tmp_display_pop_up :
										checkbox_bonus_cases2.fill()
										checkbox_bonus_cases2.turnOffHighlighted()
									if tmp_display_score :
										checkbox_calculate_score2.fill()
										checkbox_calculate_score2.turnOffHighlighted()
									if tmp_suggest_word :
										checkbox_suggest_word2.fill()
										checkbox_suggest_word2.turnOffHighlighted()

									layers.buttons_on_screen.draw(window)
									progress_bar.draw()
									ui_text.drawTextPopUp(STEP)
									

							elif STEP == 8 :

								"""
								# settings
								if checkbox_find_word2.is_filled :
									enable_shuffle_letter = True
								if checkbox_bonus_cases2.is_filled :
									display_type_of_tile_on_hoovering = True
								if checkbox_calculate_score2.is_filled :
									display_new_score_in_real_time = True
								"""
								# settings
								enable_shuffle_letter = checkbox_find_word2.is_filled
								display_type_of_tile_on_hoovering = checkbox_bonus_cases2.is_filled

								display_new_score_in_real_time = checkbox_calculate_score2.is_filled
								suggest_word = checkbox_suggest_word2.is_filled


								# ___ Reset ___
								#buttons
								for button in layers.buttons_on_screen :
									if button.is_a_checkbox :
										button.empty()

								layers.buttons_on_screen.empty()
								if enable_shuffle_letter :
									layers.buttons_on_screen.add(button_shuffle)
								layers.buttons_on_screen.add(button_end_turn)
								#layers.buttons_on_screen.add(progress_bar.button_reinit)

								# letters
								var.current_board_state = [ ['?' for i in range(TILES_PER_LINE)] for j in range(TILES_PER_LINE) ]

								# ___ NEXT TURN ___
								STEP = STEP + 1
								progress_bar.fill()

								# new letters
								x, y = 4, 8
								for letter in "ERGONOMIE" :
									var.current_board_state[y][x] = letter
									layers.letters_on_board.add( Letter(letter,DELTA+x,DELTA+y) )
									x += 1

								pos_x = (UI_LEFT_LIMIT)
								pos_y = layers.hand_holder.sprites()[0].pos_y + 0.1
								hand_state = []
								
								for tmp_letter in tmp_third_hand :
									if tmp_letter != 0 :
										letter = Letter(tmp_letter, pos_x, pos_y)
										start_hand.add(letter)
										hand_state.append(letter.id)
									else :
										hand_state.append(0)
									pos_x = pos_x+1

								PLAYERS[0].hand_state = hand_state

								# update display
								layers.background.draw(window)
								layers.tiles.draw(window)
								layers.hand_holder.draw(window)
								layers.buttons_on_screen.draw(window)
								var.background_no_letter = window.copy()

								layers.letters_on_board.draw(window)
								layers.letters_just_played.draw(window)
								var.current_player.hand.draw(window)
								var.current_background_no_text = window.copy()

								progress_bar.draw()
								ui_text.drawText(STEP)
								var.current_background = window.copy()

								layers.selected_letter.draw(window)

								pygame.display.update()
								var.current_action = "SELECT_A_LETTER"

							elif STEP == 10 :

								STEP = STEP + 1
								progress_bar.fill()

								window.blit(var.background_pop_up_empty, (0,0))

								layers.buttons_on_screen.draw(window)
								progress_bar.draw()
								ui_text.drawTextPopUp(STEP)


							elif STEP == 11 :

								STEP = 0
								progress_bar.fill()

								# Reset conf
								enable_shuffle_letter = False
								display_type_of_tile_on_hoovering = False
								display_new_score_in_real_time = False
								suggest_word = False

								# Reset Board
								var.current_board_state = [ ['?' for i in range(TILES_PER_LINE)] for j in range(TILES_PER_LINE) ]

								# Reset letters
								for letter in layers.letters_on_board :
									letter.kill()
								
								for letter in layers.letters_just_played :
									letter.kill()

								for letter in var.current_player.hand :
									letter.kill()

								x, y = 4, 2
								for letter in "METHODES" :
									layers.letters_on_board.add( Letter(letter,DELTA+x,DELTA+y) )
									y += 1

								x, y = 3, 4
								for letter in "UTILISATEUR" :
									if (x, y) != (4,4) :
										layers.letters_on_board.add( Letter(letter,DELTA+x,DELTA+y) )
									x += 1

								x, y = 4, 8
								for letter in "ERGONOMIE" :
									if (x, y) != (4,8) :
										layers.letters_on_board.add( Letter(letter,DELTA+x,DELTA+y) )
									x += 1

								# ___ CHECKBOXES ___
								checkbox_find_word.empty()
								checkbox_bonus_cases.empty()
								checkbox_function_shuffle2.empty()
								checkbox_function_display_bonus2.empty()

								layers.buttons_on_screen.empty()
								layers.buttons_on_screen.add(button_play)

								# Reset player
								var.current_player.score = 0

								pos_x = (UI_LEFT_LIMIT)
								pos_y = layers.hand_holder.sprites()[0].pos_y + 0.1

								hand_state = []
								for tmp_letter in tmp_first_hand :
									if tmp_letter != 0 :
										letter = Letter(tmp_letter, pos_x, pos_y)
										start_hand.add(letter)
										hand_state.append(letter.id)
									else :
										hand_state.append(0)
									pos_x = pos_x+1

								PLAYERS[0].hand_state = hand_state

								# ___ SNAPSHOT FOR LATER EASY REFRESH ___
								layers.buttons_on_screen.add(button_end_turn)

								layers.background.draw(window)
								layers.tiles.draw(window)
								layers.hand_holder.draw(window)
								var.background_empty = window.copy()

								layers.buttons_on_screen.draw(window)
								var.background_no_letter = window.copy()

								layers.dark_filter.draw(window)
								layers.pop_up_window.draw(window)
								layers.background_pop_up_empty = window.copy()

								# ___ FIRST IMAGE ___
								layers.buttons_on_screen.remove(button_end_turn)
								layers.buttons_on_screen.add(button_play)

								layers.background.draw(window)
								layers.tiles.draw(window)

								layers.buttons_on_screen.draw(window)

								layers.letters_on_board.draw(window)
								pygame.display.update()

								pygame.display.update()
								var.current_action = "SELECT_A_LETTER"															


							elif STEP == 2 :

								# letters on board
								x, y = 3, 4
								for letter in "UTILISATEUR" :
									layers.letters_on_board.add( Letter(letter,DELTA+x,DELTA+y) )
									var.current_board_state[y][x] = letter
									x += 1

								# ___ NEXT STEP ___
								STEP = STEP + 1
								progress_bar.fill()	

								# ___ ADD BUTTONS ___
								layers.buttons_on_screen.remove(button_ok)
								layers.buttons_on_screen.add(button_end_turn)
								if enable_shuffle_letter :
									layers.buttons_on_screen.add(button_shuffle)

								# ___ DRAW BOARD ___
								window.blit(var.background_empty, (0,0))

								layers.buttons_on_screen.draw(window)

								layers.letters_on_board.draw(window)
								var.current_player.hand.draw(window)
								var.current_background_no_text = window.copy()

								progress_bar.draw()
								ui_text.drawText(STEP)

								var.current_background = window.copy()

								pygame.display.update()
								var.current_action = "SELECT_A_LETTER"


							elif STEP == 5 :

								if checkbox_find_word.is_filled :
									enable_shuffle_letter = True
								if checkbox_bonus_cases.is_filled :
									display_type_of_tile_on_hoovering = True

								# Reset
								for button in layers.buttons_on_screen :
									if button.is_a_checkbox :
										button.empty()

								# letters on board
								x, y = 4, 2
								for letter in "METHODES" :
									layers.letters_on_board.add( Letter(letter,DELTA+x,DELTA+y) )
									var.current_board_state[y][x] = letter
									y += 1

								# letters in hand
								pos_x = (UI_LEFT_LIMIT)
								pos_y = layers.hand_holder.sprites()[0].pos_y + 0.1
								hand_state = []
								
								for tmp_letter in tmp_second_hand :
									if tmp_letter != 0 :
										letter = Letter(tmp_letter, pos_x, pos_y)
										start_hand.add(letter)
										hand_state.append(letter.id)
									else :
										hand_state.append(0)
									pos_x = pos_x+1

								PLAYERS[0].hand_state = hand_state

								# ___ NEXT STEP ___
								STEP = STEP + 1
								progress_bar.fill()	

								# ___ ADD BUTTONS ___
								layers.buttons_on_screen.remove(button_ok)	

								layers.buttons_on_screen.remove(checkbox_find_word)
								layers.buttons_on_screen.remove(checkbox_bonus_cases)

								layers.buttons_on_screen.add(button_end_turn)
								if enable_shuffle_letter :
									layers.buttons_on_screen.add(button_shuffle)

								# ___ DRAW WINDOW ___
								window.blit(var.background_empty, (0,0))

								layers.buttons_on_screen.draw(window)

								layers.letters_on_board.draw(window)
								var.current_player.hand.draw(window)

								progress_bar.draw()
								ui_text.drawText(STEP)

								var.current_action = "SELECT_A_LETTER"

								texts = [
								"Utiliser le bouton 'Mélanger' pour trouver plus",
								"  facilement un mot qui rapporte des points."
								]

								#creeate pop up
								layers.pop_up.add( createPopUp(texts, LINE_HEIGHT = LINE_HEIGHT.SUBTITLE, time=11000)  )

								# snapshot of before pop_up
								snapshot = window.copy()

								#display pop_up
								layers.dark_filter.draw(window)
								layers.pop_up.draw(window)
								pygame.display.update()

								MUST_DIPSLAY_POP_UP = True

								#prepare exit image (displayed when removing pop up)
								window.blit(snapshot, (0,0))


								#break

								"""
								#------ CLOSE WINDOW -------

								#TO DEBUG
								# Check if resolution changed during pop_up
								same_width = var.current_background.get_width() == var.background_pop_up_empty.get_width()
								same_height = var.current_background.get_height() == var.background_pop_up_empty.get_height()
								#Same resolution
								if same_width and same_height :
									window.blit(var.current_background, (0,0))
									pygame.display.update()
									break
								else :
									pygame.event.post( pygame.event.Event(pygame.VIDEORESIZE, {'size' :[var.window_width,var.window_height]} ) )
								"""

						if not MUST_DIPSLAY_POP_UP :

							#~~~~~~~~~~~ CHECKBOX ~~~~~~~~~~~
							for button in layers.buttons_on_screen :
								if button.is_a_checkbox :
									if ( (button.rect.collidepoint(cursor_pos_x, cursor_pos_y) == True) and (button.is_pushed) ):
										if button.is_filled :
											button.release()
											button.empty()
											button.turnOnHighlighted()
										else :								
											button.release()
											button.fill()
											button.turnOnHighlighted()

										need_refresh_buttons_on_screen = True
										

							#------ RELEASE CLIC ON A BUTTON OR AWAY (VISUAL) -------
							
							for button in layers.buttons_on_screen :

								if button.rect.collidepoint(cursor_pos_x, cursor_pos_y) == True :
									button.turnOnHighlighted()
									need_refresh_buttons_on_screen = True

								if button.is_pushed :
									button.release() #release all pushed buttons
									if button.rect.collidepoint(cursor_pos_x, cursor_pos_y) :
										button.turnOnHighlighted()
									else :
										button.turnOffHighlighted()
									need_refresh_buttons_on_screen = True

				if need_refresh_buttons_on_screen :
					layers.buttons_on_screen.clear(window, var.background_pop_up_empty)
					layers.buttons_on_screen.draw(window)
					pygame.display.update()



				#~~~~~~ MOUSE MOTION ~~~~~~	
				elif(event_type == pygame.MOUSEMOTION ):

					mouse_pos = pygame.mouse.get_pos()
					cursor_pos_x = mouse_pos[0]
					cursor_pos_y = mouse_pos[1]

					#------ CHANGE APPEARANCE OF BUTTONS (VISUAL) ------
					buttons_changed = False
					for button in layers.buttons_on_screen :
						if ( button.rect.collidepoint(cursor_pos_x, cursor_pos_y) == True ) and ( not button.is_highlighted ) and (not button.is_pushed ) :
							button.turnOnHighlighted()
							pygame.mouse.set_cursor(*hand)
							buttons_changed = True
						elif ( button.rect.collidepoint(cursor_pos_x, cursor_pos_y) == False ) and ( button.is_highlighted ) and (not button.is_pushed ):
							button.turnOffHighlighted()
							pygame.mouse.set_cursor(*arrow)
							buttons_changed = True

					if buttons_changed :
						layers.buttons_on_screen.clear(window, var.background_pop_up_empty)
						layers.buttons_on_screen.draw(window)

						pygame.display.update()


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

							#------ CLIC ON A LETTER IN HAND ? -------
							for letter_from_hand in var.current_player.hand :

								if letter_from_hand.rect.collidepoint(cursor_pos_x, cursor_pos_y) == True :

									pygame.mouse.set_cursor(*close_hand)

									var.delta_pos_on_tile = ( cursor_pos_x - letter_from_hand.rect.x , cursor_pos_y - letter_from_hand.rect.y)
									layers.selected_letter.add(letter_from_hand)
									
									#remove letter from hand
									var.current_player.hand.remove(letter_from_hand)
									hand_state_index = var.current_player.hand_state.index(letter_from_hand.id)
									var.current_player.hand_state[hand_state_index] = 0

									#refresh screen
									var.current_player.hand.clear(window, var.background_no_letter)
									var.current_player.hand.draw(window)

									var.current_background = window.copy()									
									layers.selected_letter.draw(window)
									pygame.display.update()

									pygame.mouse.set_cursor(*close_hand)
									var.current_action = "PLAY_A_LETTER"


							#------ CLIC ON A LETTER JUST PLAYED ? -------
							for letter_from_board in layers.letters_just_played :

								if letter_from_board.rect.collidepoint(cursor_pos_x, cursor_pos_y) == True :

									pygame.mouse.set_cursor(*close_hand)

									var.delta_pos_on_tile = ( cursor_pos_x - letter_from_board.rect.x , cursor_pos_y - letter_from_board.rect.y)

									tile_x_on_board = int(letter_from_board.pos_x - DELTA)
									tile_y_on_board = int(letter_from_board.pos_y - DELTA)

									var.current_board_state[tile_y_on_board][tile_x_on_board] = '?'

									layers.letters_just_played.remove(letter_from_board)
									layers.selected_letter.add(letter_from_board)

									#refresh screen
									layers.letters_just_played.clear(window, var.background_no_letter)
									layers.letters_just_played.draw(window)

									var.current_background = window.copy()									
									layers.selected_letter.draw(window)
									pygame.display.update()

									pygame.mouse.set_cursor(*close_hand)
									var.current_action = "PLAY_A_LETTER"
							

							#------ CLIC ON BUTTONS (VISUAL) -------
							for button in layers.buttons_on_screen :
								if button.rect.collidepoint(cursor_pos_x, cursor_pos_y) == True :
									#change button state
									button.is_highlighted = False
									button.push()
									layers.buttons_on_screen.clear(window, var.background_empty)
									layers.buttons_on_screen.draw(window) 
							pygame.display.update()



						#------ PLAY A LETTER -------
						elif var.current_action == 'PLAY_A_LETTER' :

							#------ A LETTER IS SELECTED -------
							if len(layers.selected_letter) == 1 : 

								#------ CLIC ON THE HAND HOLDER ? -------
								for hand_holder in layers.hand_holder :

									if hand_holder.rect.collidepoint(cursor_pos_x, cursor_pos_y) == True :

										index_in_hand = hand_holder.indexAtPos(cursor_pos_x)

										#------ EMPTY SPOT ? -------
										if var.current_player.hand_state[index_in_hand] == 0 :

											selected_letter = layers.selected_letter.sprites()[0]
											
											delta_x, delta_y = layers.hand_holder.sprites()[0].pos_x + 0.1, layers.hand_holder.sprites()[0].pos_y + 0.1

											selected_letter.moveAtTile( delta_x + index_in_hand, delta_y )
											var.current_player.hand_state[index_in_hand] = selected_letter.id

											#change letter from layers
											var.current_player.hand.add(selected_letter)
											layers.selected_letter.remove(selected_letter)

											#refresh screen
											layers.selected_letter.clear(window, var.current_background)
											var.current_player.hand.draw(window)

											if display_new_score_in_real_time :
												incrementPredictedScore()
												layers.mask_text.draw(window)
												ui_text.drawText(STEP)

											var.current_background = window.copy()

											pygame.display.update()

											pygame.mouse.set_cursor(*open_hand)
											CURSOR_IS_OPEN_HAND = True

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


											if display_new_score_in_real_time :
												incrementPredictedScore()
												layers.mask_text.draw(window)
												ui_text.drawText(STEP)

											#TODO REFRESH TEXT
											var.current_background = window.copy()

											pygame.display.update()

											pygame.mouse.set_cursor(*open_hand)
											CURSOR_IS_OPEN_HAND = True

											var.current_action = "SELECT_A_LETTER"


					#~~~~~~~~~~~ RELEASE LEFT CLIC ~~~~~~~~~~~
					elif ( event_type == pygame.MOUSEBUTTONUP ) :

						#------ SELECT A LETTER -------
						if var.current_action == 'SELECT_A_LETTER' :

						
							#------ RELEASE CLIC ON A BUTTON (VISUAL) -------
							for button in layers.buttons_on_screen :

								if button.rect.collidepoint(cursor_pos_x, cursor_pos_y) == True :
									button.turnOnHighlighted()
									layers.buttons_on_screen.clear(window, var.background_empty)
									layers.buttons_on_screen.draw(window)

							#------ RELEASE CLIC ON PLAY BUTTON -------
							if ( (button_play.rect.collidepoint(cursor_pos_x, cursor_pos_y) == True) and (button_play.is_pushed) ):
		
								pygame.mouse.set_cursor(*arrow)
								button_play.release()

								if STEP == 0 :

									#reset Board
									layers.letters_on_board.empty()
									var.current_board_state = [ ['?' for i in range(TILES_PER_LINE)] for j in range(TILES_PER_LINE) ]

									# ___ DRAW BOARD ___
									"""
									#screeshot background empty (USELESS ?)
									layers.background.draw(window)
									layers.tiles.draw(window)
									layers.hand_holder.draw(window)
									layers.buttons_on_screen.draw(window)

									screeshot background no letter (USELESS ?)
									var.background_no_letter = window.copy()
									ar.current_background_no_text = window.copy()
									#ui_text.drawText(STEP)
									var.current_background = window.copy()
									"""

									# ___ UI elements new screen ___
									STEP = STEP + 1

									layers.buttons_on_screen.remove(button_play)

									progress_bar.fill()
									layers.buttons_on_screen.add(button_ok)
									#layers.buttons_on_screen.add(progress_bar.button_reinit)

									# ___ DRAW WINDOW ___
									#draw new screen
									layers.dark_filter.draw(window)
									layers.pop_up_window.draw(window)
									layers.buttons_on_screen.draw(window)
									var.background_pop_up_empty = window.copy()

									progress_bar.draw()
									ui_text.drawTextPopUp(STEP)

									#UPDATE
									pygame.display.update()
									var.current_action = "WINDOW_DISPLAYED"


							#------ RELEASE CLIC ON END TURN BUTTON -------
							if ( (button_end_turn.rect.collidepoint(cursor_pos_x, cursor_pos_y) == True) and (button_end_turn.is_pushed) ):

								if STEP in (3,6,9) :
									pygame.mouse.set_cursor(*arrow)

								"""
								logging.debug("End of turn board state : ")
								for line in var.current_board_state :
									logging.debug(line)
								"""
								button_end_turn.release()
								layers.buttons_on_screen.clear(window, var.background_empty)
								layers.buttons_on_screen.draw(window)

								#SCORES
								#calculate score
								var.last_words_and_scores = calculatePoints(layers.letters_just_played)

								words = []
								for association in var.last_words_and_scores :
									var.current_player.score += association[1]
									words.append(association[0])

								move_on = False

								#nothing played
								if ( len( layers.letters_just_played.sprites() ) == 0) :
									texts = ["Déposer vos lettres sur le plateau pour marquer des points."]
								#played something
								else :
									if len(words) == 0 :
										texts =["Ecrivez votre mot verticalement ou horizontalement et sans espace."]
									else :
										if var.current_player.score == MAPING_STEP_MAX_SCORE[STEP] :
											texts = ["Félicitations ! Vous avez marqué le score maximal."]
										elif var.current_player.score > MAPING_STEP_MAX_SCORE[STEP] :
											texts = ["Wow ... Mieux que prévu. Félicitations pour vos "+str(var.current_player.score)+" points !"]
										else :
											texts = ["Vous avez marqué "+str(var.current_player.score)+" points."]
										move_on = True

								#creeate pop up
								layers.pop_up.add( createPopUp(texts, LINE_HEIGHT=LINE_HEIGHT.SUBTITLE)  )

								# snapshot of before pop_up
								snapshot = window.copy()

								#display pop_up
								layers.dark_filter.draw(window)
								layers.pop_up.draw(window)
								pygame.display.update()

								MUST_DIPSLAY_POP_UP = True

								#prepare exit image (displayed when removing pop up)
								window.blit(snapshot, (0,0))

								#display score
								#logging.debug("New Player score : %s", str(var.current_player.score))
								#ui_text.drawText(COLOR.GREEN)
								#pygame.display.update()

								#TODO !!! activate TEMPO in final version
								#pygame.time.wait(1500)

								"""
								#LETTERS (USELESS ?)
								for letter in layers.letters_just_played :
									layers.letters_on_board.add(letter)
								"""

								if move_on:

									# ___ RESET ___
									#reset letters		
									layers.letters_just_played.empty()
									for letter in var.current_player.hand :
										letter.kill()
									layers.letters_on_board.empty()

									#reset board state
									var.current_board_state = [ ['?' for i in range(TILES_PER_LINE)] for j in range(TILES_PER_LINE) ]

									#reset score between turns
									var.current_player.score = 0

									# ___ RESET VISUAL ___
									#reset screenshot background no letter (USELESS ?)
									#window.blit(var.background_no_letter, (0,0))
									var.current_player.hand.clear(window, var.background_no_letter)
									layers.letters_just_played.clear(window, var.background_no_letter)

									layers.letters_on_board.draw(window)
									var.current_player.hand.draw(window)
									var.current_background_no_text = window.copy()
									#progress_bar.draw()
									var.current_background = window.copy()


									if STEP == 3 :

										# ___ DRAW BOARD ___
										window.blit(var.background_no_letter, (0,0))
										
										var.current_player.hand.draw(window)

										var.current_background_no_text = window.copy()
										ui_text.drawText(STEP)
										var.current_background = window.copy()

										#NEW SCREEN
										STEP = STEP + 1
										progress_bar.fill()									

										# ADD BUTTONS									
										layers.buttons_on_screen.remove(button_end_turn)
										layers.buttons_on_screen.add(button_ok)

										#layers.buttons_on_screen.add(checkbox_facile)
										#layers.buttons_on_screen.add(checkbox_moyen)
										#layers.buttons_on_screen.add(checkbox_difficile)

										for emoticom in all_emoticoms :
											layers.buttons_on_screen.add(emoticom)

										layers.buttons_on_screen.add(checkbox_function_shuffle)
										layers.buttons_on_screen.add(checkbox_function_display_bonus)

										# DRAW WINDOW
										layers.dark_filter.draw(window)
										layers.pop_up_window.draw(window)
										layers.buttons_on_screen.draw(window)
										
										progress_bar.draw()
										ui_text.drawTextPopUp(STEP)							


									elif STEP == 6 :

										# ___ RESET ___
										#reset Board
										layers.letters_on_board.empty()
										var.current_board_state = [ ['?' for i in range(TILES_PER_LINE)] for j in range(TILES_PER_LINE) ]

										#reset letters
										for letter in var.current_player.hand :
											letter.kill()

										# Reset buttons
										for button in layers.buttons_on_screen :
											if button.is_a_checkbox :
												button.empty()
										
										# ___ DRAW BOARD ___
										#screeshot background no letter (USELESS ?)
										window.blit(var.background_no_letter, (0,0))
										var.current_player.hand.draw(window)

										var.current_background_no_text = window.copy()
										ui_text.drawText(STEP)
										var.current_background = window.copy()


										# ___ NEXT STEP ___	
										STEP = STEP + 1
										progress_bar.fill()

										# new buttons
										layers.buttons_on_screen.remove(button_end_turn)
										if enable_shuffle_letter :
											layers.buttons_on_screen.remove(button_shuffle)	

										layers.buttons_on_screen.add(button_ok)

										#layers.buttons_on_screen.add(checkbox_facile2)
										#layers.buttons_on_screen.add(checkbox_moyen2)
										#layers.buttons_on_screen.add(checkbox_difficile2)

										for emo in all_emoticoms :
											layers.buttons_on_screen.add(emo)

										layers.buttons_on_screen.add(checkbox_function_shuffle2)
										layers.buttons_on_screen.add(checkbox_function_display_bonus2)
										#layers.buttons_on_screen.add(checkbox_function_score2)

										# ___ DRAW WINDOW ___
										#draw new screen
										layers.dark_filter.draw(window)
										layers.pop_up_window.draw(window)
										layers.buttons_on_screen.draw(window)

										
										progress_bar.draw()
										ui_text.drawTextPopUp(STEP)
										

									#LAST STEP
									elif STEP == 9 :

										# ___ RESET ___
										#reset letters
										for letter in var.current_player.hand :
											letter.kill()

										var.predicted_score = 0

										# ___ NEXT STEP ___
										STEP = STEP + 1
										progress_bar.fill()

										# new buttons
										layers.buttons_on_screen.remove(button_end_turn)
										if enable_shuffle_letter :
											layers.buttons_on_screen.remove(button_shuffle)	

										layers.buttons_on_screen.add(button_ok)

										# ___ DRAW WINDOW ___
										window.blit(var.background_pop_up_empty, (0,0))
										layers.buttons_on_screen.draw(window)
										progress_bar.draw()
										ui_text.drawTextPopUp(STEP)
									
									#pygame.display.update()
									var.current_action = "WINDOW_DISPLAYED"
									#break 


							if enable_shuffle_letter :
								#------ RELEASE CLIC ON SHUFFLE BUTTON -------
								if ( (button_shuffle.rect.collidepoint(cursor_pos_x, cursor_pos_y) == True) and (button_shuffle.is_pushed) ):
									button_shuffle.release()

									# ___ SHUFFLE ___
									give_help = choice( [True, True, True, True] )
									more_help = choice( [True, False, False] )	

									pos_x = (UI_LEFT_LIMIT)
									pos_y = layers.hand_holder.sprites()[0].pos_y + 0.1

									shuffle(var.current_player.hand_state)

									#TODO create function

									#logging.debug("hand state : %a", var.current_player.hand_state)

									if give_help :
										#logging.debug("litte help")

										if STEP == 6 :
											#logging.debug("STEP 6")

											letters_s = var.current_player.hand.findByName('S')
											if letters_s != [] :
												#logging.debug("S in hand")
												first_letter_s = letters_s[0]
												s_index = var.current_player.hand_state.index(first_letter_s.id)
												#reshuffle
												var.current_player.hand_state[0], var.current_player.hand_state[s_index] = var.current_player.hand_state[s_index], var.current_player.hand_state[0]
											
											letters_e = var.current_player.hand.findByName('E')
											if letters_e != [] :

												#logging.debug("E in hand")
												first_letter_e = letters_e[0]
												e_index = var.current_player.hand_state.index(first_letter_e.id)
												#reshuffle
												var.current_player.hand_state[6], var.current_player.hand_state[e_index] = var.current_player.hand_state[e_index], var.current_player.hand_state[6]

											if more_help :
												#logging.debug("MORE HELP")

												letters_c = var.current_player.hand.findByName('C')
												if letters_e != [] :

													#logging.debug("C in hand")
													first_letter_c = letters_c[0]
													c_index = var.current_player.hand_state.index(first_letter_c.id)
													#reshuffle
													var.current_player.hand_state[6], var.current_player.hand_state[c_index] = var.current_player.hand_state[c_index], var.current_player.hand_state[6]



										elif STEP == 9 :

											#logging.debug("STEP 9")

											letters_a = var.current_player.hand.findByName('A')
											if letters_a != [] :
												#logging.debug("A in hand")
												first_letter_a = letters_a[0]
												a_index = var.current_player.hand_state.index(first_letter_a.id)
												#reshuffle
												var.current_player.hand_state[0], var.current_player.hand_state[a_index] = var.current_player.hand_state[a_index], var.current_player.hand_state[0]
											
											letters_r = var.current_player.hand.findByName('R')
											if letters_r != [] :

												#logging.debug("R in hand")
												first_letter_r = letters_r[0]
												r_index = var.current_player.hand_state.index(first_letter_r.id)
												#reshuffle
												var.current_player.hand_state[5], var.current_player.hand_state[r_index] = var.current_player.hand_state[r_index], var.current_player.hand_state[5]

											if more_help :
												#logging.debug("MORE HELP")

												letters_v = var.current_player.hand.findByName('V')
												if letters_v != [] :

													#logging.debug("V in hand")
													first_letter_v = letters_v[0]
													v_index = var.current_player.hand_state.index(first_letter_v.id)
													#reshuffle
													var.current_player.hand_state[1], var.current_player.hand_state[v_index] = var.current_player.hand_state[v_index], var.current_player.hand_state[1]


									#logging.debug("NEW hand state : %a", var.current_player.hand_state)

									pos_x = (UI_LEFT_LIMIT)
									pos_y = pos_y = layers.hand_holder.sprites()[0].pos_y + 0.1

									hand_state = []
									for index in var.current_player.hand_state :

										if index != 0:
											var.current_player.hand.findByIndex(index).moveAtTile(pos_x, pos_y)
										pos_x = pos_x + 1

									# ___ UPDATE DISPLAY ___
									var.current_player.hand.clear(window, var.background_no_letter)
									var.current_player.hand.draw(window)	
									pygame.display.update()


							#------ RELEASE CLIC AWAY FROM BUTTON (VISUAL) -------
							for button in layers.buttons_on_screen :
								if button.is_pushed :
									button.release() #release all pushed buttons
									if button.rect.collidepoint(cursor_pos_x, cursor_pos_y) :
										button.turnOnHighlighted()
									else :
										button.turnOffHighlighted()

									layers.buttons_on_screen.clear(window, var.background_empty)
									layers.buttons_on_screen.draw(window)
									
									#TO DO - prevent artefact see line 1287 ?
									layers.selected_letter.clear(window, var.current_background)
									var.current_background = window.copy()
									layers.selected_letter.draw(window)
									
									pygame.display.update()


						#------ PLAY A SELECTED LETTER-------
						if var.current_action == 'PLAY_A_LETTER' and len(layers.selected_letter) == 1 :

							#TODO to improve based on "is a mouse" or "is a touchescreen"
							#not a simple fast clic
							if ( timer > 200 )  : 

								#------ CLIC ON THE HAND HOLDER ? -------
								for hand_holder in layers.hand_holder :

									if hand_holder.rect.collidepoint(cursor_pos_x, cursor_pos_y) == True :

										index_in_hand = hand_holder.indexAtPos(cursor_pos_x)

										#------ EMPTY SPOT ? -------
										if var.current_player.hand_state[index_in_hand] == 0 :

											selected_letter = layers.selected_letter.sprites()[0]	
											delta_x, delta_y = layers.hand_holder.sprites()[0].pos_x + 0.1, layers.hand_holder.sprites()[0].pos_y + 0.1

											selected_letter.moveAtTile( delta_x + index_in_hand, delta_y )
											var.current_player.hand_state[index_in_hand] = selected_letter.id

											var.current_player.hand.add(selected_letter)
											layers.selected_letter.remove(selected_letter)

											layers.selected_letter.clear(window, var.current_background)
											var.current_player.hand.draw(window)

											if display_new_score_in_real_time :
												incrementPredictedScore()
												layers.mask_text.draw(window)
												ui_text.drawText(STEP)								

											"""
											#TODO SIMPLIFY (separate stuff)
											#TODO CREATE A FUNCTION
											#remove previously displayed text
											layers.background.draw(window)
											layers.tiles.draw(window)
											layers.hand_holder.draw(window)
											layers.buttons_on_screen.draw(window)
											var.background_no_letter = window.copy()

											layers.letters_on_board.draw(window)
											layers.letters_just_played.draw(window)
											var.current_player.hand.draw(window)
											
											var.current_background_no_text = window.copy()
											progress_bar.draw()
											ui_text.drawText()

											var.current_background = window.copy()
											"""
											#TODO pop up score

											pygame.display.update()

											pygame.mouse.set_cursor(*open_hand)
											CURSOR_IS_OPEN_HAND = True

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

											if display_new_score_in_real_time :
												incrementPredictedScore()
												layers.mask_text.draw(window)
												ui_text.drawText(STEP)								

											"""
											#remove previously displayed text
											layers.background.draw(window)
											layers.tiles.draw(window)
											layers.hand_holder.draw(window)
											layers.buttons_on_screen.draw(window)
											var.background_no_letter = window.copy()

											layers.letters_on_board.draw(window)
											layers.letters_just_played.draw(window)
											var.current_player.hand.draw(window)
											var.current_background_no_text = window.copy()

											progress_bar.draw()
											ui_text.drawText()
											var.current_background = window.copy()
											"""
											# TODo pop up score

											pygame.display.update()

											pygame.mouse.set_cursor(*open_hand)
											CURSOR_IS_OPEN_HAND = True

											var.current_action = "SELECT_A_LETTER"



		#~~~~~~ MOUSE MOTION ~~~~~~	
		if(event_type == pygame.MOUSEMOTION ):

			mouse_pos = pygame.mouse.get_pos()
			cursor_pos_x = mouse_pos[0]
			cursor_pos_y = mouse_pos[1]

			#------ SELECT A LETTER ------ 
			if var.current_action == 'SELECT_A_LETTER' and not MUST_DIPSLAY_POP_UP :

				#------ CHANGE APPEARANCE OF BUTTONS (VISUAL) ------
				buttons_changed = False
				#TODO restrict area to boost performance
				for button in layers.buttons_on_screen :
					if ( button.rect.collidepoint(cursor_pos_x, cursor_pos_y) == True ) and ( not button.is_highlighted ) and (not button.is_pushed ) :
						button.turnOnHighlighted()
						pygame.mouse.set_cursor(*hand)
						buttons_changed = True
					elif ( button.rect.collidepoint(cursor_pos_x, cursor_pos_y) == False ) and ( button.is_highlighted ) and (not button.is_pushed ):
						button.turnOffHighlighted()
						pygame.mouse.set_cursor(*arrow)
						buttons_changed = True

				if buttons_changed :
					layers.buttons_on_screen.clear(window, var.background_empty)
					layers.buttons_on_screen.draw(window)
					pygame.display.update()

				collide = False
				for letter in layers.letters_just_played.sprites() :
					if letter.rect.collidepoint(cursor_pos_x, cursor_pos_y) == True :
						collide = True
						pygame.mouse.set_cursor(*open_hand)
						CURSOR_IS_OPEN_HAND = True		
				for letter in var.current_player.hand :
					if letter.rect.collidepoint(cursor_pos_x, cursor_pos_y) == True :
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

				layers.selected_letter.clear(window, var.current_background)
				layers.selected_letter.draw(window)

				pygame.display.update()


			#------ INFO ABOUT HOVERED TILE ------
			#TODO improve logic for better performance
			if display_type_of_tile_on_hoovering and not MUST_DIPSLAY_POP_UP :
				if var.current_action == 'SELECT_A_LETTER' or var.current_action == 'PLAY_A_LETTER':
					cursor_on_a_special_tile = False

					#Is cursor on a special tile ?
					for tile in layers.tiles :
						if tile.rect.collidepoint(cursor_pos_x, cursor_pos_y) :
							if  ( tile.name != 'normal' ) :
								cursor_on_a_special_tile = True

								#pop up not already displayed for this tile
								if tile.id != ui_text.id_tile_pop_up :

									#remove previously displayed text
									layers.background.draw(window)
									layers.tiles.draw(window)
									layers.hand_holder.draw(window)
									layers.buttons_on_screen.draw(window)
									var.background_no_letter = window.copy()

									layers.letters_on_board.draw(window)
									layers.letters_just_played.draw(window)
									var.current_player.hand.draw(window)
									var.current_background_no_text = window.copy()

									progress_bar.draw()
									ui_text.drawText(STEP)
									ui_text.drawHelpPopPup(tile, tile.rect.x+((2/60.0)*var.tile_size), tile.rect.y+var.tile_size-(2/60.0)*(var.tile_size))

									var.current_background = window.copy()
									layers.selected_letter.draw(window)
									pygame.display.update()

									ui_text.id_tile_pop_up = tile.id
									ui_text.pop_up_displayed = True
									break

					#If cursor on a normal tile
					if ( not cursor_on_a_special_tile and ui_text.pop_up_displayed ):
						#remove previously displayed text
						layers.background.draw(window)
						layers.tiles.draw(window)
						layers.hand_holder.draw(window)
						layers.buttons_on_screen.draw(window)
						var.background_no_letter = window.copy()

						layers.letters_on_board.draw(window)
						layers.letters_just_played.draw(window)
						var.current_player.hand.draw(window)
						var.current_background_no_text = window.copy()

						progress_bar.draw()
						ui_text.drawText(STEP)

						var.current_background = window.copy()
						layers.selected_letter.draw(window)
						pygame.display.update()

						ui_text.id_tile_pop_up = 0
						ui_text.pop_up_displayed = False



	#display fps
	#logging.debug('fps : %s', str(fps_clock.get_fps() ) )

	if MUST_DIPSLAY_POP_UP :
		if FRAMES_BEFORE_POP_UP_DISAPPEAR > 0 :
			FRAMES_BEFORE_POP_UP_DISAPPEAR -= 1
		else :
			MUST_DIPSLAY_POP_UP = False
			FRAMES_BEFORE_POP_UP_DISAPPEAR = 200
			layers.pop_up.empty()
			pygame.display.update()

logging.info("")
logging.info("Game has ended")
logging.info("")
logging.info("_________END OF LOG___________")
