__author__ = 'Topper121'

import pygame

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


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
    x += xspeed
    y += yspeed

    if x+16 > width or x-16 < 0:
        xspeed *= -1
    if y+16 > height or y-16 < 0:
        yspeed *= -1

    # --- Drawing code should go here

    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(WHITE)

    pygame.draw.circle(screen, RED, (x, y), 16)

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)

# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()