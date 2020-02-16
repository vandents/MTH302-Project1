# import sympy
import numpy as np
import matplotlib.pyplot as plt



##########################
#  Global Variables
##########################

# Size of Transition matrix
NUM_SQUARES = 26
# NUM_SQUARES - 1 = NUM_SQUARES - 1

# Snake/ladder coordinates
SNAKES = [(20, 12)]
LADDERS = [(4, 22)]

# Color escape sequences
TEXT_COLOR = '\u001b[34;1m'
BKGD_COLOR = '\u001b[44m'
BCKGD_COLOR_WHITE = '\u001b[47;1m'
RESET = '\u001b[0m'
BOLD = '\u001b[1m'
ITALIC = '\u001b[3m'
UNDERLINE = '\u001b[4m'



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
        printString += '\n   '
        if col < 10:
          printString += ' '
        printString += BOLD + TEXT_COLOR + str(col) + '\t\033[0m'
        col = col + 1
      
      temp = round(M[j][i], 2)
      if M[j][i] == 1:
        printString += '\u001b[35;1m'
        temp = 1

      if temp == 0.0:
        temp = 0
      printString += str(temp) + '\t'

      if M[j][i] == 1:
        printString += RESET

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
    # if temp == 1.0 and i < NUM_SQUARES - 2 and len(vector) == NUM_SQUARES - 1:
    #   temp = ''
    printString += str(temp) + '\t'

  print(printString + '\n\n')

# Lists game facts displayed start of game
def printGameInfo():
  ladderString = ''
  snakesString = ''

  for (i1, i2) in LADDERS:
    ladderString += '(' + str(i1) + ', ' + str(i2) + '),  '
  for (i1, i2) in SNAKES:
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
  print(TEXT_COLOR + '  >> ' + RESET + BOLD + ' Board' + RESET + ': ' + str(NUM_SQUARES) + ' x ' + str(NUM_SQUARES))
  print(TEXT_COLOR + '  >> ' + RESET + BOLD + ' Snakes' + RESET + ':', snakesString)
  print(TEXT_COLOR + '  >> ' + RESET + BOLD + ' Ladders' + RESET + ':', ladderString)
  print(TEXT_COLOR + '  >> ' + RESET + BOLD + ' N' + RESET + ':', findSmallestN(), '\n\n\n')

# Finds smallest n such that every entry of P^n is within 0.01 of zero
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

# Update the transition matrix with a snake/ladder
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
#  Transition Matrix.  T => T[col][row]
##########################

# Set up transition matrix
T = np.zeros((NUM_SQUARES, NUM_SQUARES))
T[NUM_SQUARES - 1][NUM_SQUARES - 1] = 1

# Populate T with the transition matrix for a standard board
for i in range(NUM_SQUARES - 1):
  for j in range(6):
    T[min(i + j + 1, NUM_SQUARES - 1), i] = T[min(i + j + 1, NUM_SQUARES - 1), i] + 1 / 6

# Handle snakes/ladders
for (start, stop) in SNAKES + LADDERS:
  handleSL(start, stop)

# Need to define P before calling printGameInfo()
P = T[0 : NUM_SQUARES - 1, 0: NUM_SQUARES - 1]
printGameInfo()

printMatrix(T, 'T ' + RESET + BKGD_COLOR + '  >>   Transition Matrix')
# printMatrix(P, 'P ' + RESET + BKGD_COLOR + '  >>   T, but with the last row and column removed')



##########################
#  Markov Chains
##########################

# The player starts at position 0.
v = np.zeros(NUM_SQUARES)
v[0] = 1
# printVector(v, 'v ' + RESET + BKGD_COLOR + '  >>   Initial position')

# Print select Markov chains
for n in range(findSmallestN()):
  if n == 0 or n == 1 or n == 9:
    P2 = np.copy(P)
    P2 = np.linalg.matrix_power(P2, n + 1)
    printMatrix(P2, 'P^' + str(n + 1) + ' ' + RESET + BKGD_COLOR + '  >>   Markov step ' + str(n + 1))



##########################
#  Estimate Q
##########################

# Create identity matrix, m = NUM_SQUARES - 1
I = np.zeros((NUM_SQUARES - 1, NUM_SQUARES - 1))
for i in range(NUM_SQUARES - 1):
  for j in range(NUM_SQUARES - 1):
    if i == j:
      I[i, j] = 1
# printMatrix(I, 'I ' + RESET + BKGD_COLOR + '  >>   Identity Matrix')

# Calculate Q
Q_a = np.copy(I)
for i in range(11):
  Q_a += np.linalg.matrix_power(P, i + 1)
printMatrix(Q_a, 'Q_a ' + RESET + BKGD_COLOR + '  >>   Estimation')



##########################
#  Compute Q
##########################

# Q is the inverse of the identity matrix - P
Q_b = np.linalg.inv(I - P)
printMatrix(Q_b, 'Q_b ' + RESET + BKGD_COLOR + '  >>   Computation')

# Print the difference between Q_a and Q_b
printMatrix(Q_a - Q_b, 'Q_a - Q_b ' + RESET + BKGD_COLOR + '  >>   Difference Between Estimated and Computed Values')

# Create row vector of ones
ones = np.ones(NUM_SQUARES - 1)
# printVector(ones, 'ones ' + RESET + BKGD_COLOR + '  >>   Row vector of all 1\'s')

# Multiply row of 1's with Q
Q1 = ones @ Q_b
# Remove extra turn
for (i1, i2) in SNAKES + LADDERS:
  Q1[i1] -= 1
printVector(Q1, '1*Q ' + RESET + BKGD_COLOR + '  >>   Average # Turns to Win')
print('\n')
