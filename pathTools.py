from cairo import PATH_MOVE_TO, PATH_LINE_TO, PATH_CURVE_TO, PATH_CLOSE_PATH
from numpy import array

def unpackPath(path):
    pts = []
    lns = []
    for type, points in path:
        if type == PATH_MOVE_TO:
            pts.append(points)
            lns.append(1)
        elif type == PATH_LINE_TO:
            pts.append(points)
            lns.append(1)
        elif type == PATH_CURVE_TO:
            raise NotImplemented("Curves are not imnplementd in the point expander!")
        elif type == PATH_CLOSE_PATH:
            pass

    return array(pts), array(lns)
    

def rootStem(points):
    x, y = points.T
    above = y > 0
    below = y < 0
    return points[below,:], points[above,:]


def pointsStats(points):
    xs, ys = points.T
    
    xmin, ymin, xmax, ymax = xs.min(), ys.min(), xs.max(), ys.max()

    x_mean, y_mean = xs.mean(), ys.mean()

    return xmin, ymin, xmax, ymax, x_mean, y_mean


# # TODO:
# def convexHull(points):
#     dt = scipy.spatial.Delaunay(points)
    
#     to_connect = {}
#     pi1, pi2 = dt.convex_hull
#     for segment in dt.convex_hull:
#         frum_ind, to_ind = segment


