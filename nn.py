'''
Neural network that the GA governs.
'''

import numpy as np

class NeuralNetwork():
  def __init__(self, w1, w2):
    self.w1 = w1
    self.w2 = w2
  
  def forward(self, value):
    value = np.insert(value,len(value),1) # bias
    h1 = np.matmul(value, self.w1)
    h1 = self.sigmoid(h1)
    output = np.matmul(h1, self.w2)
    output = self.sigmoid(output)
    return np.argmax(output)
  
  def sigmoid(self,s):#activation function
    s = np.clip(s,-200,200)
    return 1/(1+np.exp(-s))

  # the network does not need backpropagation to learn, that's what the GA is for