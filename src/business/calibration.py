"""
Calibration file
"""

import os
import re
import socket
import numpy as np
import datetime
from panda3d.core import *
from direct.gui.DirectGui import *
from direct.task.Task import Task
from src.service import core as cc
from src.util.fusion import Fusion
from src.util.dirpath_gen import PathGenCalibration
from src.util.local_db import LocalDb
from src.util.check_conn_quality import CheckConnQuality
from src.util.check_conn import CheckConn


class Calibration:

    def __init__(self):
        print('test calibration')
        self.status_acquis = 0
        self.buffer = 0
        self.checktime = 0
        self.flagtime = 0
        self.now_t = 0
        self.last_t = 0
        self.notactivate = 0
        self.caldone = 0
        self.onlyonetime = 0
        self.calhead = 0
        self.calpitch = 0
        self.calroll = 0
        self.files_path = ""
        self.sound_back = ""
        self.button = ""
        self.button2 = ""
        self.button3 = ""
        self.title = ""
        self.instructions = ""
        self.game_version = ""

        # create UDP connection for cellphone
        self.UDP_IP = ""
        self.UDP_PORT = 2055
        self.sock = ""
        self.acquir_data = ""
        self.mainLoop = ""

        self.acq_list = [[], [], []]

        self.check_ping = 0

    def ret_variables(self):
        """
        Return variables called
        :return:
        """
        return self.calhead, self.calpitch, self.calroll

    def enterMain(self):
        """
        Start screen for calibration
        :return:
        """
        path_now = os.path.dirname(os.getcwd())
        self.files_path = PathGenCalibration().path_gen_calibration(path_now)

        self.sound_back = base.loader.loadSfx(self.files_path[0])
        self.sound_back.setVolume(0.02)
        self.sound_back.setLoop(True)
        self.sound_back.play()
        self.button = DirectButton(text="Start acquisition", command=self.cal_rot, scale=0.1, pos=(-1, 0, 0))
        self.button2 = DirectButton(text="Stop acquisition", command=self.cal_rot_stop, scale=0.1, pos=(-1, 0.0, -0.2))
        self.button3 = DirectButton(text="Return", command=self.nostop, scale=0.1, pos=(-1, 0.0, -0.4))
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

    def cal_rot(self):
        # start acquisition from cell phone
        # the cell phone is going to have a fixed Ip sending
        taskMgr.remove("accel_acquire")
        taskMgr.remove("speed_test")

        self.sock = socket.socket(socket.AF_INET,
                     socket.SOCK_DGRAM)
        self.sock.bind((self.UDP_IP, self.UDP_PORT))
        self.acquir_data = Fusion()
        taskMgr.setupTaskChain('chain5', numThreads=1, threadPriority=TPHigh, frameSync=False)
        taskMgr.setupTaskChain('chain6', numThreads=1, threadPriority=TPHigh, frameSync=False)
        taskMgr.add(self.roll_acquire_task, "accel_acquire", taskChain='chain5', uponDeath=self.cleanall)
        taskMgr.add(self.speed_test_task, "speed_test", taskChain='chain6')

        #taskMgr.add(self.speed_test_task, "speed_test")

    def cleanall(self,task):
        taskMgr.remove("accel_acquire")
        taskMgr.remove("speed_test")
        self.sound_back.stop()
        self.texthead.destroy()
        self.textpitch.destroy()
        self.textroll.destroy()
        self.button.destroy()
        self.button2.destroy()
        self.button3.destroy()
        self.sock.close()
        self.instructions.destroy()
        self.game_version.destroy()
        self.title.destroy()
        self.cal.destroy()
        cc.Xcore().request("Menu_game")

    def cal_rot_stop(self):
        taskMgr.remove("accel_acquire")
        taskMgr.remove("speed_test")
        if hasattr(self, 'texthead'):
            self.texthead.destroy()
            self.textpitch.destroy()
            self.textroll.destroy()
        if hasattr(self, 'calheadtxt'):
            self.cal.destroy()
            self.calheadtxt.destroy()
            self.calpitchtxt.destroy()
            self.calrolltxt.destroy()
        self.onlyonetime = 0
        self.buffer = 0

    def nostop(self):
        self.button.destroy()
        self.button2.destroy()
        self.button3.destroy()
        self.sound_back.stop()
        self.texthead.destroy()
        self.textpitch.destroy()
        self.textroll.destroy()
        self.button.destroy()
        self.button2.destroy()
        self.button3.destroy()
        self.cal.destroy()
        self.notactivate = 1

        cc.Xcore().request("Menu_game")

    def speed_test_task(self, task):
        print('Rodando')
        status = CheckConn().internet_on()
        check_conn = CheckConnQuality().internet_quality()

        if self.check_ping == 0:
            if status is True:
                ping = check_conn[0]
                down = check_conn[1]
                upl = check_conn[2]
            else:
                ping = 0.0
                down = 0.0
                upl = 9999.9999

        date_ping = datetime.datetime.now()

        path_now = os.path.dirname(os.getcwd())
        files_path_calibration = re.sub("/src", "", path_now)

        buff_list = [date_ping, float(down), float(upl), float(ping)]
        buff_median = LocalDb()
        buff_median.conn_db(files_path_calibration)
        buff_median.insert_tbl_conn_speed(buff_list)

        self.check_ping = 1

        return Task.cont

    def roll_acquire_task(self, task):
        self.now = datetime.datetime.now()
        dt = globalClock.getDt()
        self.buffer += dt
        data, addr = self.sock.recvfrom(1024)
        print(data)
        date_time, accx, accy, accz, magx, magy, magz, gyrx, gyry, gyrz,  = re.split(',', data.decode('utf-8'))
        gyrz = str(gyrz)
        gyrz = float(gyrz.replace("#", ""))
        self.acc = (float(accx), float(accy), float(accz))
        self.mag = (float(magx), float(magy), float(magz))
        self.gyr = (float(gyrx), float(gyry), float(gyrz))
        if self.flagtime == 0:
            print('diff time == 0')
            self.acquir_data.update(self.acc, self.gyr, self.mag, 0)
        else:
            self.now_t = date_time
            diff = int(self.now_t) - int(self.last_t)
            diff *= 1000
            print('diff time == {}'.format(str(diff)))
            self.acquir_data.update(self.acc, self.gyr, self.mag, float(diff))
        self.last_t = date_time
        if hasattr(self, 'texthead'):
            self.texthead.destroy()
            self.textpitch.destroy()
            self.textroll.destroy()
        if hasattr(self, 'calheadtxt'):
            self.calheadtxt.destroy()
            self.calpitchtxt.destroy()
            self.calrolltxt.destroy()

            # Standard technique for finding the amount of time since the last
            # frame - this technique shows up the frames per second
        self.dt = globalClock.getDt()
        # start acqusition after stabilization

        if hasattr(self, 'cal'):
            self.cal.destroy()
        if self.buffer < 20:
            reg = str(round(self.buffer*100/20))
            self.cal = \
                OnscreenText(text="Esperando para calibrar {}%".format(reg),
                             parent=base.a2dBottomRight, align=TextNode.ARight,
                             fg=(1, 1, 1, 1), pos=(-0.7, 1.1), scale=.08,
                             shadow=(0, 0, 0, 0.5))
        elif self.check_ping == 0:
            self.cal = \
                OnscreenText(text="Esperando o teste de conexão",
                             parent=base.a2dBottomRight, align=TextNode.ARight,
                             fg=(1, 1, 1, 1), pos=(-0.7, 1.1), scale=.08,
                             shadow=(0, 0, 0, 0.5))
        else:
            self.cal = \
                OnscreenText(text="Calibração e conexão ok",
                             parent=base.a2dBottomRight, align=TextNode.ARight,
                             fg=(1, 1, 1, 1), pos=(-0.7, 1.1), scale=.08,
                             shadow=(0, 0, 0, 0.5))
        if self.buffer > 10:
            self.acq_list[0].append(self.acquir_data.heading)
            self.acq_list[1].append(self.acquir_data.pitch)
            self.acq_list[2].append(self.acquir_data.roll)
        else:
            pass
        if self.notactivate == 0:
            self.texthead = \
                   OnscreenText(text="Heading: {:7.3f}".format(self.acquir_data.heading),
                                parent=base.a2dBottomRight, align=TextNode.ARight,
                                fg=(1, 1, 1, 1), pos=(-0.1, 0.3), scale=.08,
                                shadow=(0, 0, 0, 0.5))
            self.textpitch =\
                    OnscreenText(text="Pitch: {:7.3f}".format(self.acquir_data.pitch),
                                parent=base.a2dBottomRight, align=TextNode.ARight,
                                fg=(1, 1, 1, 1), pos=(-0.1, 0.5), scale=.08,
                                shadow=(0, 0, 0, 0.5))
            self.textroll =\
            OnscreenText(text="Roll: {:7.3f}".format(self.acquir_data.roll),
                        parent=base.a2dBottomRight, align=TextNode.ARight,
                        fg=(1, 1, 1, 1), pos=(-0.1, 0.7), scale=.08,
                        shadow=(0, 0, 0, 0.5))
        else:
            pass
        if self.buffer > 20 and self.onlyonetime == 0 and self.notactivate == 0:
            self.calhead = np.median(self.acq_list[0])
            self.calpitch = np.median(self.acq_list[1])
            self.calroll = np.median(self.acq_list[2])

            values_median = [self.calhead, self.calpitch, self.calroll]
            path_now = os.path.dirname(os.getcwd())
            files_path_calibration = re.sub("/src", "", path_now)

            # save on sqlite the median, but certify if the table is empyt

            buff_median = LocalDb()
            buff_median.conn_db(files_path_calibration)
            buff_median.clean_data_calibration()
            buff_median.conn_db(files_path_calibration)
            buff_median.insert_tbl_calibration(values_median)

            self.caldone = 1
            self.onlyonetime = 1
            self.calheadtxt=\
                OnscreenText(text="Mediana Head: {:7.3f}".format(self.calhead),
                             parent=base.a2dBottomRight, align=TextNode.ARight,
                             fg=(1, 1, 1, 1), pos=(-0.7, 0.3), scale=.08,
                             shadow=(0, 0, 0, 0.5))
            self.calpitchtxt=\
                OnscreenText(text="Mediana Pitch: {:7.3f}".format(self.calpitch),
                             parent=base.a2dBottomRight, align=TextNode.ARight,
                             fg=(1, 1, 1, 1), pos=(-0.7, 0.5), scale=.08,
                             shadow=(0, 0, 0, 0.5))
            self.calrolltxt=\
                OnscreenText(text="Mediana Roll: {:7.3f}".format(self.calroll),
                             parent=base.a2dBottomRight, align=TextNode.ARight,
                             fg=(1, 1, 1, 1), pos=(-0.7, 0.7), scale=.08,
                             shadow=(0, 0, 0, 0.5))
        elif self.buffer > 10 and self.onlyonetime == 1 and self.notactivate == 0:
            self.calhead = self.calhead
            self.calpitch = self.calpitch
            self.calroll = self.calroll
            self.calheadtxt=\
                OnscreenText(text="Mediana Head: {:7.3f}".format(self.calhead),
                             parent=base.a2dBottomRight, align=TextNode.ARight,
                             fg=(1, 1, 1, 1), pos=(-0.7, 0.3), scale=.08,
                             shadow=(0, 0, 0, 0.5))
            self.calpitchtxt=\
                OnscreenText(text="Mediana Pitch: {:7.3f}".format(self.calpitch),
                             parent=base.a2dBottomRight, align=TextNode.ARight,
                             fg=(1, 1, 1, 1), pos=(-0.7, 0.5), scale=.08,
                             shadow=(0, 0, 0, 0.5))
            self.calrolltxt=\
                OnscreenText(text="Mediana Roll: {:7.3f}".format(self.calroll),
                             parent=base.a2dBottomRight, align=TextNode.ARight,
                             fg=(1, 1, 1, 1), pos=(-0.7, 0.7), scale=.08,
                             shadow=(0, 0, 0, 0.5))
        self.flagtime = 1

        return Task.cont