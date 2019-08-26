import numpy as np
from math import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.widgets import Slider

import frame


class RobotSixAxis:
    def __init__(self, d, theta, a, alpha, m):
        self.d = d
        self.theta = theta
        self.a = a
        self.alpha = alpha
        self.m = m

    @staticmethod
    def matrix_from_DH(DH_list):
        d, theta, a, alpha = DH_list
        return np.asarray([[cos(theta), -sin(theta) * cos(alpha), sin(theta) * sin(alpha), a * cos(theta)],
                           [sin(theta), cos(theta) * cos(alpha), -cos(theta) * sin(alpha), a * sin(theta)],
                           [0., sin(alpha), cos(alpha), d],
                           [0., 0., 0., 1.]], dtype=np.float32)

    @property
    def T(self):
        transformations = np.empty(shape=[6, 4, 4], dtype=np.float32)
        for i in range(6):
            transformations[i] = self.matrix_from_DH([self.d[i], self.theta[i], self.a[i], self.alpha[i]])
        return transformations

    @property
    def frames(self):
        frames = [frame.world_xy]
        for i in range(6):
            frames.append(frames[i] * self.T[i])
        return frames

    def get_tool_frame(self, tool):
        return self.frames[-1] * self.matrix_from_DH(tool)

    def torque(self, tool, payload, acceleration):
        moments = []
        for i in range(6):
            f = self.frames[i]
            moment = 0.
            for j in range(i+1, 6): # calculate gravitational moment on each axis
                moment += f.get_moment_with_z(self.frames[j].origin[:3], np.array([0., 0., -self.m[j]*9.8]))
            moment += f.get_moment_with_z(self.get_tool_frame(tool).origin[:3], np.array([0., 0., -payload*9.8]))
            # consider acceleration
            I = 0
            for j in range(i+1, 6):
                dis = self.frames[i].get_distance_with_z(self.frames[j].origin[:3])
                I += self.m[j] * dis * dis
            dis_tool = self.frames[i].get_distance_with_z(self.get_tool_frame(tool).origin[:3])
            I += payload * dis_tool * dis_tool
            moment = abs(moment) + I * acceleration[i]
            # __consider acceleration
            moments.append(moment)
        return moments

    def visualization(self, tool, payload, acceleration):
        def draw_frame(f):
            ax.plot_wireframe(np.array([f.origin_x, f.origin_x + 0.05 * f.axis_z[0]]),
                              np.array([f.origin_y, f.origin_y + 0.05 * f.axis_z[1]]),
                              np.array([[f.origin_z, f.origin_z + 0.05 * f.axis_z[2]]]), color="red")
            ax.plot_wireframe(np.array([f.origin_x, f.origin_x + 0.05 * f.axis_x[0]]),
                              np.array([f.origin_y, f.origin_y + 0.05 * f.axis_x[1]]),
                              np.array([[f.origin_z, f.origin_z + 0.05 * f.axis_x[2]]]), color="blue")
        def plot():
            ax.set_xlim([-0.3, 0.3])
            ax.set_ylim([-0.3, 0.3])
            ax.set_zlim([-0.3, 0.3])
            X, Y, Z = [], [], []
            for i in range(7):
                f = self.frames[i]
                X.append(f.origin_x)
                Y.append(f.origin_y)
                Z.append(f.origin_z)
                if i < 6:
                    ax.text(f.origin_x, f.origin_y, f.origin_z, str(round(self.torque(tool, payload, acceleration)[i], 1)), None)
                draw_frame(f)
            tool_frame = self.get_tool_frame(tool)
            draw_frame(tool_frame)
            ax.plot_wireframe(np.asarray(X), np.asarray(Y), np.asarray([Z]))
            ax.scatter(X, Y, Z, c="red", marker="o")
            ax.scatter(tool_frame.origin_x, tool_frame.origin_y, tool_frame.origin_z, c="blue", marker="o")

        figure = plt.figure()
        ax = figure.add_subplot(111, projection="3d")
        # ax.text(0, 0, 0, "asdas", None)
        # f = self.frames[2]
        # ax.text(f.origin_x, f.origin_y, f.axis_z, str(round(self.torque(tool, payload)[2], 1)), None)
        plot()

        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_zlabel("z")

        axamp1 = plt.axes([0.15, .06, 0.1, 0.02])
        samp1 = Slider(axamp1, 'axis_1', -pi, pi, valinit=0)
        axamp2 = plt.axes([0.45, .06, 0.1, 0.02])
        samp2 = Slider(axamp2, 'axis_2', -pi, pi, valinit=0)
        axamp3 = plt.axes([0.75, .06, 0.1, 0.02])
        samp3 = Slider(axamp3, 'axis_3', -pi, pi, valinit=0)
        axamp4 = plt.axes([0.15, .03, 0.1, 0.02])
        samp4 = Slider(axamp4, 'axis_4', -pi, pi, valinit=0)
        axamp5 = plt.axes([0.45, .03, 0.1, 0.02])
        samp5 = Slider(axamp5, 'axis_5', -pi, pi, valinit=0)
        axamp6 = plt.axes([0.75, .03, 0.1, 0.02])
        samp6 = Slider(axamp6, 'axis_6', -pi, pi, valinit=0)


        def update(val):
            # amp is the current value of the slider
            self.theta[0] = samp1.val
            self.theta[1] = samp2.val
            self.theta[2] = samp3.val
            self.theta[3] = samp4.val
            self.theta[4] = samp5.val
            self.theta[5] = samp6.val
            # update curve
            ax.clear()
            plot()
            # redraw canvas while idle
            figure.canvas.draw_idle()

        samp1.on_changed(update)
        samp2.on_changed(update)
        samp3.on_changed(update)
        samp4.on_changed(update)
        samp5.on_changed(update)
        samp6.on_changed(update)

        plt.show()

