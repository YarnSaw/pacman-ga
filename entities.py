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

class Pacman():
  '''
  neuralNet = None if human player.
  '''
  def __init__(self, neuralNet, x, y):
    if neuralNet:
      brain = nn.NeuralNetwork(neuralNet[0], neuralNet[1])
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
    if move == 1:
      if self.y > 0 and board[self.y-1][self.x] == 0:
        self.y -= 1
    if move == 2:
      if self.x < maxX and board[self.y][self.x+1] == 0:
        self.x += 1
    if move == 3:
      if self.x > 0 and board[self.y][self.x-1] == 0:
        self.x -= 1
    

class Ghost():
  def __init__(self, neuralNet, color, x, y):
    if neuralNet:
      brain = nn.NeuralNetwork(neuralNet[0], neuralNet[1])
    self.color = color
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
    if move == 1:
      if self.y > 0 and board[self.y-1][self.x] == 0:
        self.y -= 1
    if move == 2:
      if self.x < maxX and board[self.y][self.x+1] == 0:
        self.x += 1
    if move == 3:
      if self.x > 0 and board[self.y][self.x-1] == 0:
        self.x -= 1
