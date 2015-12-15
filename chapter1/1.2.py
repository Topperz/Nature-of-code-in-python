__author__ = 'Topper121'


import pygame
import math
import random
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

colors = [GREEN,RED,BLUE]

pygame.init()

# Set the width and height of the screen [width, height]
width = 640
height = 360
size = (width, height)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("My Game")

##### Ball

x = 100
y = 100
xspeed = 2
yspeed = 4


##### Creating the PVector class, adding functions as needed.

class PVector:

    def __init__(self, x_, y_):

        self.x = x_
        self.y = y_

    def add(self, v):
        self.x = self.x + v.x
        self.y = self.y + v.y

    def sub(self, v):
        self.x = self.x - v.x
        self.y = self.y - v.y

    def mult(self, n):
        self.x = self.x * n
        self.y = self.y * n

    def div(self, n):
        self.x = self.x / n
        self.y = self.y / n

    def mag(self):
        return math.sqrt(self.x*self.x+self.y*self.y)

    def normalize(self):
        m = self.mag()
        if m != 0:
            self.div(m)

    def limit(self, maxspeed):
        if self.mag() > maxspeed:
            self.normalize()
            self.mult(maxspeed)

    def staticAdd(v1, v2):
        v3 = PVector(v1.x + v2.x, v1.y + v2.y)
        return v3

    def staticSub(v1, v2):
        v3 = PVector(v1.x - v2.x, v1.y - v2.y)
        return v3

    def staticMult(v1, v2):
        try:
            if type(v2) == int or type(v2) == float:
                v3 = PVector(v1.x * v2, v1.y * v2)
                return v3
            else:
                v3 = PVector(v1.x * v2.x, v1.y * v2.y)
                return v3
        except:
            print ("staticMult expects a number or PVector input")

    def staticDiv(v1, v2):
        try:
            if type(v2) == int or type(v2) == float:
                v3 = PVector(v1.x / v2, v1.y / v2)
                return v3
            else:
                v3 = PVector(v1.x / v2.x, v1.y / v2.y)
                return v3
        except:
            print ("staticDiv expects a number or PVector input")




######### Mover class

class Mover:

    def __init__(self):
        self.location = PVector(random.randrange(width), random.randrange(height))
        self.velocity = PVector(0,0)
        self.acceleration = PVector(0,0)
        self.topspeed = 4.0
        self.multiplier = random.randint(1,7)
        self.color = random.choice(colors)

    def update(self):
        ######## Random moving ball
        #acceleration = PVector2D()
        #acceleration.mult(random.uniform(-3,3))
        #self.velocity.add(acceleration)

        ##### Chase/flee mouse
        #mouse = PVector(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])

        #### Swap evil.location with mouse.location if needed
        direction = PVector.staticSub(evil.location, mover.location)
        direction.normalize()
        direction.mult(self.multiplier)
        self.acceleration = PVector.staticMult(direction, -1)
        #######
        self.velocity.add(self.acceleration)
        self.velocity.limit(self.topspeed)
        self.location.add(self.velocity)

    def display(self):
        pygame.draw.circle(screen, self.color, (int(self.location.x), int(self.location.y)), 16)

    def checkEdges(self):
        ####### Makes objects appear on the other side of the screen
        if self.location.x - 16 > width:
            self.location.x = 0
        elif self.location.x + 16< 0:
            self.location.x = width

        if self.location.y - 16 > height:
            self.location.y = 0
        elif self.location.y +16 < 0:
            self.location.y = height

        ####### Makes objects bounce of edge of screen
        # if self.location.x+16 > width or self.location.x-16 < 0:
        #     self.velocity.x *= -10
        # if self.location.y+16 > height or self.location.y-16 < 0:
        #     self.velocity.y *= -10

class EvilMover(Mover):

    def __init__(self):
        super().__init__()
        self.topspeed = 3

    def update(self):
        ######## Random moving ball
        #acceleration = PVector2D()
        #acceleration.mult(random.uniform(-3,3))
        #self.velocity.add(acceleration)

        ##### Chase mouse
        #mouse = PVector(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])

        #### Chase closest mover
        self.temp = 1000
        self.closest_mover = 0
        for mover in movers:
            mag = PVector.staticSub(mover.location, evil.location).mag()
            if mag < self.temp:
                self.temp = mag
                self.closest_mover = mover
        ########
        direction = PVector.staticSub(self.closest_mover.location, evil.location)
        direction.normalize()
        direction.mult(self.multiplier)
        self.acceleration = PVector.staticMult(direction, 1)
        #######
        self.velocity.add(self.acceleration)
        self.velocity.limit(self.topspeed)
        self.location.add(self.velocity)

    def display(self):
        pygame.draw.circle(screen, BLACK, (int(self.location.x), int(self.location.y)), 16)

#location = PVector(100,100)
#velocity = PVector(1,3.3)


###### Exercise 1.7
# v = PVector(1,5)
# print (v.x)
# u = PVector.staticMult(v,2)
# print (u.x)
# w = PVector.staticMult(v,u)
# print (w.x,w.y)
# w.div(3)
# print (w.x,w.y)


def PVector2D():
    m = PVector(random.randint(-100,100), random.randint(-100,100))
    m.normalize()
    return m

#mover = Mover()
movers = []
for i in range(10):
    movers.append(Mover())

evil = EvilMover()
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
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                mover.velocity.x = mover.velocity.x + -1
                mover.velocity.y = mover.velocity.y + -1
            if event.key == pygame.K_RIGHT:
                mover.velocity.x = mover.velocity.x + 1
                mover.velocity.y = mover.velocity.y + 1
            if event.key == pygame.K_DOWN:
                mover.velocity.x = 0
                mover.velocity.y = 0
    # --- Game logic should go here
    #location.add(velocity)

    #if location.x+16 > width or location.x-16 < 0:
    #     velocity.x *= -1
    # if location.y+16 > height or location.y-16 < 0:
    #     velocity.y *= -1

    #mouse = PVector(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])
    #center = PVector(width/2, height/2)

    #mouse.sub(center)
    #mouse.normalize()
    #mouse.mult(50)

    # --- Drawing code should go here

    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(WHITE)

    #pygame.draw.circle(screen, RED, (int(location.x), int(location.y)), 16)

    #pygame.draw.line(screen, BLACK, (0+width/2, 0+height/2),(mouse.x+width/2, mouse.y+height/2), 2)
    #m = mouse.mag()

    #pygame.draw.rect(screen, BLACK, [0,0,m,10])


    #print (mover.velocity.x, mover.velocity.y)
    for mover in movers:
        mover.update()
        mover.checkEdges()
        mover.display()
    #print (evil.multiplier)
    #print (evil.acceleration.x, evil.acceleration.y)
    #print (evil.velocity.x, evil.velocity.y)
    evil.update()
    evil.checkEdges()
    evil.display()

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)

# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()