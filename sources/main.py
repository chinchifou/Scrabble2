#~~~~~~~~~ MAIN ~~~~~~~~~


#~~~~~~ IMPORTS ~~~~~~

#Standard library imports
from os import path
from os import makedirs

from math import floor
from random import randint, shuffle

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


#~~~~~~ GLOBAL VARIBLES ~~~~~~

#----- Constants -----
#define global scope for variables
global REFERENCE_TILE_SIZE, TILES_PER_LINE
#reference tile size for a 1920*1080 resolution
REFERENCE_TILE_SIZE = 60
#number of tiles on the board for each column and each row
TILES_PER_LINE = 15

global DELTA, UI_LEFT_LIMIT, UI_LEFT_INDENT, UI_INTERLIGNE, UI_TRANSPARENT_COMPONENTS, UI_COMPONENTS
#delta expressed in tiles from top left corner of the Window
DELTA = 1.5
#Left limit for text of the user interface
UI_LEFT_LIMIT = DELTA + TILES_PER_LINE + DELTA + 1.0
#Left limit with an identation in the user interface text
UI_LEFT_INDENT = UI_LEFT_LIMIT + 0.5
#Size expressed in tile of the space between two consecutive line of text
UI_INTERLIGNE = 1.0
# UI Sprites wich need to load image with transparency
UI_TRANSPARENT_COMPONENTS = ["letter", "button","ui_image"]
# UI Sprites wich need to load an image without transparency 
UI_COMPONENTS = ["board", "hand_holder", "tile"]

global PLAYERS, STEP
#all players
PLAYERS = []
# Turn number
STEP = 0

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

		self.background_no_letter = []
		self.current_background = []
		self.background_pop_up_empty = []
		self.current_background_no_text = []

		self.points_for_scrabble = 50

var = GameVariable()

#class used to print error in console and log file
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

		print('INITIAL SETTINGS ERROR : not enough letters at game start.')
		print('Some player has less letters than the others.')
		print('Possible solutions :')
		print('  1. add more letters')
		print('  2. reduce number of letters authorized per player')
		print('  3. reduce the number of players')
		print('')

ERROR = ErrorPrinter()
	

#class to store the different colors used in the game
class ColorPannel():
	def __init__(self):
		self.BLACK = (0,0,0)
		self.GREY_LIGHT = (143,144,138)
		self.GREY_DEEP = (40,41,35)

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

		self.buttons = GroupOfSprites()
		self.buttons_pop_up_window = GroupOfSprites()

		self.dark_filter = GroupOfSprites()
		self.pop_up_window = GroupOfSprites()
		self.progress_bar = GroupOfSprites()


		self.all = GroupOfSprites()

layers = Layer()

#class used to create interface text
class UIText():
	all = []
	def __init__(self, text, line_heigh, bold, pos_in_tiles):
		self.text = text
		self.line_heigh = line_heigh #TODO change to line height
		self.bold = int(bold)	

		self.font = pygame.font.SysFont("Calibri", floor(self.line_heigh*var.tile_size))
		self.font.set_bold(self.bold)

		self.pos_x_tiles, self.pos_y_tiles = pos_in_tiles[0], pos_in_tiles[1]
		self.pos_x, self.pos_y = pixels(self.pos_x_tiles, self.pos_y_tiles)

		self.bottom_tiles = self.pos_y_tiles + line_heigh

		UIText.all.append(self)

	def resize(self):
		self.font = pygame.font.SysFont("Calibri", floor(self.line_heigh*var.tile_size))
		self.font.set_bold(self.bold)

		self.pos_x, self.pos_y = pixels(self.pos_x_tiles, self.pos_y_tiles)

	def moveAtPixels(self, pos_x, pos_y):
		self.pos_x, self.pos_y = pos_x, pos_y
		self.pos_x_tiles, self.pos_y_tiles = tiles(self.pos_x, self.pos_y)

	def info(self):
		logging.debug("UI Text")
		logging.debug("Text : %s", self.text)
		logging.debug("Line heigh : %s", str(self.line_heigh))
		logging.debug("Bold : %s", str(self.bold))
		logging.debug("Font : %s", str(self.font.size))
		logging.debug("Position in tiles : %s, %s", self.pos_x_tiles, self.pos_y_tiles)
		logging.debug("Position in pixels : %s, %s", self.pos_x, self.pos_y)


#class used to diaply text pop up to the user
class UserInterFacePopUp(UIText):

	def __init__(self, text, line_heigh, bold, pos_in_tiles, text_color, background_color):
		UIText.__init__(self, text, line_heigh, bold, pos_in_tiles)
		self.text_color = text_color
		self.background_color = background_color

	def drawAt(self, pixels_pos_x, pixels_pos_y):

		self.moveAtPixels(pixels_pos_x, pixels_pos_y)	
		text = self.font.render(self.text, 1, self.text_color, self.background_color )
		window.blit( text, (self.pos_x, self.pos_y) )


