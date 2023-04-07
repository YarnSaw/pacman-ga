'''
Main file that defines everything. Runs the GA over multiple game boards and generations.
'''
import game, nn, genetic, settings
import pygame as py


renderAny = True
screen = None # I hate python scoping, so having this here because it's weird.
if renderAny:
  screen = py.display.set_mode((700, 700))
  clock = py.time.Clock()

if __name__ == "__main__":
  pacmanGA = genetic.GeneticAlgorithm()
  ghostGAs = []
  for ghost in range(settings.ghostCount):
    ghostGAs.append(genetic.GeneticAlgorithm())

  # somewhere in here we need to make sure the gene -> weights conversion is done.
  # the genome will probably be a single array of i*h + h*o length, while the nn needs that broken into 2
  # 2D arrays, one i by h and the other h by o in size.
  games = [game.Game(False, screen, clock, pacmanGA.offspring[i], [ghostGAs[j].offspring[i] for j in range(settings.ghostCount)]) for i in range(settings.populationSize)]
  if renderAny:
    games[0].render = True

  for gen in range(settings.generations):
    print(gen+1)
    ghostFitnesses = [[] for g in range(settings.ghostCount)]
    pacmanFitness = []
    for g in games:

      fitnesses = g.run()
      for i in range(settings.ghostCount):
        ghostFitnesses[i].append(fitnesses[i])
      pacmanFitness.append(fitnesses[-1])
      g.reset()
    
    # Get new population
    pacmanGA.nextGeneration(pacmanFitness)
    for ghost in range(settings.ghostCount):
      ghostGAs[ghost].nextGeneration(ghostFitnesses[ghost])

    
