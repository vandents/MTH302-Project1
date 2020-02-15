import numpy as np
import matplotlib.pyplot as plt


# Prints out the board
def printMatrix(M, message: str):
  print('\n' + message)
  printString = ''

  for i in range(len(M)):
    for j in range(len(M[0])):
      temp = round(M[i, j], 2)
      if temp == 0.0:
        temp = 0
      printString += str(temp) + '\t'
    printString += '\n'

  print(printString + '\n')

# Prints out the player vector
def printVector(vector, message: str):
  print('\n' + message)
  printString = ''

  for i in range(len(vector)):
    temp = round(vector[i], 2)
    if temp == 0.0:
      temp = 0
    printString += str(temp) + '\t'

  print(printString + '\n\n')


print(
  '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~' +
  '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~' +
  '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
print(
  '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~' +
  '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~' +
  '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')


ladders = [(2, 3), (4, 23)]
# snakes = [(11,7), (18,13), (28,12), (36,34), (77,16), (47,26), (83,39), (92,75), (99,70)]
# snakes = [(10, 9)]
snakes = []
trans = ladders + snakes

# Set up the transition matrix
T = np.zeros((26, 26))
for i in range(1,26):
  T[i-1,i:i+6] = 1/6

for (i1,i2) in trans:
  iw = np.where(T[:,i1] > 0)
  T[:,i1] = 0
  T[iw,i2] += 1/6

# House rules: you don't need to land on 25, just reach it.
T[20:25,25] += np.linspace(1/6, 5/6, 5)
for snake in snakes:
  T[snake,25] = 0

printMatrix(T, 'T')

# The player starts at position 0.
v = np.zeros(26)
v[0] = 1

n, P = 0, []
cumulative_prob = 0
# Update the state vector v until the cumulative probability of winning
# is "effectively" 1
# while cumulative_prob < 0.999:
#   printVector(v, 'v')
#   n += 1
#   v = v.dot(T)
#   P.append(v[25])
#   cumulative_prob += P[-1]
# print('\nn: ' + str(n))
# print('cumulative_prob: ' + str(cumulative_prob))
# mode = np.argmax(P) + 1
# print('mode: ' + str(mode) + '\n')
# printVector(v, 'v')
# printVector(P, 'P')


# Remove last row and column
P = T[0 : 25, 0: 25]
printMatrix(P, 'P')

# Create identity matrix (25)
I25 = np.zeros((25, 25))
for i in range(25):
  for j in range(25):
    if i == j:
      I25[i, j] = 1

ones = np.ones(25)
printVector(ones, 'ones')

Q = np.linalg.inv(I25 - P)
printMatrix(Q, 'Q')

Q1 = np.dot(ones, Q)
printVector(Q1, '1 * Q')


# Plot the probability of winning as a function of the number of moves
# fig, ax = plt.subplots()
# ax.plot(np.linspace(1,n,n), P, 'g-', lw=2, alpha=0.6, label='Markov')
# ax.set_xlabel('Number of moves')
# ax.set_ylabel('Probability of winning')

# plt.show()



print('\n')
