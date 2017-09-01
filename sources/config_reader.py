#~~~~~~~ CONFIG FILE READER ~~~~~~~~

#~~~~~~~~ Imports ~~~~~~~~

from os import path
import re

#~~~~~~~~ Read file ~~~~~~~~

path_conf_file = path.abspath('../config/display_settings.ini')

config_file = open(path_conf_file,"r")
raw_display_settings = config_file.read()
config_file.close()

#~~~~~~~~ Clean data ~~~~~~~~

#remove everything except letters, numbers and symbols '_', ':' , '#' and '\n'
clean_display_settings = re.sub('[^A-Za-z0-9_:\\n#]', '', raw_display_settings)
#remove blank lines
lines_display_settings = [ line for line in clean_display_settings.split('\n') if ( line.strip() != '' ) ]

print(lines_display_settings)
#~~~~~~~~ Extract data ~~~~~~~~

h_params_values = {}

result = ["",""]
for line in lines_display_settings :
	result = line.split(':')
	h_params_values[result[0]] = result[1]

print()
print(h_params_values)

#~~~~~~~~ How to use ~~~~~~~~
#text = str(h_params_values["text"])
