
from src.service import core as cc
import time
import sys

"""
Screen to show user the results during exercise
"""


class Results:
    """
    This is a simple screen to show results and return to main page
    """

    def __init__(self):
        """
        Collect initial values
        """
        self.button_return = ""

    def show(self):
        """

        :return:
        """
        #self.button_return = DirectButton(text="Game3", command=self.quit, scale=0.1, pos=(0, 0, 0))
        #sys.exit(0)
        cc.Xcore().request("Menu_game")

    def cleanall(self):
        sys.exit(0)