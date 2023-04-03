'''
Main file that defines everything. Runs the GA over multiple game boards and generations.
'''
import game
import nn
import genetic
import pygame as py

population = 100
mutationRate = 0.1
generations = 100

renderAny = False
screen = None # I hate python scoping, so having this here because it's weird.
if renderAny:
  screen = py.display.set_mode((700, 700))

if __name__ == "__main__":
  '''
  Currently have a slightly pseudo-code main loop, meant to show the structure of what we want here.
  Note this structure only has 1 GA at the moment, we will need 4 more, for each of the ghosts.
  '''
  GA = genetic.GeneticAlgorithm(population, mutationRate)
  # somewhere in here we need to make sure the gene -> weights conversion is done.
  # the genome will probably be a single array of i*h + h*o length, while the nn needs that broken into 2
  # 2D arrays, one i by h and the other h by o in size.
  games = [game.Game(False, GA.population[i]) for i in range(100)]

  for gen in range(generations):
    allFitnesses = []
    for g in games:
      allFitnesses.append(g.run())
      g.reset()
    
    GA.nextGeneration(allFitnesses)
