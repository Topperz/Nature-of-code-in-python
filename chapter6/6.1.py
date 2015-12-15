__author__ = 'Topper121'

"""
In this chapter, while simulating direction of the object, I'll use an image.
Pygame has very poor support for rotating, so using an image file makes things easier to work with
"""

import pygame
import math
import random

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


pygame.init()

# Set the width and height of the screen [width, height]
width = 800
height = 800
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

    def setMag(self, magnitude):
        self.normalize()
        self.mult(magnitude)

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

    def dot(self, v1):
        return self.x * v1.x + self.y * v1.y

    def angleBetween(v1, v2):
        dott = v1.dot(v2)
        theta = math.acos(dott / (v1.mag() * v2.mag()))
        return theta

    def dist(v1, v2):
        temp = PVector.staticSub(v1,v2)
        return temp.mag()

class Vehicle:
    ### The player will be drawn, so the location is the center of the image
    def __init__(self, surf, x, y, number):
        self.surf = surf
        self.location = PVector(x,y)
        self.velocity = PVector(0,0)
        self.acceleration = PVector(0,0)
        self.maxspeed = 5.0
        self.maxforce = 0.1

        self.number = number

        self.angle = 0
        self.aVelocity = 0
        self.aAcceleration = 0.0

    def applyForce(self, f):
        self.acceleration.add(f)

    def update(self):
        self.velocity.add(self.acceleration)
        self.velocity.limit(self.maxspeed)
        self.location.add(self.velocity)

        self.aVelocity += self.aAcceleration
        self.angle += self.aVelocity

        self.acceleration.mult(0)

    def seek(self, target):
        desired = PVector.staticSub(target, self.location)
        desired.normalize()
        desired.mult(self.maxspeed)

        steer = PVector.staticSub(desired, self.velocity)
        steer.limit(self.maxforce)

        return steer

    def arrive(self, target):
        desired = PVector.staticSub(target, self.location)

        d = desired.mag()
        desired.normalize()
        if d < 100:
            # I multiply by 0 to cancel out the force added from the seek function, once arrive function takes over.
            self.acceleration.mult(0)
            m = proximity_magnitude(d, 0, 100, 0, self.maxspeed)
            desired.mult(m)
        else:
            desired.mult(self.maxspeed)

        steer = PVector.staticSub(desired, self.velocity)
        steer.limit(self.maxforce)

        self.applyForce(steer)

    def flee(self, target):
        desired = PVector.staticSub(target, self.location)
        desired.normalize()
        desired.mult(self.maxspeed)

        steer = PVector.staticSub(desired, self.velocity)
        steer.limit(self.maxforce)

        steer.mult(-1)

        self.applyForce(steer)

    def pursuit(self, target):
        a = target.location.get()
        b = target.velocity.get()
        b.mult(5)
        a.add(b)
        steer = self.seek(a)
        self.applyForce(steer)

    def follow(self, p):
        predict = self.velocity.get()
        predict.normalize()
        predict.mult(25)
        predict_loc = PVector.staticAdd(self.location, predict)

        a = p.start
        b = p.end
        normal_point = getNormalPoint(predict_loc, a, b)

        dir = PVector.staticSub(b, a)
        dir.normalize()
        dir.mult(10)
        target = PVector.staticAdd(normal_point, dir)

        dist = PVector.dist(normal_point, predict_loc)
        if dist > p.radius:
            self.seek(target)

    def seperate(self, vehicles):
        desired_seperation = 40
        total = PVector(0,0)
        count = 0
        for other in vehicles:
            d = PVector.dist(self.location, other.location)
            if d > 0 and d < desired_seperation:
                diff = PVector.staticSub(self.location, other.location)
                diff.normalize()
                total.add(diff)
                count += 1
        if count > 0:
            total.div(count)
            total.setMag(self.maxspeed)

            steer = PVector.staticSub(total, self.velocity)
            steer.limit(self.maxforce )

            return steer
        else:
            return PVector(0,0)

    def align(self, vehicles):
        neighbordist = 60
        total = PVector(0,0)
        count = 0
        for other in vehicles:
            d = PVector.dist(self.location, other.location)
            if d > 0 and d < neighbordist:
                total.add(other.velocity)
                count += 1
        if count > 0:
            total.div(count)
            total.normalize()
            total.mult(self.maxspeed)

            steer = PVector.staticSub(total, self.velocity)
            steer.limit(self.maxforce)

            return steer
        else:
            return PVector(0,0)

    def cohesion(self, vehicles):
        desired_cohesion = 100
        total = PVector(0,0)
        count = 0
        for other in vehicles:
            d = PVector.dist(self.location, other.location)
            if d > 0 and d < desired_cohesion:
                total.add(other.location)
                count += 1
        if count > 0:
            total.div(count)
            return self.seek(total)
        else:
            return PVector(0,0)

    def applyBehaviors(self, vehicles):
        seperate_force = self.seperate(vehicles)
        align_force = self.align(vehicles)
        seek_force = self.seek(mouse)

        # if self.number % 2 == 0:
        #     seperate_force.mult(1.5)
        #     seek_force.mult(0.5)
        # else:
        #     seperate_force.mult(0.5)
        #     seek_force.mult(1.5)

        self.applyForce(seperate_force)
        self.applyForce(seek_force)
        self.applyForce(align_force)

    def flock(self, vehicles):
        seperate_force = self.seperate(vehicles)
        align_force = self.align(vehicles)
        coh_force = self.cohesion(vehicles)

        seperate_force.mult(1.5)

        self.applyForce(seperate_force)
        self.applyForce(coh_force)
        self.applyForce(align_force)

    def direction(self):
        #atan2 returns the angle of a vector in radians.
        # Degrees converts it to degrees, so i can be passed to the rotate function.
        self.angle = math.degrees(math.atan2(self.velocity.x, self.velocity.y)) + 180

    def rotate(self):
        self.rotateSurf = pygame.transform.rotate(self.surf, self.angle)
        self.rotateSurfRect = self.rotateSurf.get_rect()
        self.rotateSurfRect.center = self.location.x, self.location.y

    def display(self):
        screen.blit(self.rotateSurf, self.rotateSurfRect)

    def checkEdgesBounce(self):
        if self.location.x  >= width or self.location.x <= 0:
            self.velocity.x = self.velocity.x * - 1
            self.velocity.mult(2)
        if self.location.y>= height or self.location.y<= 0:
            self.velocity.y = self.velocity.y * - 1

    def checkEdgesOtherSide(self):
        ####### Makes objects appear on the other side of the screen
        if self.location.x - 16 > width:
            self.location.x = 0
        elif self.location.x + 16< 0:
            self.location.x = width

        if self.location.y - 16 > height:
            self.location.y = 0
        elif self.location.y +16 < 0:
            self.location.y = height

