from panda3d.core import WindowProperties, TextNode
from direct.task.TaskManagerGlobal import taskMgr
from direct.gui.OnscreenText import OnscreenText
from direct.task import Task
from direct.showbase.ShowBase import ShowBase
import sys


class App(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.base = self
        self.setup()

    def genLabelText(self, text, i):
        text = OnscreenText(text = text, pos = (-1.3, .5-.05*i), fg=(0,1,0,1),
                      align = TextNode.ALeft, scale = .05)
        return text


    def setup(self):
        # acquisition from mouse, later we are going to acquire directly from bluetooth
        # Disable the camera trackball controls.
        self.disableMouse()

        # control mapping of mouse movement to box movement
        self.mouseMagnitude = 10

        self.moveX, self.moveY = 0, 0

        #self.genLabelText("[0] Absolute mode, [1] Relative mode, [2] Confined mode", 0)

        self.base.accept('0', lambda: self.setMouseMode(WindowProperties.M_absolute))
        #self.base.accept('1', lambda: self.setMouseMode(WindowProperties.M_relative))
        #self.base.accept('2', lambda: self.setMouseMode(WindowProperties.M_confined))

        #self.genLabelText("[C] Manually re-center mouse on each tick", 1)
        #self.base.accept('C', lambda: self.toggleRecenter())
        #self.base.accept('c', lambda: self.toggleRecenter())

        self.genLabelText("[S] Show mouse", 2)
        self.base.accept('S', lambda: self.toggleMouse())
        self.base.accept('s', lambda: self.toggleMouse())

        self.base.accept('escape', sys.exit, [0])

        self.mouseText = self.genLabelText("", 5)
        #self.deltaText = self.genLabelText("", 6)
        #self.positionText = self.genLabelText("", 8)

        self.lastMouseX, self.lastMouseY = None, None

        self.hideMouse = False

        self.setMouseMode(WindowProperties.M_absolute)
        self.manualRecenterMouse = True

        # make a box to move with the mouse
        self.model = self.loader.loadModel("models/test1")
        self.model.setScale(0.1)
        self.model.reparentTo(self.render)

        self.cam.setPos(0, -10, 0)
        self.cam.lookAt(0, 0, 0)

        self.model3 = self.loader.loadModel("models/box")
        self.model3.setScale(1.0)
        self.model3.reparentTo(self.render)
        self.model3.setPos(-0.5, -1,  0.5)
        self.model3.setColor((0, 0, 1, 1))

        '''
        self.model2 = self.loader.loadModel("models/box")
        self.model2.setScale(1.5)
        self.model2.reparentTo(self.render)
        self.model2.setPos(-0.75, -0.5, -0.75)
        self.model2.setColor((0.1, 0.1, 0.1, 1))
        '''
        self.model2 = self.loader.loadModel("models/score_end1")
        self.model2.setScale(0.5)
        self.model2.reparentTo(self.render)
        self.model2.setPos(-0.75, -0.5, -0.75)
        #self.model2.setColor((0.1, 0.1, 0.1, 1))
        self.model2.setHpr(-90, 180, 90)


        self.model1 = self.loader.loadModel("models/box")
        self.model1.setScale(2.0)
        self.model1.reparentTo(self.render)
        self.model1.setDepthTest(True)
        self.model1.setPos(-1, 0, -1)
        #self.model1.setTransparency(TransparencyAttrib.MBinary, 1)



        self.mouseTask = taskMgr.add(self.mouseTask, "Mouse Task")

    def setMouseMode(self, mode):
        print("Changing mode to %s" % mode)

        self.mouseMode = mode

        wp = WindowProperties()
        wp.setMouseMode(mode)
        self.base.win.requestProperties(wp)

        # these changes may require a tick to apply
        self.base.taskMgr.doMethodLater(0, self.resolveMouse, "Resolve mouse setting")

    def resolveMouse(self, t):
        wp = self.base.win.getProperties()

        actualMode = wp.getMouseMode()
        if self.mouseMode != actualMode:
            print("ACTUAL MOUSE MODE: %s" % actualMode)

        self.mouseMode = actualMode

        #self.rotateX, self.rotateY = -.5, -.5
        self.lastMouseX, self.lastMouseY = None, None
        self.moveX, self.moveY = 0, 0

        self.recenterMouse()

    def recenterMouse(self):
        self.base.win.movePointer(0,
              int(self.base.win.getProperties().getXSize() / 2),
              int(self.base.win.getProperties().getYSize() / 2))


    def alarm(self, value, value1):

        print value
        print value1
        if value == 0 and value1 == 0:
            self.text = 'OK'
        elif value == 1 and value1 == 0:
            self.text = 'CUIDADO LADO DIREITO'
        elif value == 2 and value1 == 0:
            self.text = 'CUIDADO LADO ESQUERDO'
        elif value == 0 and value1 == 3:
            self.text = 'CUIDADO ENCIMA'
        elif value == 0 and value1 == 4:
            self.text = 'CUIDADO EMBAIXO'
        elif value1 == 5 or value == 5:
            self.text = 'PERDENDO EQUILIBRIO, CONCENTRE-SE'
        else:
            self.text = 'CUIDADO TOTAL'
        return self.text



    def toggleRecenter(self):
        print("Toggling re-center behavior")
        self.manualRecenterMouse = not self.manualRecenterMouse

    def toggleMouse(self):
        print("Toggling mouse visibility")

        self.hideMouse = not self.hideMouse

        wp = WindowProperties()
        wp.setCursorHidden(self.hideMouse)
        self.base.win.requestProperties(wp)

    def mouseTask(self, task):
        mw = self.base.mouseWatcherNode

        hasMouse = mw.hasMouse()
        if hasMouse:
            # get the window manager's idea of the mouse position
            x, y = mw.getMouseX(), mw.getMouseY()

            if self.lastMouseX is not None:
                # get the delta
                if self.manualRecenterMouse:
                    # when recentering, the position IS the delta
                    # since the center is reported as 0, 0
                    dx, dy = x, y
                else:
                    dx, dy = x - self.lastMouseX, y - self.lastMouseY
            else:
                # no data to compare with yet
                dx, dy = 0, 0

            self.lastMouseX, self.lastMouseY = x, y

        else:
            x, y, dx, dy = 0, 0, 0, 0


        if self.manualRecenterMouse:
            # move mouse back to center
            self.recenterMouse()
            self.lastMouseX, self.lastMouseY = 0, 0

        # scale position and delta to pixels for user
        w, h = self.win.getSize()

        '''
        self.mouseText.setText("Mode: {0}, Recenter: {1}  |  Mouse: {2}, {3}  |  hasMouse: {4}".format(
             self.mouseMode, self.manualRecenterMouse,
             int(x*w), int(y*h),
             hasMouse))
        self.deltaText.setText("Delta: {0}, {1}".format(
             int(dx*w), int(dy*h)))
                        '''
        # MOVE SPHERE
        print 'check'
        print self.moveX
        print w
        print self.moveY

        w1 = w /800
        h1 = h /400
        self.moveX += dx * 1 * self.mouseMagnitude
        self.moveY += dy * 1 * self.mouseMagnitude
        if self.moveX >= (0.8 * w1):
            self.moveX = (0.8 * w1)
            self.val = 1
        elif self.moveX <= (-0.8 * w1):
            self.moveX = (-0.8 * w1)
            self.val = 2
        elif self.moveX >= w1/2.5 or self.moveX <= (-1 * w1)/2.5:
            self.val = 5
        else:
            self.val = 0
        if self.moveY >= (0.8 * h1):
            self.moveY = (0.8 * h1)
            self.val1 = 3
        elif self.moveY <= (-0.8 * h1):
            self.moveY = (-0.8 * h1)
            self.val1 = 4
        elif self.moveY >= h1/2.5 or self.moveY <= (-1 * h1)/2.5:
            self.val1 = 5
        else:
            self.val1 = 0
        # print error on the screen
        self.mouseText.setText("Status: {0}".format(
             self.alarm(self.val, self.val1)))
        self.model.setPos(self.moveX, -1, self.moveY)
        return Task.cont


'''
# Initialize the scene.
ShowBase()

# Initialize the collision traverser.
base.cTrav = CollisionTraverser()

# Initialize the Pusher collision handler.
pusher = CollisionHandlerPusher()

# Load a model.
smiley = loader.loadModel('smiley')


#base.disableMouse()
if base.mouseWatcherNode.hasMouse():
    print 'hi'
    x = base.mouseWatcherNode.getMouseX()
    y = base.mouseWatcherNode.getMouseY()


# Reparent the model to the camera so we can move it.
smiley.reparentTo(camera)
# Set the initial position of the model in the scene.
smiley.setPos(0, 25.5, 0.5)

# Create a collision node for this object.
cNode = CollisionNode('smiley')
# Attach a collision sphere solid to the collision node.
cNode.addSolid(CollisionBox((0, 0, 0),(1,1,1)))
# Attach the collision node to the object's model.
smileyC = smiley.attachNewNode(cNode)
# Set the object's collision node to render as visible.
smileyC.show()

# Load another model.
frowney = loader.loadModel('frowney')
# Reparent the model to render.
frowney.reparentTo(render)
# Set the position of the model in the scene.
frowney.setPos(5, 25, 0)

# Create a collsion node for this object.
cNode = CollisionNode('frowney')
# Attach a collision sphere solid to the collision node.
cNode.addSolid(CollisionBox((0, 0, 0), (1, 1, 1)))
# Attach the collision node to the object's model.
frowneyC = frowney.attachNewNode(cNode)
# Set the object's collision node to render as visible.
frowneyC.show()

# Add the Pusher collision handler to the collision traverser.
base.cTrav.addCollider(frowneyC, pusher)
# Add the 'frowney' collision node to the Pusher collision handler.
pusher.addCollider(frowneyC, frowney, base.drive.node())

# Have the 'smiley' sphere moving to help show what is happening.
frowney.posInterval(5, Point3(5, 25, 0), startPos=Point3(-5, 25, 0), fluid=1).loop()

# Run the scene. Move around with the mouse to see how the moving sphere changes
# course to avoid the one attached to the camera.
#base.run()
'''
app = App()
app.run()
