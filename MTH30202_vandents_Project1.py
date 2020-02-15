# import sympy
import numpy as np
import matplotlib.pyplot as plt



##########################
#  Functions
##########################

# Prints out a matrix
def printMatrix(M, message: str):
  print('\n\033[1m\u001b[45m ' + message + ' \033[0m')
  printString = '\t\033[1m\033[95m'

  for i in range(len(M)):
    printString += str(i) + '\t'
  printString += '\t\033[0m'

  col = 0

  for i in range(len(M)):
    for j in range(len(M[0])):
      if j == 0:
        printString += '\n\033[1m\033[95m' + str(col) + '\t\033[0m'
        col = col + 1

      temp = round(M[i, j], 2)
      if temp == 0.0:
        temp = 0
      printString += str(temp) + '\t'

  print(printString + '\n\n')

# Prints out a vector
def printVector(vector, message: str):
  print('\n\033[1m\u001b[45m ' + message + ' \033[0m')

  printString = '\033[1m\033[95m\t'

  for i in range(len(vector)):
    printString += str(i) + '\t'
  printString += '\033[0m\n\t'

  for i in range(len(vector)):
    temp = round(vector[i], 2)
    if temp == 0.0:
      temp = 0
    printString += str(temp) + '\t'

  print(printString + '\n\n')



##########################
#  Welcome Message
##########################

welcomeMsg = 'Welcome to Scott\'s snakes and ladders analysis!'

blank_83 = ''
for i in range(round((211 - len(welcomeMsg)) / 2)):
  blank_83 += ' '

blank_213 = ''
for i in range(211):
  blank_213 += ' '

print(
  '\n\u001b[7m' +
  blank_213 + '\u001b[0m\n\u001b[7m' +
  blank_213 + '\u001b[0m\n\u001b[7m' +
  blank_83 + welcomeMsg + blank_83 + '\u001b[0m\n\u001b[7m' +
  blank_213 + '\u001b[0m\n\u001b[7m' +
  blank_213 + '\u001b[0m\n\n\n'
)



##########################
#  Transition Matrix
##########################

ladders = [(1, 24), (2, 3)]

# Set up transition matrix
T = np.zeros((26, 26))
T[25, 25] = 1

for i in range(25):
  for j in range(6):
    T[min(i + j + 1, 25), i] = T[min(i + j + 1, 25), i] + 1 / 6

for (i1, i2) in ladders:
  iw = np.where(T[:, i1] > 0)
  T[:, i1] = 0
  T[iw, i2] += 1 / 6

printMatrix(T, 'T \u001b[0m\u001b[45m  >>   Transition Matrix')

# The player starts at position 0.
v = np.zeros(26)
v[0] = 1

printVector(v, 'v \u001b[0m\u001b[45m  >>   Initial position')



##########################
#  Estimate Q
##########################

# Remove last row and column
P = T[0 : 25, 0: 25]
printMatrix(P, 'P')

# Create identity matrix (25)
I25 = np.zeros((25, 25))
for i in range(25):
  for j in range(25):
    if i == j:
      I25[i, j] = 1

printMatrix(I25, 'I25 \u001b[0m\u001b[45m  >>   Identity Matrix')

Q = np.copy(I25)
for i in range(11):
  Q += np.linalg.matrix_power(P, i + 1)

printMatrix(Q, 'Q \u001b[0m\u001b[45m  >>   Estimated')



##########################
#  Compute Q
##########################

# Create row vector of ones
ones = np.ones(25)
printVector(ones, 'ones \u001b[0m\u001b[45m  >>   Row vector of all 1\'s')

Q = np.linalg.inv(I25 - P)
printMatrix(Q, 'Q \u001b[0m\u001b[45m  >>   Computed')

Q1 = np.dot(ones, Q)
printVector(Q1, 'Q1 \u001b[0m\u001b[45m  >>   ones * Q')
print('\n')