class Mover:

    def __init__(self, x, y):
        self.location = PVector(x, y)
        self.velocity = PVector(4,3)
        self.acceleration = PVector(0,0)
        self.topspeed = 15.0
        self.mass = 1.0

    def update(self):
        self.velocity.add(self.acceleration)
        self.velocity.limit(self.topspeed)
        self.location.add(self.velocity)
        #self.acceleration.mult(0)


    def display(self):
        pygame.draw.circle(screen, RED, (int(self.location.x), int(self.location.y)), 16)

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
            self.velocity.x = self.velocity.x * - 1
        if self.location.y+ self.mass * 16 >= height or self.location.y- self.mass * 16 <= 0:
            self.velocity.y = self.velocity.y * - 1

        ###### The constant gravity will keep pulling the object out of the window. This will lock it in place
        ###### Velocity is used to set the extra margin, since it determes how much location changes each frame.
        # if self.location.x+ self.mass * 16 >= width+3+abs(self.velocity.x) or self.location.x- self.mass * 16 <= 0-3-abs(self.velocity.x):
        #     self.acceleration.x *= 0
        #     self.velocity.x = 0
        # if self.location.y+ self.mass * 16 >= height+3+abs(self.velocity.y) or self.location.y- self.mass * 16 <= 0-3-abs(self.velocity.y):
        #     self.acceleration.y *= 0
        #     self.velocity.y = 0

