'''
Global settings.
'''


FPS = 30

colors = {
    'white': (255, 255, 255),
    'red': (255, 0, 0),
    'yellow': (255, 255, 0)
}

# GAME-BASED SETTINGS
generations = 1 # eh, kinda gameplay kinda GA. But I wanted it by iterationsPerGen cus they determine the time to train
iterationsPerGen=100
ghostCount = 1

# NEURAL NETWORK SETTINGS
inputSize = ghostCount*2 # relative position of all other entities
hiddenSize = 10 # arbitrarily chosen
outputSize = 4 # 4 possible actions

# NEURAL NET AND GA SETTINGS
geneSize = inputSize*hiddenSize + hiddenSize*outputSize

# GA SETTINGS
populationSize = 10
mating_pool_size = 10
XOVER_RATE = 0.9
MUT_RATE = 0.2
TOURNAMENT_SIZE = 4
R = 0.1 # Amount to mutate by