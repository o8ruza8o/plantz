import cairo, os
from math import pi

location_list = []
def push_ctx(ctx):
    location_list.append(ctx.get_current_point())
    ctx.save()

def pop_ctx(ctx):
    ctx.restore()
    ctx.move_to(*location_list.pop())

class ExpandRules(dict):
    def __init__(self, startString, expand_rules):
        self.startString  = startString
        self.update(expand_rules)
        self.expansions = {}
        
    def nIterations(self, n):
        if n in self.expansions:
            return expansions[n]

        string = self.startString
        # Todo: seed largest expansion in here . . .
        for x in range(n):
            new_string = ""
            for character in string:
                new_string += self.get(character, character)
            string = new_string
        self.expansions[n] = string
        return string


class RenderRules(dict):
    def __init__(self, render_rules):
        self.update(render_rules)
    
    def calculatePath(self, instructions):
        temp_surf = cairo.ImageSurface(cairo.FORMAT_A8, 1, 1)
        ctx = cairo.Context(temp_surf)

        ctx.move_to(0,0)
        for instruction in instructions:
            if instruction not in self:
                continue
            eval(self[instruction])

        return ctx.copy_path(), ctx.path_extents()

    def renderString(self, instructions, filename, size=(512, 512)):
        path, extents = self.calculatePath(instructions)

        # Do some logic about what kind of image to generate
        name, ext = os.path.splitext(filename)
        ext = ext.lower()[1:]
        if   ext == "png":
            surf = cairo.ImageSurface(cairo.FORMAT_A8, size[0], size[1])
        elif ext == "pdf":
            surf =  cairo.PDFSurface(open(filename, "w"), size[0], size[1])
        elif ext == "svg":
            surf = cairo.SVGSurface(open(filename, "w"), size[0], size[1])
        else:
            raise NotImplementedError("Rendering to filetype '%s' is not supported" % ext)

        # Get a context object
        ctx = cairo.Context(surf)

        # TODO (logic about scale and shift based on path.path_extents()
        xmin, ymin, xmax, ymax = extents
        x_extent = xmax + xmin
        y_extent = ymax + ymin
        x_center, y_center = x_extent/2., y_extent/2.

        scale_factor = min(size[0] / (xmax - xmin), size[0] / (ymax - ymin) )
        ctx.translate(-xmin, -ymin)
        ctx.scale(0.9*scale_factor, 0.9*scale_factor)
        
        ctx.append_path(path)
        ctx.stroke()
        
        surf.finish()

        # I am still confused why the png surface is different . . .
        if ext == "png":
            surf.write_to_png(filename)


if __name__ == "__main__":
    val = 2
    unit = 300
    er = ExpandRules("F", {"F":"F[+F]F[-F][F]"})
    
    rr = RenderRules({"F":"ctx.rel_line_to(%f,0)" % (1. * unit / (3**val)),
                      "[":"push_ctx(ctx)",
                      "]":"pop_ctx(ctx)",
                      "-":"ctx.rotate(-20 * pi / 180)",
                      "+":"ctx.rotate(+20 * pi / 180)"})

    rr.renderString(er.nIterations(5), "pg25-b.svg")

                     
