# Serpenski
d = {"A":"B-A-B",
     "B":"A+B+A"}

start_string = "A"

sixty_deg_in_rad = str(pi / 3)

render_rules = {"A":"rel_line_to(10,0)",
                "B":"rel_line_to(10,0)",
                "-":"rotate(-%s)" % sixty_deg_in_rad,
                "+":"rotate(+%s)" % sixty_deg_in_rad}
                    


# Snowflake:

d = {"A":"A-A++A-A"}

start_string = "A++A++A"
#start_string = "A"

sixty_deg_in_rad = str(pi / 3)

unit = 300

render_rules = {"A":"rel_line_to(%f,0)" % (1. * unit / (3**val)),
                "-":"rotate(-%s)" % sixty_deg_in_rad,
                "+":"rotate(+%s)" % sixty_deg_in_rad}

# Hex Flake

d = {"A":"A+B++B-A--AA-B+", 
     "B":"-A+BB++B+A--A-B"}

start_string = "A"

sixty_deg_in_rad = str(pi / 3)

unit = 300

render_rules = {"A":"rel_line_to(%f,0)" % (1. * unit / (3**val)),
                "B":"rel_line_to(%f,0)" % (1. * unit / (3**val)),
                "-":"rotate(-%s)" % sixty_deg_in_rad,
                "+":"rotate(+%s)" % sixty_deg_in_rad}



# Cube Flake
d = {"F":"F+FF-FF-F-F+F+FF-F-F+F+FF+FF-F"}
    
start_string = "F-F-F-F"

ninet_deg_in_rad = str(pi / 2)

unit = 300

render_rules = {"A":"rel_line_to(%f,0)" % (1. * unit / (3**val)),
                "F":"rel_line_to(%f,0)" % (1. * unit / (3**val)),
                "-":"rotate(-%s)" % ninet_deg_in_rad,
                "+":"rotate(+%s)" % ninet_deg_in_rad}
