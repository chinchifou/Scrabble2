#~~~~~~~ CONFIG FILE READER ~~~~~~~~

#~~~~~~~~ Imports ~~~~~~~~

from os import path

#~~~~~~~~ Read file ~~~~~~~~

path_conf_file = path.abspath('../config/display_settings.ini')

config_file = open(path_conf_file,"r")
raw_display_settings = config_file.read()
config_file.close()

#~~~~~~~~ Extract data ~~~~~~~~

h_params_values = {}

lines_display_settings = raw_display_settings.split('\n')

result = ["",""]
for line in lines_display_settings :
	result = line.split(':')
	h_params_values[result[0]] = result[1]

#~~~~~~~~ How to use ~~~~~~~~

#text = str(h_params_values["text"])
