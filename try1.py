__author__ = 'Topper121'

"""
 Pygame base template for opening a window

 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/

 Explanation video: http://youtu.be/vRB_983kUMc
"""

import pygame

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

import random
#import matplotlib.pyplot as plt

inputs = []
inputs.append(50)
inputs.append(-12)
inputs.append(-1)

class Perceptron:

    def __init__(self, n):

        self.weights = []
        self.c = 0.01

        for i in range(n):
            self.weights.append(random.uniform(-1,1))

    def activate(self, n):
        if n > 0:
            return 1
        else:
            return -1

    def feedforward(self, inputs):
        total = 0
        for i in range(len(self.weights)):
            total += inputs[i]*self.weights[i]
        return self.activate(total)

    def train(self, inputs, desired):
        guess = self.feedforward(inputs)
        error = desired - guess
        for i in range(len(self.weights)):
            self.weights[i] += self.c * error * inputs[i]

    def getWeights(self):
        return self.weights


class Trainer:

    def __init__(self, x, y, a):

        self.inputs = []

        self.inputs.append(x)
        self.inputs.append(y)
        self.inputs.append(1)
        self.answer = a

training = []

points = 50
count = 0
xmin = -400
ymin = -400
xmax = 400
ymax = 400

def f(x):
    return -2*x+1

pygame.init()

# Set the width and height of the screen [width, height]
size = (800, 800)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("My Game")

ptron = Perceptron(3)
greenlist = []
bluelist = []
linedraw = []



# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # --- Game logic should go here
    x = random.uniform(xmin, xmax)
    y = random.uniform(ymin, ymax)
    answer = 1
    if y < f(x):
        answer = -1
    training.append(Trainer(x, y, answer))
    #print (training)
    ptron.train(training[count].inputs, training[count].answer)
    #print (training[count])
    weights = ptron.getWeights()
    #print weights
    x1 = xmin
    y1 = (-weights[2] - weights[0]*x1)/weights[1]
    x2 = xmax
    y2 = (-weights[2] - weights[0]*x2)/weights[1]
    #print ("y1: ", x1, y1)
    #print ("y2: ", x2, y2)
    slope1 = (y2-y1)/(x2-x1)
    #print (slope1)
    guess = ptron.feedforward(training[count].inputs)
    if guess > 0:
        greenlist.append((x,y))
    else:
        bluelist.append((x,y))
    linedraw.append(((x1,y1),(x2, y2)))
    count += 1
    # --- Drawing code should go here



    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(WHITE)
    for i in range(len(bluelist)):
        x = int(bluelist[i][0])
        y = int(bluelist[i][1])
        #print(y)
        pygame.draw.circle(screen, BLACK,(x+400,y+400) ,2)


    for i in range(len(greenlist)):
        x = int(greenlist[i][0])
        y = int(greenlist[i][1])
        #print(y)
        pygame.draw.circle(screen, RED,(x+400,y+400) ,2)

    #print(linedraw)
    for i in range(len(linedraw)):
        j1 = int(linedraw[i][0][0])
        k1 = int(linedraw[i][0][1])
        j2 = int(linedraw[i][1][0])
        k2 = int(linedraw[i][1][1])
        pygame.draw.line(screen,GREEN, (j1+400,k1+400),(j2+400,k2+400), 1)


    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(10)

# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()