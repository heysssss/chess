# pyright: strict

##########
# to add #
##########

# decide if white or black using rng

###########
# imports #
###########

from __future__ import annotations

import pygame

from model import ChessModel
from view import ChessView
from controller import ChessController

################
# running code #
################

if __name__ == "__main__":

    #####################
    # initialize pygame #
    #####################
    pygame.init()

    # window size
    WIDTH = 600
    ROWS = 8
    TILE_SIZE = WIDTH // ROWS

    screen = pygame.display.set_mode((WIDTH, WIDTH))
    pygame.display.set_caption("Chess")

    clock = pygame.time.Clock()

    ####################
    # MVC architecture #
    ####################

    model = ChessModel()
    view = ChessView(screen)
    controller = ChessController(model, view)
    
    controller.run()