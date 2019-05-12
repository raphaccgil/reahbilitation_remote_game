"""Reahb core FSM."""

from direct.fsm.FSM import FSM
from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import *
from main.business import Menu_game, game2_integration, calibration
import time
from main.business.calibration import Calibration


class Xcore(FSM):
    """knows Menu, Scenario and Loading."""
    """knows Menu, Scenario and Loading."""
    def __init__(self):
        FSM.__init__(self, "Core Game Control")


        self.defaultTransitions = {"Loading": ["Menu_game"],
                                   "Menu_game": ["Game1", "Game2", "Game3", "Credits", "Calibration"],
                                   "Credits": ["Menu_game"],
                                   "Game1": ["Results"],
                                   "Game2": ["Results"],
                                   "Game3": ["Results"],
                                   "Results": ["Menu_game"],
                                   "Calibration": ["Menu_game"]
                                   }

        # Optional, but prevents a warning message.
        # The scenario task chain gives us grouping option.
        # It might get replaced by an own task manager, by chance.
        base.taskMgr.setupTaskChain("scenario", frameBudget=-1)
        print ('hei_core')

    def enterLoading(self):
        print ('kkk')
        # TODO: put this into gui package and add a black background
        self.loading = OnscreenText(text="LOADING", pos=(0,0), scale=0.1,
                                    align=TextNode.ACenter, fg=(1, 1, 1, 1))
        base.graphicsEngine.renderFrame()
        base.graphicsEngine.renderFrame()
        #self.preloader.preloadFast()  # depends on the loading screen
        time.sleep(3)
        # This moment the software calls menu game of this game
        self.demand("Menu_game")

    def exitLoading(self):
        print ('llll')
        self.loading.destroy()

    def enterMenu_game(self):
        print ('Menu FSM')
        menu = Menu_game.MainMenu(Calibration)
        menu.enterMain(Calibration)
        #self.demand("Game1")
        pass

    def exitMenu_game(self):
        print ('exit Menu')
        pass

    def enterGame1(self):
        # here is the moment to insert the time
        game2_integration.BallInMazeDemo(1)
        print ('enter Game1')

    def exitGame1(self):
        print ('exit Game1')

    def enterGame2(self):
        print ('ttt')

    def exitGame2(self):
        print ('ttt2')

    def enterGame3(self):
        print ('ttt3')

    def exitGame3(self):
        print ('ttt4')

    def enterCalibration(self):
        print ('lets calibrate')
        calibration.Calibration().enterMain()

    def exitCalibration(self):
        print ('bye calibrate')
        #calibration.Calibration()


    def enterResults(self):
        print ('ttt5')

    def exitResults(self):
        print ('ttt6')
