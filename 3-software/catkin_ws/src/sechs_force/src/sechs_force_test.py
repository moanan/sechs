#!/usr/bin/env python3

import tkinter as tk
import rospy
import time

from sechs_odrive.msg import *


def callback_feedback(feedback):
    global count_after_start, interrupt
    count_after_start += 1
    for i in range(6):
        CUR_VALUES[i] = feedback.cur.values[i]
    if count_after_start > 150:
        if abs(CUR_VALUES[3]) > 3.:
            rospy.loginfo("force sensed now!")
            interrupt = True
            pub(value_0)
            count_after_start = 0


rospy.init_node("force_test", anonymous=False)
rospy.Subscriber('Sechs/Encoder_Feedback', Sechs_State, callback_feedback)
PUB = rospy.Publisher('Sechs/Position_Command', Sechs_Pos , queue_size=10)

VALUES_SET = Sechs_Pos()
CUR_VALUES = [0., 0., 0., 0., 0., 0.]

def pub(values):
    for i in range(6):
        VALUES_SET.values[i] = values[i]
    PUB.publish(VALUES_SET)

value_0 = [0., 0., 0., -1.57, 0., 0.]
value_1 = [0., 0., 0., 0., 0., 0.]

count_after_start = 0
interrupt = False

while not rospy.is_shutdown():
    if not interrupt:
        pub(value_0)
        count_after_start = 0
        rospy.sleep(4)
    else:
        count_after_start = 0
        rospy.sleep(2)
        interrupt = False
        continue
    if not interrupt:
        pub(value_1)
        count_after_start = 0
        rospy.sleep(4)
    else:
        count_after_start = 0
        rospy.sleep(2)
        interrupt = False
        continue
