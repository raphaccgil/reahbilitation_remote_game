''' Created on Tue June 20 21:00:00 2016
@author: Raphael Gil
Revision: 0
Creation of a game interface
'''

"""Reahb main file. This module handles a few command line
options and starts the core finite state machine, followed by Panda's task
manager."""

import sys
from panda3d.core import ExecutionEnvironment as EE
from panda3d.core import Filename
'''
from options import options

# If we only need to print version, do this first and leave everything else
# untouched.
if options.print_version:
    try:
        f = Filename(EE.expandString("$MAIN_DIR/VERSION")).toOsSpecific()
        print open(f).read()
    except IOError:
        print "Version unknown. Can't find the VERSION file."
    sys.exit()
'''
from pandac.PandaModules import loadPrcFile
from pandac.PandaModules import Filename
from options import options
# Config file should be loaded as soon as possible.
from pandac.PandaModules import loadPrcFile
#loadPrcFile(Filename.expandFrom("$MAIN_DIR/etc/azure.prc"))

from direct.showbase.ShowBase import ShowBase
from Core import Core



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
        self.core = Core()
        if (options.scenario):
            # Scenario was specified at command line.
            self.core.demand("Loading", options.scenario)
        else:
            print self.core
            self.core.demand("Menu", "MainMenu")

        #base.bufferViewer.toggleEnable()

		# Start the master loop.
        self.run()

if __name__ == "__main__":
    Azure()
    # Related to relative paths.
    #print "Don't run this module directly! Use the run script instead!"
    #sys.exit(2)

