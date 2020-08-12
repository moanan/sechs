#!/usr/bin/env python3

import tkinter as tk
import rospy
import rospkg
import time
import numpy as np

from sechs_odrive.msg import Sechs_Axes

# ===============
# load path
# ===============

path = np.loadtxt(rospkg.RosPack().get_path("sechs_gui")+"/src/path.txt")

# =================
# ROS communication
# =================

rospy.init_node('offline', anonymous=False)
PUB = rospy.Publisher('Sechs/Position_Command', Sechs_Axes , queue_size=10)

VALUES_SET = Sechs_Pos()

def pub(values):
    for i in range(6):
        VALUES_SET.values[i] = values[i]
    PUB.publish(VALUES_SET)


pub(path[0])
rospy.sleep(0.1)
pub(path[0])
rospy.sleep(10)

for i in range(path.shape[0]):
    pub(path[i])
    rospy.sleep(0.002)

rospy.sleep(10)
pub([0.0]*6)
