#~~~~~~~ CONFIG FILE READER ~~~~~~~~

#~~~~~~~~ Imports ~~~~~~~~

from os import path
import re

#~~~~~~~~ Initialization ~~~~~~~~

#relative path
path_conf_disp_file = path.abspath('../config/display_settings.ini')
path_conf_rules_file = path.abspath('../config/game_rules.ini')

# match everything of format >> multiple_letters = LeTTers
match_word = re.compile(r'^([a-z_]*)\s*=\s*([A-Za-z]*)\s*$')

# match everything of format >> other_letters = 251
match_integer = re.compile(r'^([a-z_]*)\s*=\s*([0-9]*)\s*$')

# match everything of format >> multiple_letters = LeTTers OTHERletters andSoOn
match_names = re.compile(r'^([a-z_]*)\s*=([^0-9])*$')

#store result
h_display_params = {}
h_rules_params = {}
players = []

#~~~~~~~~ Retrieve data ~~~~~~~~

for line in open(path_conf_disp_file,"r") :

	word_found = match_word.search(line)
	int_found = match_integer.search(line)

	if word_found :
		param = str(word_found.group(1))
		value = bool(word_found.group(2))
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
		if param == 'custom_window_heigh' :
			h_display_params[ param ] = int(int_found.group(2))


for line in open(path_conf_rules_file,"r") :

	word_found = match_word.search(line)
	int_found = match_integer.search(line)
	names_found = match_names.search(line)

	if word_found :
		param = str(word_found.group(1))
		if param == 'display_next_player_hand' :
			h_rules_params[ param ] = bool(word_found.group(2))
		if param == 'language' :
			h_rules_params[ param ] = str(word_found.group(2))

	if names_found :
		param = str(names_found.group(1))
		if param == 'players_names' :
			start = line.index('=')+1
			string_names = line[start:]
			names = string_names.strip().split(' ')
			for name in names :
				players.append(name)

	if int_found :
		param = str(int_found.group(1))
		if param == 'number_of_letters_per_hand' :
			h_rules_params[ param ] = int(int_found.group(2))

'''
#should be alright for accents ... PROOF :
f = open('result.txt', 'w')
for name in players :
	f.write(name)
f.close()
'''
