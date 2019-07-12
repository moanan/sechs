from math import *
import numpy as np
import robot
import frame


# set DH params(data from ur3)
d = [0.1519, 0., 0., 0.11235, 0.08535, 0.0819]
theta = [0., 0., 0., 0., 0., 0.]
a = [0., -.24365, -.21325, 0., 0., 0.]
alpha = [0.5*pi, 0., 0., 0.5*pi, -0.5*pi, 0]
# set mass (kg)
m = [2.5, 2.0, 2.0, 1.5, 1.3, 1.0]

# define robot
_robot = robot.RobotSixAxis(d, theta, a, alpha, m)

# define tool
tool = [0.1, 0., 0., 0.]

# set payload (kg)
payload = 3.

# set speed (m/s)
speed = 1.

# set angular acceleration (rad/s)
acceleration = 1.*pi

# for frame in _robot.frames:
#     print(np.round(frame.mat, 2))
# print(np.round((_robot.frames[-1] * robot.RobotSixAxis.matrix_from_DH(tool)).axis_y))
print(np.round(_robot.torque(tool, payload, 0), 1))
print(np.round(_robot.torque(tool, payload, acceleration), 1))

_robot.visualization(tool, payload, acceleration)




