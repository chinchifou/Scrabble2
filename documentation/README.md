# How to start ?

--------------
## On Windows:


### Installing the game


#### Solution 1 _(recommended)_:

##### 1. Download and install Python 3

* Go to : https://www.python.org/downloads/
* Download the latest version (version > 3.6).
* Install it.


##### 2. Download and install lxml module for Pyhton:

* Open a console as and administrator.
* Execute the command line :
	pip3 install lxml


##### 3. Download and install Pygame

* Open a console as and administrator.
* Execute the command line :
	pip3 install pygame


##### 4. Download the game

* Go to : https://github.com/chinchifou/Scrabble2
* Download it by using the "clone or download' button.


#### Solution 2 _(alternative methods)_:

_Use this solution if either solution 1 failed or if you are using a python version prior to 3.4._


##### 1. Download and install Python 3

* Go to : https://www.python.org/downloads/
* Download the desired version (version > 3.0).
* Install it.

To check the installation, type in a console :
```bash
python -v
```
_If you get a version number and no error message, everything is fine._


##### 2. Download and install lxml module for Pyhton:

* Go to : https://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml
* Download the latest version depending on your system :
** lxml‑4.2.2‑cp37‑cp37m‑win32.whl (Windows 32 bits(.
** lxml‑4.2.2‑cp37‑cp37m‑win_amd64.whl (Windows 64 bits).
* Install it.


##### 3. Download and install Pygame

* Go to : https://www.pygame.org/download.shtml
* Download the desired version (version > 3.0).
* Install it.


##### 4. Download the game

* Go to : https://github.com/chinchifou/Scrabble2
* Download it by using the 'clone or download' button.


### Setting up the game

To change your peferences go to the '/Scrabble2/config' folder.
* Edit "game_rules.ini" to change the players and to create custom rules.
* Edit "display_settings.ini" to change your display settings preferences (default is fullscreen - resolution auto)

**_More information in the README.md in the '/Scrabble2/documentation' folder._**


### Launching the game

#### Solution 1 _(easiest)_:
* Go to the game folder '/Scrabble 2'
* Double-click on 'launcher.bat'.


#### Solution 2 _(create a shortcut)_:

A windows desktop shortcut named 'Scrabble.lnk' is already provided in the game main folder. You can use it but will have to change the properties to make it work on your system. To do so :
* Go to the game folder '/Scrabble2'
* Copy-paste the link to the desired location (on the desktop for instance).
* Right-click on it to open the properties menu.
* Change the values so that it correctly points to '/Scrabble2/sources/laucher/launcher.bat' (to be adapted depending of the installation folder of the game)
* Save the modifications.
* Double-click on it.

_You can also recreate your own Windows shortcut by using the icon stored in '/materials/images/icon'_


------------
## On Linux:



### Installing the game

Type these command lines :
```bash  
sudo apt-get update
sudo apt-get install python3	
pip3 install lxml
pip3 install pygame
```
_go to the desired installation folder_
```bash 
git clone https://github.com/chinchifou/Scrabble2.git
```

Alternative methods if you want to use a python vresion prior to 3.4
```bash
sudo apt-get update
sudo apt-get install python3.0	
sudo apt-get install python3-lxml
```
_go to the desired installation folder_
```bash
git clone https://github.com/chinchifou/Scrabble2.git	sudo apt-get install python-pygame
```


### Setting up the game

To change your peferences go to the '/Scrabble2/config' folder.
* Edit "game_rules.ini" to change the players and to create custom rules.
* Edit "display_settings.ini" to change your display settings preferences (default is fullscreen - resolution auto)

_More information in the README.md in the '/Scrabble2/documentation' folder._


### Launching the game

Launch 'main.py' located in the '/sources/' folder.
To do so, from the main folder, type in a console :
```bash  
cd /sources
python3 main.py
```
