"""
Return path for main routin
"""
import os
import re

class PathGen:

    def __init__(self):
        self.music = "/files/sounds/325611__shadydave__my-love-piano-loop.mp3"
        self.music_effects = "/files/sounds/NFF-whoa-whoa.wav"
        self.model = "/files/models/test_basic"
        self.actor = "/files/models/actor1_mov"
        self.model_ball = "/files/models/ball"
        self.image = "/files/images/ok.png"
        self.image_sad = "/files/images/sad.png"

    def path_gen(self, actual_path):
        """
        :param actual_path: path where the file is running
        :return: path for files
        """
        list_paths = []
        files_path = re.sub("/src", "", actual_path)
        new_path1 = str(files_path) + "{}".format(self.music)
        new_path2 = str(files_path) + "{}".format(self.music_effects)
        new_path3 = str(files_path) + "{}".format(self.model)
        new_path4 = str(files_path) + "{}".format(self.actor)
        new_path5 = str(files_path) + "{}".format(self.model_ball)
        new_path6 = str(files_path) + "{}".format(self.image)
        new_path7 = str(files_path) + "{}".format(self.image_sad)

        list_paths.append(os.path.abspath(new_path1))
        list_paths.append(os.path.abspath(new_path2))
        list_paths.append(os.path.abspath(new_path3))
        list_paths.append(os.path.abspath(new_path4))
        list_paths.append(os.path.abspath(new_path5))
        list_paths.append(os.path.abspath(new_path6))
        list_paths.append(os.path.abspath(new_path7))

        return list_paths


class PathGenCalibration:

    def __init__(self):
        self.music = "/files/sounds/325611__shadydave__my-love-piano-loop.mp3"


    def path_gen_calibration(self, actual_path):
        """
        :param actual_path: path where the file is running
        :return: path for files
        """
        list_paths = []
        files_path = re.sub("/src", "", actual_path)
        new_path1 = str(files_path) + "{}".format(self.music)
        new_path2 = str(files_path) + "{}".format(self.music_effects)
        new_path3 = str(files_path) + "{}".format(self.model)
        new_path4 = str(files_path) + "{}".format(self.actor)
        new_path5 = str(files_path) + "{}".format(self.model_ball)
        new_path6 = str(files_path) + "{}".format(self.image)
        new_path7 = str(files_path) + "{}".format(self.image_sad)

        list_paths.append(os.path.abspath(new_path1))
        list_paths.append(os.path.abspath(new_path2))
        list_paths.append(os.path.abspath(new_path3))
        list_paths.append(os.path.abspath(new_path4))
        list_paths.append(os.path.abspath(new_path5))
        list_paths.append(os.path.abspath(new_path6))
        list_paths.append(os.path.abspath(new_path7))

        return list_paths