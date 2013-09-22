import cairo
from math import pi
from collections import OrderedDict

def expandString(string, rule_dict):
    new_string = ""
    for character in string:
        new_string += rule_dict.get(character, character)
    return new_string

def iterateExpandString(string, rule_dict, n):
    for x in range(n):
        string = expandString(string, rule_dict)
    return string

bool = 1
def bracketStroke(ctx):
    ctx.save()
    if (ctx.has_current_point and bool): ctx.stroke()
    ctx.restore()

scale = 0.8
location_list = []
colors_list = [(57/256., 27/256., 57/256., 1)]
def push_ctx(ctx):
    location_list.append(ctx.get_current_point())
    rgba = tuple(c/scale for c in colors_list[-1][0:3]) + (colors_list[-1][3]*scale,)
    colors_list.append(rgba)
    ctx.set_line_width(ctx.get_line_width()*scale)
    ctx.save()
    
def pop_ctx(ctx):
    bracketStroke(ctx)
    ctx.restore()
    ctx.move_to(*location_list.pop())
    ctx.set_source_rgba(*colors_list.pop())
    ctx.set_line_width(ctx.get_line_width()/scale)

class CairoRenderer(object):
    def __init__(self, startString, rules, render_rules, x_start, y_start):
        self.startString = startString
        self.rules = rules
        self.render_rules = render_rules
        self.x_start = x_start 
        self.y_start = y_start
        
    def renderSVG(self, niterations):
        # Expand the string out
        self.instructions = iterateExpandString(self.startString, self.rules, niterations)
        #print self.instructions

        # initilize the cairo bullshitzen
        width, height = (512, 512)
        surface = cairo.SVGSurface(open("test.svg", "w"), width, height)
        ctx = cairo.Context(surface)

        ctx.identity_matrix()
        ctx.set_line_width(6.0)
        ctx.set_source_rgba(57/256., 27/256., 57/256., 1)
        ctx.move_to(self.x_start, self.y_start)

        # Magic
        for character in self.instructions:
            string_to_run = self.render_rules[character]
            # print string_to_run
            eval(string_to_run)
            
        surface.finish()
        return ctx.path_extents()

    def NOrenderSVG(self, niterations):
        global bool 
        bool = 0
        extents = self.renderSVG(niterations)
        bool = 1
        return extents

if __name__ == "__main__":
    val = int(raw_input("Number of Iterations: "))

    d = {"X":"F[+X]F[-X]+X",
         "F":"FF"}

    start_string = "|X"

    angle_in_rad = str(20 * pi / 180)
    unit = 100.0

    render_rules = {"F":"ctx.rel_line_to(%f,0)" % unit,
                    "X":"ctx.rel_line_to(%f,0)" % 0.0,
                    "[":"push_ctx(ctx)",
                    "]":"pop_ctx(ctx)",
                    "-":"ctx.rotate(-%s)" % angle_in_rad,
                    "+":"ctx.rotate(+%s)" % angle_in_rad,
                    "|":"ctx.rotate(-%f)" % (pi/2.0)}

    cr = CairoRenderer(start_string, d, render_rules, 0.0, 0.0)
    xmin, ymin, xmax, ymax = cr.NOrenderSVG(int(val))
    x_extent = xmax - xmin
    y_extent = ymax - ymin
    
    # Compute the scale and rescale unit
    scale_factor = 0.9*min(512.0 / x_extent, 512.0 / y_extent)
    unit = unit * scale_factor

    # Compute new value for recentering
    x_0 = (512.0 - (xmin+xmax)* scale_factor)/2.
    y_0 = (512.0 - (ymin+ymax)* scale_factor)/2.

    render_rules = {"F":"ctx.rel_line_to(%f,0)" % unit,
                    "X":"ctx.rel_line_to(%f,0)" % 0.0,
                    "[":"push_ctx(ctx)",
                    "]":"pop_ctx(ctx)",
                    "-":"ctx.rotate(-%s)" % angle_in_rad,
                    "+":"ctx.rotate(+%s)" % angle_in_rad,
                    "|":"ctx.rotate(-%f)" % (pi/2.0)}

    cr = CairoRenderer(start_string, d, render_rules, y_0, x_0)
    ctx = cr.renderSVG(int(val))
