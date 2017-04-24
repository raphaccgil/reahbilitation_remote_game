''' Created on Tue June 20 21:00:00 2016
@author: Raphael Gil
Revision: 0.1
Creation of a game interface
'''

"""Reahb main file. This module handles a few command line
options and starts the core finite state machine, followed by Panda's task
manager."""

from direct.showbase.ShowBase import ShowBase
from Core import Xcore
import store_variable as st

class Azure(ShowBase):

    def __init__(self):
        """Program entry point."""
        # TODO(Nemesis#13): rewrite ShowBase to not use globals.

        # This basically sets up our rendering node-tree, some builtins and
        # the master loop (which iterates each frame).
        ShowBase.__init__(self)

        # Turn off Panda3D's standard camera handling.
        self.disableMouse()
        self.setBackgroundColor(0.2, 0.2, 0.2)

        # Start our Core Finite State Machine
        self.core = Xcore()

        # change state is here?
        print 'check flag here'
        print st.flag1

        # Define transitions
        self.run()

if __name__ == "__main__":
    Azure()
    # Related to relative paths.
    #print "Don't run this module directly! Use the run script instead!"
    #sys.exit(2)

