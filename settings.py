'''
Global settings.
'''


FPS = 30

colors = {
    'white': (255, 255, 255),
    'red': (255, 0, 0),
    'yellow': (255, 255, 0)
}

# Defining the size of the neural network that will be the brain of each entity
inputSize = 8 # relative position of all other entities
hiddenSize = 10 # arbitrarily chosen
outputSize = 4 # 4 possible actions

geneSize = inputSize*hiddenSize + hiddenSize*outputSize

XOVER_RATE = 0.9
MUT_RATE = 0.2
TOURNAMENT_SIZE = 4
R = 0.1 # Amount to mutate by