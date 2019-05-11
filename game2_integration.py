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
from panda3d.core import *
from direct.task.Task import Task
import store_variable
import Core as cc

from direct.actor.Actor import Actor
import datetime
import sys

# remember to generate an actor for this game and insert an animation according kinect acquiring


class BallInMazeDemo:

    def __init__(self, time_val):

        self.minutes_requer = time_val
        # Some constants for the program
        self.alfa = 0  # buf to register when the task is finished
        self.ACCEL = 10         # Acceleration in ft/sec/sec
        self.MAX_SPEED = 5      # Max speed in ft/sec
        self.MAX_SPEED_SQ = self.MAX_SPEED ** 2  # Squared to make it easier to use lengthSquared

        # set position of camera

        camera.setPosHpr(0, 0, 25, 0, -90, 0)  # Place the camera

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
        self.actor1.setScale(0.4)
        self.actor1.setPos(-4.8, -1, 1)
        self.actor1.setColorScale(0.1, 0.1, 1.5, 0.5)  # blue color
        self.actor1.setH(self.actor1, -45)
        self.actor1.setP(self.actor1, -45)
        self.actor1.setR(self.actor1, -45)

        # read all the joint from actor
        self.shoulder_left_actor1 = self.actor1.controlJoint(None, "modelRoot", "shoulder_left_joint")

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

        # Finally, we call start for more initialization
        self.ballRoot.setPos(0, 0, 0)
        self.start(self.cHandler,  self.ballRoot, self.ball, self.score)

    def start(self, data_solid, data_ball, ball, score):
        # The maze model also has a locator in it for where to start the ball
        # To access it we use the find command
        #startPos = self.score.find("**/start").getPos()
        # Set the ball in the starting position
        #self.ballRoot.setPos(1,0,0)

        # loop music, good option to relax

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
        self.mainLoop = taskMgr.add(self.rollTask, "rollTask", uponDeath=self.cleanall)
        self.mainLoop2 = taskMgr.add(self.actorcontrol, "actorcontrol")
        print 'kkkk7'
        return

    def cleanall(self,task):
        print "end of task"
        self.sound_loop_music.stop()
        self.imageObject.destroy()
        #self.ballGroundRay.
        #self.actor.delete()
        #Vehicle.destroy(self)
        self.score.remove_node()
        self.ball.remove_node()
        self.title.destroy()
        cc.Xcore().request("Results")
        return

    # This function handles the collision between the ray and the ground
    # Information about the interaction is passed in colEntry
    def groundCollideHandler(self, colEntry):
        print 'oi'
        # Set the ball to the appropriate Z value for it to be exactly on the
        # ground
        newZ = colEntry.getSurfacePoint(render).getZ()
        self.ballRoot.setZ(newZ + .4)

        # Find the acceleration direction. First the surface normal is crossed with
        # the up vector to get a vector perpendicular to the slope
        norm = colEntry.getSurfaceNormal(render)
        accelSide = norm.cross(LVector3.up())
        # Then that vector is crossed with the surface normal to get a vector that
        # points down the slope. By getting the acceleration in 3D like this rather
        # than in 2D, we reduce the amount of error per-frame, reducing jitter
        self.accelV = norm.cross(accelSide)

    # This function handles the collision between the ball and a wall
    def wallCollideHandler(self, colEntry):

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

    def actorcontrol(self, task):
        self.shoulder_left_actor1.setHpr(30, 30, 30)

        return Task.cont




    # This is the task that deals with making everything interactive
    def rollTask(self, task):

        # in each frame is neccessary the update of render and solid
        # the following line increment the solid and recognize this element
        self.cTrav.traverse(render)

        while task.time < self.time_required:
            part_time = self.future - self.timenow
            check = part_time.seconds
            #part_time = part_time.strftime("%M:%S")
            self.timenow = datetime.datetime.now()
            if hasattr(self, 'title'):
                self.title.destroy()
            else:
                pass
            # Standard technique for finding the amount of time since the last
            # frame - this technique shows up the frames per second
            dt = globalClock.getDt()
            self.title = \
                   OnscreenText(text="Tempo para o fim do exercicio: " + str(check),
                                parent=base.a2dBottomRight, align=TextNode.ARight,
                                fg=(1, 1, 1, 1), pos=(-0.1, 0.1), scale=.08,
                                shadow=(0, 0, 0, 0.5))

            # this is the moment of insertion of images....only for test
            status_ok = 'problem'
            self.imageObject = OnscreenImage(image='images/ok.png', pos=(-1.1, 0.2, 0.92), scale=(0.075, 0.075, 0.075))
            self.comments = \
                   OnscreenText(text="Analise dos dados " + str(status_ok),
                                parent=base.a2dBottomRight, align=TextNode.ARight,
                                fg=(1, 1, 1, 1), pos=(-0.7, 1.92), scale=.08,
                                shadow=(0, 0, 0, 0.5))

            # If dt is large, then there has been a # hiccup that could cause the ball
            # to leave the field if this functions runs, so ignore the frame
            print dt
            if dt > .2:
                print 'check'
                return Task.cont

            # The collision handler collects the collisions. We dispatch which function
            # to handle the collision based on the name of what was collided into
            print 'other'
            print self.cHandler.getNumEntries()
            for i in range(self.cHandler.getNumEntries()):
                print i
                entry = self.cHandler.getEntry(i)
                print entry.getIntoNode().getName()
                name = entry.getIntoNode().getName()
                if name == "wall_collide":
                    self.wallCollideHandler(entry)
                elif name == "ground4":
                    self.groundCollideHandler(entry)
                elif name == "loseTrigger":
                    self.loseGame(entry)

            # Read the mouse position and tilt the score accordingly
            if base.mouseWatcherNode.hasMouse():
                mpos = base.mouseWatcherNode.getMouse()  # get the mouse position
                print mpos
                # here is the moment to tilt the score effectively.
                self.inclination_y = mpos.getY() * -10
                self.inclination_x = mpos.getX() * 10


                self.score.setP(mpos.getY() * -10)
                self.score.setR(mpos.getX() * 10)

            # Finally, we move the ball
            # In this part needs more modification, the ball needs to return when does not have inclination
            # Update the velocity based on acceleration
            self.ballV += self.accelV * dt * self.ACCEL

            # invertion and arrive in the middle position

            self.return_ball = self.ballV
            # Clamp the velocity to the maximum speed
            if self.ballV.lengthSquared() > self.MAX_SPEED_SQ:
                print self.MAX_SPEED_SQ
                self.ballV.normalize()
                self.ballV *= self.MAX_SPEED
            else:
                pass

            # Update the position based on the velocity
            # This is the moment to register a smile when its is done in a correct way and, in the same time, green
            # color the score.
            # However if the exercise is not done in a very good way, shows up a sad face and red color in the score
            # variable play_once is only to register only one time when the exervise is done not in the right moment

            if self.inclination_x > 2 or self.inclination_y > 2 or self.inclination_x < -2 or self.inclination_y < - 2:
                self.ballRoot.setPos(self.ballRoot.getPos() + (self.ballV * dt))
                self.score.setColorScale(0.8, 0.1, 0.1, 1.0)  # red color
                self.imageObject.setImage('images/sad.png')
                if self.play_once == 0:
                    self.sound_problem.setVolume(0.04)
                    self.sound_problem.play()
                    self.play_once = 1

            else:
                self.score.setColorScale(0.1, 0.8, 0.1, 1.0)  # green color
                self.imageObject.setImage('images/ok.png')
                var1 = float(self.ballRoot.getX())
                var2 = float(self.ballRoot.getY())
                var3 = float(self.ballRoot.getZ())
                self.ballRoot.setX(var1 - var1 * dt)
                self.ballRoot.setY(var2 - var2 * dt)
                self.ballRoot.setZ(var3 - self.ballV[2] * dt)
                self.play_once = 0
            print 'ball position' + str(self.ballRoot.getPos())
            print 'new deslocation' + str(self.ballV)
            # here is the moment to send the data for postgreSQL.


            # This block of code rotates the ball. It uses something called a quaternion
            # to rotate the ball around an arbitrary axis. That axis perpendicular to
            # the balls rotation, and the amount has to do with the size of the ball
            # This is multiplied on the previous rotation to incrimentally turn it.
            prevRot = LRotationf(self.ball.getQuat())
            axis = LVector3.up().cross(self.ballV)
            newRot = LRotationf(axis, 45.5 * dt * self.ballV.length())
            self.ball.setQuat(prevRot * newRot)

            return Task.cont       # Continue the task indefinitely
        return Task.done
        #return taskMgr.remove("rollTask")

    # If the ball hits a hole trigger, then it should fall in the hole.
    # This is faked rather than dealing with the actual physics of it.
    def loseGame(self, entry):
        # The triggers are set up so that the center of the ball should move to the
        # collision point to be in the hole
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
    print 'test'
    # Finally, create an instance of our class and start 3d rendering
    demo = BallInMazeDemo()
    wp = WindowProperties()
    # create full screen game
    wp.setSize(1024, 768)  # there will be more resolutions
    wp.setFullscreen(True)
    base.win.requestProperties(wp)
    demo.run()
