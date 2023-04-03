'''
Genetic Algorithm class.

We may allow the genetic algorithm to be aware of the game itself,
(have the initialization and running of all games for all generations occur within the GA itself),
but I think it would be better for modularity if that is kept separate, so the GA only knows about
the genes of it's population, as well as fitness values returned. It doesn't even need to know
about the neural networks that the genes represent (will need to be changed if more advanced
algorithms are used).
'''
import numpy as np

class GeneticAlgorithm():
  def __init__(self, popSize, geneSize, mutationRate):
    self.popSize = popSize
    self.mutationRate = mutationRate
    self.population = np.random.normal(size=(popSize,geneSize))

  def mutate(self, member):
    pass
  
  def parentSelection(self):
    pass
  
  def crossover(self):
    pass
  
  def nextGeneration(self, fitnesses):
    pass