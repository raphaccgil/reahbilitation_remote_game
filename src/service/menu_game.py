from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from direct.gui.DirectGui import *
from src.service import core as cc
from trash.game2 import BallInMazeDemo
import sys
from src.business.calibration import Calibration
from src.util.dirpath_gen import PathGenMenu
import os


class MainMenu(Calibration):
    """
    Menu for Calibration
    """

    def __init__(self, Calibration):
        """

        :param Calibration:
        """
        Calibration.__init__(self)
        print('test menu')

    def enterMain(self, Calibration):
        """

        :param Calibration:
        :return:
        """
        path_now = os.path.dirname(os.getcwd())
        self.files_path_menu = PathGenMenu().path_gen_menu(path_now)
        self.sound_back = base.loader.loadSfx(self.files_path_menu[0])
        self.sound_back.setVolume(0.02)
        self.sound_back.setLoop(True)
        self.sound_back.play()
        self.button = DirectButton(text="Game1", command=self.test, scale=0.1, pos=(-1, 0, 0))
        self.button1 = DirectButton(text="Game2", command=self.test, scale=0.1, pos=(-0.5, 0, 0))
        self.button2 = DirectButton(text="Game3", command=self.quit, scale=0.1, pos=(0, 0, 0))
        self.button3 = DirectButton(text="Credits", command=self.quit, scale=0.1, pos=(0.5, 0, 0))
        self.button4 = DirectButton(text="Quit", command=self.quit, scale=0.1, pos=(1.0, 0, 0))
        self.button5 = DirectButton(text="Sensor Calibration", command=self.cal_rot, scale=0.1, pos=(0, 0, -0.3))
        self.title = OnscreenText(text="Reahbilitation Game: Sensor acquisition", parent=base.a2dBottomRight,
                                 align=TextNode.ARight,fg=(1, 1, 1, 1), pos=(-0.1, 0.1),
                                 scale=.06,shadow=(0, 0, 0, 0.5))
        self.instructions = \
               OnscreenText(text="Game for reahbilitation",
                            parent=base.a2dTopLeft, align=TextNode.ALeft,
                            pos=(0.05, -0.08), fg=(1, 1, 1, 1), scale=.06,
                            shadow=(0, 0, 0, 0.5))
        self.game_version = \
               OnscreenText(text="Version 0.3",
                            parent=base.a2dBottomLeft, align=TextNode.ALeft,
                            pos=(0.0, 0.1), fg=(1, 1, 1, 1), scale=.05,
                            shadow=(0, 0, 0, 0.5))
        if hasattr(Calibration, 'calhead'):
            print('verify')
            print(Calibration.calhead)

        #self.accept("escape", sys.exit)  # Escape quits

    def exitMain(self):
        print("exit called")
        self.button.destroy()

    def quit(self):
       print("Leaving the system")
       sys.exit()

    def test(self):
        print("test clicked")
        self.sound_back.stop()
        self.button.destroy()
        self.button1.destroy()
        self.button2.destroy()
        self.button3.destroy()
        self.button4.destroy()
        self.button5.destroy()
        self.title.destroy()
        self.instructions.destroy()
        self.game_version.destroy()
        cc.Xcore().request("Game1")

    def cal_rot(self):
        print('call calibration')
        self.sound_back.stop()
        self.button.destroy()
        self.button1.destroy()
        self.button2.destroy()
        self.button3.destroy()
        self.button4.destroy()
        self.button5.destroy()
        self.title.destroy()
        self.instructions.destroy()
        self.game_version.destroy()
        cc.Xcore().request("Calibration")

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