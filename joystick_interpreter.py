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

def clip(x, minimum, maximum):
    if x < minimum:
        return minimum
    elif x > maximum:
        return maximum
    else: 
        return x
# list of MAPPINGS
#   Inputs are bounded between [-1, 1]
#   Outputs are bounded between [-1, 1]
MAPPINGS = [
    ('linear',      lambda x: clip(   x                           , -1, 1)),
    ('quadratic',   lambda x: clip(   math.copysign(x**2, x)      , -1, 1)), 
    ('log10',       lambda x: clip(   math.log10(4.95 * x + 5.05) , -1, 1))
]

# List of control modes
CONTROL_MODES = [
    'differential',
    'linear/angular'
]

# Dictionary of BUTTONS
BUTTONS = {
    'A'     : 0,
    'B'     : 1,
    'X'     : 2,
    'Y'     : 3,
    'LB'    : 4,
    'RB'    : 5,
    'SELECT': 6,
    'START' : 7,
    'HOME'  : 8,
    'LS'    : 9,
    'RS'    : 10
}

# Dictionary of Axis
AXES = {
    'LRL'   : 0,
    'LUD'   : 1,
    'LTR'   : 2,
    'RRL'   : 3,
    'RUD'   : 4,
    'RTR'   : 5
}

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

        # Maping is the mathmatical function mapping the inputs to the outputs
        self.mapping = 0

        # Dead zone is the region in which the input is considered zero
        self.dead_zone = 0.01

        # Control mode is how the user wants to drive the vehicle
        self.control_mode = 0

        # Init to zero wheel efforts
        self.left_wheel_effort = 0
        self.right_wheel_effort = 0

    def index_wrap(self, index, length):
        if index >= length:
            return 0
        elif index < 0:
            return length - 1
        else:
            return index


    def buttonDownEvent(self, event):
        button = event.button

        # Control mode
        if button == BUTTONS['SELECT'] :    # Decrement
            self.control_mode = self.index_wrap(self.control_mode - 1, len(CONTROL_MODES))
        elif button == BUTTONS['START'] :   # Increment
            self.control_mode = self.index_wrap(self.control_mode + 1, len(CONTROL_MODES))

        # Gear
        if button == BUTTONS['LB'] :    # Decrement
            self.gear = clip(self.gear - 0.1, 0.1, 1.0)
        elif button == BUTTONS['RB'] :   # Increment
            self.gear = clip(self.gear + 0.1, 0.1, 1.0)

        # Dead zone
        if button == BUTTONS['A'] :    # Decrement
            self.dead_zone = clip(self.dead_zone - 0.01, 0, 0.5)
        elif button == BUTTONS['B'] :   # Increment
            self.dead_zone = clip(self.dead_zone + 0.01, 0, 0.5)

        # Mapping
        if button == BUTTONS['X'] :    # Decrement
            self.mapping = self.index_wrap(self.mapping - 1, len(MAPPINGS))
        elif button == BUTTONS['Y'] :   # Increment
            self.mapping = self.index_wrap(self.mapping + 1, len(MAPPINGS))

    def mapAxis(self, axis):
        # Remove dead zone
        if abs(axis) < self.dead_zone:
            return 0

        # Scale the remaining numbers to the whole space
        data_range = 1 - self.dead_zone
        scaling_factor = 1 / data_range
        shifting_factor = self.dead_zone * scaling_factor
        axis = scaling_factor * axis + (-1 * axis / abs(axis)) * shifting_factor
        return MAPPINGS[self.mapping][1](-1 * axis)

    def axisEvent(self, event):
        # Not important if its a trigger
        axis = event.axis
        if axis == AXES['LTR'] or axis == AXES['RTR']:
            return

        # We don't care which axis actually trigered the event we will use all of the axis
        # Calculate wheel efforts based on control mode

        # Diferential
        if self.control_mode == CONTROL_MODES.index('differential'):
            self.left_wheel_effort = self.gear * self.mapAxis(self.joystick.get_axis(AXES['LUD']))
            self.right_wheel_effort = self.gear * self.mapAxis(self.joystick.get_axis(AXES['RUD']))


        elif self.control_mode == CONTROL_MODES.index('linear/angular'):
            pass


    def draw(self, screen):
        self.textPrinter.reset()
        self.textPrinter.printText(screen, "Joystick name: {}".format(self.joystick.get_name()) )
        self.textPrinter.printText(screen, "Gear: {}% max".format(self.gear * 100))
        self.textPrinter.printText(screen, "Mapping: {}".format(MAPPINGS[self.mapping][0]))
        self.textPrinter.printText(screen, "Dead zone: {}%".format(self.dead_zone * 100))
        self.textPrinter.printText(screen, "Control mode: {}".format(CONTROL_MODES[self.control_mode]))
        self.textPrinter.printText(screen, "Wheel efforts [LEFT, RIGHT]: [{}, {}]%".format(self.left_wheel_effort, self.right_wheel_effort))


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
                controller.buttonDownEvent(event)
            elif event.type == pygame.JOYBUTTONUP:
                print 'Joy button up'
                print event
            elif event.type == pygame.JOYAXISMOTION:
                controller.axisEvent(event)
            elif event.type == pygame.JOYBALLMOTION:
                print "Joy ball motion"
                print event
            elif event.type == pygame.JOYHATMOTION:
                print "Joy hat motion"
                print event

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