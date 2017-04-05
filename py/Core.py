"""Reahb core FSM."""

from direct.fsm.FSM import FSM
from direct.gui.OnscreenText import OnscreenText
from pandac.PandaModules import TextNode

from panda3d.core import *
from preloader import scenarioPreloader
from game2_integration import BallInMazeDemo


class Core(FSM):
    """knows Menu, Scenario and Loading."""
    def __init__(self):
        FSM.__init__(self, "Core Game Control")

        self.defaultTransitions = {"Menu_game": ["Game1", "Game2", "Game3"],
                                   "Game1": ["Results"],
                                   "Game2": ["Results"],
                                   "Game3": ["Results"],
                                   "Results": ["Menu_game"]
                                   }
        # Optional, but prevents a warning message.
        # The scenario task chain gives us grouping option.
        # It might get replaced by an own task manager, by chance.
        base.taskMgr.setupTaskChain("scenario", frameBudget=-1)
        print 'hei_core'

    def enterLoading(self, scenario):
        # TODO: put this into gui package and add a black background
        self.loading = OnscreenText(text="LOADING", pos=(0,0), scale=0.1,
                               align=TextNode.ACenter, fg=(1,1,1,1))
        self.preloader = scenarioPreloader(scenario)
        base.graphicsEngine.renderFrame()
        base.graphicsEngine.renderFrame()
        self.preloader.preloadFast()  # depends on the loading screen
        print 'hei enter'
        # Other preloader methods would specify a callback that calls
        # self.demand(scenario), but preloadFast() is executed in one frame, so
        # we can safely demand that from here. Interactive loading screens
        # might require special handling.
        self.demand("Scenario", scenario)

    def exitLoading(self):
        self.loading.destroy()
        del self.loading
        del self.preloader

    #def enterScenario(self, scenario):
    #    self.scenario = ScenarioProxy(scenario)
    #    self.scenario.begin()

    #def exitScenario(self):
    #    self.scenario.destroy()
    #    del self.scenario

    def enterMenu(self, menu, *args):
        print 'ops'
        self.menu = BallInMazeDemo()

    def exitMenu(self):
        del self.menu

    def game1(self, menu, *args):
        #self.menu = MenuProxy(menu, *args)
        import gui
        self.menu = getattr(gui, menu)()

    def exitMenu(self):
        self.menu.destroy()