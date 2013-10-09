from math import sqrt
from numpy import *

class Quaternion(object):
    def __init__(self, w, x, y, z):
        self.wxyz = array([w, x,y,z], dtype=float64)
        self.w = self.wxyz[0:1]
        self.xyz = self.wxyz[1:4]
# this does not work as i expected it to. say this sequesnce of commands:
# q = Quaternon(1, 2, 3, 4)
# q.z = 5
# q.xyz
# outputs [2, 3, 4] not [2, 3, 5]
        self.x = self.wxyz[1:2]
        self.y = self.wxyz[2:3]
        self.z = self.wxyz[3:4]

    def normalize(self):
        mag = sqrt(dot(self.wxyz, self.wxyz))
        self.wxyz /= mag

    @classmethod
    def conjugate():
        self.w[:] = self.w
        self.xyz[:] = -self.xyz

    @classmethod
    def __mult__(otherQuat):
# gives error: unsupported operand type(s) for *: 'Quaternion' and 'Quaternion'
        if type(otherQuat) is not "Quaternion":
            otherQuat = Quaternion(otherQuat, 0, 0, 0)

        w0, x0, y0, z0 = self.wxyz
        w1, x1, y1, z1 = otherQuat.wxyz
        return array([-x1*x0 - y1*y0 - z1*z0 + w1*w0,
                       x1*w0 + y1*z0 - z1*y0 + w1*x0,
                      -x1*z0 + y1*w0 + z1*x0 + w1*y0,
                       x1*y0 - y1*x0 + z1*w0 + w1*z0], dtype=float64)

    @classmethod                # applies the q-rotation to vector
    def rotate(vector):
        vecQuat = Quaternion(0, vector)
        product = self * vecQuat * self.conjugate() # rotated vecQuat
 
	return product.xyz