class FlowField:
    def __init__(self):
        self.resolution = 10
        self.cols = int(width / self.resolution)
        self.rows = int(height / self.resolution)
        self.field = []
        self.fill_field_pointcenter()

    def fill_field_uniform(self):
        for i in range(self.rows):
            self.field.append([])
            for j in range(self.cols):
                self.field[j].append(PVector(1,0))

    def fill_field_pointcenter(self):
        for i in range(self.rows):
            self.field.append([])
            for j in range(self.cols):
                temp = PVector(i*self.resolution, j*self.resolution)
                center = PVector(width/2,height/2)
                direction = PVector.staticSub( center, temp)
                direction.normalize()
                self.field[i].append(direction)

    def lookup(self, target):
        column = int(target.location.x/self.resolution)
        row = int(target.location.y/self.resolution)
        if column < 0:
            column = 0
        if column > self.cols-1:
            column = self.cols-1
        if row < 0:
            row = 0
        if row > self.rows -1:
            row = self.rows -1
        return self.field[column][row].get()

class Path:
    def __init__(self):
        self.radius = 20
        self.start = PVector(0,400)
        self.end = PVector(width,600)

    def display(self):
        a = PVector.staticSub(self.end, self.start)
        b = PVector(width, 0)
        theta = PVector.angleBetween(a,b)
        angle = math.degrees(theta) * -1
        pygame.draw.line(screen, BLACK, (self.start.x, self.start.y), (self.end.x, self.end.y))
        ### The path is drawn by tilting a surface and drawing a rect onto it. The angle is calculated,
        ### but the location is approximated, to make it look right.
        s = pygame.Surface((width+150,self.radius*2))
        s.set_alpha(128)
        s.fill(BLACK)
        s.set_colorkey(BLACK)
        pygame.draw.rect(s, RED, (0,0, width+100, self.radius*2))
        rotatedS = pygame.transform.rotate(s, angle)
        screen.blit(rotatedS,(self.start.x-50, self.start.y - self.radius -14) )

class Flock:
    def __init__(self):
        self.boids = []

    def run(self):
        for b in self.boids:
            b.flock(self.boids)
            b.update()
            b.direction()
            b.rotate()
            b.display()
            b.checkEdgesOtherSide()

    def addBoid(self, b):
        self.boids.append(b)



def make_player_surface(imagePath):
    player = pygame.image.load(imagePath).convert()
    player.set_colorkey(BLACK)
    bigplayer = pygame.transform.scale2x(player)
    return bigplayer

def proximity_magnitude(var1, min1, max1, min2, max2):
    """
    This function serves the same function as the map() function in processing.
    """
    var2 = min2+(max2-min2)*((var1-min1)/(max1-min1))
    return var2

def getNormalPoint(p, a, b):
    ap = PVector.staticSub(p, a)
    ab = PVector.staticSub(b, a)

    ab.normalize()
    ab.mult(ap.dot(ab))
    normal_point = PVector.staticAdd(a, ab)

    return normal_point

big_player = make_player_surface("player.png")

vehicle = Vehicle(big_player, 100, 200, 1)

many_vehicles = []
for i in range(5):
    many_vehicles.append(Vehicle(big_player, 100 + 30*i, 100 + 30*i, i+1))

mover = Mover(200,200)

flow = FlowField()

path = Path()

flock = Flock()
for i in range(20):
    b = Vehicle(big_player, random.randint(0,800),random.randint(0,800),1)
    flock.addBoid(b)

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

    flock.run()

    #path.display()
    #
    mouse = PVector(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])
    #
    # mover.update()
    # mover.display()
    # mover.checkEdges()

    # f = flow.lookup(vehicle)
    # f.mult(0.1)
    #
    # #vehicle.seek(mouse)
    # #vehicle.arrive(mouse)
    # vehicle.applyForce(f)
    # vehicle.pursuit(mover)
    # #vehicle.follow(path)
    # vehicle.update()
    # vehicle.direction()
    # vehicle.rotate()
    # vehicle.display()
    # vehicle.checkEdges()

    # score = PVector.staticSub(vehicle.location, mover.location)
    # distance = score.mag()
    # if distance < 3:
    #     done = True

    # for ship in many_vehicles:
    #     #s_force = flow.lookup(ship)
    #     #s_force.mult(0.1)
    #     #ship.seek(mouse)
    #
    #     #ship.applyForce(s_force)
    #     ship.pursuit(mover)
    #     #ship.cohesion(many_vehicles)
    #     #ship.seperate(many_vehicles)
    #     ship.flock(many_vehicles)
    #     ship.update()
    #     ship.direction()
    #     ship.rotate()
    #     ship.display()

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)

# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()

