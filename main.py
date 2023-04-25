'''
Main file that defines everything. Runs the GA over multiple game boards and generations.
'''
import game, nn, genetic, settings
import pygame as py
import matplotlib.pyplot as plt


def stepGeneration(games, pacmanGA=None, ghostGAs=None, phase=None):
  ghostFitnesses = [[] for g in range(settings.ghostCount)]
  pacmanFitness = []
  for g in games:
    fitnesses = g.run()
    for i in range(settings.ghostCount):
      ghostFitnesses[i].append(fitnesses[i])
    pacmanFitness.append(fitnesses[-1])
    g.reset()

  point = 0

  # comment out if too many logs, but useful to verify the ghosts are learning.
  # print("Count of best fitness for generation: ",ghostFitnesses[i].count(0), "out of ", len(ghostFitnesses[i]))
  if phase == 1:
    count = pacmanFitness.count(0) + sum([ghostFitnesses[i].count(0) for i in range(len(ghostFitnesses))])
    print("Number of entities that avoid walls completely:",count, "of", len(games)*(len(ghostFitnesses)+1), "entities.")
    point = (count*100)/(len(games)*(len(ghostFitnesses)+1))
  if phase == 2:
    print("Number of games the ghost caught pacman and avoided all walls: ",ghostFitnesses[0].count(0), "out of ", len(ghostFitnesses[0]))
    point = (ghostFitnesses[0].count(0)*100)/len(ghostFitnesses[0])
  if phase == 3:
    count = pacmanFitness.count(0) + sum([ghostFitnesses[i].count(0) for i in range(len(ghostFitnesses))])
    print("Best pacman fitness: ",max(pacmanFitness)," which occurred",  pacmanFitness.count(max(pacmanFitness))," times out of ", len(pacmanFitness))
    point = (pacmanFitness.count(max(pacmanFitness))*100)/len(pacmanFitness)
  # no phase 4 print rn because I'm not sure what we would want to
  
  # Get new population
  if pacmanGA:
    pacmanGA.nextGeneration(pacmanFitness)
  if ghostGAs:
    for ghost in range(settings.ghostCount):
      ghostGAs[ghost].nextGeneration(ghostFitnesses[ghost])

  return point

def nextPhase(ga):
  # In between phases, loose the most recent children, so have 1 wasted generation. But allow
  # easy transition between learning phases
  ga.offspring = ga.parent
  ga.parentFitness = [0 for _ in range(ga.popSize)]
  ga.offspringFitness = [0 for _ in range(ga.popSize)]
  ga.firstGen = True


renderAny = True
screen = None # I hate python scoping, so having this here because it's weird.
if renderAny:
  screen = py.display.set_mode((700, 700))
  clock = py.time.Clock()

