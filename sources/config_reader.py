#~~~~~~~ CONFIG FILE READER ~~~~~~~~

#~~~~~~~~ Imports ~~~~~~~~

from os import path
import re

#~~~~~~~~ Initialization ~~~~~~~~

#relative path
path_conf_file = path.abspath('../config/display_settings.ini')

# list of authorized parameters
params_list = (
'fullscreen',
'resizable',
'resolution_auto',
'custom_window_heigh',
'enable_double_buffer',
'enable_hardware_accelerated')

# match everything of format : multiple_letters : LeTTers
match_boolean = re.compile(r'^([a-z_]*)\s*:\s*([A-Za-z]*)\s*$')
# match everything of format : other_letters : 251
match_numeric = re.compile(r'^([a-z_]*)\s*:\s*([0-9]*)\s*$')

#store result
h_params_values = {}

#~~~~~~~~ Retrieve data ~~~~~~~~

for line in open(path_conf_file,"r") :

	bool_found = match_boolean.search(line)
	int_found = match_numeric.search(line)

	if bool_found :
		param = str(bool_found.group(1))
		if param in params_list :
			h_params_values[ param ] = bool(bool_found.group(2))

	if int_found :
		param = str(int_found.group(1))
		if param in params_list :
			h_params_values[ param ] = int(int_found.group(2))

#print(h_params_values)
