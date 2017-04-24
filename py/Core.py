"""Reahb core FSM."""

from direct.fsm.FSM import FSM
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import *
from game2_integration import BallInMazeDemo
from Menu_game import MainMenu
import time
import store_variable as st

class Xcore(FSM):
    """knows Menu, Scenario and Loading."""
    def __init__(self):
        FSM.__init__(self, "Core Game Control")

        self.defaultTransitions = {"Loading": ["Menu_game"],
                                   "Menu_game": ["Game1", "Game2", "Game3"],
                                   "Game1": ["Results"],
                                   "Game2": ["Results"],
                                   "Game3": ["Results"],
                                   "Results": ["Menu_game"]
                                   }

        self.request("Loading")
        # Optional, but prevents a warning message.
        # The scenario task chain gives us grouping option.
        # It might get replaced by an own task manager, by chance.
        base.taskMgr.setupTaskChain("scenario", frameBudget=-1)
        print 'hei_core'

    def enterLoading(self):
        print 'kkk'
        # TODO: put this into gui package and add a black background
        self.loading = OnscreenText(text="LOADING", pos=(0,0), scale=0.1,
                                    align=TextNode.ACenter, fg=(1, 1, 1, 1))
        base.graphicsEngine.renderFrame()
        base.graphicsEngine.renderFrame()
        #self.preloader.preloadFast()  # depends on the loading screen
        print 'hei enter'
        time.sleep(3)
        # This moment the software calls menu game of this game
        self.demand("Menu_game")

    def exitLoading(self):
        print 'llll'
        self.loading.destroy()
        del self.loading

    def enterMenu_game(self):
        print 'hi man'
        print 'test flag'
        print st.flag1
        MainMenu()
        #self.demand("Game1")
        pass

    def exitMenu_game(self):
        print 'kkk3'
        pass

    def enterGame1(self):
        BallInMazeDemo()
        global end_task
        end_task = 0
        #self.demand("Results")
        pass

    def exitGame1(self):
        print 'psiu'
        pass

    def enterGame2(self):
        print 'ttt'
        pass

    def exitGame2(self):
        print 'ttt2'
        pass

    def enterGame3(self):
        print 'ttt3'
        pass

    def exitGame3(self):
        print 'ttt4'
        pass

    def enterResults(self):
        print 'ttt5'
        pass

    def exitResults(self):
        print 'ttt6'
        pass

    def enterMenu(self, menu, *args):
        print menu
        self.menu = BallInMazeDemo()

    def exitMenu(self):
        print 'fuck1'
        del self.menu

    def game1(self, menu, *args):
        print 'jjj'
        #self.menu = MenuProxy(menu, *args)
        import gui
        self.menu = getattr(gui, menu)()

    def exitMenu(self):
        print 'zzz'
        self.menu.destroy()