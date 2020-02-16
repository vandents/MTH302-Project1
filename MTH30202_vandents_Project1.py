"""
Instructor: Prof. Brian Drake
Course: MTH 302-02
Program: Project 1 - Snakes and Ladders Analysis

@date Tuesday, February 18, 2020
@author Scott VandenToorn
"""



# -----------------------------------------------------------------------------
#  Libraries
# -----------------------------------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt



# -----------------------------------------------------------------------------
#  Global Variables
#  Feel free to change the board size and the snakes/ladders to analyze other game variants
# -----------------------------------------------------------------------------

# Size of Transition matrix and game board
NUM_SQUARES = 26

# Snake/ladder coordinates
SNAKES = [(20, 1), (19, 2), (18, 3), (17, 4)]
LADDERS = [(6, 22)]

# Color escape sequences
TEXT_COLOR = '\u001b[34;1m'
BKGD_COLOR = '\u001b[44m'
BCKGD_COLOR_WHITE = '\u001b[47;1m'
RESET = '\u001b[0m'
BOLD = '\u001b[1m'
ITALIC = '\u001b[3m'
UNDERLINE = '\u001b[4m'



# -----------------------------------------------------------------------------
#  Functions
# -----------------------------------------------------------------------------

"""
Lists game facts displayed start of game
"""
def printHeader():
  ###   "Welcome" header   ###
  welcomeMsg = 'Welcome to Scott\'s snakes and ladders analysis!'
  short_blank = ''
  long_blank = ''

  for _ in range(round((211 - len(welcomeMsg)) / 2)):
    short_blank += ' '

  for _ in range(211):
    long_blank += ' '

  print(
    '\n' + BCKGD_COLOR_WHITE +
    long_blank + RESET + '\n' + BCKGD_COLOR_WHITE +
    long_blank + RESET + '\n' + BCKGD_COLOR_WHITE +
    short_blank + RESET + TEXT_COLOR + BCKGD_COLOR_WHITE + BOLD + welcomeMsg + RESET + BCKGD_COLOR_WHITE + short_blank + RESET + '\n' + BCKGD_COLOR_WHITE +
    long_blank + RESET + '\n' + BCKGD_COLOR_WHITE +
    long_blank + RESET + '\n\n'
  )

  ###   Game Info   ###
  ladderString = ''
  snakesString = ''

  for (i1, i2) in LADDERS:
    ladderString += '(' + str(i1) + ', ' + str(i2) + '), '
  for (i1, i2) in SNAKES:
    snakesString += '(' + str(i1) + ', ' + str(i2) + '), '

  if ladderString == '':
    ladderString = 'None'
  else:
    ladderString = ladderString[0 : len(ladderString) - 2]
  if snakesString == '':
    snakesString = 'None'
  else:
    snakesString = snakesString[0 : len(snakesString) - 2]

  print(BOLD + BKGD_COLOR + ' Game Info ' + RESET)
  print(TEXT_COLOR + '  >> ' + RESET + BOLD + ' N' + RESET + ':', findSmallestN())
  print(TEXT_COLOR + '  >> ' + RESET + BOLD + ' Board' + RESET + ': ' + str(NUM_SQUARES) + ' x ' + str(NUM_SQUARES))
  print(TEXT_COLOR + '  >> ' + RESET + BOLD + ' det(T)' + RESET + ':', np.linalg.det(T))
  print(TEXT_COLOR + '  >> ' + RESET + BOLD + ' Snakes' + RESET + ':', snakesString)
  print(TEXT_COLOR + '  >> ' + RESET + BOLD + ' Ladders' + RESET + ':', ladderString, '\n')


"""
Prints a subheading
"""
def printSubheading(part: int, message: str):
  left_blank = ''
  middle_blank = ''
  message = 'Part ' + str(part) + ' - ' + message
  message = '                     ' + message + '                     '

  for _ in range(round((211 - len(message)) / 2)):
    left_blank += ' '
  
  for _ in range(len(message)):
    middle_blank += ' '

  # Insert italic escape sequence
  index = message.find('- ') + 1
  message = message[:index] + ITALIC + message[index:]
  
  print(
    RESET + '\n\n\n\n' +
    left_blank + BCKGD_COLOR_WHITE + middle_blank + RESET + '\n' +
    left_blank + BCKGD_COLOR_WHITE + TEXT_COLOR + message + RESET + '\n' +
    left_blank + BCKGD_COLOR_WHITE + middle_blank + RESET + '\n'
  )


"""
Prints a matrix
"""
def printMatrix(M, message: str):
  print('\n' + RESET + BOLD + BKGD_COLOR + ' ' + message + ' ' + RESET)
  printString = '\t' + BOLD + TEXT_COLOR

  for i in range(len(M)):
    printString += str(i) + '\t'
  printString += '\t' + RESET

  col = 0

  for i in range(len(M)):
    for j in range(len(M[0])):
      if j == 0:
        printString += '\n   '
        if col < 10:
          printString += ' '
        printString += BOLD + TEXT_COLOR + str(col) + '\t' + RESET
        col = col + 1
      
      idxValue = round(M[j][i], 2)
      if idxValue == 1.0:
        printString += '\u001b[35;1m'
        idxValue = 1

      if idxValue == 0.0:
        idxValue = 0

      printString += str(idxValue) + '\t'

      if idxValue == 1.0:
        printString += RESET

  print(printString + '\n\n')


