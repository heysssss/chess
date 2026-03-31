# pyright: strict

##########
# to add #
##########

# decide if white or black using rng

###########
# imports #
###########

from __future__ import annotations
from model import ChessModel
from view import ChessView
from controller import ChessController

################
# running code #
################

if __name__ == "__main__":
    model = ChessModel()
    view = ChessView()
    controller = ChessController(model, view)
    controller.run()