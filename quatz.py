from math import sqrt
from numpy import *

class Quaternion(object):
    def __init__(self, w, x, y, z):
        self.wxyz = array([w, x,y,z], dtype=float64)
        self.w = self.wxyz[0:1]
        self.xyz = self.wxyz[1:4]
        self.x = self.wxyz[1:2]
        self.y = self.wxyz[2:3]
        self.z = self.wxyz[3:4]
        # must do assignment with [:]

    def normalize(self):
        mag = sqrt(dot(self.wxyz, self.wxyz))
        self.wxyz /= mag

    def conjugate(self):
        self.w[:] = self.w
        self.xyz[:] = -self.xyz
        return self

    def __mul__(self, otherQuat):
        if type(otherQuat) is not Quaternion:
            otherQuat = Quaternion(otherQuat, 0, 0, 0)

        w0, x0, y0, z0 = self.wxyz
        w1, x1, y1, z1 = otherQuat.wxyz
        return Quaternion(-x1*x0 - y1*y0 - z1*z0 + w1*w0,
                           x1*w0 + y1*z0 - z1*y0 + w1*x0,
                          -x1*z0 + y1*w0 + z1*x0 + w1*y0,
                           x1*y0 - y1*x0 + z1*w0 + w1*z0)

    __rmul__ = __mul__          # ????? check the logic here !!!!!
    # something like this is needed or int/float * Quat is not defined
    # but the operaion is not commutative so lmul != rmul except when
    # one of the factors is an int/float

    # applies the q-rotation to vector
    def rotate(self, vector):
        vecQuat = Quaternion(0, vector[0], vector[1], vector[2])
        return (self * vecQuat * self.conjugate()).xyz

