'''
Global settings.
'''


FPS = 60

colors = {
    'white': (255, 255, 255),
    'black': (0, 0, 0),
    'red': (255, 0, 0),
    'yellow': (255, 255, 0)
}

# GAME-BASED SETTINGS
phase1Generations = 5 # Training all entities to avoid the walls
phase2Generations = 5 # Train ghosts to approach a stand-alone pacman
phase3Generations = 5 # Train pacman to run away from stand-alone ghosts
phase4Generations = 5 # Train everything all together
iterationsPerGen=100
ghostCount = 1
boardSize=10

# NEURAL NETWORK SETTINGS
inputSize = (ghostCount+1)*2 + 1 # relative position of all other entities + bias
hiddenSize = 10 # arbitrarily chosen
outputSize = 4 # 4 possible actions

# NEURAL NET AND GA SETTINGS
geneSize = inputSize*hiddenSize + hiddenSize*outputSize

# GA SETTINGS
populationSize = 100
mating_pool_size = 10
XOVER_RATE = 0.9
MUT_RATE = 0.2
TOURNAMENT_SIZE = 4
R = 0.5 # Amount to mutate by