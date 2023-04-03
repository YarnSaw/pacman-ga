'''
File to describe the entities that will exist within the game.
Current entities include:
  - Pac-man
  - ghost
We may want to include the walls as entities, or we may include them directly in the game themselves,
depending on how complex operations including walls end up.
'''

import nn, settings
import pygame as py
import numpy as np
import random
vec=py.math.Vector2


'''
Currently, updating both the x/y and the rect for the entity
at the same time. When we want to go to a smoother animation and 
have the entity move smoother on the field, these will need to be
separated. Always change the x/y by 1, while the rectangle increases
by 16 to complete the visual movement.
'''
def genericMove(entity, board, move):
  maxX = len(board[0])-1
  maxY = len(board)-1

  if move == 0:
    if entity.y < maxY and board[entity.y+1][entity.x] == 0:
      entity.y += 1
      entity.rect.top += 16
  if move == 1:
      if entity.y > 0 and board[entity.y-1][entity.x] == 0:
        entity.y -= 1
        entity.rect.top -= 16

  if move == 2:
    if entity.x < maxX and board[entity.y][entity.x+1] == 0:
      entity.x += 1
      entity.rect.left += 16
  if move == 3:
    if entity.x > 0 and board[entity.y][entity.x-1] == 0:
      entity.x -= 1
      entity.rect.left -= 16


class Pacman(py.sprite.Sprite):
  '''
  neuralNet = None if human player.
  '''
  def __init__(self, nnWeights, startPos):
    py.sprite.Sprite.__init__(self)
    if not nnWeights is None:
      w1 = nnWeights[0:settings.inputSize * settings.hiddenSize].reshape(settings.inputSize, settings.hiddenSize)
      w2 = nnWeights[settings.inputSize * settings.hiddenSize:].reshape(settings.hiddenSize, settings.outputSize)

      self.brain = nn.NeuralNetwork(w1, w2)
      self.movement = "ai"
    else:
      self.movement = "random"
    
    self.image = py.Surface((16, 16))
    self.image.fill(settings.colors['yellow'])
    self.rect=self.image.get_rect()
    self.rect.topleft = vec(startPos[0]*16,startPos[1]*16)
    self.x = startPos[0]
    self.y = startPos[1]
    self.startPos = startPos

    self.living = True

  def update(self, board):
    if self.living:
      # Temporary: random movement
      if self.movement == 'random':
        move = random.randint(0,3)
        genericMove(self, board, move)

      elif self.movement == 'ai':
        # don't have logic for determining other entities positions,
        # so use random numbers for input
        move = self.brain.forward(np.random.rand(1,settings.inputSize))
        genericMove(self, board, move)

  def reset(self):
    self.rect.topleft = vec(self.startPos[0]*16,self.startPos[1]*16)
    self.x = self.startPos[0]
    self.y = self.startPos[1]

    self.image.fill(settings.colors['yellow'])
    self.living = True


class Ghost(py.sprite.Sprite):
  def __init__(self, neuralNet, color, startPos):
    py.sprite.Sprite.__init__(self)
    if neuralNet:
      brain = nn.NeuralNetwork(neuralNet[0], neuralNet[1])
    self.color = color
    
    self.image = py.Surface((16, 16))
    self.image.fill(settings.colors[color])
    self.rect=self.image.get_rect()
    self.rect.topleft = vec(startPos[0]*16,startPos[1]*16)

    self.x = startPos[0]
    self.y = startPos[1]
    self.startPos = startPos

  
  def update(self, board):
    # Temporary: random movement
    move = random.randint(0,3)

    genericMove(self, board, move)
        
  def reset(self):
    self.rect.topleft = vec(self.startPos[0]*16,self.startPos[1]*16)
    self.x = self.startPos[0]
    self.y = self.startPos[1]