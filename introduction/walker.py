__author__ = 'Topper121'


import pygame
import random
import time
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

width = 600
height = 400

class Walker:

    def __init__(self, width, height):
        self.x = int(width/2)
        self.y = int(height/2)
        self.trail = []


    def draw(self):
        pygame.draw.circle(screen, BLACK, (self.x, self.y),0)

    def step(self):
        ######### First random walk
        # choice = random.randint(0,3)
        # #print (choice)
        # if choice == 0:
        #     self.x += 1
        # elif choice == 1:
        #     self.x -= 1
        # elif choice == 2:
        #     self.y += 1
        # elif choice == 3:
        #     self.y -= 1
        # trail.append((self.x, self.y))

        ######## Second random walk
        # stepx = random.randint(-1,1)
        # stepy = random.randint(-1,1)
        #
        # self.x += stepx
        # self.y += stepy
        # trail.append((self.x, self.y))

        ######## Random walk with mouse

        usemouse = random.random()

        if usemouse <= 0.001:
            stepmod = montecarlo()
            stepsize = int(100*stepmod)
            print (stepsize)
            stepx = random.randint(-stepsize,stepsize)
            stepy = random.randint(-stepsize,stepsize)

            self.x += stepx
            self.y += stepy
            self.trail.append((self.x, self.y))

        if usemouse < 0.95:
            stepx = random.randint(-1,1)
            stepy = random.randint(-1,1)

            self.x += stepx
            self.y += stepy
            self.trail.append((self.x, self.y))
        else:
            if self.x < mousepos[0] and self.y < mousepos[1]:
                stepx = random.randint(0,1)
                stepy = random.randint(0,1)
                self.x += stepx
                self.y += stepy
            elif self.x < mousepos[0] and self.y > mousepos[1]:
                stepx = random.randint(0,1)
                stepy = random.randint(-1,0)
                self.x += stepx
                self.y += stepy
            elif self.x > mousepos[0] and self.y < mousepos[1]:
                stepx = random.randint(-1,0)
                stepy = random.randint(0,1)
                self.x += stepx
                self.y += stepy
            elif self.x > mousepos[0] and self.y > mousepos[1]:
                stepx = random.randint(-1,0)
                stepy = random.randint(-1,0)
                self.x += stepx
                self.y += stepy
            else:
                stepx = random.randint(-1,1)
                stepy = random.randint(-1,1)

                self.x += stepx
                self.y += stepy
        self.trail.append((self.x, self.y))

def montecarlo():
    while True:
        r1 = random.random()
        probability = r1
        r2 = random.random()
        if r2 < probability:
            return r1




pygame.init()

# Set the width and height of the screen [width, height]
size = (width, height)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("My Game")

dot = Walker(width,height)
time1 = time.time()
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            time2 = time.time() - time1
            print ("Time run: %0.2f" % time2)
            print (len(trail))
            print (dot.x)


    # --- Game logic should go here
    mousepos = pygame.mouse.get_pos()

    # --- Drawing code should go here



    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(WHITE)
    dot.draw()
    dot.step()
    #print (trail)
    for i in dot.trail:
       pygame.draw.circle(screen, BLACK, i,0)


    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)

# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()