#class storing userface interface text and displaying them
class UITextPrinter():

	def __init__(self, ui_content):


		#UI text init
		self.current_player_turn = UIText(ui_content['current_player_turn'][language_id], LINE_HEIGHT.TITLE, True, ( UI_LEFT_LIMIT, 2*UI_INTERLIGNE) )

		self.next_player_hand_header = UIText(ui_content['next_player_hand'][language_id], LINE_HEIGHT.NORMAL, True, ( UI_LEFT_LIMIT, self.current_player_turn.bottom_tiles+1.2+1*UI_INTERLIGNE) )

		self.next_player_hand = UIText("", LINE_HEIGHT.NORMAL, False, ( UI_LEFT_INDENT, self.next_player_hand_header.pos_y_tiles+1) )

		if display_next_player_hand :
			self.scores = UIText(ui_content['scores'][language_id], LINE_HEIGHT.NORMAL, True, ( UI_LEFT_LIMIT, self.next_player_hand.bottom_tiles+UI_INTERLIGNE) )
		else :
			self.scores = UIText(ui_content['scores'][language_id], LINE_HEIGHT.NORMAL, True, ( UI_LEFT_LIMIT, self.current_player_turn.bottom_tiles+1+UI_INTERLIGNE) )

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
		
		#hardcoded help pop-up
		self.id_tile_pop_up = 0
		self.pop_up_displayed = False

		self.double_letter = UserInterFacePopUp( ui_content['double_letter'][language_id], LINE_HEIGHT.POP_UP, False, (0, 0), COLOR.BLACK, COLOR.BLUE_LIGHT )
		self.triple_letter = UserInterFacePopUp( ui_content['triple_letter'][language_id], LINE_HEIGHT.POP_UP, False, (0, 0), COLOR.BLACK, COLOR.BLUE_DEEP )

		self.double_word = UserInterFacePopUp( ui_content['double_word'][language_id], LINE_HEIGHT.POP_UP, False, (0, 0), COLOR.BLACK, COLOR.RED_LIGHT )
		self.triple_word = UserInterFacePopUp( ui_content['triple_word'][language_id], LINE_HEIGHT.POP_UP, False, (0, 0), COLOR.BLACK, COLOR.RED_DEEP )


	#Draw UI text
	def drawText(self, *args):

		custom_color = COLOR.GREY_LIGHT
		for arg in args:
			custom_color = arg

		#Current player hand
		text = self.current_player_turn.font.render( self.current_player_turn.text.replace('<CURRENT_PLAYER>',var.current_player.name), 1, COLOR.GREY_LIGHT )
		window.blit(text, (self.current_player_turn.pos_x, self.current_player_turn.pos_y))

		#display next player hand
		if display_next_player_hand :
			#Next player hand header
			text = self.next_player_hand_header.font.render( self.next_player_hand_header.text.replace('<NEXT_PLAYER>',var.current_player.next().name), 1, COLOR.GREY_LIGHT )
			window.blit(text, (self.next_player_hand_header.pos_x, self.next_player_hand_header.pos_y))

			#Next player hand content
			str_hand = ""
			for index in var.current_player.next().hand_state :
				letter_to_display = var.current_player.next().hand.findByIndex(index) 
				if letter_to_display == None :
					str_hand += ' '
				else :
					str_hand += str ( letter_to_display.name ) + "  " 

			text = self.next_player_hand.font.render( str_hand , 1, COLOR.GREY_LIGHT )
			window.blit(text, (self.next_player_hand.pos_x, self.next_player_hand.pos_y))

		#Scores header
		text = self.scores.font.render( self.scores.text, 1, COLOR.GREY_LIGHT )
		window.blit(text, (self.scores.pos_x, self.scores.pos_y))

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
				window.blit(text, (self.player_score.pos_x, self.player_score.pos_y+(pos_y_delta*var.tile_size) ) )
			else :
				text = self.player_score.font.render( self.player_score.text.replace('_',' ').replace('<PLAYER>', player.name).replace('<SCORE>', str(player.score)), 1, COLOR.GREY_LIGHT )
				window.blit(text, (self.player_score.pos_x, self.player_score.pos_y+(pos_y_delta*var.tile_size) ) )
			pos_y_delta += 0.8

		#previous turn summary
		if False :
			if len(var.last_words_and_scores) > 0 :

				#header
				text = self.previous_turn_summary.font.render( self.previous_turn_summary.text.replace('<PREVIOUS_PLAYER>',var.current_player.previous().name), 1, COLOR.GREY_LIGHT )
				window.blit(text, (self.previous_turn_summary.pos_x, self.previous_turn_summary.pos_y))

				pos_y_delta = 0
				for association in var.last_words_and_scores :
					if association[0] == "!! SCRABBLE !!" :
						text = self.scrabble_obtained.font.render( self.scrabble_obtained.text.replace('<PREVIOUS_PLAYER>',var.current_player.previous().name).replace('<SCRABBLE_POINTS>', str(var.points_for_scrabble)), 1, COLOR.RED_DEEP )
						window.blit(text, (self.scrabble_obtained.pos_x, self.scrabble_obtained.pos_y+(pos_y_delta*var.tile_size)))
					else :		
						text = self.word_and_points.font.render( self.word_and_points.text.replace('<WORD>',association[0]).replace('<POINTS>', str(association[1])), 1, COLOR.GREY_LIGHT )
						window.blit(text, (self.word_and_points.pos_x, self.word_and_points.pos_y+(pos_y_delta*var.tile_size)))
					pos_y_delta += 0.8

			else :
				#nothing played
				text = self.nothing_played.font.render( self.nothing_played.text.replace('<PREVIOUS_PLAYER>',var.current_player.previous().name), 1, COLOR.GREY_LIGHT )
				window.blit(text, (self.nothing_played.pos_x, self.nothing_played.pos_y) )

		#remaining_letters
		if False :

			if len(var.bag_of_letters) == 0 :
				text = self.no_remaining_letter.font.render( self.no_remaining_letter.text, 1, COLOR.GREY_LIGHT )
					
				if len(var.last_words_and_scores) > 0 :
					window.blit(text, (self.no_remaining_letter.pos_x, self.no_remaining_letter.pos_y+ (pos_y_delta+UI_INTERLIGNE)*var.tile_size ) )
				else :
					window.blit(text, (self.no_remaining_letter.pos_x, self.nothing_played.pos_y+ (2*UI_INTERLIGNE)*var.tile_size ) )

			elif len(var.bag_of_letters) == 1 :
				text = self.remaining_letter.font.render( self.remaining_letter.text, 1, COLOR.GREY_LIGHT )
					
				if len(var.last_words_and_scores) > 0 :
					window.blit(text, (self.remaining_letter.pos_x, self.remaining_letter.pos_y+ (pos_y_delta+UI_INTERLIGNE)*var.tile_size ) )
				else :
					window.blit(text, (self.remaining_letter.pos_x, self.nothing_played.pos_y+ (2*UI_INTERLIGNE)*var.tile_size ) )

			else :
				text = self.remaining_letters.font.render( self.remaining_letters.text.replace( '<LETTERS_REMAINING>', str(len(var.bag_of_letters)) ), 1, COLOR.GREY_LIGHT )

				if len(var.last_words_and_scores) > 0 :
					window.blit(text, (self.remaining_letters.pos_x, self.remaining_letters.pos_y+ (pos_y_delta+UI_INTERLIGNE)*var.tile_size ) )
				else :
					window.blit(text, (self.remaining_letters.pos_x, self.nothing_played.pos_y+ (2*UI_INTERLIGNE)*var.tile_size ) )


	def drawTextPopUp(self, step):

		pop_up_window = layers.pop_up_window.sprites()[0]
		limit_left = tiles1( pop_up_window.rect.left )
		limit_top = tiles1( pop_up_window.rect.top )

		if step == 0 :
			all_texts = [
			UIText( "Bonjour !", LINE_HEIGHT.TITLE, True, (limit_left+1, limit_top+1) ),
			UIText( "Je suis votre ergonome virtuel.", LINE_HEIGHT.TITLE, True, (limit_left+1, limit_top+3) ),
			UIText( "Pouvez-vous m'aider à améliorer ce logiciel ?", LINE_HEIGHT.TITLE, True, (limit_left+1, limit_top+5) )
			]
		elif step == 1 :
			all_texts = [
			UIText( "Votre objectif :", LINE_HEIGHT.TITLE, True, (limit_left+1, limit_top+1) ),
			UIText( "Jouer un mot et marquer le plus de points possible.", LINE_HEIGHT.TITLE, False, (limit_top+1, limit_top+2.5) ),
			UIText( "Astuce :", LINE_HEIGHT.TITLE, True, (limit_left+1, limit_top+4.5) ),
			UIText( "Les cases bonus rapportent plus de points.", LINE_HEIGHT.TITLE, False, (limit_left+1, limit_top+6) )
			]
		elif step == 3 :
			all_texts = [
			UIText( "Alors, comment cela vous a t'il paru ? Je pense que l'on peut faire mieux ...", LINE_HEIGHT.NORMAL, False, (limit_left+1, limit_top+0.5) ),
			UIText( "Aidez moi à améliorer l'ergonomie de ce logiciel en répondant à ces questions.", LINE_HEIGHT.NORMAL, False, (limit_left+1, limit_top+1.5) ),
			UIText( "Marquer des points vous a paru :", LINE_HEIGHT.NORMAL, True, (limit_left+1, limit_top+3) ),
			UIText( "Facile", LINE_HEIGHT.NORMAL, False, (limit_left+2.5, limit_top+4.25) ),
			UIText( "Moyennement difficile", LINE_HEIGHT.NORMAL, False, (limit_left+2.5, limit_top+5.75) ),
			UIText( "Difficile", LINE_HEIGHT.NORMAL, False, (limit_left+2.5, limit_top+7.25) ),
			UIText( "Cochez ce qui vous a posé problème :", LINE_HEIGHT.NORMAL, True, (limit_left+1, limit_top+9) ),
			UIText( "Réussir à composer un mot", LINE_HEIGHT.NORMAL, False, (limit_left+2.5, limit_top+10.25) ),
			UIText( "Connaître l'effet des cases bonus", LINE_HEIGHT.NORMAL, False, (limit_left+2.5, limit_top+11.75) )
			]
		elif step == 4 :
			all_texts = [
			UIText( "J'ai pris en compte vos remarques.", LINE_HEIGHT.NORMAL, True, (limit_left+1, limit_top+0.5) ),
			UIText( "Voici une nouvelle version dans laquelle j'ai apporté quelques améliorations.", LINE_HEIGHT.NORMAL, False, (limit_left+1, limit_top+1.5) ),
			UIText( "Vous pouvez maintenant:", LINE_HEIGHT.NORMAL, False, (limit_left+1, limit_top+3) ),
			UIText( "> Mélanger les lettres.", LINE_HEIGHT.NORMAL, True, (limit_left+2, limit_top+4) ),
			UIText( "> Afficher l'effet des cases bonus.", LINE_HEIGHT.NORMAL, True, (limit_left+2, limit_top+5) )
			]
		elif step == 6 :
			all_texts = [
			UIText( "Alors, comment vous a paru cette nouvelle version ?", LINE_HEIGHT.NORMAL, True, (limit_top+1, limit_top+0.5) ),
			UIText( "Marquer des points vous a paru :", LINE_HEIGHT.NORMAL, True, (limit_left+1, limit_top+2) ),
			UIText( "Facile", LINE_HEIGHT.NORMAL, False, (limit_left+2.5, limit_top+3.25) ),
			UIText( "Moyennement difficile", LINE_HEIGHT.NORMAL, False, (limit_left+2.5, limit_top+4.75) ),
			UIText( "Difficile", LINE_HEIGHT.NORMAL, False, (limit_left+2.5, limit_top+6.25) ),
			UIText( "Cochez ce qui vous a posé problème :", LINE_HEIGHT.NORMAL, True, (limit_left+1, limit_top+8) ),
			UIText( "Réussir à composer un mot", LINE_HEIGHT.NORMAL, False, (limit_left+2.5, limit_top+9.25) ),
			UIText( "Connaître l'effet des cases bonus", LINE_HEIGHT.NORMAL, False, (limit_left+2.5, limit_top+10.75) ),
			UIText( "Calculer mon score", LINE_HEIGHT.NORMAL, False, (limit_left+2.5, limit_top+12.25) )
			]
		elif step == 7 :
			all_texts = [
			UIText( "J'ai pris en compte ces nouvelles remarques.", LINE_HEIGHT.NORMAL, True, (limit_left+1, limit_top+0.5) ),
			UIText( "Voici une dernière version dans laquelle j'ai apporté quelques améliorations.", LINE_HEIGHT.NORMAL, False, (limit_top+1, limit_top+2) ),
			UIText( "Voici ma proposition mais vous avez le choix d'ajouter ou de retirer des aides.", LINE_HEIGHT.NORMAL, False, (limit_top+1, limit_top+3) ),
			UIText( "Améliorations :", LINE_HEIGHT.NORMAL, True, (limit_left+1, limit_top+5) ),
			UIText( "Pouvoir mélanger les lettres.", LINE_HEIGHT.NORMAL, False, (limit_left+2.5, limit_top+6.5) ),
			UIText( "Afficher l'effet des cases bonus au survol.", LINE_HEIGHT.NORMAL, False, (limit_left+2.5, limit_top+8) ),
			UIText( "Afficher le score en temps réel", LINE_HEIGHT.NORMAL, False, (limit_left+2.5, limit_top+9.5) ),
			UIText( "Me proposer des mots", LINE_HEIGHT.NORMAL, False, (limit_left+2.5, limit_top+11) )
			]
		elif step == 9 :			
			all_texts = [
			UIText( "Notre travail est maintenant terminé.", LINE_HEIGHT.SUBTITLE, False, (limit_left+1, limit_top+4) ),
			UIText( "Merci de m'avoir aidé à améliorer l'ergonomie de ce logiciel.", LINE_HEIGHT.SUBTITLE, False, (limit_left+1, limit_top+6) ),
			UIText( "Il est bien mieux ainsi, n'est-ce pas ?", LINE_HEIGHT.SUBTITLE, False, (limit_left+1, limit_top+7) ),
			]
		elif step == 10 :
			all_texts = [
			UIText( "Comme nous venons de le voir, l'ergonomie c'est :", LINE_HEIGHT.SUBTITLE, False, (limit_left+1, limit_top+1) ),
			UIText( "> Ecouter et observer l'utilisateur pour cerner son besoin", LINE_HEIGHT.SUBTITLE, False, (limit_left+2, limit_top+2.5) ),
			UIText( "> Une science avec des méthodes pour améliorer le logiciel", LINE_HEIGHT.SUBTITLE, False, (limit_left+2, limit_top+4) ),
			UIText( "> Recommencer et améliorer jusqu'à satisfaire l'utilisateur", LINE_HEIGHT.SUBTITLE, False, (limit_left+2, limit_top+5.5) ),
			UIText( "En fait, l'ergonomie c'est l'avenir !", LINE_HEIGHT.SUBTITLE, False, (limit_left+1, limit_left+7.5) ),
			UIText( "Apprenez-en plus en regardant notre vidéo de présentation.", LINE_HEIGHT.SUBTITLE, False, (limit_left+1, limit_top+9.5) ),
			UIText( "A bientôt !", LINE_HEIGHT.SUBTITLE, True, (limit_left+1, limit_top+11.5) ),
			]			

		for text_it in all_texts :
			window.blit( text_it.font.render(text_it.text, 1, COLOR.WHITE), (text_it.pos_x, text_it.pos_y) )


	def drawHelpPopPup(self, tile, pixel_pos_x, pixel_pos_y):
		if tile.name == 'double_letter' :
			self.double_letter.drawAt(pixel_pos_x, pixel_pos_y)
		elif tile.name == 'triple_letter':
			self.triple_letter.drawAt(pixel_pos_x, pixel_pos_y)
		elif tile.name == 'double_word'or tile.name == 'start':
			self.double_word.drawAt(pixel_pos_x, pixel_pos_y)
		elif tile.name == 'triple_word':
			self.triple_word.drawAt(pixel_pos_x, pixel_pos_y)


