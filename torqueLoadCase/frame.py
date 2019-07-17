import numpy as np
from math import *


class Frame:
    def __init__(self, frame):
        self.mat = frame

    def __mul__(self, other):
        if isinstance(other, Frame):
            return Frame(np.dot(self.mat, other.mat))
        return Frame(np.dot(self.mat, other))

    @property
    def origin(self):
        return np.dot(self.mat, np.array([[0.], [0.], [0.], [1.]])).flatten()

    @property
    def origin_x(self):
        return self.origin[0]

    @property
    def origin_y(self):
        return self.origin[1]

    @property
    def origin_z(self):
        return self.origin[2]

    @property
    def axis_x(self):
        return np.dot(self.mat, np.array([[1.], [0.], [0.], [1.]])).flatten() - self.origin

    @property
    def axis_y(self):
        return np.dot(self.mat, np.array([[0.], [1.], [0.], [1.]])).flatten() - self.origin

    @property
    def axis_z(self):
        return  np.dot(self.mat, np.array([[0.], [0.], [1.], [1.]])).flatten() - self.origin

    def get_distance_with_z(self, position):
        displacement = position - self.origin[:3]
        x = np.dot(displacement, self.axis_x[:3])
        y = np.dot(displacement, self.axis_y[:3])
        return sqrt(x*x+y*y)

    def get_moment_with_z(self, position, force):
        displacement = position - self.origin[:3]
        moment_temp = np.cross(displacement, force)
        moment = np.dot(moment_temp, self.axis_z[:3])
        return moment

world_xy = Frame(np.eye(4, dtype=np.float32))
