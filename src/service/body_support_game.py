"""
Animation during games
"""

class Game1Mov:

    """
    Pos 0: Change left leg
    Pos 1: Wait to return
    Pos 2: Return original position
    Pos 3: Change right leg
    Pos 4: Wait to return
    Pos 5: Return to original position
    """

    def legs_movimentation_pos0_3(self, flag_leg, leg_change):
        """
        Change the left or right leg
        :param flag:
        :return:
        """
        if flag_leg == 0 or flag_leg == 3:
            leg_change += 1
            if leg_change >= 90:
                flag_leg += 1
                leg_change = 90
        else:
            leg_change -= 1
            if leg_change <= 0:
                flag_leg += 1
                leg_change = 0

        if flag_leg == 6:
            flag_leg = 0

        list_values = [flag_leg, leg_change]

        return list_values

    def legs_wait_pos2_4(self, flag_leg, time_check, value_diff):

        """
        :param flag_leg: Position of leg
        :param time_check: Verification of time necessary
        :param value_diff: Time already used
        :return: value of time and position of leg
        """
        new_time = time_check - value_diff

        if new_time < 0:
            flag_leg += 1
            new_time = 10

        list_values = [new_time, flag_leg]

        return list_values