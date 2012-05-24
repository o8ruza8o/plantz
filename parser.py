import cairo
from math import pi, sin, cos
from  collections import OrderedDict

def expandString(string, rule_dict):
    new_string = ""
    for character in string:
        new_string += rule_dict.get(character, character)
    return new_string

def iterateExpandString(string, rule_dict, n):
    for x in range(n):
        string = expandString(string, rule_dict)
    return string

def sign(x):
    return abs(x) / x

def eoo(x):
    if (x % 2) == 0:
        return 1
    else:
        return -1 
    
location_list = []
def push_ctx(ctx):
    location_list.append(ctx.get_current_point())
    ctx.save()

def pop_ctx(ctx):
    ctx.restore()
    ctx.move_to(*location_list.pop())


class CairoRenderer(object):
    def __init__(self, startString, rules, render_rules):
        self.startString = startString
        self.rules = rules
        self.render_rules = render_rules

    def renderSVG(self, niterations, unit):
        # Expand the string out
        self.instructions = iterateExpandString(self.startString, self.rules, niterations)

        #print self.instructions

        # initilize the cairo bullshitzen
        # width, height = (4*8*512, 4*8*512)
        width, height = (512, 512)


        surface = cairo.SVGSurface(open("test.svg", "w"), width, height)
        ctx = cairo.Context(surface)
        print ctx.user_to_device(5,5)

        ctx.identity_matrix()
        ctx.set_line_width(0.1)

        # Calculate the extents we will go to by tracking the path
        angle = 0
        x_lenght = 0
        x_max = x_lenght
        x_min = x_lenght
        y_lenght = 0
        y_max = y_min = y_lenght
        for x in self.instructions:
            if x == '+': angle += pi/3
            elif x == '-': angle += -pi/3
            else:
                x_lenght += unit*cos(angle) 
                y_lenght += unit*sin(angle) 
                if x_lenght > x_max: x_max = x_lenght
                if y_lenght > y_max: y_max = y_lenght
                if x_lenght < x_min: x_min = x_lenght
                if y_lenght < y_min: y_min = y_lenght
        x_start = (width - x_max - x_min) / 2
        y_start = (height - y_max - y_min) / 2
        #ctx.move_to(x_start, y_start)
        ctx.move_to(20, height/2)
        #print "x_lenght", x_lenght, "y_lenght", y_lenght
        print "x_max", x_max, "y_max", y_max
        print "x_min", x_min, "y_min", y_min
        print "x_start", x_start, "y_start", y_start
        # Magic
        for character in self.instructions:
            string_to_run = self.render_rules[character]
            # print string_to_run
            eval(string_to_run)
            
        #print dir(ctx)

        ctx.stroke()
        surface.finish()


if __name__ == "__main__":
    val = int(raw_input("Number of Iterations:"))

    #d = {"F":"FF-[[-F+F+F]+[+F-F-F]]"}
    #d = {"F":"FF[-FF][+FF]"}
    d = {"A":"BB[-BAAAAA][+BAAAAA]BB",
         "B":"BBBB"}
    
    start_string = "BAAAAA"
    
    ninet_deg_in_rad = str(22.5 * pi / 180)

    unit = 50

    render_rules = {"A":"ctx.rel_line_to(%f,0)" % (1. * unit / (4**val)),
                    "B":"ctx.rel_line_to(%f,0)" % (1. * unit / (4**val)),
                    "[":"push_ctx(ctx)",
                    "]":"pop_ctx(ctx)",
                    "-":"ctx.rotate(-%s)" % ninet_deg_in_rad,
                    "+":"ctx.rotate(+%s)" % ninet_deg_in_rad}

    cr = CairoRenderer(start_string, d, render_rules)
    ctx = cr.renderSVG(int(val), unit)
