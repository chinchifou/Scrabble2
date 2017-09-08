#~~~~ GAME RULES ~~~~

#DICTIONARIES
#ENGLISH
english_letters = [] #total length must be 100
for i in range(12):
	english_letters.append('E')
for i in range(9):
	english_letters.append('I')
for i in range(8):
	english_letters.append('O')
for i in range(6):
	english_letters.append('N')
	english_letters.append('R')
	english_letters.append('T')
for i in range(4) :
	english_letters.append('S')
	english_letters.append('U')
	english_letters.append('L')
	english_letters.append('D')
for i in range(3):
	english_letters.append('G')
for i in range(2):	
	english_letters.append('M')
	english_letters.append('B')
	english_letters.append('C')
	english_letters.append('P')
	english_letters.append('F')
	english_letters.append('H')
	english_letters.append('V')
	english_letters.append('*')
	english_letters.append('W')
	english_letters.append('Y')
english_letters.append('J')
english_letters.append('Q')
english_letters.append('K')
english_letters.append('X')
english_letters.append('Z')

#FRENCH
french_letters = [] #total length must be 102
for i in range(15):
	french_letters.append('E')
for i in range(9):
	french_letters.append('A')
for i in range(8):
	french_letters.append('I')
for i in range(6):
	french_letters.append('N')
	french_letters.append('O')
	french_letters.append('R')
	french_letters.append('S')
	french_letters.append('T')
	french_letters.append('U')
for i in range(5):
	french_letters.append('L')
for i in range(3):
	french_letters.append('D')
	french_letters.append('M')
for i in range(2):
	french_letters.append('G')
	french_letters.append('B')
	french_letters.append('C')
	french_letters.append('P')
	french_letters.append('F')
	french_letters.append('H')
	french_letters.append('V')
	french_letters.append('*')
french_letters.append('J')
french_letters.append('Q')
french_letters.append('K')
french_letters.append('W')
french_letters.append('X')
french_letters.append('Y')
french_letters.append('Z')


#POINTS
#ENGLISH
english_points = {
'*' : 0,
'A' : 1,
'B' : 3,
'C' : 3,
'D' : 2,
'E' : 1,
'F' : 4,
'G' : 2,
'H' : 4,
'I' : 1,
'J' : 8,
'K' : 5,
'L' : 1,
'M' : 3,
'N' : 1,
'O' : 1,
'P' : 3,
'Q' : 10,
'R' : 1,
'S' : 1,
'T' : 1,
'U' : 1,
'V' : 4,
'W' : 4,
'X' : 8,
'Y' : 4,
'Z' : 10
}

#FRENCH
french_points = {
'*' : 0,
'A' : 1,
'B' : 3,
'C' : 3,
'D' : 2,
'E' : 1,
'F' : 4,
'G' : 2,
'H' : 4,
'I' : 1,
'J' : 8,
'K' : 10,
'L' : 1,
'M' : 2,
'N' : 1,
'O' : 1,
'P' : 3,
'Q' : 8,
'R' : 1,
'S' : 1,
'T' : 1,
'U' : 1,
'V' : 4,
'W' : 10,
'X' : 10,
'Y' : 10,
'Z' : 10
}

#LAYOUT OF THE BONUSES ON THE BOARD
# 0 : start
# 1 : normal tile
# 2 : double letter
# 3 : triple letter
# 4 : double word
# 5 : triple word
LAYOUT = [
[5,1,1,2,1,1,1,5,1,1,1,2,1,1,5],
[1,4,1,1,1,3,1,1,1,3,1,1,1,4,1],
[1,1,4,1,1,1,2,1,2,1,1,1,4,1,1],
[2,1,1,4,1,1,1,2,1,1,1,4,1,1,2],
[1,1,1,1,4,1,1,1,1,1,4,1,1,1,1],
[1,3,1,1,1,3,1,1,1,3,1,1,1,3,1],
[1,1,2,1,1,1,2,1,2,1,1,1,2,1,1],
[5,1,1,2,1,1,1,0,1,1,1,2,1,1,5],
[1,1,2,1,1,1,2,1,2,1,1,1,2,1,1],
[1,3,1,1,1,3,1,1,1,3,1,1,1,3,1],
[1,1,1,1,4,1,1,1,1,1,4,1,1,1,1],
[2,1,1,4,1,1,1,2,1,1,1,4,1,1,2],
[1,1,4,1,1,1,2,1,2,1,1,1,4,1,1],
[1,4,1,1,1,3,1,1,1,3,1,1,1,4,1],
[5,1,1,2,1,1,1,5,1,1,1,2,1,1,5]
]


'''
TO DO : PUT ELSEWHERE
# /// DO NOT REMOVE ///
#AUTOMATICALY CHOOSE DICTIONNARY AND POINTS BASED ON LANGUAGE SELECTION
if LANGUAGE == 'french' :
	BAG_OF_LETTERS = french_letters #choose current dictionary
	POINTS = french_points #choose points attributed per letter

elif LANGUAGE == 'english' :
	BAG_OF_LETTERS = english_letters
	POINTS = english_points

elif LANGUAGE == 'custom': #create your custom mix inside this one
	BAG_OF_LETTERS = french_letters
	LANGUAGE = 'french' #needed to find the folder where the letters are sotored
	POINTS = english_points

else: #default value
	BAG_OF_LETTERS = english_letters
	POINTS = english_points
'''
