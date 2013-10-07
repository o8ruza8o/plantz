from numpy import *
from classy import ExpandRules

starting_direction = matrix([[1, 0, 0],
                             [0, 1, 0],
                             [0, 0, 1]], dtype=float64)

class RenderingContext(dict):
    def __init__(self, instrucitons, point = zeros((3,1)), mat = starting_direction):
        self.update(instrucitons)
        self.p = point
        self.m = matrix(mat)
        
        self.segments   = []
        self.stateStack = []
        
    def _compute_start_ends(self, length):
        s, e = self.p.copy(), self.p + (self.m * (ones((3,1)) * length))
        # print s
        # print e
        return s, e
        
    def move_to(self, point):
        self.p[:] = point

    def line_rel(self, length):
        start_point, end_point = self._compute_start_ends(length)
        # print start_point, end_point
        self.segments.append((start_point, end_point))
        
        self.p[:] = end_point

    def move_rel(self, length):
        start_point, end_point = self._compute_start_ends(length)
        self.p[:] = end_point
        
    def rotate(self, rx, ry, rz):
        rmx = matrix([[1, 0,       0       ],
                      [0, cos(rx), -sin(rx)],
                      [0, sin(rx),  cos(rx)]])
        rmy = matrix([[cos(ry), 0, sin(ry)],
                      [0,       1, 0      ],
                      [-sin(ry),0, cos(ry)]])
        rmz = matrix([[cos(rz), -sin(rz), 0],
                      [sin(rz),  cos(rz), 0], 
                      [0      ,  0      , 1]])

        self.m *= (rmx * rmy * rmz)


    def save(self):
        self.stateStack.append((self.p.copy(), self.m.copy()))

    def load(self):
        self.p[:], self.m[:] = self.stateStack.pop()


    def renderString(self, instructions):
        # print instructions
        for instruction in instructions:
            # print instruction, instruction in self
            if instruction not in self:
                continue
            eval(self[instruction])


er = ExpandRules("A", {"A":"A[+A+A+A][<A<A<A]"})

    
rr = RenderingContext({"A":"self.line_rel(1)",
                       "[":"self.save()",
                       "]":"self.load()",
                       "-":"self.rotate(-pi/ 6, 0, 0)",
                       "+":"self.rotate( pi/ 6, 0, 0)",
                       "<":"self.rotate(0, -pi/ 6, 0)",
                       ">":"self.rotate(0,  pi/ 6, 0)"})


rr.renderString(er.nIterations(3))

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

for seg in rr.segments:
    xs, ys, zs = array(seg).squeeze().T
    # print xs, ys, zs 
    ax.plot(xs, ys, zs)
fig.show()
raw_input()
