#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from colorama import init as colorama_init
from colorama import Fore, Back

def plot(X, Y, marker='·', color=None, size=(96,24), xlim=[None,None], ylim=[None,None], bgcolor=None, fmt='G'):
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

    # expand dimensions
    if type(X[0]) != list: X = [X]
    if type(Y[0]) != list: Y = [Y]
    if type(marker) != list: marker = [marker]*len(X)
    if type(color) != list: color = [color]*len(X)

    width, height = size
    buffer = [[' ' for w in range(width)] for h in range(height)]

    xlim[0] = xlim[0] or min([min(x) for x in X])
    xlim[1] = xlim[1] or max([max(x) for x in X])
    ylim[0] = ylim[0] or min([min(y) for y in Y])
    ylim[1] = ylim[1] or max([max(y) for y in Y])

    # calculate size of left margin to fit y-axis tick labels
    y_tick_min = format(ylim[0], fmt)
    y_tick_max = format(ylim[1], fmt)
    margin_left = max(len(y_tick_min), len(y_tick_max))

    # find transform from data space to plot space
    x_scaling = (width-margin_left-1) / (xlim[1] - xlim[0])
    x_offset = xlim[0] * -x_scaling + margin_left
    y_scaling = -(height-MARGIN_BOTTOM-1) / (ylim[1] - ylim[0])
    y_offset = ylim[0] * -y_scaling - 1 - MARGIN_BOTTOM
    transform = lambda x,y: (int(round(x*x_scaling+x_offset)),
                             int(round(y*y_scaling+y_offset)))

    # if background color is set, set best contrasting default foreground colors
    if not bgcolor: c, cr = ('', '')
    elif bgcolor in BRIGHT_COLORS: c, cr = (COLORS['fore']['black'], Fore.RESET)
    else: c, cr = (COLORS['fore']['white'], Fore.RESET)

    # draw axes
    for y in range(height): # vertical
        buffer[y][margin_left] = c+'│'+cr
    for x in range(margin_left, width):  # horizontal
        buffer[-MARGIN_BOTTOM-1][x] = c+'─'+cr
    buffer[-MARGIN_BOTTOM-1][margin_left] = c+'┼'+cr

    # draw tick marks
    buffer[-MARGIN_BOTTOM-1][-1] = c+'┬'+cr
    buffer[0][margin_left] = c+'┤'+cr

    # draw tick labels
    for i, character in enumerate(format(xlim[0])): # min x
        buffer[-MARGIN_BOTTOM][margin_left+i] = c+character+cr
    for i, character in enumerate(reversed(format(xlim[1]))): # max x
        buffer[-MARGIN_BOTTOM][-i-1] = c+character+cr
    for i, character in enumerate(reversed(y_tick_min)): # min y
        buffer[-MARGIN_BOTTOM-1][margin_left-i-1] = c+character+cr
    for i, character in enumerate(reversed(y_tick_max)): # max y`
        buffer[0][margin_left-i-1] = c+character+cr

    # draw data
    for X_, Y_, marker_, color_ in zip(X, Y, marker, color):
        # set marker color
        if color_: marker_ = COLORS['fore'][color_] + marker_ + Fore.RESET
        elif bgcolor in BRIGHT_COLORS: marker_ = COLORS['fore']['black'] + marker_ + Fore.RESET
        else: marker_ = COLORS['fore']['white'] + marker_ + Fore.RESET
        # draw data
        for x,y in zip(X_,Y_):
            if xlim[1] >= x >= xlim[0] and ylim[1] >= y >= ylim[0]: # in bounds
                x_buffer, y_buffer = transform(x,y)
                buffer[y_buffer][x_buffer] = marker_

    if bgcolor: # set background color
        buffer[0].insert(0, COLORS['back'][bgcolor])
        buffer[-1].append(Back.RESET)

    return '\n'.join([''.join(row) for row in buffer])

def test():
    from math import sin, cos
    from time import time

    X = [x/10 for x in range(100)]
    Y = [sin(x) for x in X]
    X2 = [x/10 for x in range(200)]
    Y2 = [cos(x) for x in X2]

    t0 = time()
    print(plot([X,X2], [Y,Y2], color=[None, 'red'], bgcolor='white'))
    return 'All tests passed in {:G} seconds.'.format(time()-t0)

print(test())
