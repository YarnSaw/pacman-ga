'''
File to contain the game of pacman.

The game will have an option to render or not, since rending is computationally expensive,
so we may not want to render during training.
'''

import entities


class Game():
  def __init__(self, render):
    self.render = render
    self.pacman = entities.Pacman()
    self.ghosts = [entities.Ghost('red')]


  def run(self):
    pass

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
    pass

  def reset(self):
    '''
    Reset the game so it can be used for a new generation.
    Alternatively, we may want to just delete the instance and create a new one. Whichever is faster
    '''
    pass

  def draw(self):
    if (self.render):
      pass
  
  