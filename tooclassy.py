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
        # Todo: line width as a function of x
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
        self.size = 1
        
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

        # Logic about scale and shift based on path.path_extents()
        xmin, ymin, xmax, ymax = extents
        x_extent = xmax - xmin
        y_extent = ymax - ymin
        x_center, y_center = x_extent/2., y_extent/2.
        scale_factor = 0.9*min(size[0] / x_extent, size[1] / y_extent)
        x_rextent, y_rextent = scale_factor*x_extent, scale_factor*y_extent
        x_recenter, y_recenter = (size[0]-x_rextent)/2., (size[1]-y_rextent)/2.
        x_0, y_0 = x_recenter-scale_factor*xmin, y_recenter-scale_factor*ymin
        ctx.move_to(0, y_0)
        ctx.line_to(size[0], y_0)
        
        ctx.set_source_rgb(0.0, 0.0, 0.0)
        ctx.select_font_face("Helvetica",
                cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(20)
        rule_cnt = 0
        ctx.move_to(100, size[1]/10 + rule_cnt*40)
        ctx.show_text("axiom = "+axiom)
        for r in rules: 
            rule_cnt+=1
            ctx.move_to(100, size[1]/10 + rule_cnt*40)
            ctx.show_text(r+u' --> '+rules[r])
        draw_cnt = 0
        for d in draws:
            draw_cnt+=1
            ctx.move_to(100, y_0 + draw_cnt*40)
            if 'rot' in draws[d]:
                ctx.show_text(d+' == rotate for '+draws[d][11:len(draws[d])-1])
            elif 'push' in draws[d]:
                ctx.show_text(d+' == push')
            elif 'pop' in draws[d]:
                ctx.show_text(d+' == pop')
            elif 'line' in draws[d]:
                ctx.show_text(d+' == draw line')
            elif 'scale' in draws[d]:
                if '/' in draws[d]:
                    ctx.show_text(d+' == scale down by '+draws[d][42:len(draws[d])-1])
                if '*' in draws[d]:
                    ctx.show_text(d+' == scale up by '+draws[d][42:len(draws[d])-1])
        ctx.translate(x_0, y_0)
        ctx.scale(scale_factor, scale_factor)
        ctx.append_path(path)
        ctx.stroke()
        surf.finish()

        # I am still confused why the png surface is different . . .
        if ext == "png":
            surf.write_to_png(filename)

if __name__ == "__main__":
    unit = 10
    scale_factor = 1

    axiom = "[|r]a++"
    print "axiom =", axiom
    rules = {"F":"<F>", 
             "a":"F[+x]FFb", 
             "b":"F[-y]Fa", 
             "x":"a", "y":"b", 
             "r":"F[{Fq]FFl", 
             "l":"F[}Fw]FFr", 
             "q":"l", 
             "w":"r"}
    for r in rules: print r, u"\u2192", rules[r]
    draws = {"F":"ctx.rel_line_to(unit,0)",
              "[":"push_ctx(ctx)",
              "]":"pop_ctx(ctx)",
              ">":"ctx.scale(scale_factor/1.36, scale_factor/1.36)",
              "<":"ctx.scale(scale_factor*1.36, scale_factor*1.36)",
              "|":"ctx.rotate(pi)",
              "-":"ctx.rotate(- 3*pi / 8)",
              "+":"ctx.rotate(+ pi / 4)",
              "{":"ctx.rotate(+ pi / 8)",
              "}":"ctx.rotate(- pi / 12)"}
    
    er = ExpandRules(axiom, rules)
    
    rr = RenderRules(draws)

    rr.renderString(er.nIterations(12), "plan12.pdf", size=(1024, 1024))
