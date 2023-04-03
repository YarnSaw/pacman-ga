'''
File to describe the entities that will exist within the game.
Current entities include:
  - Pac-man
  - ghost
We may want to include the walls as entities, or we may include them directly in the game themselves,
depending on how complex operations including walls end up.
'''

import nn
import pygame as py

class Pacman():
  '''
  neuralNet = None if human player.
  '''
  def __init__(self, neuralNet):
    if neuralNet:
      brain = nn.NeuralNetwork(neuralNet[0], neuralNet[1])

class Ghost():
  def __init__(self, color):
    self.color = color
