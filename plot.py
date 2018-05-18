#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from colorama import init as colorama_init
from colorama import Fore, Back

colors = {'fore': {'black': Fore.BLACK,
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
bright_colors = ['white', 'yellow', 'cyan', 'green']

class Figure:

    def __init__(self, figsize=(96,24), xlim=[None,None], ylim=[None,None], bgcolor=None):
        self.width = figsize[0]
        self.height = figsize[1]
        self.margin_bottom = 1
        self.xlim = xlim
        self.ylim = ylim
        self.plot_queue = []
        self.margin_left = None
        self.canvas = None
        self.buffer = None
        self.bgcolor = bgcolor
        colorama_init()

    def scatter(self, X, Y, marker='·', color=None):
        self.plot_queue.append({'type':'scatter', 'X':X, 'Y':Y, 'marker':marker[0], 'color':color})

    def show(self):
        self.buffer = [[' '] * self.width for n in range(self.height)]
        self._draw_axes()
        self.canvas = Canvas((self.width-self.margin_left, self.height-self.margin_bottom),
                             (self.margin_left, self.margin_bottom),
                             self.buffer,
                             self.xlim,
                             self.ylim)
        for plot in self.plot_queue:
            if self.bgcolor in bright_colors and plot['color']==None:
                plot['color'] = 'black'
            if plot['type']=='scatter':
                self.canvas.scatter(plot['X'], plot['Y'], plot['marker'], plot['color'])
        if self.bgcolor:
            print(colors['back'][self.bgcolor])
        for row in self.buffer:
            print(''.join(row))
        print(Fore.RESET + Back.RESET)


    def _draw_axes(self):

        format = lambda x: '{:G}'.format(x)

        if self.xlim[0] == None: self.xlim[0] = min([min(p['X']) for p in self.plot_queue])
        if self.xlim[1] == None: self.xlim[1] = max([max(p['X']) for p in self.plot_queue])
        if self.ylim[0] == None: self.ylim[0] = min([min(p['Y']) for p in self.plot_queue])
        if self.ylim[1] == None: self.ylim[1] = max([max(p['Y']) for p in self.plot_queue])

        # paint it black if using bright background
        c, cr = (colors['fore']['black'], Fore.RESET) if self.bgcolor in bright_colors else ('', '')

        # get size of left margin to fit y-axis tick labels
        y_tick_min = format(self.ylim[0])
        y_tick_max = format(self.ylim[1])
        self.margin_left = max(len(y_tick_min), len(y_tick_max))

        # draw axes
        for y in range(self.height): # vertical
            self.buffer[y][self.margin_left] = c+'│'+cr
        for x in range(self.margin_left, self.width):  # horizontal
            self.buffer[-self.margin_bottom-1][x] = c+'─'+cr
        self.buffer[-self.margin_bottom-1][self.margin_left] = c+'┼'+cr

        # draw ticks
        self.buffer[-self.margin_bottom-1][-1] = c+'┬'+cr
        self.buffer[0][self.margin_left] = c+'┤'+cr

        # draw tick labels
        for i, character in enumerate(format(self.xlim[0])): # min x
            self.buffer[-self.margin_bottom][self.margin_left+i] = c+character+cr
        for i, character in enumerate(reversed(format(self.xlim[1]))): # max x
            self.buffer[-self.margin_bottom][-i-1] = c+character+cr
        for i, character in enumerate(reversed(y_tick_min)): # min y
            self.buffer[-self.margin_bottom-1][self.margin_left-i-1] = c+character+cr
        for i, character in enumerate(reversed(y_tick_max)): # max y`
            self.buffer[0][self.margin_left-i-1] = c+character+cr

class Canvas(Figure):
    
    def __init__(self, shape, offset, buffer_, xlim, ylim):
        self.width = shape[0]
        self.height = shape[1]
        self.offset_x = offset[0]
        self.offset_y = offset[1]
        self.buffer = buffer_
        self.xlim = xlim
        self.ylim = ylim
        self.transform = self._find_transform()

    def _find_transform(self):
        """Find transform from data space to buffer space"""
        x_scaling = (self.width-1) / (self.xlim[1] - self.xlim[0])
        x_offset = self.xlim[0] * -x_scaling + self.offset_x
        y_scaling = -(self.height-1) / (self.ylim[1] - self.ylim[0])
        y_offset = self.ylim[0] * -y_scaling - 1 - self.offset_y
        return lambda x,y: (int(round(x*x_scaling+x_offset)),
                            int(round(y*y_scaling+y_offset)))

    def scatter(self, X, Y, marker='.', color=None):
        if color: marker = colors['fore'][color] + marker + Fore.RESET
        for x,y in zip(X,Y):
            if self.xlim[1] >= x >= self.xlim[0] and self.ylim[1] >= y >= self.ylim[0]:
                x_buffer, y_buffer = self.transform(x,y)
                self.buffer[y_buffer][x_buffer] = marker
        

from math import sin
from time import time

X = [x/10 for x in range(100)]
Y = [sin(x) for x in X]
Y2 = [y*2 for y in Y]

t0 = time()
fig = Figure(xlim=[-15,15], ylim=[0,2], bgcolor='cyan')
fig.scatter(X,Y)
fig.scatter(X,Y2,marker='*',color='red')
fig.show()
print(time()-t0)