#~~~~~~ CONVERTION ~~~~~~

#----- convert bewten tiles numbers and pixels -----
def tiles(value_in_pixels1, value_in_pixels2) :
	return ( round( value_in_pixels1/float(var.tile_size) ), round( value_in_pixels2/float(var.tile_size) ) )

def tiles1(value_in_pixels) :
	return ( round( value_in_pixels/float(var.tile_size) ) )

def pixels(value1_in_tiles, value2_in_tiles) :
	return ( (value1_in_tiles*var.tile_size), (value2_in_tiles*var.tile_size) )

def solo_pixels(value_in_tiles) :
	return ( (value_in_tiles*var.tile_size) )

def int_pixels(value1_in_tiles, value2_in_tiles) :
	return ( round(value1_in_tiles*var.tile_size), round(value2_in_tiles*var.tile_size) )

def indexInHandHolder(cursor_pos_x):
	delta_x_hand_holder_pix = layers.hand_holder.sprites()[0].rect.x
	index_in_hand = int( floor( (cursor_pos_x - delta_x_hand_holder_pix) / float(var.tile_size) ) )
	return index_in_hand


#~~~~~~ GAME CLASSES ~~~~~~


#----- ResizableSprite -----
#add native capacity to be resized
class ResizableSprite(pygame.sprite.Sprite):
	nb_created_instances = 0
	#received coordinates are expresed in tiles
	def __init__(self, name, pos_x, pos_y):
		#super class constructor
		pygame.sprite.Sprite.__init__(self, self.containers) #self.containers need to have a default container

		#unique id
		ResizableSprite.nb_created_instances += 1
		self.id = ResizableSprite.nb_created_instances
		#name and type
		self.name = name
		#position
		self.pos_x = pos_x
		self.pos_y = pos_y

		#load image
		if self.type in UI_TRANSPARENT_COMPONENTS :
			self.image = loadTransparentImage(path.join(self.path, self.name.replace('*','joker')+'.png'))
		elif self.type in UI_COMPONENTS :
			self.image = loadImage(path.join(self.path, self.name+'.png'))


		if not ( hasattr(self, 'width') and hasattr(self, 'height') ) :
			#auto detect width and height
			self.width, self.height = tiles (self.image.get_width(), self.image.get_height())

		#resize image
		self.image = pygame.transform.smoothscale(self.image, int_pixels(self.width, self.height ) )

		#set area to be displayed
		self.rect = pygame.Rect( pixels(self.pos_x, self.pos_y), pixels(self.width, self.height) )

	def resize(self):

		#reload image
		if self.type in UI_TRANSPARENT_COMPONENTS :
			self.image = loadTransparentImage(path.join(self.path, self.name.replace('*','joker')+'.png'))
		elif self.type in UI_COMPONENTS :
			self.image = loadImage(path.join(self.path, self.name+'.png'))

		#resize image
		self.image = pygame.transform.smoothscale(self.image, int_pixels(self.width, self.height) )
		#set area to be displayed
		self.rect = pygame.Rect( pixels(self.pos_x, self.pos_y), pixels(self.width, self.height) )

		if self.type == "board":
			ui_text.drawText()

	def info(self) :
		logging.debug("Sprite info :")
		logging.debug("id : %s", self.id)
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
		
		ResizableSprite.__init__(self, name, pos_x, pos_y)


