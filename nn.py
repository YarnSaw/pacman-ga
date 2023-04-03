'''
Neural network that the GA governs.
'''

import numpy as np

class NeuralNetwork():
  def __init__(self, w1, w2):
    self.w1 = w1
    self.w2 = w2
  
  def forward(self, input):
    h1 = input * self.w1
    # may want some form of activation function here
    output = h1 * self.w2
    #almost certainly want an activation function here
    return output

  # the network does not need backpropagation to learn, that's what the GA is for