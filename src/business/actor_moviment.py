#!/usr/bin/env python

"""
 Author: Raphael Castilho Gil
 Last Updated: 2019-05-18

 This is the movimentation of actor depending of teh game
"""
import datetime
from src.service.body_support_game import Game1Mov


class ActorMov1:
    """
    According selected game, choose move
    """
    def __int__(self):
        self.time_exerc_past = ''
        self.time_exerc_now = ''

    def game1(self, past_time, legs_change, leg_angle1, leg_angle2,
              text_advice, time_change):
        """
        Control the position of legs during the game
        :param past_time: Last reg time
        :return:
        """
        self.time_exerc_past = past_time
        self.time_exerc_now = datetime.datetime.now()

        diff_time = self.time_exerc_now - self.time_exerc_past
        diff_time = float(diff_time.microseconds) / 1000000

        if legs_change == 0:
            values = Game1Mov(). \
                legs_movimentation_pos0_3(legs_change,
                                          leg_angle1)
            legs_change = values[0]
            leg_angle1 = values[1]
            text_advice.setText("Levante a perna esquerda...")

        elif legs_change == 1 or \
                legs_change == 4:
            values = Game1Mov(). \
                legs_wait_pos2_4(legs_change,
                                 time_change,
                                 diff_time)

            time_change = values[0]
            legs_change = values[1]
            text_advice.setText("Segure a perna levantada...")


        elif legs_change == 2:
            values = Game1Mov(). \
                legs_movimentation_pos0_3(legs_change, leg_angle1)
            legs_change = values[0]
            leg_angle1 = values[1]
            text_advice.setText("Troque a perna...")


        elif legs_change == 3:
            values = Game1Mov(). \
                legs_movimentation_pos0_3(legs_change, leg_angle2)
            legs_change = values[0]
            leg_angle2 = values[1]
            text_advice.setText("Levante a perna direita...")

        elif legs_change == 5:
            values = Game1Mov(). \
                legs_movimentation_pos0_3(legs_change, leg_angle2)
            legs_change = values[0]
            leg_angle2 = values[1]
            text_advice.setText("Troque a perna...")

        return [self.time_exerc_now,
                legs_change,
                leg_angle1,
                leg_angle2,
                text_advice,
                time_change]