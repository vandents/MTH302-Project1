import numpy as np
import matplotlib.pyplot as plt

CHUTES_LADDERS = {
  2:15
}

def cl_markov_matrix(max_roll=6, jump_at_end=True):
  """
  Create a Markov transition matrix
  
  If jump_at_end is True, then apply ladder/chute jumps at the end of each turn.
  If False, then apply them at the beginning of the next turn.
  """  
  # Create the basic transition matrix:
  mat = np.zeros((26, 26))
  for i in range(26):
    mat[i + 1:i + 1 + max_roll, i] = 1. / max_roll
      
  # We could alternatively use scipy.linalg.circulent as follows:
  # mat = circulant([0, *np.ones(max_rolls) / 6, *np.zeros(100)])[:101, :101]

  # rolls off the end of the board don't change the state;
  # add these probabilities to the diagonal
  mat[range(26), range(26)] += 1 - mat.sum(0)

  # account for the presence of chutes and ladders
  # we'll do this via  another transition matrix
  cl_mat = np.zeros((26, 26))
  ind = [CHUTES_LADDERS.get(i, i) for i in range(26)]
  cl_mat[ind, range(26)] = 1
  if jump_at_end:
    return cl_mat @ mat
  else:
    return mat @ cl_mat

mat = cl_markov_matrix()
plt.matshow(mat)
plt.grid(False)
plt.show()