#----- Hand holder -----
class Hand_holder(ResizableSprite):
	def __init__(self, name, pos_x, pos_y):
		self.type = 'hand_holder'
		#create custom width and height 
		self.width, self.height = 0.2 + var.number_of_letters_per_hand, 1.2
		self.path = path_background
		ResizableSprite.__init__(self, name, pos_x, pos_y)

#----- UI Surface -----
class UI_Surface(ResizableSprite):
	def __init__(self, name, pos_x, pos_y, surface):
		self.type = 'ui_surface'

		self.image = surface

		ResizableSprite.__init__(self, name, pos_x, pos_y)


#----- UI Image -----
class UI_Image(ResizableSprite):
	def __init__(self, name, path, pos_x, pos_y, width, height):

		self.type = 'ui_image'

		self.name = name
		self.path = path

		self.width, self.height = width, height

		ResizableSprite.__init__(self, name, pos_x, pos_y)


#----- Board -----
class Board(ResizableSprite):
	def __init__(self, name, pos_x, pos_y):
		self.type = 'board'
		self.width, self.height = 32, 18
		self.path = path_background
		
		ResizableSprite.__init__(self, name, pos_x, pos_y)


#----- Tiles -----
class Tile(ResizableSprite):
	def __init__(self, name, pos_x, pos_y):
		self.type = 'tile'
		self.path = path_tiles
		ResizableSprite.__init__(self, name, pos_x, pos_y)


#----- Buttons -----
class Button(ResizableSprite):
	def __init__(self, name, pos_x, pos_y):
		self.type = 'button'
		#self.width, self.height = 3, 1
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


class Checkbox(Button):
	def __init__(self, name, pos_x, pos_y):
		Button.__init__(self, name, pos_x, pos_y)
		self.type = 'checkbox'
		self.is_filled = False

	def fill(self):
		self.name = 'filled_'+self.name
		self.is_filled = True
		self.turnOnHighlighted()

	def empty(self):
		self.name = self.name.replace("filled_", "")
		self.is_filled = False
		self.turnOnHighlighted()


#----- Letter -----
class Letter(ResizableSprite):
	def __init__(self, name, pos_x, pos_y):
		self.type = 'letter'
		self.path = path_letters

		ResizableSprite.__init__(self, name, pos_x, pos_y)		

		self.points = POINTS_FOR[name]

	#move a letter at a given position expressed in tiles
	def moveAtTile(self, pos_x, pos_y) :
		self.rect.x, self.rect.y = pixels(pos_x, pos_y)
		self.pos_x, self.pos_y  = pos_x, pos_y

	#move a letter at a given position expressed in pixels
	def moveAtPixels(self, pos_x, pos_y) :
		self.rect.x, self.rect.y = pos_x, pos_y
		self.pos_x, self.pos_y  = tiles(pos_x, pos_y)


##----- Progress Bar -----
class ProgressBar():
	def __init__(self, pos_x, pos_y, width, height, nb_state):

		#create progress bar
		self.progress_bar_bck = UI_Image('progress_bar_background', path_background, pos_x, pos_y, width, height)
		layers.progress_bar.add(self.progress_bar_bck)

		#filling of the progress bar
		self.progress_bar_filling = UI_Image('progress_bar_tile', path_background, pos_x, pos_y, 0, height)
		layers.progress_bar.add(self.progress_bar_filling)

		self.state = 0
		self.nb_state = nb_state

		self.ratio_width = width/float(nb_state-1)


	def draw(self):

		layers.progress_bar.draw(window)

		text = UIText( "Etape : "+str(self.state)+" / 7", LINE_HEIGHT.PROGRESS_BAR, False, (28.6-7/3.0, 14.4) )
		window.blit( text.font.render(text.text, 1, COLOR.WHITE), (text.pos_x, text.pos_y) )

	def fill(self):

		self.state = (self.state+1)%(self.nb_state)

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

#----- Game window creation -----
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
		if (delta_x > 0 and delta_y > 0) :
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

			#TODO not close to older letters
			if (start_y == min_y and end_y == max_y and len( layers.letters_on_board.sprites() ) > 0):
				logging.debug("not played close to another word")
				if (delta_y+1 != len(letters_played) ) :
					logging.debug("there is a hole in the word")
				pass

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

			#TODO not close to older letters
			if (start_x == min_x and end_x == max_x and len( layers.letters_on_board.sprites() ) > 0):
				logging.debug("not played close to another word")
				if (delta_x+1 != len(letters_played) ) :
					logging.debug("there is a hole in the word")
				pass

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

fps_clock = pygame.time.Clock()
clic_clock = pygame.time.Clock() #TODO to use
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

tmp_first_hand = ['B','I','N','S','E', 'O']
tmp_second_hand = ['S','E','I','C','N','E','C']
tmp_third_hand = ['A','R','E','V','I', 'N']


start_hand = GroupOfSprites()
hand_state = []
pos_x = (UI_LEFT_LIMIT)
pos_y = ui_text.current_player_turn.pos_y_tiles+1


for tmp_letter in tmp_first_hand :

	letter = Letter(tmp_letter, pos_x, pos_y)
	start_hand.add(letter)
	hand_state.append(letter.id)
	pos_x = pos_x+1

hand_state.append(0)


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
		pos_y = ui_text.current_player_turn.pos_y_tiles+1

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

#----- Create board game -----

