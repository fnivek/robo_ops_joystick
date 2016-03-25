#!/usr/bin/env python

import pygame
import math

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)

# This is a simple class that will help us print to the screen
# It has nothing to do with the joysticks, just outputing the
# information.
class TextPrint:
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 20)

    def printText(self, screen, textString):
        textBitmap = self.font.render(textString, True, WHITE)
        screen.blit(textBitmap, [self.x, self.y])
        self.y += self.line_height
        
    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15
        
    def indent(self):
        self.x += 10
        
    def unindent(self):
        self.x -= 10

def clip(x):
    if x < -1.0:
        return -1.0
    elif x > 1.0:
        return 1.0
    else: 
        return x
# list of mappings
#   Inputs are bounded between [-1, 1]
#   Outputs are bounded between [-1, 1]
mappings = [
    ('linear',      lambda x: clip(   x                           )),
    ('quadratic',   lambda x: clip(   math.copysign(x**2, x)      )), 
    ('log10',       lambda x: clip(   math.log10(4.95 * x + 5.05) ))
]

# List of control modes
control_modes = [
    'differential',
    'linear/angular'
]

# Class for representing a controller
class Controller:
    def __init__(self, joystick):
        self.joystick = joystick
        self.joystick.init()

        # Text writer
        self.textPrinter = TextPrint()

        # Gear is between 0.1 and 1.0
        #   It is represents the maximum output possible in percentage
        self.gear = 1.0

        # Maping is the mathmatical function maping the inputs to the outputs
        self.mapping = 0

        # Dead zone is the region in which the input is considered zero
        self.dead_zone = 0.01

        # Control mode is how the user wants to drive the vehicle
        self.control_mode = control_modes[0]

    def draw(self, screen):
        self.textPrinter.reset()
        self.textPrinter.printText(screen, "Joystick name: {}".format(self.joystick.get_name()) )
        self.textPrinter.printText(screen, "Gear: {}".format(self.gear))
        self.textPrinter.printText(screen, "Mapping: {}".format(mappings[self.mapping][0]))
        self.textPrinter.printText(screen, "Dead zone: {}".format(self.dead_zone))
        self.textPrinter.printText(screen, "Control mode: {}".format(self.control_mode))


def main():
    # Init pygame
    pygame.init()

    size = [650, 480]
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Robo Ops joystick interface")
    running = True
    clock = pygame.time.Clock()

    # Initilize joysticks
    pygame.joystick.init()
    if pygame.joystick.get_count() == 0:
        print "No joystick detected please plug one in and try again"
        return

    
    # Init a controller
    controller = Controller(pygame.joystick.Joystick(0))        # TODO: cmd line arg for device

    # Get a text printer
    textPrinter = TextPrint()

    # main loop
    while running:
        # Process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            elif event.type == pygame.JOYBUTTONDOWN:
                print 'Joy button down'
            elif event.type == pygame.JOYBUTTONUP:
                print 'Joy button up'
            elif event.type == pygame.JOYAXISMOTION:
                print "Joy axis motion"
            elif event.type == pygame.JOYBALLMOTION:
                print "Joy ball motion"
            elif event.type == pygame.JOYHATMOTION:
                print "Joy hat motion"

        # DRAWING STEP
        # First, clear the screen to white. Don't put other drawing commands
        # above this, or they will be erased with this command.
        screen.fill(BLACK)
        textPrinter.reset()

        controller.draw(screen)

        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
    
        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

        # Limit to 20 frames per second
        clock.tick(20)

    pygame.quit()

if __name__ == '__main__':
    main()