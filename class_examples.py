def serpenski():
    er = ExpandRules("A", {"A":"B-A-B",
                           "B":"A+B+A"})

    rr = RenderRules({"A":"ctx.rel_line_to(10,0)",
                      "B":"ctx.rel_line_to(10,0)",
                      "-":"ctx.rotate(-pi / 3)",
                      "+":"ctx.rotate( pi / 3)"})


    for x in [2,4,6,8,10]:
        rr.renderString(er.nIterations(x), "serpenski/%02i.svg" % x)




def thinger():
    val = 2
    er = ExpandRules("BAAAAAAA", {"A":"B[+BAAAAAA][-BAAAAAA]"})

    unit = 300

    rr = RenderRules({"A":"ctx.rel_line_to(100,0)",
                      "B":"ctx.rel_line_to(100,0)",
                      "[":"push_ctx(ctx)",
                      "]":"pop_ctx(ctx)",
                      "-":"ctx.rotate(-pi / 6)",
                      "+":"ctx.rotate( pi / 5)"})

    rr.renderString(er.nIterations(2), "feather.pdf")


def snowflake():
    val = 4
    unit = 300

    er = ExpandRules("A++A++A", {"A":"A-A++A-A"})

    rr = RenderRules({"A":"ctx.rel_line_to(%f,0)" % (1. * unit / (3**val)),
                      "-":"ctx.rotate(-pi/3)",
                      "+":"ctx.rotate(+pi/3)"})

    rr.renderString(er.nIterations(4), "snowflake.svg")


def hex_flake():
    val = 4
    unit = 300
    er = ExpandRules("A", {"A":"A+B++B-A--AA-B+", 
                           "B":"-A+BB++B+A--A-B"})
    
    rr = RenderRules({"A":"ctx.rel_line_to(%f,0)" % (1. * unit / (3**val)),
                      "B":"ctx.rel_line_to(%f,0)" % (1. * unit / (3**val)),
                      "-":"ctx.rotate(-pi / 3)",
                      "+":"ctx.rotate(+pi / 3)"})

    rr.renderString(er.nIterations(4), "hex-flake.svg")


def p25_c():
    val = 2
    unit = 300
    er = ExpandRules("F", {"F":"FF-[-F+F+F]+[+F-F-F]"})
    
    rr = RenderRules({"F":"ctx.rel_line_to(%f,0)" % (1. * unit / (3**val)),
                      "[":"push_ctx(ctx)",
                      "]":"pop_ctx(ctx)",
                      "-":"ctx.rotate(-22.5 * pi / 180)",
                      "+":"ctx.rotate(+22.5 * pi / 180)"})

    rr.renderString(er.nIterations(4), "pg25-c.svg")

def p25_b():
    val = 2
    unit = 300
    er = ExpandRules("F", {"F":"F[+F]F[-F][F]"})
    
    rr = RenderRules({"F":"ctx.rel_line_to(%f,0)" % (1. * unit / (3**val)),
                      "[":"push_ctx(ctx)",
                      "]":"pop_ctx(ctx)",
                      "-":"ctx.rotate(-20 * pi / 180)",
                      "+":"ctx.rotate(+20 * pi / 180)"})

    rr.renderString(er.nIterations(5), "pg25-b.svg")
