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

simulationFlag = 1


def maybeStroke(ctx):
    # Check if we have a current point
    if (ctx.has_current_point() and simulationFlag):
        # If so save it, stroke, then move back there
        # so the next code traces forward from it.
        pointBefore = ctx.get_current_point()
        ctx.stroke()
        ctx.move_to(*pointBefore)

scale = 0.7
location_list = []
colors_list = [(0.07, 0.35, 0.12, 1)]
def push_ctx(ctx):
    location_list.append(ctx.get_current_point())
    maybeStroke(ctx)
    # Current rgba can be gotten from ctx.get_source().get_rgba() Refactor?
    rgba = tuple(c / scale for c in colors_list[-1][0:3]) + (colors_list[-1][3]*scale,)
    ctx.set_source_rgba(*rgba)            # <-- This line was missing.  That is what was doofing everything up.
    colors_list.append(rgba)
    ctx.set_line_width(ctx.get_line_width()*scale)
    ctx.save()

def pop_ctx(ctx):
    maybeStroke(ctx)
    ctx.restore()
    ctx.move_to(*location_list.pop())
    ctx.set_source_rgba(*colors_list.pop())
    ctx.set_line_width(ctx.get_line_width()/scale)

class CairoRenderer(object):
    def __init__(self, startString, string_rules, render_rules):
        self.startString  = startString
        self.string_rules = string_rules
        self.render_rules = render_rules

    def expandString(self, niterations):
        return iterateExpandString(self.startString, self.string_rules, niterations)

    def renderSVG(self, niterations):
        # Expand the string out
        instructions = self.expandString(niterations)

        print instructions

        # initilize the cairo bullshitzen
        width, height = (512, 512)
        margin = 20
        surface = cairo.SVGSurface(open("test.svg", "w"), width, height)
        ctx = cairo.Context(surface)

        ctx.identity_matrix()
        ctx.set_line_width(6.0)
        # ctx.set_source_rgba(1, 0, 0, 1)

        # Do an initial context push to set the colors and line-widths etc
        push_ctx(ctx)
        ctx.move_to(width/2, height-margin)

        # Magic
        for character in instructions:
            string_to_run = self.render_rules[character]
            #print character, "-->", string_to_run
            eval(string_to_run)

        # Do a final pop to clean up the last path ends.
        pop_ctx(ctx)

        surface.finish()
        return ctx.path_extents()

    def NOrenderSVG(self, niterations):
        global simulationFlag
        simulationFlag = 0
        extents = self.renderSVG(niterations)
        simulationFlag = 1
        return extents



def makeSomeRules(length, angle):
    rules = {"A":"ctx.rel_line_to(%f,0)" % length,
             "B":"ctx.rel_line_to(%f,0)" % length,
             "[":"push_ctx(ctx)",
             "]":"pop_ctx(ctx)",
             "-":"ctx.rotate(%f)" % -angle,
             "+":"ctx.rotate(%f)" % angle,
             "|":"ctx.rotate(%f)" % -(pi/2.0)}
    return rules


if __name__ == "__main__":
    val = int(raw_input("Number of Iterations: "))

    # string_rules = {"F":"FF-[[-F+F+F]+[+F-F-F]]"}
    # string_rules = {"F":"FF[-FF][+FF]", "|":"|"}

    string_rules = {"A":"BB[-BAAAAA][+BAAAAA]BB",
                   "B":"BBBB"}

    start_string = "|BAAAAA"
    #start_string = "|F"

    angle_in_rad = 22.5 * pi / 180
    unit = 1.0

    render_rules = makeSomeRules(unit, angle_in_rad)

    # render_rules = {"F":"ctx.rel_line_to(%f,0)" % unit,
    #                 "[":"push_ctx(ctx)",
    #                 "]":"pop_ctx(ctx)",
    #                 "-":"ctx.rotate(-%s)" % angle_in_rad,
    #                 "+":"ctx.rotate(+%s)" % angle_in_rad,
    #                 "|":"ctx.rotate(-%f)" % (pi/2.0)}


    # Make a
    cr = CairoRenderer(start_string, string_rules, render_rules)
    ex = cr.NOrenderSVG(int(val))
    rescale = max(ex[2] - ex[0], ex[3] - ex[1])
    unit = unit * (512 - 40) / rescale

    render_rules = makeSomeRules(unit, angle_in_rad)
    cr = CairoRenderer(start_string, string_rules, render_rules)
    ctx = cr.renderSVG(int(val))
