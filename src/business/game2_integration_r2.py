#!/usr/bin/env python

# Author: Raphael Castilho Gil
# Last Updated: 2017-04-04
#
# This is the first game to adapt the reahbilitation


from direct.gui.OnscreenText import OnscreenText
from direct.interval.MetaInterval import Sequence, Parallel
from direct.interval.LerpInterval import LerpFunc
from direct.interval.FunctionInterval import Func, Wait
from direct.gui.OnscreenImage import OnscreenImage
from src.util.fusion import Fusion
from panda3d.core import *
from direct.task.Task import Task
import src.util.store_variable
import src.business.core as cc
import src.util.postgresql_request as postg
import socket
from direct.actor.Actor import Actor
from src.util.dirpath_gen import PathGen
import datetime
import re
import sys
import math
import os
from pykinect import nui
from pykinect.nui import JointId

# remember to generate an actor for this game and insert an animation according kinect acquiring


class BallInMazeDemo:

    def __init__(self, time_val):
        """

        :param time_val:
        """
        # list of joints on the actor

        self.listjoint = [JointId.HipCenter, JointId.Spine, JointId.ShoulderCenter,
             JointId.Head, JointId.ShoulderLeft, JointId.ElbowLeft,
             JointId.WristLeft, JointId.HandLeft, JointId.ShoulderRight,
             JointId.ElbowRight, JointId.WristRight, JointId.HandRight,
             JointId.HipLeft, JointId.KneeLeft, JointId.AnkleLeft,
             JointId.FootLeft, JointId.HipRight, JointId.KneeRight,
             JointId.AnkleRight, JointId.FootRight]

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
        self.postg = postg.PostgreSQL()
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

        # load the sounds oduring the game

        self.sound_loop_music = base.loader.loadSfx("sounds/325611__shadydave__my-love-piano-loop.mp3")
        self.sound_problem = base.loader.loadSfx("sounds/NFF-whoa-whoa.wav")

        # import the score and render it
        self.score = loader.loadModel("models/test_basic")

        # variable to register when is possible to play problem music
        self.play_once = 0

        # import a model that will be an actor on the future
        self.actor1 = Actor("models/actor1_mov")
        self.actor1.reparentTo(render)
        self.actor1.setScale(0.5)
        self.actor1.setPos(-4.8, -1, 1)
        self.actor1.setColorScale(0.1, 0.1, 1.5, 0.5)  # blue color
        self.actor1.setH(self.actor1, -45)
        self.actor1.setP(self.actor1, -45)
        self.actor1.setR(self.actor1, -45)

        # import a second model to create a position on the system where the people need to follow

        self.actor2 = Actor("models/actor1_mov")
        self.actor2.reparentTo(render)
        self.actor2.setScale(0.5)
        self.actor2.setPos(6, -1, 1)
        self.actor2.setColorScale(1.5, 0.1, 0.1, 0.5)  # red color
        self.actor2.setH(self.actor2, -45)
        self.actor2.setP(self.actor2, -45)
        self.actor2.setR(self.actor2, -45)

        # read all the joint from actor1
        self.shoulder_left_actor1 = self.actor1.controlJoint(None, "modelRoot", "shoulder_left_joint")
        self.shoulder_right_actor1 = self.actor1.controlJoint(None, "modelRoot", "shoulder_right_joint")

        # read all the joint from actor2
        self.shoulder_left_actor2 = self.actor2.controlJoint(None, "modelRoot", "shoulder_left_joint")
        self.shoulder_right_actor2 = self.actor2.controlJoint(None, "modelRoot", "shoulder_right_joint")


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
        self.ball = loader.loadModel("models/ball")
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
        #startPos = self.score.find("**/start").getPos()
        # Set the ball in the starting position
        #self.ballRoot.setPos(1,0,0)


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
        self.del_lat = 0
        print('kkkk7')
        return

    def quaternion2euler(self, var1):
        """

        :param var1:
        :return:
        """

        q = var1
        qx2 = q.x * q.x
        qy2 = q.y * q.y
        qz2 = q.z * q.z

        test = q.x*q.y + q.z*q.w

        if test > 0.499:
            roll = math.radians(360/math.pi*math.atan2(q.x,q.w))
            pitch = math.pi/2
            yaw = 0
        elif test < -0.499:
            roll = math.radians(-360/math.pi*math.atan2(q.x,q.w))
            pitch = -math.pi/2
            yaw = 0

        else:
            roll = math.atan2(2 * q.y * q.w - 2 * q.x * q.z, 1 - 2 * qy2 - 2 * qz2)
            pitch = math.asin(2*q.x*q.y+2*q.z*q.w)
            yaw = math.atan2(2*q.x*q.w-2*q.y*q.z, 1-2*qx2-2*qz2)
        roll = math.degrees(roll)
        pitch = math.degrees(pitch)
        yaw = math.degrees(yaw)
        print [roll, pitch, yaw]
        return [roll, pitch, yaw]

    '''
    def actorcontrol (self, task):
        # define position of actor using kinect sensor
        self.del_lat += 1
        if self.del_lat > 100:
            self.del_lat = 0
        self.shoulder_left_actor1.setHpr(self.del_lat, 30, 30)
        self.a = 0
        with nui.Runtime() as kinect:
            print 'test2'
            kinect.skeleton_engine.enabled = True
            while self.a == 0:
                frame = kinect.skeleton_engine.get_next_frame()
                for cont, skeleton in enumerate(frame.SkeletonData):
                    print nui.SkeletonTrackingState.TRACKED
                    print skeleton.eTrackingState
                    if skeleton.eTrackingState == nui.SkeletonTrackingState.TRACKED:
                        self.a = 1
                        print 'oi'
                        for cont2, posjoint in enumerate(self.listjoint):
                            print str(posjoint) + ' ' + str(cont2)
                            if cont2 == 9:
                                print posjoint
                                print 'test'
                                print skeleton.calculate_bone_orientations()[JointId.ShoulderRight].absolute_rotation
                                var2 = skeleton.calculate_bone_orientations()[JointId.ShoulderRight].absolute_rotation.rotation_quaternion
                                var2r = self.quaternion2euler(var2)
                                print skeleton.calculate_bone_orientations()[JointId.ShoulderRight].hierarchical_rotation.rotation_quaternion
                                var1 = skeleton.calculate_bone_orientations()[JointId.ShoulderRight].hierarchical_rotation.rotation_quaternion
                                var1r = self.quaternion2euler(var1)
                                self.shoulder_right_actor1.setHpr(var1r[2], var1r[1], var1r[0])
        return task.cont
    '''

    def database (self, task):
        """


        :param task: Routine of pandas3d to collect data from sendor
        :return:
        """

        # acquire the data from acceloremeter, the most important data is pithc and roll for sensor
        data, addr = self.sock.recvfrom(1024)
        ## modification during 15/06/2017, try to test without magnometer sensor
        #date_time, accx, accy, accz, magx, magy, magz, gyrx, gyry, gyrz,  = re.split(',', data)
        #date_val = datetime.datetime.fromtimestamp(float(date_time)/1000).strftime('%Y-%m-%d %H:%M:%S.%f')
        date_time, accx, accy, accz, gyrx, gyry, gyrz,  = re.split(',', data)
        date_val = datetime.datetime.fromtimestamp(float(date_time)/1000).strftime('%Y-%m-%d %H:%M:%S.%f')
        magx = 0
        magy = 0
        magz = 0
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

        self.postg.sql_con("127.0.0.1", "postgres", "ra2730ar", "log_iot_acquire", "5432")
        self.rdt1, self.rdt2, self.rmed_head, self.rmed_pitch, self.rmed_roll = self.postg.read_sensor_game2()
        self.postg.post_close_connection()

        # here is the moment to analyze the absolute variation between the median and the
        self.y_var = abs(self.rmed_pitch - self.acquir_data.pitch)
        self.x_var = abs(self.rmed_roll - self.acquir_data.roll)

        # write on cloud database
        # all the acc and kinect data
        return task.cont

    def cleanall(self,task):
        print("end of task")
        self.sound_loop_music.stop()
        #self.imageObject.destroy()
        taskMgr.remove("actorcontrol")
        taskMgr.remove("database")
        self.actor1.remove_node()
        self.score.remove_node()
        self.ball.remove_node()
        self.title.destroy()
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
                   OnscreenText(text=" Tempo para o fim do exercicio: " + str(check),
                                parent=base.a2dBottomRight, align=TextNode.ARight,
                                fg=(1, 1, 1, 1), pos=(-0.1, 0.1), scale=.08,
                                shadow=(0, 0, 0, 0.5))

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
            # Read the mouse position and tilt the score accordingly
            # modified to use the sensor
            '''
            if base.mouseWatcherNode.hasMouse():
                mpos = base.mouseWatcherNode.getMouse()  # get the mouse position
                print mpos
                # here is the moment to tilt the score effectively.
                self.inclination_y = mpos.getY() * -10
                self.inclination_x = mpos.getX() * 10
                self.score.setP(mpos.getY() * -10)
                self.score.setR(mpos.getX() * 10)
                '''

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
            if hasattr(self, 'rroll'):
                self.comments = \
               OnscreenText(text="Analise dos dados roll " + str(self.rroll),
                            parent=base.a2dBottomRight, align=TextNode.ARight,
                            fg=(1, 1, 1, 1), pos=(-0.1, 0.4), scale=.08,
                            shadow=(0, 0, 0, 0.5))
                self.comments2 = \
               OnscreenText(text="Analise dos dados pitchl " + str(self.rpitch),
                            parent=base.a2dBottomRight, align=TextNode.ARight,
                            fg=(1, 1, 1, 1), pos=(-0.1, 0.6), scale=.08,
                            shadow=(0, 0, 0, 0.5))
            else:
                pass

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

if __name__=="__main__":
    # Finally, create an instance of our class and start 3d rendering
    demo = BallInMazeDemo()
    wp = WindowProperties()
    # create full screen game
    wp.setSize(1024, 768)  # there will be more resolutions
    wp.setFullscreen(True)
    base.win.requestProperties(wp)
    demo.run()
