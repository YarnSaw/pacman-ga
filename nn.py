'''
Neural network that the GA governs.
'''

class NeuralNetwork():
  def __init__(self, inputSize, hiddenSize, outputSize):
    self.input = inputSize
    self.hidden = hiddenSize
    self.output = outputSize
  
  def forward(self):
    '''
    Feed forward in the network
    '''
    pass

  # the network does not need backpropagation to learn, that's what the GA is for