#!/usr/bin/env python3

from visual_kinematics import Robot
from visual_kinematics import Frame
import numpy as np
from math import pi


def main():
    np.set_printoptions(precision=3, suppress=True)

    dh_params = np.array([[0.112, 0., 0., 0.],
                          [0., -0.5 * pi, 0., -0.5 * pi],
                          [-0.0525, 0.5 * pi, 0.2, 0.],
                          [0.2, 0., 0., 0.5 * pi],
                          [0.085, 0., 0., -0.5 * pi],
                          [0.08, 0., 0., 0.5 * pi]])

    robot = Robot(dh_params, dh_type="modified", plot_xlim=[-0.3, 0.3], plot_ylim=[-0.3, 0.3], plot_zlim=[0., 0.6])

    trajectory = []
    trajectory.append(Frame.from_euler_3(np.array([1.0 * pi, 0., pi]), np.array([[0.12], [-0.08], [0.33]])))
    trajectory.append(Frame.from_euler_3(np.array([0.5 * pi, 0., pi]), np.array([[0.08], [-0.08], [0.33]])))
    trajectory.append(Frame.from_euler_3(np.array([0.25 * pi, 0., 0.75 * pi]), np.array([[0.08], [-0.08], [0.43]])))
    trajectory.append(Frame.from_euler_3(np.array([0.5 * pi, 0., pi]), np.array([[0.12], [-0.08], [0.43]])))

    inter_values = robot.interpolate(trajectory, 5000, motion="p2p")
    np.savetxt("path.txt", inter_values)
    # print(inter_values)

    robot.show_trajectory(trajectory, motion="lin")


if __name__ == "__main__":
    main()
