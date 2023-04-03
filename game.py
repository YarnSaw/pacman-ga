'''
File to contain the game of pacman.

The game will have an option to render or not, since rending is computationally expensive,
so we may not want to render during training.
'''

import entities, settings
import pygame as py

class Game():
  def __init__(self, render, screen, clock, pacmanNet):
    # Define general pygame requirements
    self.render = render
    self.screen = screen
    self.clock = clock

    # Define Entities
    self.pacman = entities.Pacman(None, 4, 9);
    self.ghosts = [entities.Ghost(None, 'red', 9, 0)]

    # add entities to group that will draw them
    self.allSprites = py.sprite.Group()
    self.allSprites.add(self.pacman)
    for i in range(len(self.ghosts)):
      self.allSprites.add(self.ghosts[i])

    # The pacman playing board. Current idea for functionality is having it be a 2d array,
    # where 0=empty, 1=wall
    self.board = [[0 for i in range(10)] for j in range(10)] 


  def run(self, iterations):
    for i in range(iterations):
      self.timestep()
      self.draw()

    return 1 # return the fitness

  def timestep(self):
    '''
    Single time step of the game. Since pacman is drawn on a grid, each time step will move pacman and the ghosts
    to their next integer location.

    Draw should be called multiple times within 1 time step with an float between 0 and 1 to say how far each entity has moved
    along the path to it's next location, so we have fluid instead of jumpy movement.

    Alternatively, timesteps can be the smaller units of movement, and we define "key time steps" to happen whenever all entities
    each integer value locations, at which point we perform collision detection between pacman and the ghosts, as well as let
    each entity pick a new direction to move. 
    '''
    self.pacman.update(self.board)
    for ghost in self.ghosts:
      ghost.update(self.board)
    
    # Detect collisions here

    pass

  def reset(self):
    '''
    Reset the game so it can be used for a new generation.
    Alternatively, we may want to just delete the instance and create a new one. Whichever is faster
    '''
    pass

  def draw(self):
    if not self.render:
      return
    
    # Limit frames per second (comment out to uncap)
    self.clock.tick(settings.FPS)
    
    self.screen.fill((255,255,255))


    self.allSprites.draw(self.screen)
    py.display.update()

  
    