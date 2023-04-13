'''
File to contain the game of pacman.

The game will have an option to render or not, since rending is computationally expensive,
so we may not want to render during training.
'''

import entities, settings
import pygame as py
import AStar

class Game():
  def __init__(self, render, screen, clock, pacmanNet, ghostNets, boardSize=10, wallMaxPenalty=10, onlyWallFitness=False, pacmanCanDie=True, pacmanStart=(2,9), ghostStarts=[(4,0)]):
    # Define general pygame requirements
    self.render = render
    self.screen = screen
    self.clock = clock

    size = self.screen.get_size()
    self.boardPixelSize = boardSize*16
    self.offset = ((size[0]-self.boardPixelSize)/2, (size[1]-self.boardPixelSize)/2)

    if len(ghostStarts) != 1 and len(ghostStarts) != len(ghostNets):
      raise Exception("mis-specified number of ghost start points for the number of ghosts given")
    if len(ghostStarts) == 1:
      ghostStarts *= len(ghostNets)
    self.ghostStarts = ghostStarts
    self.pacmanStart = pacmanStart

    self.wallMaxPenalty = wallMaxPenalty
    self.onlyWallFitness = onlyWallFitness
    self.pacmanCanDie = pacmanCanDie

    sheet = py.image.load("spritesheet.png").convert()

    # Define Entities
    self.pacman = entities.Pacman(pacmanNet, self.pacmanStart, self.offset, sheet);
    self.ghosts = [entities.Ghost(ghostNets[g], 'red', self.ghostStarts[g], self.offset, sheet) for g in range(settings.ghostCount)]

    # add entities to group that will draw them
    self.allSprites = py.sprite.Group()
    self.allSprites.add(self.pacman)
    for i in range(len(self.ghosts)):
      self.allSprites.add(self.ghosts[i])

    # The pacman playing board. Current idea for functionality is having it be a 2d array,
    # where 0=empty, 1=wall
    self.board = [[0 for i in range(boardSize)] for j in range(boardSize)] 


  def run(self, iterations=settings.iterationsPerGen):
    for i in range(iterations):
      self.timestep()
      self.draw()
      if not self.pacman.living:
        break # no need to waste computation

    fitness = [] # List of ghost fitnesses, followed by pacman's fitness at the end.
    # For training all entities to avoid the walls
    if self.onlyWallFitness:
      for g in self.ghosts:
        fitness.append(g.fitnessPenalty)
      fitness.append(self.pacman.fitnessPenalty)
    else:
      pacmanFitness = 0
      for g in self.ghosts:
        if self.pacman.living:
          fit = AStar.astar(self.board, (g.x, g.y), (self.pacman.x, self.pacman.y))
        else:
          fit = 0
        pacmanFitness = max(pacmanFitness, fit)
        fit = fit + min(self.wallMaxPenalty, g.fitnessPenalty) # cap the penalty for running into walls 
        fitness.append(fit)

      pacmanFitness = pacmanFitness - min(self.wallMaxPenalty, self.pacman.fitnessPenalty) # cap the penalty for running into walls 
      fitness.append(pacmanFitness) #pacman's fitness is the distance from the closest ghost

    return fitness # return the fitness

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

    # @TODO:
    # currently giving absolute values for the location of each entity. Learning may be better generalized 
    # by giving relative locations, however walls may mess this strategy up. Need to test to see what works best.

    locations = []
    for ghost in self.ghosts:
      locations.append(ghost.x)
      locations.append(ghost.y)
    locations.append(self.pacman.x)
    locations.append(self.pacman.y)
    
    self.pacman.update(self.board, locations)

    # Detect collisions
    for ghost in self.ghosts:
      if self.pacman.x == ghost.x and self.pacman.y == ghost.y and self.pacmanCanDie:
        # print("RIP pacman is dead")
        self.pacman.living = False
        self.pacman.x = 10000 # off the screen so the RIP message won't be spammed
        return;

    for ghost in self.ghosts:
      ghost.update(self.board, locations)
    
    # Detect collisions
    for ghost in self.ghosts:
      if self.pacman.x == ghost.x and self.pacman.y == ghost.y and self.pacmanCanDie:
        # print("RIP pacman is dead")
        self.pacman.living = False
        self.pacman.x = 10000 # off the screen so the RIP message won't be spammed
        return

  def assignPopToGame(self, pacmanNet, ghostNets):
    self.pacman.assignNewNet(pacmanNet)
    for i in range(len(self.ghosts)):
      self.ghosts[i].assignNewNet(ghostNets[i])

  def reset(self):
    '''
    Reset the game so it can be used for a new generation.
    '''
    self.pacman.reset()
    for ghost in self.ghosts:
      ghost.reset()

  def draw(self):
    if not self.render:
      return
    
    # Limit frames per second (comment out to uncap)
    self.clock.tick(settings.FPS)
    
    self.screen.fill(settings.colors['white'])
    py.draw.rect(self.screen, settings.colors['black'], py.Rect(self.offset[0], self.offset[1], self.boardPixelSize, self.boardPixelSize))


    self.allSprites.draw(self.screen)
    py.display.update()

  
    