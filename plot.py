# -*- coding: utf-8 -*- 

from colorama import init as colorama_init
from colorama import Fore, Back
from termplot.utils import *

def scatter(X, Y, marker=None, color=None, size=(96,24), xlim=None, ylim=None, bgcolor=None, silent=False, fmt='G'):
    COLORMAP = {'fore': {'black': Fore.BLACK,
                       'red': Fore.RED,
                       'green': Fore.GREEN,
                       'yellow': Fore.YELLOW,
                       'blue': Fore.BLUE,
                       'magenta': Fore.MAGENTA,
                       'cyan': Fore.CYAN,
                       'white': Fore.WHITE},
              'back': {'black': Back.BLACK,
                       'red': Back.RED,
                       'green': Back.GREEN,
                       'yellow': Back.YELLOW,
                       'blue': Back.BLUE,
                       'magenta': Back.MAGENTA,
                       'cyan': Back.CYAN,
                       'white': Back.WHITE}
              }
    BRIGHT_COLORS = ['white', 'yellow', 'cyan', 'green']
    MARGIN_BOTTOM = 1

    colorama_init()

    # set best contrast foreground color
    if bgcolor and not color:
        if bgcolor in BRIGHT_COLORS: color = 'black'
        else: color = 'white'

    # always work with a list of datasets
    try: len(X[0])
    except TypeError: X = [X]
    try: len(Y[0])
    except TypeError: Y = [Y]
    if not len(X) == len(Y): raise ValueError('X and Y must be the same length')
    if not color or type(color)==str: color = [color]*len(X)
    if type(marker)==str or marker==None: marker = [marker]*len(X)

    # initialize buffer
    width, height = size
    buffer = [[' ' for w in range(width)] for h in range(height)]

    # initialize colors drawn tracker (colors are added at the end)
    colors_drawn = {}
    for c in COLORMAP['fore']: colors_drawn[c] = []

    # set axes limits
    if xlim==None: xlim = (min((min(x) for x in X)), max((max(x) for x in X)))
    if ylim==None: ylim = (min((min(y) for y in Y)), max((max(y) for y in Y)))
    assert(xlim[1]>xlim[0])
    assert(ylim[1]>ylim[0])

    # make room for y-axis tick labels
    y_tick_min = format(ylim[0], fmt)
    y_tick_max = format(ylim[1], fmt)
    margin_left = max(len(y_tick_min), len(y_tick_max))
    y_axis_pos = margin_left
    x_axis_pos = -MARGIN_BOTTOM - 1

    # find transform function from data space to plot space
    x_scaling = (width-margin_left-1) / (xlim[1] - xlim[0])
    x_offset = xlim[0] * -x_scaling + margin_left
    y_scaling = -(height-MARGIN_BOTTOM-1) / (ylim[1] - ylim[0])
    y_offset = ylim[0] * -y_scaling - 1 - MARGIN_BOTTOM
    transform = lambda x,y: (x*x_scaling+x_offset,
                             y*y_scaling+y_offset)

    # set highest contrast colors for axes, tickmarks, and tick labels
    if bgcolor:
        bg, bg_r = (COLORMAP['back'][bgcolor], Back.RESET)
        if bgcolor in BRIGHT_COLORS: c, cr = (COLORMAP['fore']['black'], Fore.RESET)
        else: c, cr = (COLORMAP['fore']['white'], Fore.RESET)
    else: c, cr, bg, bg_r = ('', '', '', '')

    # draw axes
    for y in range(height): # vertical
        buffer[y][y_axis_pos] = c+'│'+cr
    for x in range(margin_left, width):  # horizontal
        buffer[x_axis_pos][x] = c+'─'+cr
    buffer[x_axis_pos][y_axis_pos] = c+'└'+cr

    # draw origin (if within bounds)
    x_origin, y_origin = [int(round(x)) for x in transform(0,0)]
    if ylim[0] <= 0 <= ylim[1]:
        for i in range(margin_left+1, width):
            buffer[y_origin][i] = c+'─'+cr
        buffer[y_origin][margin_left-1] = c+'0'+cr
    if xlim[0] <= 0 <= xlim[1]:
        for i in range(-height, MARGIN_BOTTOM-3):
            buffer[i][x_origin] = c+'│'+cr
        buffer[-1][x_origin] = c+'0'+cr
    if xlim[1] >= 0 >= xlim[0] and ylim[1] >= 0 >= ylim[0]:
        buffer[y_origin][x_origin] = c+'┼'+cr

    # draw data to buffer
    for X_, Y_, marker_, color_ in zip(X, Y, marker, color):
        if not len(X_) == len(Y_): raise ValueError('x and y must be the same length')
        for x,y in zip(X_, Y_):
            if xlim[1] >= x >= xlim[0] and ylim[1] >= y >= ylim[0]: # in bounds
                x_b, y_b = transform(x,y)
                if marker_:
                    buffer[int(round(y_b))][int(round(x_b))] = marker_
                else:
                    # which braille dot does this remainder correspond to?
                    braille_index = int(((y_b+.5)%1)/.25) + 4*(((x_b+.5)%1)>.5)
                    if len(buffer[int(round(y_b))][int(round(x_b))]) != 8: # convert to braille
                        buffer[int(round(y_b))][int(round(x_b))] = list('00000000')
                    buffer[int(round(y_b))][int(round(x_b))][braille_index] = '1'
                if color_: colors_drawn[color_] += [(int(round(y_b)), int(round(x_b)))]

    # draw tick labels
    for i, character in enumerate(format(xlim[0], fmt)): # min x
        buffer[x_axis_pos+1][y_axis_pos+i] = c+character+cr
    for i, character in enumerate(reversed(format(xlim[1]))): # max x
        buffer[x_axis_pos+1][-i-1] = c+character+cr
    for i, character in enumerate(reversed(y_tick_min)): # min y
        buffer[-MARGIN_BOTTOM-1][y_axis_pos-i-1] = c+character+cr
    for i, character in enumerate(reversed(y_tick_max)): # max y`
        buffer[0][y_axis_pos-i-1] = c+character+cr

    # turn braille placeholders into braille characters
    buffer = [[get_braille(''.join(v)) if len(v)==8 else v for v in w] for w in buffer]
    # add foreground colors
    for c in colors_drawn:
        for i,j in colors_drawn[c]:
            buffer[i][j] = COLORMAP['fore'][c] + buffer[i][j] + Fore.RESET
    output = '\n'.join([bg+''.join(row)+bg_r for row in buffer]) # add background color and concatenate output string
    if not silent: print(output)
    else: return output
