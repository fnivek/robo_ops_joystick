#!/usr/bin/env python

import pygame

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
        textBitmap = self.font.render(textString, True, BLACK)
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
    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
    for joystick in joysticks:
        joystick.init()

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
        screen.fill(WHITE)
        textPrinter.reset()

        # For each joystick:
        for i in range(pygame.joystick.get_count()):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()
        
            textPrinter.printText(screen, "Joystick {}".format(i) )
            textPrinter.indent()
        
            # Get the name from the OS for the controller/joystick
            name = joystick.get_name()
            textPrinter.printText(screen, "Joystick name: {}".format(name) )
            
            # Usually axis run in pairs, up/down for one, and left/right for
            # the other.
            axes = joystick.get_numaxes()
            textPrinter.printText(screen, "Number of axes: {}".format(axes) )
            textPrinter.indent()
            
            for i in range( axes ):
                axis = joystick.get_axis( i )
                textPrinter.printText(screen, "Axis {} value: {:>6.3f}".format(i, axis) )
            textPrinter.unindent()
                
            buttons = joystick.get_numbuttons()
            textPrinter.printText(screen, "Number of buttons: {}".format(buttons) )
            textPrinter.indent()

            for i in range( buttons ):
                button = joystick.get_button( i )
                textPrinter.printText(screen, "Button {:>2} value: {}".format(i,button) )
            textPrinter.unindent()
                
            # Hat switch. All or nothing for direction, not like joysticks.
            # Value comes back in an array.
            hats = joystick.get_numhats()
            textPrinter.printText(screen, "Number of hats: {}".format(hats) )
            textPrinter.indent()

            for i in range( hats ):
                hat = joystick.get_hat( i )
                textPrinter.printText(screen, "Hat {} value: {}".format(i, str(hat)) )
            textPrinter.unindent()
            
            textPrinter.unindent()

        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
    
        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

        # Limit to 20 frames per second
        clock.tick(20)

    pygame.quit()

if __name__ == '__main__':
    main()