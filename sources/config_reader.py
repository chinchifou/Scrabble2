#~~~~~~~~~ CONFIG FILE READER ~~~~~~~~~

#This file read value from display_settings.ini and game_rules.ini and store them respectively into h_display_params and h_rules_params

#~~~~~~~~ Imports ~~~~~~~~

from os import path
import re


#~~~~~~~~ Returned variables ~~~~~~~~

#store result
h_display_params = {}
h_rules_params = {}
h_ui_params = {}
players = []


#~~~~~~~~ Returned variables ~~~~~~~~
def str_to_bool(s):
	if s == 'True' or s == 'true':
		return True
	elif s == 'False' or s == 'false':
		return False
	else :
		raise ValueError("Cannot convert {} to a bool".format(s))


#~~~~~~~~ Initialization ~~~~~~~~

#relative path
path_conf_disp_file = path.abspath('../config/display_settings.ini')
path_conf_rules_file = path.abspath('../config/game_settings.ini')
path_conf_language_file = path.abspath('../config/ui_content.ini')

#match everything of format >> multiple_letters = LeTTers
match_word = re.compile(r'^([a-z_]*)\s*=\s*([A-Za-z]*)\s*$')

#match everything of format >> other_letters = 251
match_integer = re.compile(r'^([a-z_]*)\s*=\s*([0-9]*)\s*$')

#match everything of format >> multiple_letters = LeTTers OTHERletters andSoOn
match_names = re.compile(r'^([a-z_]*)\s*=([^0-9])*$')

#match everything of format >> multiple_letters = UI text <VALUE1> / other UI text <VALUE1> AND <VALUE2>
match_ui_word = re.compile(r'([a-z_]*)\s*=\s*([éA-Za-z12<>\'/\s:._]*)\s*')



#~~~~~~~~ Retrieve data ~~~~~~~~

#display settings
for line in open(path_conf_disp_file,"r") :

	word_found = match_word.search(line)
	int_found = match_integer.search(line)

	if word_found :
		param = str(word_found.group(1))
		value = str_to_bool(word_found.group(2))
		if param == 'fullscreen' :
			h_display_params[ param ] = value		
		if param == 'resizable' :
			h_display_params[ param ] = value		
		if param == 'resolution_auto' :
			h_display_params[ param ] = value		
		if param == 'enable_hardware_accelerated' :
			h_display_params[ param ] = value	
		if param == 'enable_double_buffer' :
			h_display_params[ param ] = value

	if int_found :
		param = str(int_found.group(1))
		if param == 'custom_window_height' :
			h_display_params[ param ] = int(int_found.group(2))
		if param == 'max_fps' :
			h_display_params[ param ] = int(int_found.group(2))

#groupe rules
for line in open(path_conf_rules_file,"r") :

	word_found = match_word.search(line)
	int_found = match_integer.search(line)
	names_found = match_names.search(line)

	if word_found :
		param = str(word_found.group(1))
		if param == 'display_next_player_hand' :
			h_rules_params[ param ] = str_to_bool(word_found.group(2))
		if param == 'letters_language' :
			h_rules_params[ param ] = str(word_found.group(2))
		if param == 'ui_language' :
			h_rules_params[ param ] = str(word_found.group(2))

	if names_found :
		param = str(names_found.group(1))
		if param == 'players_names' :
			start = line.index('=')+1
			string_names = line[start:]
			names = string_names.strip().split(' ')
			for name in names :
				if name != '' :
					players.append(name)

	if int_found :
		param = str(int_found.group(1))
		if param == 'number_of_letters_per_hand' :
			h_rules_params[ param ] = int(int_found.group(2))

ui_possible_values = (
'current_player_turn',
'next_player_hand',
'scores',
'player_score',
'previous_turn_summary',
'word_and_score',
'scrabble_obtained',
'nothing_played',
'remaining_letters',
'remaining_letter',
'no_remaining_letter')

for line in open(path_conf_language_file,"r") :

	text_found = match_ui_word.search(line)

	if text_found :
		param = str(text_found.group(1))
		text = []

		if param in ui_possible_values:
			start = line.index('=')+1
			all_values = line[start:]
			all_values = all_values.strip().split('/')
			for value in all_values :
				if value != '' :
					text.append(value)
			h_ui_params [ param ] = text 
 


#should be alright for accents ... PROOF :
'''
f = open('result.txt', 'w')
for name in players :
	f.write(name)
	f.write('\n')
f.close()
'''
