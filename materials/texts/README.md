# How to add support for new language in the UI

## User interface content for different languages

_file : ui_content.ini_
_file : ui_error_pop_up.ini_

This file defines the text content to be displayed on the user interface. For now, only english and french are implemented.
In these files each parameter recieved a value in english and a value in french.

Rules to respect to edit each file :
* The different value come always in the same specific specific order.
* Values in different language are separated by the symbol '/'.
* Each element which will then be replaced by a value in the UI is written like <THIS> _(these elements are not mandatory)._

_The begining and trailling blank spaces of each text value will be dismissed when displayed on the UI._

To add a new language, you need to :
* Add the value for this language for each parameter by respecting the formatting rules and not changing the existing order. For instance :  
	current_player_turn = <CURRENT_PLAYER>'s turn / Tour de <CURRENT_PLAYER> / <CURRENT_PLAYER>s tur
* In the file '/config/game_settings.ini' change the value of 'ui_language' to the value of the added language. For instance :  
	ui_language = swedish

To also add a new language for the UI bouttons, you need to :
* In the folder'/Scrabble2/materials/images/assets/buttons/primary/' create a folder containing the buttons for your language. The names of these buttons must be exactly the same ones as the names ot the buttons already existing in the folders for other languages.
* Edit the file 'sources/main.py' like this :  
```python
path_buttons_french = path.abspath('../materials/images/assets/buttons/primary/french/')
path_buttons_english = path.abspath('../materials/images/assets/buttons/primary/english/')
path_buttons_swedish = path.abspath('../materials/images/assets/buttons/primary/swedish/') #new line

#...

if UI_LANGUAGE == 'english' :
	language_id = 0
	path_buttons = path_buttons_english
elif UI_LANGUAGE == 'french' :
	language_id = 1
	path_buttons = path_buttons_french
elif UI_LANGUAGE == 'swedish' : #new line
	language_id = 2 #new line
	path_buttons = path_buttons_swedish #new line
else :
	language_id = 0
	path_buttons = path_buttons_english
```
_This language_id  tells the system wich value to take for each parameters. This language_id respects the order given in the 'ui_content.ini' file_
