# https://www.universal-robots.com/how-tos-and-faqs/faq/ur-faq/parameters-for-calculations-of-kinematics-and-dynamics-45257/

from math import *
import numpy as np
import robot
import frame


# set DH params(data from ur3)
d = [0.03, 0., 0.06, 0., 0., 0.]
theta = [0., -0.5*pi, 0., 0., 1.5*pi, 0.]
a = [0., 0.2, 0.2, 0.1, 0., 0.]
alpha = [0.5*pi, 0., -0.5*pi, 0.5*pi, 0.5*pi, 0.]
# set mass (kg)
m = [2., 2., 2., 1.5, 0.6, 0.5]

# define robot
_robot = robot.RobotSixAxis(d, theta, a, alpha, m)

# define tool
tool = [0.1, 0., 0., 0.]	# DH

# set payload (kg)
payload = 1.5

# set speed (m/s)
speed = 1.

# set angular acceleration (rad/s)
acceleration = [0.5*pi, 0.5*pi, 1*pi, 0.5*pi, 0.5*pi, 0.5*pi]

# for frame in _robot.frames:
#     print(np.round(frame.mat, 2))
# print(np.round((_robot.frames[-1] * robot.RobotSixAxis.matrix_from_DH(tool)).axis_y))
# print(np.round(_robot.torque(tool, payload, 0), 1))
# print(np.round(_robot.torque(tool, payload, acceleration), 1))

_robot.visualization(tool, payload, acceleration)




