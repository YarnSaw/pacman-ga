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
import random
import settings


class GeneticAlgorithm():
  def __init__(self, maximize=True, popSize=settings.populationSize, geneSize=settings.geneSize, mutationRate=settings.MUT_RATE):
    self.popSize = popSize
    self.mutationRate = mutationRate
    self.parent = np.random.normal(size=(popSize,geneSize))
    self.offspring = self.parent                          # in the first generation, think of the new random pop as all offspring.

    self.parentFitness = [0 for _ in range(popSize)]          # Doesn't matter, first iteration is all 'offspring'
    self.offspringFitness = [0 for _ in range(popSize)]       # Will be immediately replaced in first iteration

    self.maximize = maximize
    self.firstGen = True

  def mutate(self, individual):
    mutant = individual.copy()

    # Amount to add
    change = (random.random()*2 - 1) * settings.R

    # Weight to add random value to
    idx = random.randrange(0, len(mutant))

    # Update weight
    mutant[idx] = mutant[idx] + change

    return mutant

  
  def parentSelection(self, mating_pool_size=settings.mating_pool_size, tournament_size=settings.TOURNAMENT_SIZE):
    """Tournament selection without replacement"""

    selected_to_mate = []

    # run tournaments until enough mates are selected
    while len(selected_to_mate) < mating_pool_size:
      # Select <tournament_size> random individuals (without replacement, so 
      # each individual will be different)
      tournament = random.sample(range(0, len(self.parentFitness)), tournament_size)
      best = tournament[0]

      # Find the best individual in the tournament (based on the self.parentFitness)
      for i in tournament:
        if (self.parentFitness[i] > self.parentFitness[best]) == self.maximize:
          best = i
      
      selected_to_mate.append(best)
    return np.array(selected_to_mate)
  

  def crossover(self, parent1, parent2):
    p1 = parent1.copy()
    p2 = parent2.copy()

    crossover_point = random.randrange(1, len(p1)-1)

    p1[crossover_point:] = parent2[crossover_point:]
    p2[crossover_point:] = parent1[crossover_point:]

    return p1, p2
  

  def survivor_selection(self, maximize=True):
    """mu+lambda selection"""

    population = []
    fitness = []

    pooled_pop = [i for i in range(self.parent.shape[0] + self.offspring.shape[0])]
    pooled_fitness = self.parentFitness + self.offspringFitness

    ranked_pop = [x for _, x in sorted(zip(pooled_fitness, pooled_pop), reverse=maximize)]
    fitness = sorted(pooled_fitness, reverse=maximize)[0:len(self.parentFitness)]

    # Get the best mu individuals where mu is the size of the current population (without offspring)
    population = np.zeros(self.parent.shape)
    for i in range(len(ranked_pop[:self.parent.shape[0]])):
      try:
        population[i] = self.parent[ranked_pop[i]]
      except (IndexError):
        population[i] = self.offspring[ranked_pop[i] - self.parent.shape[0]]
    
    self.parent = population
    self.parentFitness = fitness

  def nextGeneration(self, offspringFitness):
    if self.firstGen:
      self.parentFitness = offspringFitness
      self.firstGen = False
    else:
      self.offspringFitness = offspringFitness
      self.survivor_selection()

    parents = self.parentSelection()
    offspring = []
    for i in range(0, len(parents), 2):
      if random.random() < settings.XOVER_RATE:
        off1,off2 = self.crossover(self.parent[parents[i]], self.parent[parents[i+1]])
      else:
        off1 = self.parent[parents[i]].copy()
        off2 = self.parent[parents[i+1]].copy()
      
      offspring.append(self.mutate(off1))
      offspring.append(self.mutate(off2))

    self.offspring = np.array(offspring)


      

if __name__ == "__main__":
  # Test
  a=np.array([[1., 2., 3.], [1., 5., 3.], [4., 2., 2.], [2., 65., 6.]])
  b=np.array([[6., 8., 4.], [6., 9., 2.], [3., 7., 1.]])

  ga = GeneticAlgorithm(4, 3, 0.2)
  ga.population = a

  # Random fitness values
  a_fit = [2, 4, 1, 4]
  b_fit = [0, 5, 3]

  # Survivor selection
  print(ga.survivor_selection(a, a_fit, b, b_fit, False))

  # parent selection
  print(ga.parentSelection(a_fit, 2, 2, False))

  # Mutation
  print(ga.mutate(ga.population[1]))

  # Crossover
  print(ga.crossover(ga.population[0], ga.population[2]))
