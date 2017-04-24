from panda3d.core import *
from pandac.PandaModules import loadPrcFile, loadPrcFileData
from direct.showbase.ShowBase import ShowBase

import sys


from panda3d.core import *
from direct.fsm.FSM import FSM
from direct.gui.DirectGui import *
from game2_integration import BallInMazeDemo
import store_variable
# import files of game

from game2 import BallInMazeDemo


class MainMenu:

    def __init__(self):
        print 'test menu'
        self.enterMain()

    def enterMain(self):
        self.button = DirectButton(text="Game1", command=self.quit, scale=0.1, pos=(-1, 0, 0))
        self.button1 = DirectButton(text="Game2", command=self.quit, scale=0.1, pos=(-0.5, 0, 0))
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



if __name__=="__main__":

   class myapp(ShowBase):


      def __init__(self):

           # Initialize the ShowBase class from which we inherit, which will
           # create a window and set up everything we need for rendering into it.
           ShowBase.__init__(self)

           # This code puts the standard title and instruction text on screen
           self.title = \
               OnscreenText(text="Game1: Sensor acquisition - Collision Detection",
                            parent=base.a2dBottomRight, align=TextNode.ARight,
                            fg=(1, 1, 1, 1), pos=(-0.1, 0.1), scale=.08,
                            shadow=(0, 0, 0, 0.5))
           self.instructions = \
               OnscreenText(text="Sensor tilts the board",
                            parent=base.a2dTopLeft, align=TextNode.ALeft,
                            pos=(0.05, -0.08), fg=(1, 1, 1, 1), scale=.06,
                            shadow=(0, 0, 0, 0.5))

           self.accept("escape", sys.exit)  # Escape quits

           # Disable default mouse-based camera control.  This is a method on the
           # ShowBase class from which we inherit.
           self.disableMouse()
           self.maingame = BallInMazeDemo().base_calc()

           def callback(self, request):
               if request == "quit":
                  self.mainMenu.cleanup()
                  sys.exit()
   app = myapp()
   app.run()