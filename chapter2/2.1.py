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



##### PVector class

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


def checkWind():
    r = random.random()
    if r < 0.5:
        return PVector(-0.2,0)
    else:
        return PVector(0.2,0)
######### Mover class

class Mover:

    def __init__(self, m, x, y):
        self.location = PVector(x, y)
        self.velocity = PVector(0,0)
        self.acceleration = PVector(0,0)
        self.topspeed = 15.0
        self.multiplier = random.randint(1,7)
        self.color = random.choice(colors)
        self.mass = m
        self.firstHit = False
        self.G = 100
        self.maxdistance = 100
        self.mindistance = 50


    def update(self):
        self.velocity.add(self.acceleration)
        #self.velocity.limit(self.topspeed)
        self.location.add(self.velocity)
        # if self.location.x + self.mass * 16 > width or self.location.x - self.mass * 16 < 0:
        #     self.velocity.x *= -1
        # if self.location.y+ self.mass * 16 > height or self.location.y- self.mass * 16 < 0:
        #     self.velocity.y = self.velocity.y * - 1 - gravity.y / self.mass
        self.acceleration.mult(0)


    def display(self):
        pygame.draw.circle(screen, self.color, (int(self.location.x), int(self.location.y)), int(self.mass * 2))

    def checkEdges(self):
        ####### Makes objects appear on the other side of the screen
        # if self.location.x - 16 > width:
        #     self.location.x = 0
        # elif self.location.x + 16< 0:
        #     self.location.x = width
        #
        # if self.location.y - 16 > height:
        #     self.location.y = 0
        # elif self.location.y +16 < 0:
        #     self.location.y = height
        # print ("velocity: ", self.velocity.x, self.velocity.y)
        # print ("acceleration: ", self.acceleration.x, self.acceleration.y)
        # print ("location: ", self.location.x, height - self.location.y)
        ####### Makes objects bounce of edge of screen - gravity / mass is added to correct 1 frame not being calculated in return velocity
        if self.location.x + self.mass * 16 >= width or self.location.x - self.mass * 16 <= 0:
            self.velocity.x = self.velocity.x * - 1 - gravity.x / self.mass
        # if self.location.y+ self.mass * 16 >= height or self.location.y- self.mass * 16 <= 0:
        #     self.velocity.y = self.velocity.y * - 1 - gravity.y / self.mass

        ###### The constant gravity will keep pulling the object out of the window. This will lock it in place
        ###### Velocity is used to set the extra margin, since it determes how much location changes each frame.
        if self.location.x+ self.mass * 16 >= width+3+abs(self.velocity.x) or self.location.x- self.mass * 16 <= 0-3-abs(self.velocity.x):
            self.acceleration.x *= 0
            self.velocity.x = 0
        # if self.location.y+ self.mass * 16 >= height+3+abs(self.velocity.y) or self.location.y- self.mass * 16 <= 0-3-abs(self.velocity.y):
        #     self.acceleration.y *= 0
        #     self.velocity.y = 0

    def applyForce(self, force):
        f = PVector.staticDiv(force, self.mass)
        self.acceleration.add(f)

    def pocketCheck(self, pocket):
        mag = PVector.staticSub(self.location, pocket.location).mag()
        if mag <= pocket.mass*16*2:
            self.velocity.mult(1.05)

    def pushBack(self):
        ###### Upper left
        if self.location.x < width/2 and self.location.y < height/2:
            p1 = PVector(0, self.location.y)
            p2 = PVector(self.location.x, 0)
            mag1 = PVector.staticSub(self.location, p1).mag()
            mag2 = PVector.staticSub(self.location, p2).mag()
            f1 = PVector(5/mag1, 0)
            f2 = PVector(0, 5/mag2)
            self.acceleration.add(f1)
            self.acceleration.add(f2)

        ##### Upper right
        if self.location.x > width/2 and self.location.y < height/2:
            p1 = PVector(width, self.location.y)
            p2 = PVector(self.location.x, 0)
            mag1 = PVector.staticSub(self.location, p1).mag()
            mag2 = PVector.staticSub(self.location, p2).mag()
            f1 = PVector(-5/mag1, 0)
            f2 = PVector(0, 5/mag2)
            self.acceleration.add(f1)
            self.acceleration.add(f2)
            #print (mag1)
        ###### Lower left
        if self.location.x < width/2 and self.location.y > height/2:
            p1 = PVector(0, self.location.y)
            p2 = PVector(self.location.x, height)
            mag1 = PVector.staticSub(self.location, p1).mag()
            mag2 = PVector.staticSub(self.location, p2).mag()
            f1 = PVector(5/mag1, 0)
            f2 = PVector(0, -5/mag2)
            self.acceleration.add(f1)
            self.acceleration.add(f2)
        ##### Lower right
        if self.location.x > width/2 and self.location.y > height/2:
            p1 = PVector(width, self.location.y)
            p2 = PVector(self.location.x, height)
            mag1 = PVector.staticSub(self.location, p1).mag()
            mag2 = PVector.staticSub(self.location, p2).mag()
            f1 = PVector(-5/mag1, 0)
            f2 = PVector(0, -5/mag2)
            self.acceleration.add(f1)
            self.acceleration.add(f2)

    def isInside(self, l):
        if self.location.x > l.x and self.location.x < l.x+l.w and self.location.y > l.y and self.location.y < l.y+l.h:
            return True
        else:
            return False

    def dragLiquid(self, liquid):
        speed = self.velocity.mag()
        dragMagnitude = liquid.c * speed * speed
        drag = self.velocity.get()
        drag.mult(-1)
        drag.normalize()
        drag.mult(dragMagnitude)
        drag.mult(0.5)
        print (dragMagnitude)
        self.applyForce(drag)
        if not self.firstHit:
            self.velocity.mult(0.5)
            self.firstHit = True
            print ("first hit")

    def dragAir(self):
        speed = self.velocity.mag()
        dragMagnitude = 0.1 * speed * speed
        drag = self.velocity.get()
        drag.mult(-1)
        drag.normalize()
        drag.mult(dragMagnitude)
        drag.mult(0.2)
        self.applyForce(drag)

    def repel(self, object):
        force = PVector.staticSub(self.location, object.location)
        distance = force.mag()
        #print ("Distance:", distance)
        if distance < self.mindistance:
            distance = self.mindistance
        if distance > self.maxdistance:
            force.mult(0)
            return force

        m = (self.G * object.mass * self.mass) / (distance * distance)
        m *= -1
        force.normalize()
        force.mult(m)
        return force

