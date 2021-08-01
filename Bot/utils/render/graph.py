from PIL import Image, ImageDraw
# from operator import itemgetter


def gradient_color(minval, maxval, val, color_palette):
    """ Computes intermediate RGBA color of a value in the range of minval
        to maxval (inclusive) based on a color_palette representing the range.
    """
    max_index = len(color_palette)-1
    delta = maxval - minval
    if delta == 0:
        delta = 1
    v = float(val-minval) / delta * max_index
    i1, i2 = int(v), min(int(v)+1, max_index)
    (r1, g1, b1, a1), (r2, g2, b2, a2) = color_palette[i1], color_palette[i2]
    f = v - i1
    return int(r1 + f*(r2-r1)), int(g1 + f*(g2-g1)), int(b1 + f*(b2-b1)), int(a1 + f*(a2-a1))


def vertical_gradient(image, poly, color_func, color_palette):
    gradient = Image.new("RGBA", image.size)
    draw = ImageDraw.Draw(gradient, "RGBA")

    polymaxy = 1026  # max(poly, key=itemgetter(1))[1]
    polyminy = 200  # min(poly, key=itemgetter(1))[1]
    polymaxx = 2045  # max(poly, key=itemgetter(0))[0]
    polyminx = 335  # min(poly, key=itemgetter(0))[0]
    polyheight = polymaxy - polyminy

    minval, maxval = 1, len(color_palette)
    delta = maxval - minval
    for y in range(polyminy, polymaxy+1):
        f = (y - polyminy) / float(polyheight)
        val = minval + f * delta
        color = color_func(minval, maxval, val, color_palette)
        draw.line([(polyminx, y), (polymaxx, y)], fill=color)

    return gradient


def linear_gradient(image, poly, color_func, color_palette):
    temp = Image.new("RGBA", image.size)
    draw = ImageDraw.Draw(temp)
    draw.polygon(poly, fill=(0, 0, 0, 256), outline=None)

    gradient = vertical_gradient(image, poly, color_func, color_palette)
    temp.paste(gradient.crop(
        (0, 0, temp.size[0], temp.size[1])), mask=temp)

    image.paste(temp, mask=temp)
    # return temp


def gen_point(val_x, val_y, maxd_x=2045):
    space_x = 285
    space_y = 200
    max_y = 4  # from zero
    max_x = 6  # from zero

    margin_x = 335
    margin_y = 230

    if val_x == max_x:
        return (maxd_x, space_y * (max_y - val_y) + margin_y)
    return (space_x * val_x + margin_x, space_y * (max_y - val_y) + margin_y)
