"""Reahb core FSM."""

from direct.fsm.FSM import FSM
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import *
from src.business import calibration, game1
from src.service import menu_game
import time
from src.business.calibration import Calibration
from src.util.check_conn import CheckConn
from src.util.local_db import LocalDb, CheckDb
import sys
import os
import re


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
        print('hei_core')

        self.files_path_core = ""

    def enterLoading(self):
        """
        In this moment, verify if has internet connection and try to send
        data to server
        :return:
        """
        # TODO: put this into gui package and add a black background
        self.loading = OnscreenText(text="LOADING", pos=(0,0.2), scale=0.1,
                                    align=TextNode.ACenter, fg=(1, 1, 1, 1))

        self.text = TextNode('TestConnection')
        self.text.setText("Verificando conexão internet...")
        self.textNodePath = aspect2d.attachNewNode(self.text)
        self.textNodePath.setScale(0.07)
        self.text.setAlign(TextNode.ACenter)

        base.graphicsEngine.renderFrame()
        base.graphicsEngine.renderFrame()
        #self.preloader.preloadFast()  # depends on the loading screen
        time.sleep(2)
        status = CheckConn().internet_on()

        path_now = os.path.dirname(os.getcwd())
        files_path_core = re.sub("/src", "", path_now)

        conn_temp_database = LocalDb()
        conn_temp_database.conn_db(files_path_core)
        conn_temp_database.create_db()
        conn_temp_database.conn_db(files_path_core)
        conn_temp_database.create_tbl_calibration()

        conn_temp_database.conn_db(files_path_core)
        results_local = conn_temp_database.verify_data()
        print(status)
        if status is True:
            self.text.setText("Conexão com Internet, verificando dados armazenados...")
            base.graphicsEngine.renderFrame()
            base.graphicsEngine.renderFrame()
            time.sleep(2)
            #ping base local e se tiver já envia
            CheckDb().check_conn()
            if results_local == 0:
                self.text.setText("Sem dados armazenados, iniciando jogo...")
                base.graphicsEngine.renderFrame()
                base.graphicsEngine.renderFrame()
                time.sleep(2)
            elif results_local == 1:
                self.text.setText("Existe dados armazenados, enviando dados...")
                base.graphicsEngine.renderFrame()
                base.graphicsEngine.renderFrame()
                time.sleep(2)
            else:
                sys.exit(1)
        else:
            self.text.setText("Sem Internet, carregando jogo em offline")
            base.graphicsEngine.renderFrame()
            base.graphicsEngine.renderFrame()
            #ping base local e se tiver já envia
            time.sleep(2)
        # This moment the software calls menu game of this game
        self.demand("Menu_game")

    def exitLoading(self):
        self.loading.destroy()
        self.textNodePath.removeNode()

    def enterMenu_game(self):
        menu = menu_game.MainMenu(Calibration)
        menu.enterMain(Calibration)
        #self.demand("Game1")
        pass

    def exitMenu_game(self):
        print('exit Menu')
        pass

    def enterGame1(self):
        # here is the moment to insert the time
        game1.BallInMazeDemo(1)

    def exitGame1(self):
        print('exit Game1')

    def enterGame2(self):
        print('ttt')

    def exitGame2(self):
        print('ttt2')

    def enterGame3(self):
        print('ttt3')

    def exitGame3(self):
        print('ttt4')

    def enterCalibration(self):
        print('lets calibrate')
        calibration.Calibration().enterMain()

    def exitCalibration(self):
        print('bye calibrate')
        #calibration.Calibration()


    def enterResults(self):
        print('ttt5')

    def exitResults(self):
        print ('ttt6')
