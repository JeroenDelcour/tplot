# -*- coding: utf-8 -*- 

from colorama import init as colorama_init
from colorama import Fore, Back

def scatter(X, Y, marker='·', color=None, size=(96,24), xlim=None, ylim=None, bgcolor=None, silent=False, fmt='G'):
    COLORS = {'fore': {'black': Fore.BLACK,
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

    # always work with a list of datasets
    try: len(X[0])
    except TypeError: X = [X]
    try: len(Y[0])
    except TypeError: Y = [Y]
    if not color or type(color)==str: color = [color]*len(X)
    if type(marker)==str: marker = [marker]*len(X)

    # initialize buffer
    width, height = size
    buffer = [[' ' for w in range(width)] for h in range(height)]

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
    transform = lambda x,y: (int(round(x*x_scaling+x_offset)),
                             int(round(y*y_scaling+y_offset)))

    # set highest contrast default colors
    if bgcolor:
        bg, bg_r = (COLORS['back'][bgcolor], Back.RESET)
        if bgcolor in BRIGHT_COLORS: c, cr = (COLORS['fore']['black'], Fore.RESET)
        else: c, cr = (COLORS['fore']['white'], Fore.RESET)
    else: c, cr, bg, bg_r = ('', '', '', '')

    # draw axes
    for y in range(height): # vertical
        buffer[y][y_axis_pos] = c+'│'+cr
    for x in range(margin_left, width):  # horizontal
        buffer[x_axis_pos][x] = c+'─'+cr
    buffer[x_axis_pos][y_axis_pos] = c+'└'+cr

    # draw origin
    x_origin, y_origin = transform(0,0)
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

    def draw(X, Y, marker):
        assert(len(X)==len(Y))
        for x,y in zip(X,Y):
            if xlim[1] >= x >= xlim[0] and ylim[1] >= y >= ylim[0]: # in bounds
                x_buffer, y_buffer = transform(x,y)
                buffer[y_buffer][x_buffer] = marker

    # draw data
    for X_, Y_, marker_, color_ in zip(X, Y, marker, color):
        # set marker color
        if color_: marker_ = COLORS['fore'][color_] + marker_ + Fore.RESET
        elif bgcolor in BRIGHT_COLORS: marker_ = COLORS['fore']['black'] + marker_ + Fore.RESET
        draw(X_, Y_, marker_)

    # draw tick labels
    for i, character in enumerate(format(xlim[0], fmt)): # min x
        buffer[x_axis_pos+1][y_axis_pos+i] = c+character+cr
    for i, character in enumerate(reversed(format(xlim[1]))): # max x
        buffer[x_axis_pos+1][-i-1] = c+character+cr
    for i, character in enumerate(reversed(y_tick_min)): # min y
        buffer[-MARGIN_BOTTOM-1][y_axis_pos-i-1] = c+character+cr
    for i, character in enumerate(reversed(y_tick_max)): # max y`
        buffer[0][y_axis_pos-i-1] = c+character+cr

    output = '\n'.join([bg+''.join(row)+bg_r for row in buffer])
    if not silent: print(output)
    else: return output
