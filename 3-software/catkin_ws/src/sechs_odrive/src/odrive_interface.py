#!/usr/bin/env python3

from __future__ import print_function

import odrive
import time
from odrive.enums import *
from math import pi

import rospy
from sechs_odrive.msg import Sechs_Axes
# from sensor_msgs.msg import Joy


class Sechs:
    def __init__(self):

        # --------------------------
        # find odrives and load axes
        # --------------------------

        odrv0 = odrive.find_any(serial_number="208A3592524B") # 56V axis_1 axis_2
        odrv1 = odrive.find_any(serial_number="2083359F524B") # 24V axis_0
        # odrv2 = None
        self.axes = []
        self.axes.append(odrv1.axis0)
        self.axes.append(odrv0.axis0)
        self.axes.append(odrv0.axis1)

        # ---------------
        # load directions
        # ---------------

        self.directions = []
        for i in range(6):
            self.directions.append(rospy.get_param(("/axis_%d/direction" % i), default=0))

        # ---------------
        # load reductions
        # ---------------

        self.reductions = []
        for i in range(6):
            self.reductions.append(rospy.get_param(("/axis_%d/reduction" % i), default=1.0))
        
        # -------------------------------
        # load control related parameters
        # -------------------------------

        # for i in range(6):
        #     self.axes[i].config.startup_encoder_index_search = True
        #     # ...

        for i in range(0, 3):
            self.axes[i].config.startup_encoder_index_search = rospy.get_param(("/axis_%d/startup_encoder_index_search" % i))
            self.axes[i].motor.config.pre_calibrated = rospy.get_param(("/axis_%d/motor_config/pre_calibrated" % i))
            self.axes[i].motor.config.pole_pairs = rospy.get_param(("/axis_%d/motor_config/pole_pairs" % i))
            self.axes[i].motor.config.current_lim = rospy.get_param(("/axis_%d/motor_config/current_lim" % i))
            self.axes[i].motor.config.calibration_current = rospy.get_param(("/axis_%d/motor_config/calibration_current" % i))
            self.axes[i].motor.config.current_lim_tolerance = rospy.get_param(("/axis_%d/motor_config/current_lim_tolerance" % i))
            self.axes[i].encoder.config.pre_calibrated = rospy.get_param(("/axis_%d/encoder_config/pre_calibrated" % i))
            self.axes[i].encoder.config.cpr = rospy.get_param(("/axis_%d/encoder_config/cpr" % i))
            self.axes[i].encoder.config.use_index = rospy.get_param(("/axis_%d/encoder_config/use_index" % i))
            self.axes[i].controller.config.vel_limit = rospy.get_param(("/axis_%d/controller_config/vel_limit" % i))
            self.axes[i].controller.config.vel_limit_tolerance = rospy.get_param(("/axis_%d/controller_config/vel_limit_tolerance" % i))
            self.axes[i].controller.config.pos_gain = rospy.get_param(("/axis_%d/controller_config/pos_gain" % i))
            self.axes[i].controller.config.vel_gain = rospy.get_param(("/axis_%d/controller_config/vel_gain" % i))
            self.axes[i].controller.config.vel_integrator_gain = rospy.get_param(("/axis_%d/controller_config/vel_integrator_gain" % i))
            self.axes[i].controller.config.control_mode = rospy.get_param(("/axis_%d/controller_config/control_mode" % i))
    
    def start_closed_loop(self):
        for i in range(0, 3):
            self.axes[i].requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL 

    @property
    def axes_value(self):
        sensor_msg = Sechs_Axes()
        for i in range(0, 3):
            sensor_msg.values[i] = self.axes[i].encoder.pos_estimate * pi / 2000.0 / self.reductions[i]
        return sensor_msg
    
    def move_axes(self, values):
        for i in range(0, 3):
            sechs.axes[i].controller.move_to_pos(values[i] * 2000.0 * sechs.reductions[i] / pi)


def callback_pos_command(sechs_axes):
    global sechs
    rospy.loginfo("pos_1: %f", sechs_axes.values[1])
    sechs.move_axes(sechs_axes.values)


rospy.init_node('odrive_interface', anonymous=False)
sechs = Sechs()
sechs.start_closed_loop()

# rospy.loginfo("%f", sechs.axes[1].controller.config.vel_gain)
rospy.Subscriber('Sechs/Position_Command', Sechs_Axes, callback_pos_command)
pub = rospy.Publisher('Sechs/Encoder_Feedback', Sechs_Axes , queue_size=10)

rate = rospy.Rate(100) 
while not rospy.is_shutdown():
    pub.publish(sechs.axes_value)
    rate.sleep()

rospy.spin()