if __name__ == "__main__":
  pacmanGA = genetic.GeneticAlgorithm()
  ghostGAs = []
  for ghost in range(settings.ghostCount):
    ghostGAs.append(genetic.GeneticAlgorithm(maximize=False))

  # initial set of game boards
  games = [game.Game( False, screen, clock, pacmanGA.offspring[i],
                      [ghostGAs[j].offspring[i] for j in range(settings.ghostCount)],
                      pacmanCanDie=False, boardSize=settings.boardSize, wallMaxPenalty=100, onlyWallFitness=True)
            for i in range(settings.populationSize)]


  # Phase 1
  print("PHASE 1: teach entities to avoid the walls")

  y_axis = []
  for gen in range(settings.phase1Generations):
    print(gen+1)

    # Run the games, evaluate fitness
    point = stepGeneration(games, pacmanGA, ghostGAs, phase=1)
    y_axis.append(point)
    games = games[0:len(pacmanGA.offspring)] # prune games after initial generation

    # assign offspring to each game field, so next iteration runs all of them.
    for i in range(len(games)):
      games[i].assignPopToGame(pacmanGA.offspring[i], [ghostGAs[j].offspring[i] for j in range(settings.ghostCount)])

  plt.plot([x for x in range(settings.phase1Generations)], y_axis, 'k.-')
  plt.title("Percentage of Agents that Successfully Avoided All Walls")
  plt.xlabel("Generation")
  plt.ylabel("Percentage that Avoided Walls")
  plt.show()

  # Transition Phase 1 -> Phase 2
  nextPhase(pacmanGA)
  for g in ghostGAs:
    nextPhase(g)
  # reset all game boards for the new generation, there's a few important changes to them
  games = [game.Game( False, screen, clock, pacmanGA.offspring[i],
                      [ghostGAs[j].offspring[i] for j in range(settings.ghostCount)],
                      boardSize=settings.boardSize, allRandomStart=True, pacmanMove=False)
            for i in range(settings.populationSize)]


  # Phase 2
  print("PHASE 2: Ghosts learn to go after pacman")

  y_axis = []
  for gen in range(settings.phase2Generations):
    print(gen+1)

    # Run the games, evaluate fitness
    point = stepGeneration(games, ghostGAs=ghostGAs, phase=2)
    y_axis.append(point)
    games = games[0:len(ghostGAs[0].offspring)]

    # assign offspring to each game field, so next iteration runs all of them.
    for i in range(len(games)):
      games[i].assignPopToGame(pacmanGA.offspring[i], [ghostGAs[j].offspring[i] for j in range(settings.ghostCount)])

  plt.plot([x for x in range(settings.phase2Generations)], y_axis, 'k.-')
  plt.title("Percentage of Ghosts that Successfully Caught Pacman and Avoided All Walls")
  plt.xlabel("Generation")
  plt.ylabel("Percentage that Caught Pacman and Avoided Walls")
  plt.show()

  # Transition Phase 2 -> Phase 3
  for g in ghostGAs:
    nextPhase(g)
  # reset all game boards for the new generation, there's a few important changes to them
  games = [game.Game( False, screen, clock, pacmanGA.offspring[i],
                      [ghostGAs[j].offspring[i] for j in range(settings.ghostCount)],
                      boardSize=settings.boardSize, allRandomStart=True, ghostMove=False)
            for i in range(settings.populationSize)]

  # Phase 3
  print("PHASE 3: Pacman learns to go avoid ghosts")

  y_axis = []
  for gen in range(settings.phase3Generations):
    print(gen+1)

    # Run the games, evaluate fitness
    point = stepGeneration(games, pacmanGA=pacmanGA, phase=3)
    y_axis.append(point)
    games = games[0:len(pacmanGA.offspring)]

    # assign offspring to each game field, so next iteration runs all of them.
    for i in range(len(games)):
      games[i].assignPopToGame(pacmanGA.offspring[i], [ghostGAs[j].offspring[i] for j in range(settings.ghostCount)])

  plt.plot([x for x in range(settings.phase3Generations)], y_axis, 'k.-')
  plt.title("Percentage of Pacman Agents that Have the Maximum Fitness")
  plt.xlabel("Generation")
  plt.ylabel("Percentage that Have Maximum Fitness")
  plt.show()

  # Transition Phase 3 -> Phase 4
  nextPhase(pacmanGA)
  # reset all game boards for the new generation, there's a few important changes to them
  games = [game.Game( False, screen, clock, pacmanGA.offspring[i],
                      [ghostGAs[j].offspring[i] for j in range(settings.ghostCount)],
                      boardSize=settings.boardSize)
            for i in range(settings.populationSize)]
  if renderAny:
    games[0].render = True


  # Phase 4
  print("PHASE 4: Full co-evolution of all entities")
  for gen in range(settings.phase4Generations):
    print(gen+1)

    # Run the games, evaluate fitness
    stepGeneration(games, pacmanGA, ghostGAs)
    games = games[0:len(pacmanGA.offspring)]

    # assign offspring to each game field, so next iteration runs all of them.
    for i in range(len(games)):
      games[i].assignPopToGame(pacmanGA.offspring[i], [ghostGAs[j].offspring[i] for j in range(settings.ghostCount)])