class Attractor:

    def __init__(self):
        self.location = PVector(width/2, height/2)
        self.mass = 20.0
        self.G = 100
        self.maxdistance = 450
        self.mindistance = 150

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

class Liquid:
    def __init__(self, x, y, w, h, c):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.c = c

    def display(self):
        s = pygame.Surface((self.w,self.h))
        s.set_alpha(128)
        s.fill(BLACK)
        screen.blit(s,(self.x, self.y) )

class Mover_Box(Mover):

    def __init__(self, m, x, y, w, h):
        self.location = PVector(x, y)
        self.width = w
        self.height = h
        self.velocity = PVector(0,0)
        self.acceleration = PVector(0,0)
        self.topspeed = 15.0
        self.multiplier = random.randint(1,7)
        self.color = random.choice(colors)
        self.mass = m
        self.firstHit = False

    def display(self):
        pygame.draw.rect(screen, self.color, [self.location.x, self.location.y, self.width, self.height])

    def drag(self, l):
        speed = self.velocity.mag()
        dragMagnitude = l.c * speed * speed * self.width
        drag = self.velocity.get()
        drag.mult(-1)
        drag.normalize()
        drag.mult(dragMagnitude)
        drag.mult(0.1)
        print (dragMagnitude)
        self.applyForce(drag)
        if not self.firstHit:
            self.velocity.mult(0.5)
            self.firstHit = True
            print ("first hit")


def rotate45(gameObject, rotations={}):
    r = rotations.get(gameObject,0) + 45
    rotations[gameObject] = r
    return pygame.transform.rotate(gameObject, r)


movers = []
for i in range(5):
   movers.append(Mover(3,50+75*i,50))
#m = Mover(3,150,150)
a = Attractor()
# mover = Mover(1,400,100)

speedPocket = Mover(2,300,150)
box = Mover_Box(3,100,100,100,100)
#gravity = PVector(0, 0.0)
wind = PVector(0.05, 0)

liquid = Liquid(0,height/2,width,height/2, 0.5)

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
            if event.key == pygame.K_UP:
                mover.velocity.mult(2)
            if event.key == pygame.K_DOWN:
                mover.velocity.mult(0.5)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            a.location = PVector(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])

    # --- Game logic should go here


    # --- Drawing code should go here

    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(WHITE)
    # for mover in movers:
    #     m = mover.mass * 0.1
    #     gravity = PVector(0,m)
    #
    #     frictionCoef = 0.03
    #     friction = mover.velocity.get()
    #     friction.mult(-1)
    #     friction.normalize()
    #     friction.mult(frictionCoef)
    #
    #     if mover.isInside(liquid):
    #         mover.dragLiquid(liquid)
    #
    #
    #     #mover.applyForce(friction)
    #     mover.applyForce(gravity)
    #     #mover.applyForce(wind)
    #     #mover.pocketCheck(speedPocket)
    #     mover.update()
    #     mover.display()
    #     mover.checkEdges()

    #speedPocket.display()
    box.display()
    ######## Mouse attract, other objects repel each other
    # a.location = PVector(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])
    # for i in range(len(movers)):
    #     for j in range(len(movers)):
    #         if i != j:
    #             force = movers[j].repel(movers[i])
    #             movers[i].applyForce(force)
    #     f = a.attract(movers[i])
    #     movers[i].applyForce(f)
    #     movers[i].dragAir()
    #
    #     movers[i].update()
    #     movers[i].display()
    #####################

    #a.display()
    # f = a.attract(m)
    # m.applyForce(f)
    # m.update()
    # m.display()
    # mover.applyForce(gravity)
    # mover.applyForce(wind)
    # #mover.pushBack()
    # mover.update()
    # mover.display()
    # mover.checkEdges()

    #liquid.display()

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)

# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()