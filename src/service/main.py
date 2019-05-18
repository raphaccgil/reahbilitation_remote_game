''' Created on Tue June 20 21:00:00 2016
@author: Raphael Gil
Revision: 0.2
Creation of a game interface
R0.1 - Initial Version

R0.2 - Adaptation for:
* Python 3
* Remove Kinect
* Universal module (could be used in Any S))

'''

"""Reahb main file. This module handles a few command line
options and starts the core finite state machine, followed by Panda's task
manager."""

from direct.showbase.ShowBase import ShowBase
from src.service.menu_game import MainMenu
from src.service.core import Xcore
from src.util import store_variable as st
from panda3d.core import *
from src.business.calibration import Calibration
from src.util.dirpath_gen import PathGenMain
import os

class Azure(ShowBase):

    def __init__(self):
        """Program entry point."""

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
        # change state is here?
        print('check flag here')
        print(st.flag1)

        self.main = MainMenu(Calibration)

        # Define transitions
        self.run()
'''
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
        time.sleep(3)
        # This moment the software calls menu game of this game
        self.demand("Menu_game")

    def exitLoading(self):
        print 'llll'
        self.loading.destroy()

    def enterMenu_game(self):
        print 'Menu FSM'
        menu = MainMenu()
        menu.enterMain()
        #self.demand("Game1")
        pass

    def exitMenu_game(self):
        print 'exit Menu'
        pass

    def enterGame1(self):
        print 'enter Game1'

    def exitGame1(self):
        print 'exit Game1'

    def enterGame2(self):
        print 'ttt'

    def exitGame2(self):
        print 'ttt2'

    def enterGame3(self):
        print 'ttt3'

    def exitGame3(self):
        print 'ttt4'

    def enterResults(self):
        print 'ttt5'

    def exitResults(self):
        print 'ttt6'

    #def enterMenu(self, menu, *args):
    #    print menu
    #    self.menu = BallInMazeDemo()

    #def exitMenu(self):
    #    print 'fuck1'
    #    del self.menu

    #def game1(self, menu, *args):
    #    print 'jjj'
    #    import gui
    #    self.menu = getattr(gui, menu)()

    #def exitMenu(self):
    #    print 'zzz'
    #    self.menu.destroy()

    def trans1(self):
        print 'check'

class MainMenu:

    def __init__(self):
        print 'test menu'

        #self.pass_tr.request('Menu_game')

    def enterMain(self):
        self.button = DirectButton(text="Game1", command=self.test, scale=0.1, pos=(-1, 0, 0))
        self.button1 = DirectButton(text="Game2", command=self.test, scale=0.1, pos=(-0.5, 0, 0))
        self.button2 = DirectButton(text="Game3", command=self.quit, scale=0.1, pos=(0, 0, 0))
        self.button3 = DirectButton(text="Credits", command=self.quit, scale=0.1, pos=(0.5, 0, 0))
        self.button4 = DirectButton(text="Quit", command=self.quit, scale=0.1, pos=(1.0, 0, 0))
        self.button5 = DirectButton(text="Sensor Calibration", command=self.quit, scale=0.1, pos=(0, 0, -0.3))
        self.title = OnscreenText(text="Reahbilitation Game: Sensor acquisition", parent=base.a2dBottomRight,
                                 align=TextNode.ARight,fg=(1, 1, 1, 1), pos=(-0.1, 0.1),
                                 scale=.06,shadow=(0, 0, 0, 0.5))
        self.instructions = \
               OnscreenText(text="Game for reahbilitation",
                            parent=base.a2dTopLeft, align=TextNode.ALeft,
                            pos=(0.05, -0.08), fg=(1, 1, 1, 1), scale=.06,
                            shadow=(0, 0, 0, 0.5))
        self.game_version = \
               OnscreenText(text="Version 0.1",
                            parent=base.a2dBottomLeft, align=TextNode.ALeft,
                            pos=(0.0, 0.1), fg=(1, 1, 1, 1), scale=.05,
                            shadow=(0, 0, 0, 0.5))

        #self.accept("escape", sys.exit)  # Escape quits

    def enterMain2(self):
        self.button = DirectButton(text="Call Game", scale=0.05, pos=(0.5,0,0))
        self.request

    def exitMain(self):
        print "exit called"
        self.button.destroy()

    def quit(self):
       print "quit clicked"
       self.appCallback("quit")

    def test(self):
       print "test clicked"
       self.button.destroy()
       self.button1.destroy()
       self.button2.destroy()
       self.button3.destroy()
       self.button4.destroy()
       self.button5.destroy()
       self.title.destroy()
       self.instructions.destroy()
       self.game_version.destroy()
       Xcore("Core Game Control").request('Game1')
'''

if __name__ == "__main__":
    Azure()
    # Related to relative paths.
    #print "Don't run this module directly! Use the run script instead!"
    #sys.exit(2)

