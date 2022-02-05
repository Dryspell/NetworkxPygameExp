import networkx as nx
import matplotlib.pyplot as plt
import pygame
#
# G = nx.complete_graph(5)
# G
#
# G = nx.petersen_graph()
# subax1 = plt.subplot(121)
# nx.draw(G, with_labels=True, font_weight='bold')
# subax2 = plt.subplot(122)
# nx.draw_shell(G, nlist=[range(5, 10), range(5)], with_labels=True, font_weight='bold')
# plt.show()
#
#
# def pypltDraw(G):
#     subax1 = plt.subplot(121)
#     nx.draw(G, with_labels=True, font_weight='bold')
#     plt.show()
#
# G = nx.grid_graph(dim=(5, 5))
# pypltDraw(G)

import pygame, sys
from pygame.locals import *

def main():
    pygame.init()
    clock = pygame.time.Clock()

    DISPLAY=pygame.display.set_mode((500,400),0,32)

    WHITE=(255,255,255)
    BLUE=(0,0,255)

    DISPLAY.fill(WHITE)

    pygame.draw.rect(DISPLAY,BLUE,(200,150,100,50))

    while True:
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()

main2()

def main2():
    # activate the pygame library
    # initiate pygame and give permission
    # to use pygame's functionality.
    pygame.init()

    # define the RGB value for white,
    #  green, blue colour .
    white = (255, 255, 255)
    green = (0, 255, 0)
    blue = (0, 0, 128)

    # assigning values to X and Y variable
    X = 400
    Y = 400

    # create the display surface object
    # of specific dimension..e(X, Y).
    display_surface = pygame.display.set_mode((X, Y))

    # set the pygame window name
    pygame.display.set_caption('Show Text')

    # create a font object.
    # 1st parameter is the font file
    # which is present in pygame.
    # 2nd parameter is size of the font
    font = pygame.font.Font('freesansbold.ttf', 32)

    # create a text surface object,
    # on which text is drawn on it.
    text = font.render('GeeksForGeeks', True, green, blue)

    # create a rectangular object for the
    # text surface object
    textRect = text.get_rect()

    # set the center of the rectangular object.
    textRect.center = (X // 2, Y // 2)

    # infinite loop
    while True:

        # completely fill the surface object
        # with white color
        display_surface.fill(white)

        # copying the text surface object
        # to the display surface object
        # at the center coordinate.
        display_surface.blit(text, textRect)

        # iterate over the list of Event objects
        # that was returned by pygame.event.get() method.
        for event in pygame.event.get():

            # if event object type is QUIT
            # then quitting the pygame
            # and program both.
            if event.type == pygame.QUIT:
                # deactivates the pygame library
                pygame.quit()

                # quit the program.
                quit()

            # Draws the surface object to the screen.
            pygame.display.update()