''' Created on Tue June 20 21:00:00 2016
@author: Raphael Gil
Revision: 0
Creation of a kinect interface
'''

from pykinect import nui



#class DATA_READ_KINECT():
#    print 'test'
#    def read_kinect(self):
#        print 'test1'
with nui.Runtime() as kinect:
    print 'test2'
    kinect.skeleton_engine.enabled = True
    while True:
        frame = kinect.skeleton_engine.get_next_frame()
        for skeleton in frame.SkeletonData:
            if skeleton.eTrackingState == nui.SkeletonTrackingState.TRACKED:
                print skeleton


