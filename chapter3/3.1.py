__author__ = 'Topper121'

import pygame
import math
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


pygame.init()

# Set the width and height of the screen [width, height]
width = 400
height = 400
size = (width, height)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("My Game")

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

    def get(self):
        return PVector(self.x, self.y)


class RectRotate():

    def __init__(self, x, y, width, height):
        self.location = PVector(x,y)
        self.velocity = PVector(0,0)
        self.acceleration = PVector(0,0)
        self.width = width
        self.height = height
        self.angle = 0
        self.aVelocity = 0
        self.aAcceleration = 0.0
        self.mass = 1.0


        self.color = GREEN

    def draw(self):
        self.surf = pygame.Surface((self.width, self.height))
        self.surf.fill((255, 255, 0))
        self.surf.set_colorkey((255,255,0))
        pygame.draw.rect(self.surf, self.color, (0,0, self.width, self.height))
        pygame.draw.circle(self.surf, BLACK, (0+10,int(self.height/2)),10)
        # pygame.draw.line(self.surf, BLACK, (20,self.height/2),(self.width-20, self.height/2))
        # pygame.draw.circle(self.surf, BLACK, (self.width - 10,int(self.height/2)),10)

    def update(self):
        self.velocity.add(self.acceleration)
        self.velocity.limit(10)
        self.location.add(self.velocity)

        self.aVelocity += self.aAcceleration
        self.angle += self.aVelocity

        self.acceleration.mult(0)

    def applyForce(self, force):
        f = PVector.staticDiv(force, self.mass)
        self.acceleration.add(f)

    def direction(self):
        self.angle = math.degrees(math.atan2(self.velocity.x, self.velocity.y)) + 90

    def rotate(self):
        self.surface_center = self.location.x + self.width/2 , self.location.y + self.height/2
        self.rotateSurf = pygame.transform.rotate(self.surf, self.angle)
        self.rotatedRect = self.rotateSurf.get_rect()
        self.rotatedRect.center = self.surface_center

    def display(self):
        screen.blit(self.rotateSurf, self.rotatedRect)

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

class Attractor:

    def __init__(self):
        self.location = PVector(width/2, height/2)
        self.mass = 20.0
        self.G = 100
        self.maxdistance = 500
        self.mindistance = 50

    def display(self):
        pygame.draw.circle(screen, BLACK, (int(self.location.x), int(self.location.y)), int(self.mass * 2))

    def attract(self, object):
        force = PVector.staticSub(self.location, object.location)
        distance = force.mag()
        #print ("Distance:", distance)
        if distance < self.mindistance:
            distance = self.mindistance
        if distance > self.maxdistance:
            distance = self.maxdistance
        m = (self.G * object.mass * self.mass) / (distance * distance)
        #print (m)
        force.normalize()
        force.mult(m)
        return force


mover = RectRotate(200,200,100,100)
mover2 = RectRotate(50,50,50,5)

a = Attractor()

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

    # --- Drawing code should go here

    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(WHITE)

    mouse = PVector(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])
    hu = mover2.location
    mouse.sub(hu)
    mouse.normalize()
    mouse.mult(2)

    mover2.applyForce(mouse)

    mover.draw()
    mover.rotate()
    mover.update()
    mover.display()
    mover.checkEdges()

    mover2.draw()
    mover2.rotate()
    mover2.direction()
    mover2.update()
    mover2.display()
    mover2.checkEdges()

    pygame.display.flip()
    # --- Limit to 60 frames per second
    clock.tick(30)

# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()