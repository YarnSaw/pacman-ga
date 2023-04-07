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
  def __init__(self, popSize, geneSize, mutationRate):
    self.popSize = popSize
    self.mutationRate = mutationRate
    self.population = np.random.normal(size=(popSize,geneSize))


  def mutate(self, individual):
    mutant = individual.copy()

    for i in range(len(individual)):
      m = random.random()
      
      if m < settings.MUT_RATE:
        change = random.gauss(0, settings.R)
        mutant[i] = mutant[i] + change

    return mutant

  
  def parentSelection(self, fitness, mating_pool_size, tournament_size=settings.TOURNAMENT_SIZE, maximize=True):
    """Tournament selection without replacement"""

    selected_to_mate = []

    # run tournaments until enough mates are selected
    while len(selected_to_mate) < mating_pool_size:
      # Select <tournament_size> random individuals (without replacement, so 
      # each individual will be different)
      tournament = random.sample(range(0, len(fitness)), tournament_size)
      best = tournament[0]

      # Find the best individual in the tournament (based on the fitness)
      for i in tournament:
        if (fitness[i] > fitness[best]) == maximize:
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
  

  def survivor_selection(self, current_pop, current_fitness, offspring, offspring_fitness, maximize=True):
    """mu+lambda selection"""

    population = []
    fitness = []

    pooled_pop = [i for i in range(current_pop.shape[0] + offspring.shape[0])]
    pooled_fitness = current_fitness + offspring_fitness

    ranked_pop = [x for _, x in sorted(zip(pooled_fitness, pooled_pop), reverse=maximize)]
    fitness = sorted(pooled_fitness, reverse=maximize)[0:len(current_fitness)]

    # Get the best mu individuals where mu is the size of the current population (without offspring)
    population = np.zeros(current_pop.shape)
    for i in range(len(ranked_pop[:current_pop.shape[0]])):
      try:
        population[i] = current_pop[ranked_pop[i]]
      except (IndexError):
        population[i] = offspring[ranked_pop[i] - current_pop.shape[0]]
    
    return population, fitness
  

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