"""
Prints a vector
"""
def printVector(v, message: str):
  print('\n' + RESET + BOLD + BKGD_COLOR + ' ' + message + ' ' + RESET)

  printString = BOLD + '\t' + TEXT_COLOR

  for i in range(len(v)):
    printString += str(i) + '\t'
  printString += RESET + '\n\t'

  for i in range(len(v)):
    idxValue = round(v[i], 2)
    if idxValue == 1.0:
      printString += '\u001b[35;1m'
      idxValue = 1

    if idxValue == 0.0:
      idxValue = 0

    printString += str(idxValue) + '\t'

    if idxValue == 1.0:
      printString += RESET

  print(printString + '\n\n')


"""
Finds smallest n such that every entry of P^n is within 0.01 of zero
"""
def findSmallestN():
  for n in range(1, 101):
    temp = np.linalg.matrix_power(P, n)
    isValid = True

    for i in range(len(temp)):
      for j in range(len(temp)):
        if temp[j][i] >= 0.01 or temp[j][i] >= 0.01:
          isValid = False
    
    if isValid:
      return n

  return -1


"""
Update the transition matrix with a snake/ladder
"""
def handleSL(start: int, stop: int):
  # Set row and col of starting spot to 0
  for i in range(NUM_SQUARES):
    T[start][i] = 0
    T[i][start] = 0

  # Add a 1 in the start row
  T[stop][start] = 1

  # Add probability so each row sums to 1
  for i in range(1, 7):
    if start - i >= 0:
      T[stop][start - i] += 1 / 6



# -----------------------------------------------------------------------------
#  Transition Matrix.  T => T[col][row]
# -----------------------------------------------------------------------------

# Set up transition matrix
T = np.zeros((NUM_SQUARES, NUM_SQUARES))
T[NUM_SQUARES - 1][NUM_SQUARES - 1] = 1

# Populate T with the transition matrix for a standard board
for i in range(NUM_SQUARES - 1):
  for j in range(6):
    T[min(i + j + 1, NUM_SQUARES - 1), i] = T[min(i + j + 1, NUM_SQUARES - 1), i] + 1 / 6

# Handle snakes/ladders
for (start, stop) in sorted(SNAKES + LADDERS, key = lambda x: x[0], reverse = True):
  handleSL(start, stop)

# Need to define P before calling printGameInfo()
P = T[0 : len(T) - 1, 0: len(T[0]) - 1]
printHeader()

printSubheading(1, 'Transition matrix')
printMatrix(T, 'T ' + RESET + BKGD_COLOR + '  >>   Transition matrix')
# printMatrix(P, 'P ' + RESET + BKGD_COLOR + '  >>   T, but with the last row and column removed')



# -----------------------------------------------------------------------------
#  Markov Chains
# -----------------------------------------------------------------------------

printSubheading(2, 'Markov chains')

# The player starts at position 0.
# v = np.zeros(NUM_SQUARES)
# v[0] = 1
# printVector(v, 'v ' + RESET + BKGD_COLOR + '  >>   Initial position')

# Print select Markov chains
for n in range(findSmallestN()):
  if n == 0 or n == 1 or n == 9 or n == 24 or n == 49:
    P2 = np.copy(P)
    P2 = np.linalg.matrix_power(P2, n + 1)
    printMatrix(P2, 'P^' + str(n + 1) + ' ' + RESET + BKGD_COLOR + '  >>   Markov step ' + str(n + 1))



# -----------------------------------------------------------------------------
#  Eigenvalues and eigenvectors of T
# -----------------------------------------------------------------------------

# Get eigenvalues and eigenvectors for T
eValues, eVectors = np.linalg.eig(T)
printSubheading(3, 'Eigenvalues and eigenvectors of T')
printMatrix(eVectors.real, 'eVectors ' + RESET + BKGD_COLOR + '  >>   Eigen vectors of T (rows)')
printVector(eValues.real, 'eValues ' + RESET + BKGD_COLOR + '  >>   Eigen values of T')



# -----------------------------------------------------------------------------
#  Estimate Q
# -----------------------------------------------------------------------------

printSubheading(4, 'Expected number of steps to finish a single player game')

# Create identity matrix, m = NUM_SQUARES - 1
I = np.zeros((NUM_SQUARES - 1, NUM_SQUARES - 1))
for i in range(NUM_SQUARES - 1):
  for j in range(NUM_SQUARES - 1):
    if i == j:
      I[i, j] = 1

# Calculate Q
Q_a = np.copy(I)
for i in range(1, findSmallestN() + 1):
  Q_a += np.linalg.matrix_power(P, i)
printMatrix(Q_a, 'Q_a ' + RESET + BKGD_COLOR + '  >>   Estimation')



# -----------------------------------------------------------------------------
#  Compute Q
# -----------------------------------------------------------------------------

# Q is the inverse of the identity matrix - P
Q_b = np.linalg.inv(I - P)
printMatrix(Q_b, 'Q_b ' + RESET + BKGD_COLOR + '  >>   Computation')

# Print the difference between Q_a and Q_b
printMatrix(Q_a - Q_b, 'Q_a - Q_b ' + RESET + BKGD_COLOR + '  >>   Difference between estimated & computed values')

# Create row vector of ones
ones = np.ones(NUM_SQUARES - 1)

# Multiply row of 1's with Q
Q1 = ones @ Q_b
# Remove extra turn
for (i1, i2) in sorted(SNAKES + LADDERS, key = lambda x: x[0], reverse = True):
  Q1[i1] -= 1
printVector(Q1, '1*Q ' + RESET + BKGD_COLOR + '  >>   Expected number of steps to finish')
print('\n\n')
