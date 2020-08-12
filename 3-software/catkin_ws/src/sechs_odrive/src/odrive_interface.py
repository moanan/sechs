#!/usr/bin/env python3

from __future__ import print_function

import odrive
import time
from odrive.enums import *
from math import pi

import rospy
from sechs_odrive.msg import *
# from sensor_msgs.msg import Joy


class Sechs:
    def __init__(self):

        # --------------------------
        # find odrives and load axes
        # --------------------------
        
        odrv0 = odrive.find_any(serial_number="208A3592524B") # 56V axis_1 axis_2
        rospy.loginfo("odrive_0 found!")
        odrv1 = odrive.find_any(serial_number="2083359F524B") # 24V_taobao axis_3 axis_4
        rospy.loginfo("odrive_1 found!")
        odrv2 = odrive.find_any(serial_number="385D37803437") # 24V axis_0 
        rospy.loginfo("odrive_2 found!")
        self.axes = []
        self.axes.append(odrv2.axis0)
        self.axes.append(odrv0.axis0)
        self.axes.append(odrv0.axis1)
        self.axes.append(odrv1.axis0)
        self.axes.append(odrv1.axis1)

        # -------------------------------------------
        # load directions, reductions, initial offset
        # -------------------------------------------

        self.directions = []
        self.reductions = []
        self.init_offset = []
        for i in range(6):
            self.directions.append(rospy.get_param(("/axis_%d/direction" % i), default=0))
            self.reductions.append(rospy.get_param(("/axis_%d/reduction" % i), default=1.0))
            self.init_offset.append(rospy.get_param(("/axis_%d/init_offset" % i), default=0.0))
        
        # -------------------------------
        # load control related parameters
        # -------------------------------

        for i in range(0, 5):
            # self.axes[i].config.startup_encoder_index_search = rospy.get_param(("/axis_%d/startup_encoder_index_search" % i))
            # self.axes[i].motor.config.pre_calibrated = rospy.get_param(("/axis_%d/motor_config/pre_calibrated" % i))
            # self.axes[i].motor.config.pole_pairs = rospy.get_param(("/axis_%d/motor_config/pole_pairs" % i))
            self.axes[i].motor.config.current_lim = rospy.get_param(("/axis_%d/motor_config/current_lim" % i))
            self.axes[i].motor.config.calibration_current = rospy.get_param(("/axis_%d/motor_config/calibration_current" % i))
            self.axes[i].motor.config.current_lim_tolerance = rospy.get_param(("/axis_%d/motor_config/current_lim_tolerance" % i))
            # self.axes[i].encoder.config.pre_calibrated = rospy.get_param(("/axis_%d/encoder_config/pre_calibrated" % i))
            # self.axes[i].encoder.config.cpr = rospy.get_param(("/axis_%d/encoder_config/cpr" % i))
            # self.axes[i].encoder.config.use_index = rospy.get_param(("/axis_%d/encoder_config/use_index" % i))
            self.axes[i].controller.config.vel_limit = rospy.get_param(("/axis_%d/controller_config/vel_limit" % i))
            self.axes[i].controller.config.vel_limit_tolerance = rospy.get_param(("/axis_%d/controller_config/vel_limit_tolerance" % i))
            self.axes[i].controller.config.pos_gain = rospy.get_param(("/axis_%d/controller_config/pos_gain" % i))
            self.axes[i].controller.config.vel_gain = rospy.get_param(("/axis_%d/controller_config/vel_gain" % i))
            self.axes[i].controller.config.vel_integrator_gain = rospy.get_param(("/axis_%d/controller_config/vel_integrator_gain" % i))
            # self.axes[i].controller.config.control_mode = rospy.get_param(("/axis_%d/controller_config/control_mode" % i))
            pass
    
    def start_closed_loop(self):
        # rospy.loginfo("start calibration")
        # for i in range(0, 5):
        #     rospy.loginfo("calibrating axis_%d" % i)
        #     self.axes[i].requested_state = AXIS_STATE_ENCODER_INDEX_SEARCH
        #     time.sleep(1)
        for i in range(0, 5):
            rospy.loginfo("axis_%d entering closed loop control!" % i)
            self.axes[i].requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
            time.sleep(1)
        self.home()
    
    def home(self):
        self.move_axes([0.0]*6)

    def close(self):
        self.move_to([-500.0, -500.0, -500.0, -500.0, -500.0, 0.0]) # end pose
        time.sleep(1)
        for i in range(0, 5):
            rospy.loginfo("axis_%d closed!" % i)
            self.axes[i].requested_state = AXIS_STATE_IDLE
            time.sleep(1)

    @property
    def axes_feedback(self):
        sensor_msg = Sechs_State()
        # pos
        for i in range(0, 5):
            sensor_msg.pos.values[i] = (self.axes[i].encoder.pos_estimate + self.init_offset[i]) * pi * self.directions[i] / 2000.0 / self.reductions[i]
        sensor_msg.pos.values[2] -= sensor_msg.pos.values[1]  # joint 2 velocity coupled
        # cur
        for i in range(0, 5):
            sensor_msg.cur.values[i] = self.axes[i].motor.current_control.Iq_measured
        return sensor_msg
    
    def move_to(self, values):
        # count in cpr
        for i in range(0, 5):
            # sechs.axes[i].controller.move_to_pos(values[i])
            sechs.axes[i].controller.pos_setpoint = values[i]

    def move_axes(self, values):
        values_cpr = [0.0] * 6
        for i in range(0, 6):
            if i == 2:  # joint 2 velocity coupled
                values_cpr[i] = (values[i] + values[1]) * 2000.0 * sechs.reductions[i] * self.directions[i] / pi - self.init_offset[i]
            else:
                values_cpr[i] = values[i] * 2000.0 * sechs.reductions[i] * self.directions[i] / pi - self.init_offset[i]
        self.move_to(values_cpr)


def callback_pos_command(pos_command):
    global sechs
    # rospy.loginfo("pos_1: %f", pos_command.values[1])
    sechs.move_axes(pos_command.values)


rospy.init_node('odrive_interface', anonymous=False)
rospy.loginfo("odrive_interface init...")
sechs = Sechs()
sechs.start_closed_loop()

# rospy.loginfo("%f", sechs.axes[1].controller.config.vel_gain)
rospy.Subscriber('Sechs/Position_Command', Sechs_Pos, callback_pos_command)
pub = rospy.Publisher('Sechs/Encoder_Feedback', Sechs_State , queue_size=10)

rate = rospy.Rate(100) 
while not rospy.is_shutdown():
    pub.publish(sechs.axes_feedback)
    rate.sleep()

sechs.close()
# rospy.spin()
