# import sympy
import numpy as np
import matplotlib.pyplot as plt



##########################
#  Global Variables
##########################

# Size of Transition matrix
SIZE = 26
SIZE_1 = SIZE - 1

# Color escape sequences
TEXT_COLOR = '\u001b[34;1m'
BKGD_COLOR = '\u001b[44m'
BCKGD_COLOR_WHITE = '\u001b[47;1m'
RESET = '\u001b[0m'
BOLD = '\u001b[1m'
ITALIC = '\u001b[3m'



##########################
#  Functions
##########################

# Prints out a matrix
def printMatrix(M, message: str):
  print('\n' + RESET + BOLD + BKGD_COLOR + ' ' + message + ' ' + RESET)
  printString = '\t' + BOLD + TEXT_COLOR

  for i in range(len(M)):
    printString += str(i) + '\t'
  printString += '\t\033[0m'

  col = 0

  for i in range(len(M)):
    for j in range(len(M[0])):
      if j == 0:
        printString += '\n' + BOLD + TEXT_COLOR + str(col) + '\t\033[0m'
        col = col + 1

      temp = round(M[i][j], 2)
      if temp == 0.0:
        temp = 0
      printString += str(temp) + '\t'

  print(printString + '\n\n')

# Prints out a vector
def printVector(vector, message: str):
  print('\n' + RESET + BOLD + BKGD_COLOR + ' ' + message + ' \033[0m')

  printString = BOLD + '\t' + TEXT_COLOR

  for i in range(len(vector)):
    printString += str(i) + '\t'
  printString += '\033[0m\n\t'

  for i in range(len(vector)):
    temp = round(vector[i], 2)
    if temp == 0.0:
      temp = 0
    printString += str(temp) + '\t'

  print(printString + '\n\n')

# Lists game facts displayed start of game
def printGameInfo():
  ladderString = ''
  snakesString = ''

  for (i1, i2) in ladders:
    ladderString += '(' + str(i1) + ', ' + str(i2) + '),  '
  for (i1, i2) in snakes:
    snakesString += '(' + str(i1) + ', ' + str(i2) + '),  '

  if ladderString == '':
    ladderString = 'None'
  else:
    ladderString = ladderString[0 : len(ladderString) - 3]
  if snakesString == '':
    snakesString = 'None'
  else:
    snakesString = snakesString[0 : len(snakesString) - 3]

  print(BOLD + BKGD_COLOR + ' Game Info \033[0m')
  print(TEXT_COLOR + '  >> ' + RESET + BOLD + ' Board' + RESET + ': ' + str(SIZE) + ' x ' + str(SIZE))
  print(TEXT_COLOR + '  >> ' + RESET + BOLD + ' Snakes' + RESET + ':', snakesString)
  print(TEXT_COLOR + '  >> ' + RESET + BOLD + ' Ladders' + RESET + ':', ladderString, '\n\n\n')



##########################
#  Welcome Header
##########################

welcomeMsg = 'Welcome to Scott\'s snakes and ladders analysis!'

short_blank = ''
for i in range(round((211 - len(welcomeMsg)) / 2)):
  short_blank += ' '

long_blank = ''
for i in range(211):
  long_blank += ' '

print(
  '\n' + BCKGD_COLOR_WHITE +
  long_blank + RESET + '\n' + BCKGD_COLOR_WHITE +
  long_blank + RESET + '\n' + BCKGD_COLOR_WHITE +
  short_blank + RESET + TEXT_COLOR + BCKGD_COLOR_WHITE + BOLD + welcomeMsg + RESET + BCKGD_COLOR_WHITE + short_blank + RESET + '\n' + BCKGD_COLOR_WHITE +
  long_blank + RESET + '\n' + BCKGD_COLOR_WHITE +
  long_blank + RESET + '\n\n'
)



##########################
#  Transition Matrix
##########################

# Snake/ladder coordinates
ladders = [(13, 18)]
snakes = [(14, 10)]
trans = ladders + snakes

printGameInfo()

# Set up transition matrix
T = np.zeros((SIZE, SIZE))
T[SIZE_1][SIZE_1] = 1

# Populate T with the transition matrix for a standard board
for i in range(SIZE_1):
  for j in range(6):
    T[min(i + j + 1, SIZE_1), i] = T[min(i + j + 1, SIZE_1), i] + 1 / 6

for (i1, i2) in trans:
  iw = np.where(T[:, i1] > 0)
  T[:, i1] = 0
  T[iw, i2] += 1 / 6

# House rules: you don't need to land on 100, just reach it.
T[SIZE - 6 : SIZE_1, SIZE_1] += np.linspace(1/6, 5/6, 5)
for snake in snakes:
  T[snake, SIZE_1] = 0
printMatrix(T, 'T ' + RESET + BKGD_COLOR + '  >>   Transition Matrix')

# The player starts at position 0.
v = np.zeros(SIZE)
v[0] = 1
# printVector(v, 'v ' + RESET + BKGD_COLOR + '  >>   Initial position')



##########################
#  Estimate Q
##########################

# Remove last row and column
P = T[0 : SIZE_1, 0: SIZE_1]
printMatrix(P, 'P ' + RESET + BKGD_COLOR + '  >>   T, but with the last row and column removed')

# Create identity matrix, m = SIZE_1
I = np.zeros((SIZE_1, SIZE_1))
for i in range(SIZE_1):
  for j in range(SIZE_1):
    if i == j:
      I[i, j] = 1
printMatrix(I, 'I ' + RESET+ BKGD_COLOR + '  >>   Identity Matrix')

# Calculate Q
Q = np.copy(I)
for i in range(11):
  Q += np.linalg.matrix_power(P, i + 1)
printMatrix(Q, 'Q ' + RESET + BKGD_COLOR + '  >>   Estimation')



##########################
#  Compute Q
##########################

# Q is the inverse of the identity matrix - P
Q = np.linalg.inv(I - P)
printMatrix(Q, 'Q ' + RESET + BKGD_COLOR + '  >>   Computation')

# Create row vector of ones
ones = np.ones(SIZE_1)
# printVector(ones, 'ones ' + RESET + BKGD_COLOR + '  >>   Row vector of all 1\'s')

# Multiply row of 1's with Q
Q1 = ones @ Q
printVector(Q1, 'Q1 ' + RESET + BKGD_COLOR + '  >>   Average # Turns to Win')
print('\n')
