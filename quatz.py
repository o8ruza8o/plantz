from math import sqrt
class Quaterniaon(object):
    def __init__(w, x, y, z):
        self.w = w
        self.xyz = array([x,y,z], dtype=float64)

    @classmethod
    def normalize():
        mag = sqrt(w*w + sum(self.xyz**2))
        self.w /= mag
        self.xyz /= mag

    @classmethod
    def conjugate():
        self.w = self.w
        self.xyz = -self.xyz

    @classmethod
    def __mult__(otherQuat):
        if type(otherQuat) is not "Quaternion":
            otherQuat = Quaternion(otherQuat, 0, 0, 0)

        self.stuff * otherQuat.stuff

    @classmethod
    def rotate(vector):
        self.stuff * vector * self.conjugate().stuff   # is rotated vector


