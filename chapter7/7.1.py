__author__ = 'Topper121'

import pygame
import random
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


pygame.init()

# Set the width and height of the screen [width, height]
width = 1200
height = 800
size = (width, height)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("My Game")

class CA:
    def __init__(self):
        self.cells = []
        self.ruleset = [0,0,0,1,1,1,1,0]
        self.cellwitdh = 10
        self.cellcount = width / self.cellwitdh + 4

        self.generation = 0

        self.resetCells()

    def resetCells(self):
        del self.cells[:]
        for i in range(int(self.cellcount)):
            self.cells.append(0)
        self.cells[int(len(self.cells)/2)] = 1

    def generate(self):
        nextgen = []
        for i in range(1, len(self.cells)-1):
            left = self.cells[i-1]
            mid = self.cells[i]
            right = self.cells[i+1]
            nextgen.append(self.rules(left, mid, right))
        nextgen.insert(0, 0)
        nextgen.append(0)
        self.cells = nextgen
        self.generation += 1

    def rules(self, a, b, c):
        if (a == 1 and b == 1 and c == 1): 
            return self.ruleset[0]
        elif (a == 1 and b == 1 and c == 0): 
            return self.ruleset[1]
        elif (a == 1 and b == 0 and c == 1): 
            return self.ruleset[2]
        elif (a == 1 and b == 0 and c == 0): 
            return self.ruleset[3]
        elif (a == 0 and b == 1 and c == 1): 
            return self.ruleset[4]
        elif (a == 0 and b == 1 and c == 0): 
            return self.ruleset[5]
        elif (a == 0 and b == 0 and c == 1): 
            return self.ruleset[6]
        elif (a == 0 and b == 0 and c == 0): 
            return self.ruleset[7]
        else:
            return 0

    def display(self):

        for i in range(len(self.cells)):
            if self.cells[i] == 0:
                pygame.draw.rect(screen, BLACK, (self.cellwitdh * i - self.cellwitdh*2, self.generation * self.cellwitdh, self.cellwitdh, self.cellwitdh), 1)
            else:
                pygame.draw.rect(screen, BLACK, (self.cellwitdh * i - self.cellwitdh*2, self.generation * self.cellwitdh, self.cellwitdh, self.cellwitdh), 0)

def generateRuleSet():
    ruleset = []
    for i in range(8):
        ruleset.append(random.randint(0,1))
    return ruleset

ca = CA()
# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()
screen.fill(WHITE)
# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # --- Game logic should go here

    # --- Drawing code should go here

    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.


    # for i in range(len(cells)):
    #     if cells[i] == 0:
    #         pygame.draw.rect(screen, BLACK, (0 + 50*i, 0, 50, 50), 1)
    #     else:
    #         pygame.draw.rect(screen, BLACK, (0 + 50*i, 0, 50, 50), 0)
    ca.display()
    ca.generate()

    if ca.generation > height / ca.cellwitdh:
        ca.ruleset = generateRuleSet()
        ca.generation = 0
        ca.resetCells()
        print (ca.ruleset)
        screen.fill(WHITE)
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(10)

# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()