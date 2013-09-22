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

scale = 0.9
location_list = []
colors_list = [(0.07, 0.35, 0.12, 1)]
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
    def __init__(self, startString, rules, render_rules):
        self.startString = startString
        self.rules = rules
        self.render_rules = render_rules
        
    def renderSVG(self, niterations):
        # Expand the string out
        self.instructions = iterateExpandString(self.startString, self.rules, niterations)
        #print self.instructions

        # initilize the cairo bullshitzen
        width, height = (512, 512)
        margin = 20
        surface = cairo.SVGSurface(open("test.svg", "w"), width, height)
        ctx = cairo.Context(surface)

        ctx.identity_matrix()
        ctx.set_line_width(6.0)
        ctx.set_source_rgba(0.07, 0.35, 0.12, 1)
        ctx.move_to(width/2, height-margin)

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

    #d = {"F":"FF-[[-F+F+F]+[+F-F-F]]"}
    #d = {"F":"FF[-FF][+FF]", "|":"|"}
    d = {"A":"BB[-BAAAAA][+BAAAAA]BB",
         "B":"BBBB"}

    start_string = "|BAAAAA"
    #start_string = "|F"

    angle_in_rad = str(22.5 * pi / 180)
    unit = 100.0

    render_rules = {"A":"ctx.rel_line_to(%f,0)" % (1. * unit / (4**val)),
                    "B":"ctx.rel_line_to(%f,0)" % (1. * unit / (4**val)),
                    "[":"push_ctx(ctx)",
                    "]":"pop_ctx(ctx)",
                    "-":"ctx.rotate(-%s)" % angle_in_rad,
                    "+":"ctx.rotate(+%s)" % angle_in_rad,
                    "|":"ctx.rotate(-%f)" % (pi/2.0)}

    # render_rules = {"F":"ctx.rel_line_to(%f,0)" % unit,
    #                 "[":"push_ctx(ctx)",
    #                 "]":"pop_ctx(ctx)",
    #                 "-":"ctx.rotate(-%s)" % angle_in_rad,
    #                 "+":"ctx.rotate(+%s)" % angle_in_rad,
    #                 "|":"ctx.rotate(-%f)" % (pi/2.0)}

    cr = CairoRenderer(start_string, d, render_rules)
    ex = cr.NOrenderSVG(int(val))
    rescale = max(ex[2] - ex[0], ex[3] - ex[1])
    unit = unit*(512-40)/rescale
    render_rules = {"A":"ctx.rel_line_to(%f,0)" % (1. * unit / (4**val)),
                    "B":"ctx.rel_line_to(%f,0)" % (1. * unit / (4**val)),
                    "[":"push_ctx(ctx)",
                    "]":"pop_ctx(ctx)",
                    "-":"ctx.rotate(-%s)" % angle_in_rad,
                    "+":"ctx.rotate(+%s)" % angle_in_rad,
                    "|":"ctx.rotate(-%f)" % (pi/2.0)}

    cr = CairoRenderer(start_string, d, render_rules)
    ctx = cr.renderSVG(int(val))
