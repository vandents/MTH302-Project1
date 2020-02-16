import numpy as np
from matplotlib import pyplot



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



size=25

def special(p, pos_start, pos_end):
  p[pos_start]= np.zeros(size+1)
  p[pos_start][pos_start]=1
  
  #make sure that p stays row stocastic
  #i.e the sum of each row must be always kept to 1
  for i in range(size+1):
    pp = p[i][pos_start]
    p[i][pos_start] = 0
    p[i][pos_end]   = p[i][pos_end] + pp

def snake(p, pos_start, pos_end=0):
  if (pos_end<pos_start):
    special(p, pos_start, pos_end)

def ladder(p, pos_start, pos_end=size):
  if (pos_end>pos_start):
    special(p, pos_start, pos_end)

def nullgame():
  p=np.zeros((size+1,size+1))
  
  for i in range(size+1):
    for j in range(6):
      if (i+j<size):
        p[i][i+j+1]=1.0/6.0
  
  p[size][size]=1
  
  p[size-1][size]=6.0/6.0
  p[size-2][size]=5.0/6.0
  p[size-3][size]=4.0/6.0
  p[size-4][size]=3.0/6.0
  p[size-5][size]=2.0/6.0
  p[size-6][size]=1.0/6.0
  
  return p

a=np.zeros(size+1)
p=nullgame()

printMatrix(p, 'p')

#initial matrix is p
m=p

iterations = 50
pr_end=np.zeros(iterations)

a

for k in range(iterations):
  #plot the probability distribution at the k-th iteration
  pyplot.figure(1)
  pyplot.plot(m[0][0:size])
  
  #store the probability of ending after the k-th iteration
  pr_end[k] = m[0][size]
  
  #store/plot the accumulated marginal probability at the k-th iteration
  a=a+m[0]
  pyplot.figure(2)
  pyplot.plot(a[0:size])
  
  if k == 0 or k == 1 or k == 23:
    printMatrix(m, 'm   >>   k = ' + str(k))

  #calculate the stocastic matrix for iteration k+1
  m=np.dot(m,p)

printVector(a, 'a')

#plot the probability of ending the game
# after k iterations
pyplot.figure(3)
pyplot.plot(pr_end[0:iterations-1])

#show the three graphs
# pyplot.show()