if game_is_running :

	#create background
	board = Board("empty_background", 0, 0) #automatically stored in the corresponding layer

	#create hand_holder
	hand_holder = Hand_holder("hand_holder", UI_LEFT_LIMIT - 0.1, ui_text.current_player_turn.pos_y_tiles+0.9)#automatically stored in the corresponding layer

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
	x, y = 2, 4
	for letter in "METHODES" :
		layers.letters_on_board.add( Letter(letter,DELTA+x,DELTA+y) )
		y += 1

	x, y = 1, 6
	for letter in "UTILISATEUR" :
		if (x, y) != (2,6) :
			layers.letters_on_board.add( Letter(letter,DELTA+x,DELTA+y) )
		x += 1

	x, y = 2, 10
	for letter in "ERGONOMIE" :
		if (x, y) != (2,10) :
			layers.letters_on_board.add( Letter(letter,DELTA+x,DELTA+y) )
		x += 1

	# ------- CREATES BUTTONS --------
	button_ok = Button("ok", 32/2.0 - 1, 14.5 )

	button_end_turn = Button("end_turn", tiles1(hand_holder.rect.x)+var.number_of_letters_per_hand + 0.2 + 0.75, ui_text.current_player_turn.pos_y_tiles+1)

	button_shuffle = Button("shuffle", tiles1(hand_holder.rect.x)+var.number_of_letters_per_hand + 0.2 + 0.75, button_end_turn.pos_y + 1.25)

	button_play = Button("play", 32/2.0 + 6, 8.5)

	button_reinit = Button("reinit", 29, 15) #TODO button reinit


	# ------- CHECKBOXES --------
	checkbox_facile = Checkbox("checkbox", 3, 6 )
	checkbox_moyen = Checkbox("checkbox", 3, 7.5 )
	checkbox_difficile = Checkbox("checkbox", 3, 9 )

	checkbox_facile2 = Checkbox("checkbox", 3, 5 )
	checkbox_moyen2 = Checkbox("checkbox", 3, 6.5 )
	checkbox_difficile2 = Checkbox("checkbox", 3, 8 )

	checkbox_function_shuffle = Checkbox("checkbox", 3, 12 )
	checkbox_function_display_bonus = Checkbox("checkbox", 3, 13.5 )
	#checkbox_function_score = Checkbox("checkbox", 3, 16 )

	checkbox_function_shuffle2 = Checkbox("checkbox", 3, 11 )
	checkbox_function_display_bonus2 = Checkbox("checkbox", 3, 12.50 )
	checkbox_function_score2 = Checkbox("checkbox", 3, 14 )

	checkbox_find_word = Checkbox("checkbox", 3, 8.25 )
	checkbox_bonus_cases = Checkbox("checkbox", 3, 9.75 )
	checkbox_calculate_score = Checkbox("checkbox", 3, 11.25 )
	checkbox_suggest_word = Checkbox("checkbox", 3, 12.75 )


	#create dark_filter
	mask_surface = pygame.Surface((var.window_width, var.window_height))
	mask_surface.fill(COLOR.BLACK)
	mask_surface.set_alpha(180)
	mask_surface = mask_surface.convert_alpha()
	dark_filter = UI_Surface('dark_filter', 0, 0, mask_surface)
	layers.dark_filter.add(dark_filter)

	#create window_pop_up
	pop_up_window_surface = pygame.Surface((28*var.tile_size, 14*var.tile_size))
	pop_up_window_surface.fill(COLOR.GREY_DEEP)				
	pop_up_window = UI_Surface('pop_up_window', 2, 2, pop_up_window_surface)
	layers.pop_up_window.add(pop_up_window)

	#create avatar
	#ui_avatar = UI_Image('ergonome', path_background, 22, 2.84, 6, 6) #Screen 32*18
	#ui_avatar = UI_Image('ergonome', path_background, 24, 3.84, 5, 5) #Screen 32*18
	ui_avatar = UI_Image('ergonome', path_background, 24, 9, 5, 5) #Screen 32*18

	layers.pop_up_window.add(ui_avatar)

	#create progress bar
	progress_bar = ProgressBar(28.6-7/3.0, 15, 7/3.0, 1.2/3.0, 8)


#----- first image -----

