#~~~~~~ GAMES RULES ~~~~~~


#~~~~~~ DICTIONARIES ~~~~~~

#----- English -----
letters_english = [] #total length must be 100
for i in range(12):
	letters_english.append('E')
for i in range(9):
	letters_english.append('I')
for i in range(8):
	letters_english.append('O')
for i in range(6):
	letters_english.append('N')
	letters_english.append('R')
	letters_english.append('T')
for i in range(4) :
	letters_english.append('S')
	letters_english.append('U')
	letters_english.append('L')
	letters_english.append('D')
for i in range(3):
	letters_english.append('G')
for i in range(2):	
	letters_english.append('M')
	letters_english.append('B')
	letters_english.append('C')
	letters_english.append('P')
	letters_english.append('F')
	letters_english.append('H')
	letters_english.append('V')
	letters_english.append('*')
	letters_english.append('W')
	letters_english.append('Y')
letters_english.append('J')
letters_english.append('Q')
letters_english.append('K')
letters_english.append('X')
letters_english.append('Z')

#----- French -----
letters_french = [] #total length must be 102
for i in range(15):
	letters_french.append('E')
for i in range(9):
	letters_french.append('A')
for i in range(8):
	letters_french.append('I')
for i in range(6):
	letters_french.append('N')
	letters_french.append('O')
	letters_french.append('R')
	letters_french.append('S')
	letters_french.append('T')
	letters_french.append('U')
for i in range(5):
	letters_french.append('L')
for i in range(3):
	letters_french.append('D')
	letters_french.append('M')
for i in range(2):
	letters_french.append('G')
	letters_french.append('B')
	letters_french.append('C')
	letters_french.append('P')
	letters_french.append('F')
	letters_french.append('H')
	letters_french.append('V')
	letters_french.append('*')
letters_french.append('J')
letters_french.append('Q')
letters_french.append('K')
letters_french.append('W')
letters_french.append('X')
letters_french.append('Y')
letters_french.append('Z')


#~~~~~~ POINTS ~~~~~~

#----- English -----
points_english = {
'*': 0,
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

#----- French -----
points_french = {
'*': 0,
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


#~~~~~~ BOARD LAYOUT ~~~~~~

#LAYOUT FOR THE BONUSES ON THE BOARD
# 0 : start
# 1 : normal tile
# 2 : double letter
# 3 : triple letter
# 4 : double word
# 5 : triple word
BOARD_LAYOUT = [
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

#Override the board layout to customize it to your will
BOARD_LAYOUT = [
[5,1,1,3,1,1,3,1,3,1,1,3,1,1,5],
[1,1,3,1,1,4,1,1,1,4,1,1,3,1,1],
[1,3,1,1,4,1,1,2,1,1,4,1,1,3,1],
[3,1,1,4,1,1,3,1,3,1,1,4,1,1,3],
[1,1,4,1,1,2,1,2,1,2,1,1,4,1,1],
[1,4,1,1,2,1,1,1,1,1,2,1,1,4,1],
[3,1,1,3,1,1,1,1,1,1,1,3,1,1,3],
[1,1,2,1,2,1,1,0,1,1,2,1,2,1,1],
[3,1,1,3,1,1,1,1,1,1,1,3,1,1,3],
[1,4,1,1,2,1,1,1,1,1,2,1,1,4,1],
[1,1,4,1,1,2,1,2,1,2,1,1,4,1,1],
[3,1,1,4,1,1,3,1,3,1,1,4,1,1,3],
[1,3,1,1,4,1,1,2,1,1,4,1,1,3,1],
[1,1,3,1,1,4,1,1,1,4,1,1,3,1,1],
[5,1,1,3,1,1,3,1,3,1,1,3,1,1,5]
]
