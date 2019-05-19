#!/usr/bin/env python

"""
 Author: Raphael Castilho Gil
 Last Updated: 2019-05-18

 This is the first game to adapt the reahbilitation
"""

from direct.gui.OnscreenText import OnscreenText
from direct.interval.MetaInterval import Sequence, Parallel
from direct.interval.LerpInterval import LerpFunc
from direct.interval.FunctionInterval import Func, Wait
from src.util.fusion import Fusion
from src.util.local_db import LocalDb
from panda3d.core import *
from direct.task.Task import Task
from src.service import core as cc
import socket
from direct.actor.Actor import Actor
from src.util.dirpath_gen import PathGen
import datetime
import re
import os
from src.service.body_support_game import Game1Mov


class BallInMazeDemo:
    """
    Remember to generate an actor for this game
    """

    def __init__(self, time_val):
        """
        Initial conditions before start game
        :param time_val: ???
        """

        self.rhead = 0
        self.rpitch = 0
        self.rroll = 0

        # variables for beginning reading
        self.x_var = 0
        self.y_var = 0

        # creating connection to acquire data on real time
        self.UDP_IP = ""
        self.UDP_PORT = 2055
        self.sock = socket.socket(socket.AF_INET,
                     socket.SOCK_DGRAM)
        self.sock.bind((self.UDP_IP, self.UDP_PORT))

        # creating connection with database postgrSQL

        #self.postg = postg.PostgreSQL()
        self.flagtime = 0
        # definition of time during exercise
        self.minutes_requer = time_val
        # Some constants for the program
        self.alfa = 0  # buf to register when the task is finished
        self.ACCEL = 10         # Acceleration in ft/sec/sec
        self.MAX_SPEED = 5      # Max speed in ft/sec
        self.MAX_SPEED_SQ = self.MAX_SPEED ** 2  # Squared to make it easier to use lengthSquared
        self.last_t = 0

        # collect info of sensor
        self.acquir_data = Fusion()

        # set position of camera
        camera.setPosHpr(0, 0, 25, 0, -90, 0)  # Place the camera

        # load the sounds oduring the game
        path_now = os.path.dirname(os.getcwd())
        self.files_path = PathGen().path_gen(path_now)

        self.sound_loop_music = base.loader.loadSfx(self.files_path[0])
        self.sound_problem = base.loader.loadSfx(self.files_path[1])

        # import the score and render it
        self.score = loader.loadModel(self.files_path[2])

        # variable to register when is possible to play problem music
        self.play_once = 0

        # import a model to create a position on the system where the people need to follow
        self.actor1 = Actor(self.files_path[3])
        self.actor1.reparentTo(render)
        self.actor1.setScale(0.5)
        self.actor1.setPos(6, -1, 1)
        self.actor1.setColorScale(2.6, 0.1, 0.1, 0.6)  # red color
        self.actor1.setH(self.actor1, -45)
        self.actor1.setP(self.actor1, -45)
        self.actor1.setR(self.actor1, -45)

        # read all the joint from actor1
        self.shoulder_left_actor1 = self.actor1.controlJoint(None, "modelRoot", "shoulder_left_joint")
        self.shoulder_right_actor1 = self.actor1.controlJoint(None, "modelRoot", "shoulder_right_joint")
        self.shoulder_head_actor1 = self.actor1.controlJoint(None, "modelRoot", "head_joint")
        self.knee_left_actor1 = self.actor1.controlJoint(None, "modelRoot", "knee_left_joint")
        self.knee_right_actor1 = self.actor1.controlJoint(None, "modelRoot", "knee_right_joint")
        self.spine_joint_actor1 = self.actor1.controlJoint(None, "modelRoot", "spine_joint")
        self.hip_right_actor1 = self.actor1.controlJoint(None, "modelRoot", "hip_right_joint")
        self.hip_left_actor1 = self.actor1.controlJoint(None, "modelRoot", "hip_left_joint")
        self.ankle_right_actor1 = self.actor1.controlJoint(None, "modelRoot", "ankle_right_joint")
        self.ankle_left_actor1 = self.actor1.controlJoint(None, "modelRoot", "ankle_left_joint")
        self.foot_left_actor1 = self.actor1.controlJoint(None, "modelRoot", "foot_left_joint")
        self.foot_right_actor1 = self.actor1.controlJoint(None, "modelRoot", "foot_right_joint")
        self.hand_left_actor1 = self.actor1.controlJoint(None, "modelRoot", "hand_left_joint")
        #self.hand_right_actor1 = self.actor1.controlJoint(None, "modelRoot", "hand_right_joint")
        self.wrist_left_actor1 = self.actor1.controlJoint(None, "modelRoot", "wrist_left_joint")
        self.wrist_right_actor1 = self.actor1.controlJoint(None, "modelRoot", "wrist_right_joint")
        self.elbow_left_actor1 = self.actor1.controlJoint(None, "modelRoot", "elbow_left_joint")
        self.elbow_right_actor1 = self.actor1.controlJoint(None, "modelRoot", "elbow_right_joint")

        # set shoulder to be in normla position
        self.shoulder_left_actor1.setHpr(180, 55, 290)
        self.shoulder_right_actor1.setHpr(0, 0, -15)

        #self.shoulder_right_actor1.setHpr(0, 0, 0)

        # verification of change of legs
        self.legs_change = 0
        self.time_change = 10
        self.time_exerc_now = datetime.datetime.now()
        self.time_exerc_past = datetime.datetime.now()
        self.leg_angle = 0

        # cont times of repetion
        self.repetion = 0

        #self.score = loader.loadModel("models/baisc")
        self.score.setScale(1.2)
        self.score.reparentTo(render)

        # import the collisions walls from  score
        self.walls = self.score.find("**/wall_collide")
        self.walls.node().setIntoCollideMask(BitMask32.bit(0))
        # CollisionNodes are usually invisible but can be shown. Uncomment the next
        # line to see the collision walls
        # self.walls.show()

        # Ground_collide is a single polygon on the same plane as the ground in the
        # maze. We will use a ray to collide with it so that we will know exactly
        # what height to put the ball at every frame. Since this is not something
        # that we want the ball itself to collide with, it has a different
        # bitmask.
        #self.scoreGround = self.score.find("**/polySurface4")
        self.scoreGround = self.score.find("**/ground4")
        self.scoreGround.node().setIntoCollideMask(BitMask32.bit(1))

        # Load the ball and attach it to the scene
        # It is on a root dummy node so that we can rotate the ball itself without
        # rotating the ray that will be attached to it
        self.ballRoot = render.attachNewNode("ballRoot")
        self.ball = loader.loadModel(self.files_path[4])
        self.ball.reparentTo(self.ballRoot)

        # Find the collison sphere for the ball which was created in the egg file
        # Notice that it has a from collision mask of bit 0, and an into collison
        # mask of no bits. This means that the ball can only cause collisions, not
        # be collided into
        self.ballSphere = self.ball.find("**/ball")
        self.ballSphere.node().setFromCollideMask(BitMask32.bit(0))
        self.ballSphere.node().setIntoCollideMask(BitMask32.allOff())

        # No we create a ray to start above the ball and cast down. This is to
        # Determine the height the ball should be at and the angle the floor is
        # tilting. We could have used the sphere around the ball itself, but it
        # would not be as reliable
        self.ballGroundRay = CollisionRay()     # Create the ray
        self.ballGroundRay.setOrigin(0, 0, 10)    # Set its origin
        self.ballGroundRay.setDirection(0, 0, -1)  # And its direction
        # Collision solids go in CollisionNode
        # Create and name the node
        self.ballGroundCol = CollisionNode('groundRay')
        self.ballGroundCol.addSolid(self.ballGroundRay)  # Add the ray
        self.ballGroundCol.setFromCollideMask(BitMask32.bit(1))  # Set its bitmasks
        self.ballGroundCol.setIntoCollideMask(BitMask32.allOff())
        # Attach the node to the ballRoot so that the ray is relative to the ball
        # (it will always be 10 feet over the ball and point down)
        self.ballGroundColNp = self.ballRoot.attachNewNode(self.ballGroundCol)
        # Uncomment this line to see the ray
        # self.ballGroundColNp.show()

        # Finally, we create a CollisionTraverser. CollisionTraversers are what
        # do the job of walking the scene graph and calculating collisions.
        # For a traverser to actually do collisions, you need to call
        # traverser.traverse() on a part of the scene. Fortunately, ShowBase
        # has a task that does this for the entire scene once a frame.  By
        # assigning it to self.cTrav, we designate that this is the one that
        # it should call traverse() on each frame.
        self.cTrav = CollisionTraverser()

        # Collision traversers tell collision handlers about collisions, and then
        # the handler decides what to do with the information. We are using a
        # CollisionHandlerQueue, which simply creates a list of all of the
        # collisions in a given pass. There are more sophisticated handlers like
        # one that sends events and another that tries to keep collided objects
        # apart, but the results are often better with a simple queue
        self.cHandler = CollisionHandlerQueue()
        # Now we add the collision nodes that can create a collision to the
        # traverser. The traverser will compare these to all others nodes in the
        # scene. There is a limit of 32 CollisionNodes per traverser
        # We add the collider, and the handler to use as a pair

        self.cTrav.addCollider(self.ballSphere, self.cHandler)
        self.cTrav.addCollider(self.ballGroundColNp, self.cHandler)

        # Collision traversers have a built in tool to help visualize collisions.
        # Uncomment the next line to see it.
        # self.cTrav.showCollisions(render)

        # This section deals with lighting for the ball. Only the ball was lit
        # because the maze has static lighting pregenerated by the modeler
        ambientLight = AmbientLight("ambientLight")
        ambientLight.setColor((.55, .55, .55, 1))
        directionalLight = DirectionalLight("directionalLight")
        directionalLight.setDirection(LVector3(0, 0, -1))
        directionalLight.setColor((0.375, 0.375, 0.375, 1))
        directionalLight.setSpecularColor((1, 1, 1, 1))
        self.ballRoot.setLight(render.attachNewNode(ambientLight))
        self.ballRoot.setLight(render.attachNewNode(directionalLight))
        m = Material()
        m.setSpecular((1, 1, 1, 1))
        m.setShininess(80)
        self.ball.setMaterial(m, 1)
        base.graphicsEngine.renderFrame()
        # create a message
        self.exercice_com = \
               OnscreenText(text="Hora de treinar: Repita os movimentos do boneco vermelho",
                            parent=base.a2dTopLeft, align=TextNode.ALeft,
                            fg=(1, 1, 1, 1), pos=(0, -0.1), scale=.08,
                            shadow=(0, 0, 0, 0.5))

        # Finally, we call start for more initialization
        self.ballRoot.setPos(0, 0, 0)
        self.start(self.cHandler,  self.ballRoot, self.ball, self.score)

        # Insert doctor message
        self.text_doctor = TextNode('TestConnection')
        self.text_doctor.setText("Sem recomendações do fisioterapeuta")
        self.textNodePathDoctor = aspect2d.attachNewNode(self.text_doctor)
        self.textNodePathDoctor.setScale(0.07)
        self.textNodePathDoctor.reparentTo(base.a2dBottomLeft)
        self.textNodePathDoctor.setPos(0, 0, 0.1)

        # Insert doctor message
        self.text_advice = TextNode('TestConnection')
        self.text_advice.setText("Comece o exercício")
        self.textNodePathAdvice = aspect2d.attachNewNode(self.text_advice)
        self.textNodePathAdvice.setScale(0.07)
        self.textNodePathAdvice.reparentTo(base.a2dTopLeft)
        self.textNodePathAdvice.setPos(0, 0, -0.2)

    def start(self, data_solid, data_ball, ball, score):
        """
        The maze model also has a locator in it for where to start the ball
        To access it we use the find command

        loop music, good option to relax

        :param data_solid:
        :param data_ball:
        :param ball:
        :param score:
        :return:
        """
        # startPos = self.score.find("**/start").getPos()
        # Set the ball in the starting position
        # self.ballRoot.setPos(1,0,0)

        self.sound_loop_music.setVolume(0.02)
        self.sound_loop_music.setLoop(True)
        self.sound_loop_music.play()

        # parameters
        self.ball = ball
        self.cHandler = data_solid
        self.ballRoot = data_ball
        self.score = score
        self.minutes_requer = 1
        self.time_required = self.minutes_requer * 60  # in minutes

        self.ballV = LVector3(0, 0, 0)         # Initial velocity is 0
        self.accelV = LVector3(0, 0, 0)        # Initial acceleration is 0
        self.timenow = datetime.datetime.now()
        self.future = datetime.datetime.now() + datetime.timedelta(minutes=self.minutes_requer)

        # Create the movement task, but first make sure it is not already
        # running
        taskMgr.remove("rollTask")
        taskMgr.remove("actorcontrol")
        taskMgr.remove("database")
        taskMgr.setupTaskChain('chain1', numThreads=1, threadPriority=TPUrgent, frameSync=True)
        taskMgr.setupTaskChain('chain2', numThreads=1, threadPriority=TPHigh, frameSync=True)
        taskMgr.setupTaskChain('chain3', numThreads=1, threadPriority=TPHigh, frameSync=True)
        taskMgr.add(self.database, "database", taskChain='chain1')
        taskMgr.add(self.rollTask, "rollTask", uponDeath=self.cleanall, taskChain='chain2')
        taskMgr.add(self.actorcontrol, "actorcontrol", taskChain='chain3')

        return

    def actorcontrol(self, task):
        """
        Control the position of legs during the game

        :param task: Task to modify actor
        :return: New status of actor
        """
        self.time_exerc_past = self.time_exerc_now
        self.time_exerc_now = datetime.datetime.now()

        diff_time = self.time_exerc_now - self.time_exerc_past
        diff_time = float(diff_time.microseconds)/1000000

        if self.legs_change == 0:
            values = Game1Mov().\
                legs_movimentation_pos0_3(self.legs_change,
                                          self.leg_angle)
            self.legs_change = values[0]
            self.leg_angle = values[1]
            self.knee_left_actor1.setHpr(self.leg_angle, 0, 0)
            self.text_advice.setText("Levante a perna esquerda...")

        elif self.legs_change == 1 or \
                self.legs_change == 4:
            values = Game1Mov(). \
                legs_wait_pos2_4(self.legs_change,
                                 self.time_change,
                                 diff_time)

            self.time_change = values[0]
            self.legs_change = values[1]
            self.text_advice.setText("Segure a perna levantada...")


        elif self.legs_change == 2:
            values = Game1Mov().\
                legs_movimentation_pos0_3(self.legs_change,
                                          self.leg_angle)
            self.legs_change = values[0]
            self.leg_angle = values[1]
            self.knee_left_actor1.setHpr(self.leg_angle, 0, 0)
            self.text_advice.setText("Troque a perna...")


        elif self.legs_change == 3:
            values = Game1Mov().\
                legs_movimentation_pos0_3(self.legs_change,
                                          self.leg_angle)
            self.legs_change = values[0]
            self.leg_angle = values[1]
            self.knee_right_actor1.setHpr(self.leg_angle, 0, 0)
            self.text_advice.setText("Levante a perna direita...")

        elif self.legs_change == 5:
            values = Game1Mov(). \
                legs_movimentation_pos0_3(self.legs_change,
                                          self.leg_angle)
            self.legs_change = values[0]
            self.leg_angle = values[1]
            self.knee_right_actor1.setHpr(self.leg_angle, 0, 0)
            self.text_advice.setText("Troque a perna...")

        return task.cont


    def database(self, task):
        """
        Routine to save on remote database according with available communication

        :param task: Routine of pandas3d to collect data from sensor
        :return:
        """

        # acquire the data from acceloremeter, the most important data is pithc and roll for sensor
        data, addr = self.sock.recvfrom(1024)
        ## modification during 15/06/2017, try to test without magnometer sensor
        #date_time, accx, accy, accz, magx, magy, magz, gyrx, gyry, gyrz,  = re.split(',', data)
        #date_val = datetime.datetime.fromtimestamp(float(date_time)/1000).strftime('%Y-%m-%d %H:%M:%S.%f')
        date_time, accx, accy, accz, magx, magy, magz, gyrx, gyry, gyrz,  = re.split(',', data.decode('utf-8'))
        date_val = datetime.datetime.fromtimestamp(float(date_time)/1000).strftime('%Y-%m-%d %H:%M:%S.%f')
        gyrz = str(gyrz)
        gyrz = float(gyrz.replace("#", ""))
        self.acc = (float(accx), float(accy), float(accz))
        self.mag = (float(magx), float(magy), float(magz))
        self.gyr = (float(gyrx), float(gyry), float(gyrz))
        if self.flagtime == 0:
            self.acquir_data.update_nomag(self.acc, self.gyr, 0)
            self.flagtime = 1
        else:
            self.now_t = date_time
            diff = int(self.now_t) - int(self.last_t)
            diff *= 1000
            self.acquir_data.update_nomag(self.acc, self.gyr, float(diff))
        self.last_t = date_time

        self.rhead = self.acquir_data.heading
        self.rpitch = self.acquir_data.pitch
        self.rroll = self.acquir_data.roll

        print('all data acquired')
        print(self.acc)
        print(self.rhead)
        print(self.rpitch)
        print(self.rroll)

        '''
        Inserir aqui conexão com o mongo e leitura de rede
        Os dados enviados são os 6 dos sensores, mais o tipo do jogo
        Remover conexão com o postgresql
        '''

        #self.postg.sql_con("127.0.0.1", "postgres", "ra2730ar", "log_iot_acquire", "5432")
        #self.rdt1, self.rdt2, self.rmed_head, self.rmed_pitch, self.rmed_roll = self.postg.read_sensor_game2()
        #self.postg.post_close_connection()

        path_now = os.path.dirname(os.getcwd())
        files_path_game = re.sub("/src", "", path_now)

        buff_game = LocalDb()
        buff_game.conn_db(files_path_game)
        data_collect = buff_game.verify_data_calibration()
        self.rmed_pitch = data_collect[1]
        self.rmed_roll = data_collect[2]

        # here is the moment to analyze the absolute variation between the median and the
        self.y_var = abs(self.rmed_pitch - self.acquir_data.pitch)
        self.x_var = abs(self.rmed_roll - self.acquir_data.roll)

        # write on cloud database
        # all the acc and kinect data
        return task.cont

    def cleanall(self, task):

        """
        Clean all nodes of this game
        :param task:
        :return:
        """

        self.sound_loop_music.stop()
        #self.imageObject.destroy()
        taskMgr.remove("rollTask")
        taskMgr.remove("actorcontrol")
        taskMgr.remove("database")
        self.actor1.cleanup()
        self.score.remove_node()
        self.ball.remove_node()
        self.title.destroy()
        self.exercice_com.destroy()
        self.textNodePathDoctor.removeNode()
        self.textNodePathAdvice.removeNode()
        cc.Xcore().request("Results")
        return

    # This function handles the collision between the ray and the ground
    # Information about the interaction is passed in colEntry
    def groundCollideHandler(self, colEntry):
        """
        Set the ball to the appropriate Z value for it to be exactly on the
        ground
        :param colEntry:
        :return:
        """

        newZ = colEntry.getSurfacePoint(render).getZ()
        self.ballRoot.setZ(newZ + 0.8)

        # Find the acceleration direction. First the surface normal is crossed with
        # the up vector to get a vector perpendicular to the slope
        norm = colEntry.getSurfaceNormal(render)
        accelSide = norm.cross(LVector3.up())
        # Then that vector is crossed with the surface normal to get a vector that
        # points down the slope. By getting the acceleration in 3D like this rather
        # than in 2D, we reduce the amount of error per-frame, reducing jitter
        self.accelV = norm.cross(accelSide)

    def wallCollideHandler(self, colEntry):
        """
        This function handles the collision between the ball and a wall
        :param colEntry:
        :return:
        """

        # First we calculate some numbers we need to do a reflection
        norm = colEntry.getSurfaceNormal(render) * -1  # The normal of the wall
        curSpeed = self.ballV.length()                # The current speed
        inVec = self.ballV / curSpeed                 # The direction of travel
        velAngle = norm.dot(inVec)                    # Angle of incidance
        hitDir = colEntry.getSurfacePoint(render) - self.ballRoot.getPos()
        hitDir.normalize()
        # The angle between the ball and the normal
        hitAngle = norm.dot(hitDir)

        # Ignore the collision if the ball is either moving away from the wall
        # already (so that we don't accidentally send it back into the wall)
        # and ignore it if the collision isn't dead-on (to avoid getting caught on
        # corners)
        if velAngle > 0 and hitAngle > .995:
            # Standard reflection equation
            reflectVec = (norm * norm.dot(inVec * -1) * 2) + inVec

            # This makes the velocity half of what it was if the hit was dead-on
            # and nearly exactly what it was if this is a glancing blow
            self.ballV = reflectVec * (curSpeed * (((1 - velAngle) * .5) + .5))
            # Since we have a collision, the ball is already a little bit buried in
            # the wall. This calculates a vector needed to move it so that it is
            # exactly touching the wall
            disp = (colEntry.getSurfacePoint(render) -
                    colEntry.getInteriorPoint(render))
            newPos = self.ballRoot.getPos() + disp
            self.ballRoot.setPos(newPos)

    def rollTask(self, task):
        """
        This is the task that deals with making everything interactive

        In each frame is neccessary the update of render and solid
        the following line increment the solid and recognize this element

        :param task: funcion from pandas3d
        :return:
        """

        self.cTrav.traverse(render)
        if task.time < self.time_required:
            #base.graphicsEngine.renderFrame()
            if hasattr(self, 'comments'):
                self.comments.destroy()
                self.comments2.destroy()
            else:
                pass
            part_time = self.future - self.timenow
            check = part_time.seconds

            self.timenow = datetime.datetime.now()
            if hasattr(self, 'title'):
                self.title.destroy()
            else:
                pass
            self.checktime = self.timenow.strftime("%M:%S")
            # Standard technique for finding the amount of time since the last
            # frame - this technique shows up the frames per second
            dt = globalClock.getDt()
            self.title = \
                   OnscreenText(text=" Fim do exercicio em: {}s".format(str(check)),
                                parent=base.a2dBottomRight, align=TextNode.ARight,
                                fg=(1, 1, 1, 1), pos=(-0.1, 0.1), scale=.06,
                                shadow=(0, 0, 0, 0.5))
            self.text_doctor.setText("{}".format(str(check)))
            # this is the moment of insertion of images....only for test
            #status_ok = 'problem'
            #self.imageObject = OnscreenImage(image='images/ok.png', pos=(-1.1, 0.2, 0.92), scale=(0.075, 0.075, 0.075))
            # If dt is large, then there has been a # hiccup that could cause the ball
            # to leave the field if this functions runs, so ignore the frame
            print('delay value: {}'.format(str(dt)))
            if dt > .2:
                return Task.cont
            # The collision handler collects the collisions. We dispatch which function
            # to handle the collision based on the name of what was collided into
            print(self.cHandler.getNumEntries())
            for i in range(self.cHandler.getNumEntries()):
                entry = self.cHandler.getEntry(i)
                name = entry.getIntoNode().getName()
                if name == "wall_collide":
                    self.wallCollideHandler(entry)
                elif name == "ground4":
                    self.groundCollideHandler(entry)
                elif name == "loseTrigger":
                    self.loseGame(entry)

            if self.y_var < 0:
                self.inclination_y = self.y_var + 4
            else:
                self.inclination_y = self.y_var - 4

            if self.x_var < 0:
                self.inclination_x = self.x_var + 4
            else:
                self.inclination_x = self.x_var - 4

            if self.inclination_y > 10:
                self.inclination_y = 10
            else:
                pass
            if self.inclination_x > 10:
                self.inclination_x = 10
            else:
                pass
            self.score.setP(self.inclination_y)
            self.score.setR(self.inclination_x)

            # Finally, we move the ball
            # In this part needs more modification, the ball needs to return when does not have inclination
            # Update the velocity based on acceleration
            self.ballV += self.accelV * dt * self.ACCEL
            # invertion and arrive in the middle position
            self.return_ball = self.ballV
            # Clamp the velocity to the maximum speed
            if self.ballV.lengthSquared() > self.MAX_SPEED_SQ:
                self.ballV.normalize()
                self.ballV *= self.MAX_SPEED
            else:
                pass
            # Update the position based on the velocity
            # This is the moment to register a smile when its is done in a correct way and, in the same time, green
            # color the score.
            # However if the exercise is not done in a very good way, shows up a sad face and red color in the score
            # variable play_once is only to register only one time when the exervise is done not in the right moment

            if self.inclination_x > 4 or self.inclination_y > 4 or self.inclination_x < -4 or self.inclination_y < - 4:
                self.ballRoot.setPos(self.ballRoot.getPos() + (self.ballV * dt))
                self.score.setColorScale(0.8, 0.1, 0.1, 1.0)  # red color
                # put as comment because i still do not hve sure about smile/sad face
                #self.imageObject.setImage('images/sad.png')
                if self.play_once == 0:
                    self.sound_problem.setVolume(0.04)
                    self.sound_problem.play()
                    self.play_once = 1
                    self.repetion = 0

            else:
                self.repetion += dt
                self.score.setColorScale(0.1, 0.8, 0.1, 1.0)  # green color
                # put as comment because i still do not hve sure about smile/sad face
                #self.imageObject.setImage('images/ok.png')
                var1 = float(self.ballRoot.getX())
                var2 = float(self.ballRoot.getY())
                var3 = float(self.ballRoot.getZ())
                if self.repetion > 5:
                    self.ballRoot.setX(self.ballRoot.getX())
                    self.ballRoot.setY(self.ballRoot.getY())
                    #self.ballRoot.setZ(self.ballRoot.getZ())

                else:
                    self.ballRoot.setX(var1 - var1 * dt)
                    self.ballRoot.setY(var2 - var2 * dt)
                    #self.ballRoot.setZ(var3 - self.ballV[2] * dt)
                    self.play_once = 0
            #print 'ball position' + str(self.ballRoot.getPos())
            #print 'new deslocation' + str(self.ballV)
            # here is the moment to send the data for postgreSQL.


            # This block of code rotates the ball. It uses something called a quaternion
            # to rotate the ball around an arbitrary axis. That axis perpendicular to
            # the balls rotation, and the amount has to do with the size of the ball
            # This is multiplied on the previous rotation to incrimentally turn it.
            if self.repetion > 5:
                # not modificate the rotation of ball
                pass
            else:
                prevRot = LRotationf(self.ball.getQuat())
                axis = LVector3.up().cross(self.ballV)
                newRot = LRotationf(axis, 45.5 * dt * self.ballV.length())
                self.ball.setQuat(prevRot * newRot)

            return Task.cont       # Continue the task indefinitely
        else:
            return Task.done
        #return taskMgr.remove("rollTask")

    # If the ball hits a hole trigger, then it should fall in the hole.
    # This is faked rather than dealing with the actual physics of it.
    def loseGame(self, entry):
        """
        The triggers are set up so that the center of the ball should move to the
        collision point to be in the hole

        :param entry:
        :return:
        """

        toPos = entry.getInteriorPoint(render)
        taskMgr.remove('rollTask')  # Stop the maze task

        # Move the ball into the hole over a short sequence of time. Then wait a
        # second and call start to reset the game
        Sequence(
            Parallel(
                LerpFunc(self.ballRoot.setX, fromData=self.ballRoot.getX(),
                         toData=toPos.getX(), duration=.1),
                LerpFunc(self.ballRoot.setY, fromData=self.ballRoot.getY(),
                         toData=toPos.getY(), duration=.1),
                LerpFunc(self.ballRoot.setZ, fromData=self.ballRoot.getZ(),
                         toData=self.ballRoot.getZ() - .9, duration=.2)),
            Wait(1),
            Func(self.start)).start()
