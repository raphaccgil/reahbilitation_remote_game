"""
Created on Tue June 20 21:00:00 2016
@author: Raphael Gil
Revision: 0.2
Creation of a game interface
R0.1 - Initial Version

R0.2 - Adaptation for:
* Python 3
* Remove Kinect
* Universal module (could be used in Any S))
"""

from direct.showbase.ShowBase import ShowBase
from src.service.menu_game import MainMenu
from src.service.core import Xcore
from panda3d.core import *
from src.business.calibration import Calibration
from src.util.dirpath_gen import PathGenMain
import os


class Azure(ShowBase):
    """
    Reahb main file. This module handles a few command line
    options and starts the core finite state machine, followed by Panda's task
    manager.
    """

    def __init__(self):
        """
        Program entry point.
        """

        # call standard config
        path_now = os.path.dirname(os.getcwd())
        self.files_path_main = PathGenMain().path_gen_menu(path_now)
        loadPrcFile(self.files_path_main[0])

        # This basically sets up our rendering node-tree, some builtins and
        # the master loop (which iterates each frame).
        ShowBase.__init__(self)

        # Turn off Panda3D's standard camera handling.
        self.disableMouse()
        #self.setBackgroundColor(0.2, 0.2, 0.2)
        self.setBackgroundColor(0, 0, 0)

        # Start our Core Finite State Machine
        self.core = Xcore()
        self.core.request("Loading")

        self.main = MainMenu(Calibration)

        # Define transitions
        self.run()


if __name__ == "__main__":
    Azure()

