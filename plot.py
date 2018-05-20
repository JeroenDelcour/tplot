#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from colorama import init as colorama_init
from colorama import Fore, Back

def plot(X, Y, marker='·', color=None, size=(96,24), xlim=None, ylim=None, bgcolor=None, fmt='G'):
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

    colorama_init()

    # expand dimensions
    if type(X[0])   in (int, float): X = [X]
    if type(Y[0])   in (int, float): Y = [Y]
    if not color or type(color)==str: color = [color]*len(X)
    if type(marker)==str: marker = [marker]*len(X)

    width, height = size
    buffer = [[' ' for w in range(width)] for h in range(height)]

    if xlim==None: xlim = (min((min(x) for x in X)), max((max(x) for x in X)))
    if ylim==None: ylim = (min((min(y) for y in Y)), max((max(y) for y in Y)))
    assert(xlim[1]>xlim[0])
    assert(ylim[1]>ylim[0])

    def find_transform():
        "Find transform from data space to plot space"
        x_scaling = (width-margin_left-margin_right-1) / (xlim[1] - xlim[0])
        x_offset = xlim[0] * -x_scaling + margin_left
        y_scaling = -(height-margin_bottom-margin_top-1) / (ylim[1] - ylim[0])
        y_offset = ylim[0] * -y_scaling - 1 - margin_bottom
        return lambda x,y: (int(round(x*x_scaling+x_offset)),
                                 int(round(y*y_scaling+y_offset)))
    margin_left, margin_bottom, margin_top, margin_right = 0, 0, 0, 0
    transform = find_transform()

    # determine axes positions
    y_axis_pos, x_axis_pos = transform(0,0)
    clamp = lambda x, min_x, max_x: max(min(x, max_x), min_x)
    y_axis_pos = clamp(y_axis_pos, 0, width-1)
    x_axis_pos = clamp(x_axis_pos, -height, -1)
    if y_axis_pos >= width: y_axis_pos = 0
    if x_axis_pos <= -height: x_axis_pos = -1

    # calculate margins for tick labels
    y_tick_min = format(ylim[0], fmt)
    y_tick_max = format(ylim[1], fmt)
    y_label_len = max(len(y_tick_min), len(y_tick_max))
    margin_left = max(y_label_len - y_axis_pos, 0)
    if y_axis_pos == width-1: margin_right = y_label_len
    print(margin_right)
    margin_bottom = 0 + (x_axis_pos==-1)
    margin_top = 0 + (x_axis_pos==-height)

    # correct axes and transform for margins
    y_axis_pos += margin_left - margin_right
    x_axis_pos -= margin_bottom - margin_top
    transform = find_transform()

    # if background color is set, set best contrasting default foreground colors
    if not bgcolor: c, cr = ('', '')
    elif bgcolor in BRIGHT_COLORS: c, cr = (COLORS['fore']['black'], Fore.RESET)
    else: c, cr = (COLORS['fore']['white'], Fore.RESET)

    # draw axes
    for y in range(height): # vertical
        buffer[y][y_axis_pos] = c+'│'+cr
    for x in range(margin_left, width-margin_right):  # horizontal
        buffer[x_axis_pos][x] = c+'─'+cr
    buffer[x_axis_pos][y_axis_pos] = c+'┼'+cr

    # draw tick marks
    buffer[x_axis_pos][-margin_right-1] = c+'┼'+cr
    buffer[x_axis_pos][margin_left] = c+'┼'+cr
    buffer[margin_top][y_axis_pos] = c+'┼'+cr
    buffer[-1][y_axis_pos] = c+'┼'+cr

    # draw data
    for X_, Y_, marker_, color_ in zip(X, Y, marker, color):
        assert(len(X_)==len(Y_))
        # set marker color
        if color_: marker_ = COLORS['fore'][color_] + marker_ + Fore.RESET
        elif bgcolor in BRIGHT_COLORS: marker_ = COLORS['fore']['black'] + marker_ + Fore.RESET
        # draw data
        for x,y in zip(X_,Y_):
            if xlim[1] >= x >= xlim[0] and ylim[1] >= y >= ylim[0]: # in bounds
                x_buffer, y_buffer = transform(x,y)
                buffer[y_buffer][x_buffer] = marker_

    # draw tick labels
    for i, character in enumerate(format(xlim[0], fmt)): # min x
        buffer[x_axis_pos+1-margin_top*2][margin_left+i] = c+character+cr
    for i, character in enumerate(reversed(format(xlim[1], fmt))): # max x
        buffer[x_axis_pos+1-margin_top*2][-i-1-margin_right] = c+character+cr
    for i, character in enumerate(reversed(y_tick_min)): # min y
        buffer[-margin_bottom-1][y_axis_pos-i-1+margin_right+(margin_right>0)] = c+character+cr
    for i, character in enumerate(reversed(y_tick_max)): # max y`
        buffer[margin_top][y_axis_pos-i-1+margin_right+(margin_right>0)*(len(y_tick_max)-margin_right+1)] = c+character+cr

    if bgcolor: # set background color
        buffer[0].insert(0, COLORS['back'][bgcolor])
        buffer[-1].append(Back.RESET)

    return '\n'.join([''.join(row) for row in buffer])

def test():
    from math import sin, cos
    from time import time

    small = (33,13)
    t0 = time()
    X = [0,1,2,3,4,5]
    Y = [0,1,2,3,4,5]
    print(plot(X, Y, size=small))
    print()
    X, Y = range(-5,1), range(-10,-4)
    print(plot(X, Y, marker='+', color='red', bgcolor='blue', size=small))
    print()
    X1 = (-5,-4,-3,-2,-1,0,1,2,3,4,5)
    X2 = (-5,-4,-3,-2,-1,0,1,2,3,4,5)
    Y1 = (-5,-4,-3,-2,-1,0,1,2,3,4,5)
    Y2 = (5,4,3,2,1,0,-1,-2,-3,-4,-5)
    print(plot((X1,X2), (Y1,Y2), marker='*', color=['red', 'white'],
               xlim=(-12,12), ylim=(-6,6), size=small))
    print()
    X = [x/10 for x in range(150)]
    Y = [cos(x) for x in X]
    print(plot(X, Y, color=['red'], bgcolor='white'))
    return 'All tests finished in {:G} seconds.'.format(time()-t0)

print(test())
