#!/usr/bin/env python3

from __future__ import print_function

import odrive
import time
from odrive.enums import *
# from math import pi

import rospy
from sechs_odrive.msg import Position_Command
# from sensor_msgs.msg import Joy


class Sechs:
    def __init__(self):

        # --------------------------
        # find odrives and load axes
        # --------------------------

        odrv0 = odrv0 = odrive.find_any(serial_number="208A3592524B") # 56V
        # odrv1 = odrive.find_any(serial_number="2083359F524B") # 24V
        # odrv2 = None
        self.axes = []
        self.axes.append(odrv0.axis0)
        self.axes.append(odrv0.axis1)
        # axes.append(odrv1.axis0)
        # axes.append(odrv1.axis1)
        # axes.append(odrv2.axis0)
        # axes.append(odrv2.axis1)

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

        i = 1
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


def callback_pos_command(pos_command):
    rospy.loginfo("pos_1: %f", pos_command.pos[1])


rospy.init_node('odrive_interface', anonymous=False)
sechs = Sechs()

# rospy.loginfo("%f", sechs.axes[1].controller.config.vel_gain)
rospy.Subscriber('Sechs/Position_Command', Position_Command, callback_pos_command)
rospy.spin()
