'''
Main file that defines everything. Runs the GA over multiple game boards and generations.
'''
import game, nn, genetic, settings
import pygame as py

population = 1
mutationRate = 0.1
generations = 1
iterationsPerGen = 100

renderAny = True
screen = None # I hate python scoping, so having this here because it's weird.
if renderAny:
  screen = py.display.set_mode((700, 700))
  clock = py.time.Clock()

if __name__ == "__main__":
  '''
  Currently have a slightly pseudo-code main loop, meant to show the structure of what we want here.
  Note this structure only has 1 GA at the moment, we will need 4 more, for each of the ghosts.
  '''
  GA = genetic.GeneticAlgorithm(population, settings.geneSize, mutationRate)
  # somewhere in here we need to make sure the gene -> weights conversion is done.
  # the genome will probably be a single array of i*h + h*o length, while the nn needs that broken into 2
  # 2D arrays, one i by h and the other h by o in size.
  games = [game.Game(False, screen, clock, GA.population[i]) for i in range(population)]
  if renderAny:
    games[0].render = True

  for gen in range(generations):
    print(gen+1)
    allFitnesses = []
    for g in games:
      allFitnesses.append(g.run(iterationsPerGen))
      g.reset()
    
    GA.nextGeneration(allFitnesses)
