import cairo

i = cairo.ImageSurface(cairo.FORMAT_A8, 500, 500)
s = cairo.Context(i)

s.move_to(5,5)
