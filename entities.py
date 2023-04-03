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
import random
vec=py.math.Vector2


class Pacman(py.sprite.Sprite):
  '''
  neuralNet = None if human player.
  '''
  def __init__(self, neuralNet, x, y):
    py.sprite.Sprite.__init__(self)
    if neuralNet:
      brain = nn.NeuralNetwork(neuralNet[0], neuralNet[1])
    
    self.image = py.Surface((16, 16))
    self.image.fill((255, 255, 0))
    self.rect=self.image.get_rect()
    self.rect.topleft = vec(x*16,y*16)
    self.x = x
    self.y = y

  def update(self, board):
    maxX = len(board[0])-1
    maxY = len(board)-1
    # Temporary: random movement
    move = random.randint(0,3)
    if move == 0:
      if self.y < maxY and board[self.y+1][self.x] == 0:
        self.y += 1
        self.rect.top += 16
    if move == 1:
        if self.y > 0 and board[self.y-1][self.x] == 0:
          self.y -= 1
          self.rect.top -= 16

    if move == 2:
      if self.x < maxX and board[self.y][self.x+1] == 0:
        self.x += 1
        self.rect.left += 16
    if move == 3:

      if self.x > 0 and board[self.y][self.x-1] == 0:
        self.x -= 1
        self.rect.left -= 16

  def draw(self):
    import pdb
    pdb.set_trace()

class Ghost(py.sprite.Sprite):
  def __init__(self, neuralNet, color, x, y):
    py.sprite.Sprite.__init__(self)
    if neuralNet:
      brain = nn.NeuralNetwork(neuralNet[0], neuralNet[1])
    self.color = color
    
    self.image = py.Surface((16, 16))
    self.image.fill((255, 0, 0))
    self.rect=self.image.get_rect()
    self.rect.topleft = vec(x*16,y*16)

    self.x = x
    self.y = y
  
  def update(self, board):
    maxX = len(board[0])-1
    maxY = len(board)-1
    # Temporary: random movement
    move = random.randint(0,3)
    if move == 0:
      if self.y < maxY and board[self.y+1][self.x] == 0:
        self.y += 1
        self.rect.top += 16
    if move == 1:
        if self.y > 0 and board[self.y-1][self.x] == 0:
          self.y -= 1
          self.rect.top -= 16

    if move == 2:
      if self.x < maxX and board[self.y][self.x+1] == 0:
        self.x += 1
        self.rect.left += 16
    if move == 3:

      if self.x > 0 and board[self.y][self.x-1] == 0:
        self.x -= 1
        self.rect.left -= 16