if game_is_running :

	layers.buttons.add(button_play)
	#layers.buttons.add(button_reinit)

	layers.background.draw(window)
	layers.tiles.draw(window)
	layers.buttons.draw(window)

	var.background_no_letter = window.copy()

	layers.letters_on_board.draw(window)
	var.current_background_no_text = window.copy()
	var.current_background = window.copy()

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

		#~~~~~~ WINDOW RESIZE ~~~~~~
		#TODO create a specific function ?
		elif ( event_type == pygame.VIDEORESIZE ) : #properly refresh the game window if a resize is detected
			
			#new width and height
			width = event.dict['size'][0]
			height = event.dict['size'][1]

			#create a fullscreen image fully black to prevent later artefacts
			window = resizeWindow(var.monitor_resolution.current_w, var.monitor_resolution.current_h, cfg_fullscreen, cfg_resizable, cfg_resolution_auto, cfg_custom_window_height, cfg_double_buffer, cfg_hardware_accelerated)
			pygame.draw.rect(window, COLOR.BLACK, ( (0,0), (var.monitor_resolution.current_w, var.monitor_resolution.current_h) ) )
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

			progress_bar.draw()
			ui_text.drawText()
			var.current_background = window.copy()

			layers.selected_letter.draw(window)

			if var.current_action == "POP_UP_DISPLAYED":
				layers.dark_filter.draw(window)
				layers.pop_up_window.draw(window)
				layers.buttons_pop_up_window.draw(window)
				progress_bar.draw()
				ui_text.drawTextPopUp(STEP)					

			pygame.display.update()
			

		# NORMAL EVENTS
		else :

			# //////// POP UP DISPLAYED ////////

			if (var.current_action == "POP_UP_DISPLAYED") :

				need_refresh_buttons_on_screen = False

				#~~~~~~~~~~~ MOUSE BUTTONS ~~~~~~~~~~~
				if ( ( (event_type == pygame.MOUSEBUTTONDOWN) or (event_type == pygame.MOUSEBUTTONUP) ) and event.button == 1 ) :

					timer = clic_clock.tick()

					#~~~~~~~~~~~ PRESS LEFT CLIC ~~~~~~~~~~~
					if ( event_type == pygame.MOUSEBUTTONDOWN ) :

						cursor_pos_x, cursor_pos_y = event.pos[0], event.pos[1]

						#------ CLIC ON BUTTONS (VISUAL) -------
						for button in layers.buttons_pop_up_window :
							if button.rect.collidepoint(cursor_pos_x, cursor_pos_y) == True :
								#change button state
								button.is_highlighted = False
								button.push()
								need_refresh_buttons_on_screen = True

					#~~~~~~~~~~~ RELEASE LEFT CLIC ~~~~~~~~~~~
					elif ( event_type == pygame.MOUSEBUTTONUP ) :

						#~~~~~~~~~~~ BUTTON OK ~~~~~~~~~~~
						if ( (button_ok.rect.collidepoint(cursor_pos_x, cursor_pos_y) == True) and (button_ok.is_pushed) ):

							button_ok.release()

							if STEP == 1 :

								window.blit(var.current_background, (0,0))

								layers.dark_filter.draw(window)
								layers.pop_up_window.draw(window)
								layers.buttons_pop_up_window.draw(window)

								progress_bar.draw()

								ui_text.drawTextPopUp(STEP)

								pygame.display.update()

								STEP = STEP + 1


							elif STEP == 4 :


								if checkbox_function_shuffle.is_filled :
									enable_shuffle_letter = True
									layers.buttons.add(button_shuffle)
								if checkbox_function_display_bonus.is_filled :
									display_type_of_tile_on_hoovering = True

								# Reset checkboxes
								for button in layers.buttons_pop_up_window :
									if button.type == "checkbox":
										button.empty()

								layers.background.draw(window)
								layers.tiles.draw(window)
								layers.hand_holder.draw(window)
								layers.buttons.draw(window)
								var.background_no_letter = window.copy()
								layers.letters_on_board.draw(window)
								layers.letters_just_played.draw(window)
								var.current_player.hand.draw(window)
								var.current_background_no_text = window.copy()
								ui_text.drawText()
								var.current_background = window.copy()
								layers.selected_letter.draw(window)

								layers.dark_filter.draw(window)
								layers.pop_up_window.draw(window)

								layers.buttons_pop_up_window.empty()
								layers.buttons_pop_up_window.add(button_ok)
								layers.buttons_pop_up_window.draw(window)

								progress_bar.draw()

								ui_text.drawTextPopUp(STEP)
								#TODO based on selected checkboxes

								STEP = STEP + 1


							elif STEP == 7 :

								# Keep track of choice
								tmp_enable_shuffle, tmp_display_pop_up, tmp_display_score = False, False, False

								if checkbox_function_shuffle2.is_filled :
									tmp_enable_shuffle = True
								if checkbox_function_display_bonus2.is_filled :
									tmp_display_pop_up = True
								if checkbox_function_score2.is_filled :
									tmp_display_score = True

								# Reset
								for button in layers.buttons_pop_up_window :
									if button.type == "checkbox":
										button.empty()
								layers.buttons_pop_up_window.empty()


								layers.background.draw(window)
								layers.tiles.draw(window)
								layers.hand_holder.draw(window)
								layers.buttons.draw(window)
								var.background_no_letter = window.copy()

								layers.letters_on_board.draw(window)
								layers.letters_just_played.draw(window)
								var.current_player.hand.draw(window)
								var.current_background_no_text = window.copy()

								progress_bar.draw()
								ui_text.drawText()
								var.current_background = window.copy()
								layers.selected_letter.draw(window)

								layers.dark_filter.draw(window)
								layers.pop_up_window.draw(window)

								layers.buttons_pop_up_window.add(button_ok)
								layers.buttons_pop_up_window.add(checkbox_find_word)
								layers.buttons_pop_up_window.add(checkbox_bonus_cases)
								layers.buttons_pop_up_window.add(checkbox_calculate_score)
								layers.buttons_pop_up_window.add(checkbox_suggest_word)

								if tmp_enable_shuffle :
									checkbox_find_word.fill()
								if tmp_display_pop_up :
									checkbox_bonus_cases.fill()
								if tmp_display_score :
									checkbox_calculate_score.fill()

								layers.buttons_pop_up_window.draw(window)
								
								progress_bar.draw()

								ui_text.drawTextPopUp(STEP)

								STEP = STEP + 1


							elif STEP == 8 :

								STEP = STEP + 1
								var.current_action = "SELECT_A_LETTER"

								if checkbox_find_word.is_filled :
									enable_shuffle_letter = True
									layers.buttons.add(button_shuffle)
								if checkbox_bonus_cases.is_filled :
									display_type_of_tile_on_hoovering = True
								if checkbox_calculate_score.is_filled :
									display_new_score_in_real_time = True

								# Reset
								for button in layers.buttons_pop_up_window :
									if button.type == "checkbox":
										button.empty()
								layers.buttons_pop_up_window.empty()

								var.current_board_state = [ ['?' for i in range(TILES_PER_LINE)] for j in range(TILES_PER_LINE) ]

								x, y = 2, 10
								for letter in "ERGONOMIE" :
									layers.letters_on_board.add( Letter(letter,DELTA+x,DELTA+y) )
									var.current_board_state[y][x] = letter
									x += 1

								layers.background.draw(window)
								layers.tiles.draw(window)
								layers.hand_holder.draw(window)
								layers.buttons.draw(window)
								var.background_no_letter = window.copy()

								layers.letters_on_board.draw(window)
								layers.letters_just_played.draw(window)
								var.current_player.hand.draw(window)
								var.current_background_no_text = window.copy()

								progress_bar.fill()
								progress_bar.draw()
								ui_text.drawText()
								var.current_background = window.copy()

								layers.selected_letter.draw(window)

								pygame.display.update()

							elif STEP == 10 :

								window.blit(var.background_pop_up_empty, (0,0))

								layers.buttons_pop_up_window.draw(window)
								progress_bar.draw()
								ui_text.drawTextPopUp(STEP)

								STEP = STEP + 1


							elif STEP == 11 :

								progress_bar.fill()

								# Reset conf
								enable_shuffle_letter = False
								display_type_of_tile_on_hoovering = False
								display_new_score_in_real_time = False

								# Reset Board
								var.current_board_state = [ ['?' for i in range(TILES_PER_LINE)] for j in range(TILES_PER_LINE) ]

								# Reset letters
								for letter in layers.letters_on_board :
									letter.kill()
								
								for letter in layers.letters_just_played :
									letter.kill()

								for letter in var.current_player.hand :
									letter.kill()

								x, y = 2, 4
								for letter in "METHODES" :
									layers.letters_on_board.add( Letter(letter,DELTA+x,DELTA+y) )
									y += 1

								x, y = 1, 6
								for letter in "UTILISATEUR" :
									if (x, y) != (2,6) :
										layers.letters_on_board.add( Letter(letter,DELTA+x,DELTA+y) )
									x += 1

								x, y = 2, 10
								for letter in "ERGONOMIE" :
									if (x, y) != (2,10) :
										layers.letters_on_board.add( Letter(letter,DELTA+x,DELTA+y) )
									x += 1

								layers.buttons.empty()
								layers.buttons_pop_up_window.empty()
								layers.buttons.add(button_play)

								# Reset player
								var.current_player.score = 0

								pos_x = (UI_LEFT_LIMIT)
								pos_y = ui_text.current_player_turn.pos_y_tiles+1

								hand_state = []
								for tmp_letter in tmp_first_hand :
									letter = Letter(tmp_letter, pos_x, pos_y)
									var.current_player.hand.add(letter)
									hand_state.append(letter.id)
									pos_x = pos_x+1

								PLAYERS[0].hand_state = hand_state


								layers.background.draw(window)
								layers.tiles.draw(window)
								layers.buttons.draw(window)
								var.background_no_letter = window.copy()

								layers.letters_on_board.draw(window)
								var.current_background_no_text = window.copy()
								var.current_background = window.copy()

								pygame.display.update()

								var.current_action = "SELECT_A_LETTER"							

								STEP = 0


							#STEP 2 / STEP 5
							elif STEP == 2 or STEP == 5 :

								layers.background.draw(window)
								layers.tiles.draw(window)
								layers.hand_holder.draw(window)
								layers.buttons.draw(window)
								var.background_no_letter = window.copy()

								layers.letters_on_board.draw(window)
								var.current_player.hand.draw(window)
								var.current_background_no_text = window.copy()

								progress_bar.fill()
								progress_bar.draw()
								ui_text.drawText()
								var.current_background = window.copy()

								pygame.display.update()

								STEP = STEP + 1
								var.current_action = "SELECT_A_LETTER"
								break

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


						#~~~~~~~~~~~ CHECKBOX ~~~~~~~~~~~
						for button in layers.buttons_pop_up_window :
							if button.type == "checkbox":
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
						
						for button in layers.buttons_pop_up_window :

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
					layers.buttons_pop_up_window.clear(window, var.background_pop_up_empty)
					layers.buttons_pop_up_window.draw(window)
					pygame.display.update()



				#~~~~~~ MOUSE MOTION ~~~~~~	
				elif(event_type == pygame.MOUSEMOTION ):

					mouse_pos = pygame.mouse.get_pos()
					cursor_pos_x = mouse_pos[0]
					cursor_pos_y = mouse_pos[1]

					#------ CHANGE APPEARANCE OF BUTTONS (VISUAL) ------
					buttons_changed = False
					for button in layers.buttons_pop_up_window :
						if ( button.rect.collidepoint(cursor_pos_x, cursor_pos_y) == True ) and ( not button.is_highlighted ) and (not button.is_pushed ) :
							button.turnOnHighlighted()
							buttons_changed = True
						elif ( button.rect.collidepoint(cursor_pos_x, cursor_pos_y) == False ) and ( button.is_highlighted ) and (not button.is_pushed ):
							button.turnOffHighlighted()
							buttons_changed = True

					if buttons_changed :
						layers.buttons_pop_up_window.clear(window, var.background_pop_up_empty)
						layers.buttons_pop_up_window.draw(window)

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

									#refresh screen
									layers.letters_just_played.clear(window, var.background_no_letter)
									layers.letters_just_played.draw(window)

									var.current_background = window.copy()									
									layers.selected_letter.draw(window)
									pygame.display.update()

									var.current_action = "PLAY_A_LETTER"
							

							#------ CLIC ON BUTTONS (VISUAL) -------
							for button in layers.buttons :
								if button.rect.collidepoint(cursor_pos_x, cursor_pos_y) == True :
									#change button state
									button.is_highlighted = False
									button.push()
									layers.buttons.clear(window, var.current_background)
									layers.buttons.draw(window) 
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
											
											delta_x, delta_y = layers.hand_holder.sprites()[0].pos_x + 0.1, layers.hand_holder.sprites()[0].pos_y + 0.1

											selected_letter.moveAtTile( delta_x + index_in_hand, delta_y )
											var.current_player.hand_state[index_in_hand] = selected_letter.id

											#change letter from layers
											var.current_player.hand.add(selected_letter)
											layers.selected_letter.remove(selected_letter)

											#refresh screen
											layers.selected_letter.clear(window, var.current_background)
											var.current_player.hand.draw(window)

											#print( calculatePoints(layers.letters_just_played) ) #TODO POINTS

											if display_new_score_in_real_time :
												incrementPredictedScore()									

											#TODO SIMPLIFY (separate stuff)
											#TODO CREATE A FUNCTION
											#remove previously displayed text
											"""
											layers.background.draw(window)
											layers.tiles.draw(window)
											layers.hand_holder.draw(window)
											layers.buttons.draw(window)
											var.background_no_letter = window.copy()

											layers.letters_on_board.draw(window)
											layers.letters_just_played.draw(window)
											
											var.current_player.hand.draw(window)
										
											var.current_background_no_text = window.copy()

											progress_bar.draw()
											ui_text.drawText()
											"""

											#TODO REFRESH TEXT
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


											#print( calculatePoints(layers.letters_just_played) ) #TODO POINTS

											if display_new_score_in_real_time :
												incrementPredictedScore()


											"""
											#remove previously displayed text
											layers.background.draw(window)
											layers.tiles.draw(window)
											layers.hand_holder.draw(window)
											layers.buttons.draw(window)
											var.background_no_letter = window.copy()

											layers.letters_on_board.draw(window)
											layers.letters_just_played.draw(window)
											var.current_player.hand.draw(window)
											var.current_background_no_text = window.copy()

											progress_bar.draw()
											ui_text.drawText()
											"""

											#TODO REFRESH TEXT
											var.current_background = window.copy()

											pygame.display.update()

											var.current_action = "SELECT_A_LETTER"


					#~~~~~~~~~~~ RELEASE LEFT CLIC ~~~~~~~~~~~
					elif ( event_type == pygame.MOUSEBUTTONUP ) :

						#------ SELECT A LETTER -------
						if var.current_action == 'SELECT_A_LETTER' :

						
							#------ RELEASE CLIC ON A BUTTON (VISUAL) -------
							for button in layers.buttons :

								if button.rect.collidepoint(cursor_pos_x, cursor_pos_y) == True :
									button.turnOnHighlighted()
									layers.buttons.clear(window, var.current_background)
									layers.buttons.draw(window)

							#------ RELEASE CLIC ON PLAY BUTTON -------
							if ( (button_play.rect.collidepoint(cursor_pos_x, cursor_pos_y) == True) and (button_play.is_pushed) ):

								button_play.release()

								if STEP == 0 :

									layers.letters_on_board.empty()
									var.current_board_state = [ ['?' for i in range(TILES_PER_LINE)] for j in range(TILES_PER_LINE) ]

									x, y = 1, 6
									for letter in "UTILISATEUR" :
										layers.letters_on_board.add( Letter(letter,DELTA+x, DELTA+y) )
										var.current_board_state[y][x] = letter
										x += 1

									layers.buttons_pop_up_window.add(button_ok)
									layers.buttons.empty()
									layers.buttons.add(button_end_turn)	

									layers.background.draw(window)
									layers.tiles.draw(window)
									layers.hand_holder.draw(window)
									layers.buttons.draw(window)

									var.background_no_letter = window.copy()

									layers.letters_on_board.draw(window)
									var.current_player.hand.draw(window)
									var.current_background_no_text = window.copy()

									ui_text.drawText()
									var.current_background = window.copy()

									layers.dark_filter.draw(window)
									layers.pop_up_window.draw(window)
									layers.buttons_pop_up_window.draw(window)

									var.background_pop_up_empty = window.copy()									

									progress_bar.fill()
									progress_bar.draw()
									ui_text.drawTextPopUp(STEP)

									pygame.display.update()

									STEP = STEP + 1

									var.current_action = "POP_UP_DISPLAYED"


							#------ RELEASE CLIC ON END TURN BUTTON -------
							if ( (button_end_turn.rect.collidepoint(cursor_pos_x, cursor_pos_y) == True) and (button_end_turn.is_pushed) ):

								"""
								logging.debug("End of turn board state : ")
								for line in var.current_board_state :
									logging.debug(line)
								"""

								button_end_turn.release()

								#scores
								var.last_words_and_scores = calculatePoints(layers.letters_just_played)


								for association in var.last_words_and_scores :
									var.current_player.score +=  association[1]
								
								var.predicted_score = 0

								logging.debug("New Player score : %s", str(var.current_player.score))

								#letters
								for letter in layers.letters_just_played :
									layers.letters_on_board.add(letter)

								layers.letters_just_played.empty()
								window.blit(var.background_no_letter, (0,0))

								var.current_player.hand.clear(window, var.background_no_letter)
								layers.letters_just_played.clear(window, var.background_no_letter)

								layers.letters_on_board.draw(window)
								var.current_player.hand.draw(window)
								var.current_background_no_text = window.copy()

								progress_bar.draw()
								ui_text.drawText(COLOR.GREEN)
								var.current_background = window.copy()

								pygame.display.update()

								#reset score between turns
								var.current_player.score = 0


								#TEMPO to see score
								#TODO activate in final version
								#pygame.time.wait(1500)


								if STEP == 3 :

									layers.letters_on_board.empty()
									var.current_board_state = [ ['?' for i in range(TILES_PER_LINE)] for j in range(TILES_PER_LINE) ]

									x, y = 2, 4
									for letter in "METHODES" :
										layers.letters_on_board.add( Letter(letter,DELTA+x,DELTA+y) )
										var.current_board_state[y][x] = letter
										y += 1

									for letter in var.current_player.hand :
										letter.kill()

									pos_x = (UI_LEFT_LIMIT)
									pos_y = ui_text.current_player_turn.pos_y_tiles+1

									hand_state = []
									for tmp_letter in tmp_second_hand :

										letter = Letter(tmp_letter, pos_x, pos_y)
										var.current_player.hand.add(letter)
										hand_state.append(letter.id)
										pos_x = pos_x+1

									PLAYERS[0].hand_state = hand_state

									window.blit(var.background_no_letter, (0,0))
									
									var.current_player.hand.draw(window)

									var.current_background_no_text = window.copy()
									ui_text.drawText(COLOR.GREY_LIGHT)
									var.current_background = window.copy()

									layers.buttons_pop_up_window.add(checkbox_facile)
									layers.buttons_pop_up_window.add(checkbox_moyen)
									layers.buttons_pop_up_window.add(checkbox_difficile)

									layers.buttons_pop_up_window.add(checkbox_function_shuffle)
									layers.buttons_pop_up_window.add(checkbox_function_display_bonus)

									layers.dark_filter.draw(window)
									layers.pop_up_window.draw(window)
									layers.buttons_pop_up_window.draw(window)
									
									progress_bar.fill()
									progress_bar.draw()

									ui_text.drawTextPopUp(STEP)

									STEP = STEP + 1


								elif STEP == 6 :

									layers.letters_on_board.empty()
									var.current_board_state = [ ['?' for i in range(TILES_PER_LINE)] for j in range(TILES_PER_LINE) ]

									for letter in var.current_player.hand :
										letter.kill()

									pos_x = (UI_LEFT_LIMIT)
									pos_y = ui_text.current_player_turn.pos_y_tiles+1

									hand_state = []
									for tmp_letter in tmp_third_hand :

										letter = Letter(tmp_letter, pos_x, pos_y)
										var.current_player.hand.add(letter)
										hand_state.append(letter.id)
										pos_x = pos_x+1

									PLAYERS[0].hand_state = hand_state


									window.blit(var.background_no_letter, (0,0))
									var.current_player.hand.draw(window)

									var.current_background_no_text = window.copy()
									ui_text.drawText(COLOR.GREY_LIGHT)
									var.current_background = window.copy()

									layers.dark_filter.draw(window)
									layers.pop_up_window.draw(window)

									# Reset
									for button in layers.buttons_pop_up_window :
										if button.type == "checkbox":
											button.empty()
									layers.buttons_pop_up_window.empty()

									layers.buttons_pop_up_window.add(button_ok)
									layers.buttons_pop_up_window.add(checkbox_facile2)
									layers.buttons_pop_up_window.add(checkbox_moyen2)
									layers.buttons_pop_up_window.add(checkbox_difficile2)

									layers.buttons_pop_up_window.add(checkbox_function_shuffle2)
									layers.buttons_pop_up_window.add(checkbox_function_display_bonus2)
									layers.buttons_pop_up_window.add(checkbox_function_score2)

									layers.buttons_pop_up_window.draw(window)

									progress_bar.fill()
									progress_bar.draw()

									ui_text.drawTextPopUp(STEP)

									STEP = STEP + 1

								#LAST STEP
								elif STEP == 9 :

									for letter in var.current_player.hand :
										letter.kill()


									window.blit(var.background_no_letter, (0,0))
									
									var.current_player.hand.draw(window)
									var.current_background_no_text = window.copy()

									ui_text.drawText(COLOR.GREY_LIGHT)
									var.current_background = window.copy()

									layers.buttons_pop_up_window.add(button_ok)

									layers.dark_filter.draw(window)
									layers.pop_up_window.draw(window)
									layers.buttons_pop_up_window.draw(window)

									progress_bar.fill()
									progress_bar.draw()

									ui_text.drawTextPopUp(STEP)

									STEP = STEP + 1

								
								pygame.display.update()
								var.current_action = "POP_UP_DISPLAYED"
								break 


							if enable_shuffle_letter :
								#------ RELEASE CLIC ON SHUFFLE BUTTON -------
								if ( (button_shuffle.rect.collidepoint(cursor_pos_x, cursor_pos_y) == True) and (button_shuffle.is_pushed) ):
									button_shuffle.release()

									shuffle(var.current_player.hand_state)

									pos_x = (UI_LEFT_LIMIT)
									pos_y = ui_text.current_player_turn.pos_y_tiles+1

									hand_state = []
									for index in var.current_player.hand_state :

										if index != 0:
											var.current_player.hand.findByIndex(index).moveAtTile(pos_x, pos_y)
										pos_x = pos_x + 1

									layers.background.draw(window)
									layers.tiles.draw(window)
									layers.hand_holder.draw(window)
									layers.buttons.draw(window)
									var.background_no_letter = window.copy()
									layers.letters_on_board.draw(window)
									layers.letters_just_played.draw(window)
									var.current_player.hand.draw(window)
									
									var.current_background_no_text = window.copy()
									progress_bar.draw()
									ui_text.drawText()
									var.current_background = window.copy()

									layers.selected_letter.draw(window)
									
									pygame.display.update()


							#------ RELEASE CLIC AWAY FROM BUTTON (VISUAL) -------
							for button in layers.buttons :
								if button.is_pushed :
									button.release() #release all pushed buttons
									if button.rect.collidepoint(cursor_pos_x, cursor_pos_y) :
										button.turnOnHighlighted()
									else :
										button.turnOffHighlighted()

									layers.buttons.clear(window, var.current_background)
									layers.buttons.draw(window)
									
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

										index_in_hand = indexInHandHolder(cursor_pos_x)

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


											#print( calculatePoints(layers.letters_just_played) ) #TODO POINTS

											if display_new_score_in_real_time :
												incrementPredictedScore()									

											#TODO SIMPLIFY (separate stuff)
											#TODO CREATE A FUNCTION
											#remove previously displayed text
											layers.background.draw(window)
											layers.tiles.draw(window)
											layers.hand_holder.draw(window)
											layers.buttons.draw(window)
											var.background_no_letter = window.copy()

											layers.letters_on_board.draw(window)
											layers.letters_just_played.draw(window)
											var.current_player.hand.draw(window)
											
											var.current_background_no_text = window.copy()
											progress_bar.draw()
											ui_text.drawText()

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


											#print( calculatePoints(layers.letters_just_played) ) #TODO POINTS

											if display_new_score_in_real_time :
												incrementPredictedScore()									

											#remove previously displayed text
											layers.background.draw(window)
											layers.tiles.draw(window)
											layers.hand_holder.draw(window)
											layers.buttons.draw(window)
											var.background_no_letter = window.copy()

											layers.letters_on_board.draw(window)
											layers.letters_just_played.draw(window)
											var.current_player.hand.draw(window)
											var.current_background_no_text = window.copy()

											progress_bar.draw()
											ui_text.drawText()
											var.current_background = window.copy()

											pygame.display.update()

											var.current_action = "SELECT_A_LETTER"



		#~~~~~~ MOUSE MOTION ~~~~~~	
		if(event_type == pygame.MOUSEMOTION ):

			mouse_pos = pygame.mouse.get_pos()
			cursor_pos_x = mouse_pos[0]
			cursor_pos_y = mouse_pos[1]

			#------ SELECT A LETTER ------ 
			if var.current_action == 'SELECT_A_LETTER' :

				#------ CHANGE APPEARANCE OF BUTTONS (VISUAL) ------
				buttons_changed = False
				#TODO restrict area to boost performance
				for button in layers.buttons :
					if ( button.rect.collidepoint(cursor_pos_x, cursor_pos_y) == True ) and ( not button.is_highlighted ) and (not button.is_pushed ) :
						button.turnOnHighlighted()
						buttons_changed = True
					elif ( button.rect.collidepoint(cursor_pos_x, cursor_pos_y) == False ) and ( button.is_highlighted ) and (not button.is_pushed ):
						button.turnOffHighlighted()
						buttons_changed = True

				if buttons_changed :
					layers.buttons.clear(window, var.current_background)
					layers.buttons.draw(window)
					pygame.display.update()


			#------ MOVE SELECTED LETTER ------ 
			if len(layers.selected_letter) == 1 :
				layers.selected_letter.sprites()[0].moveAtPixels(cursor_pos_x - var.delta_pos_on_tile[0], cursor_pos_y - var.delta_pos_on_tile[1])

				layers.selected_letter.clear(window, var.current_background)
				layers.selected_letter.draw(window)

				pygame.display.update()


			#------ INFO ABOUT HOVERED TILE ------
			#TODO improve logic for better performance
			if display_type_of_tile_on_hoovering :
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
									layers.buttons.draw(window)
									var.background_no_letter = window.copy()

									layers.letters_on_board.draw(window)
									layers.letters_just_played.draw(window)
									var.current_player.hand.draw(window)
									var.current_background_no_text = window.copy()

									progress_bar.draw()
									ui_text.drawText()
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
						layers.buttons.draw(window)
						var.background_no_letter = window.copy()

						layers.letters_on_board.draw(window)
						layers.letters_just_played.draw(window)
						var.current_player.hand.draw(window)
						var.current_background_no_text = window.copy()

						progress_bar.draw()
						ui_text.drawText()

						var.current_background = window.copy()
						layers.selected_letter.draw(window)
						pygame.display.update()

						ui_text.id_tile_pop_up = 0
						ui_text.pop_up_displayed = False

	#display fps
	#logging.debug('fps : %s', str(fps_clock.get_fps() ) )

logging.info("")
logging.info("Game has ended")
logging.info("")
logging.info("_________END OF LOG___________")
