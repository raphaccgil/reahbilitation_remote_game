''' Created on Tue June 20 21:00:00 2016
@author: Raphael Gil
Revision: 0
Creation of a game interface
'''

import Tkinter
import pygame
import kinect_module
from multiprocessing import Process
import panda3d
from pygame.locals import*
from OpenGL.GL import *
from OpenGL.GLU import *

vertices = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1),
)

edges = (
    (0, 1),
    (0, 3),
    (0, 4),
    (2, 1),
    (2, 3),
    (2, 7),
    (6, 3),
    (6, 4),
    (6, 7),
    (5, 1),
    (5, 4),
    (5, 7),
)

def Cube():
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

#def Esfera():

def main():
    pygame.init()
    display = (1000, 800)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

    glTranslatef(0.0, 0.0, -5)
    glRotatef(0, 0, 0, 0)
    print 'ok'
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        Cube()
        pygame.display.flip()
        pygame.time.wait(1)

if __name__ == '__main__':
    data = kinect_module.DATA_READ_KINECT()
    p1 = Process(target=main)
    p1.start()
    p2 = Process(target=data.read_kinect())
    p2.start()
    p1.join()
    p2.join()
    #Thread(target = test1).start()
    #Thread(target = test2).start()

