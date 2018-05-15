class Figure(object):

    def __init__(self, figsize=(96,24), xlim=[None,None], ylim=[None,None]):
        self.width = figsize[0]
        self.height = figsize[1]
        self.margin_bottom = 1
        self.xlim = xlim
        self.ylim = ylim
        self.plot_queue = []
        self.margin_left = None
        self.canvas = None
        self.buffer = None

    def scatter(self, X, Y, marker='·'):
        self.plot_queue.append({'type':'scatter', 'X':X, 'Y':Y, 'marker':marker})

    def show(self):
        self.buffer = [[' '] * self.width for n in range(self.height)]
        self._draw_axes()
        self.canvas = Canvas((self.width-self.margin_left, self.height-self.margin_bottom),
                             (self.margin_left, self.margin_bottom),
                             self.buffer,
                             self.xlim,
                             self.ylim)
        for plot in self.plot_queue:
            if plot['type']=='scatter':
                self.canvas.scatter(plot['X'], plot['Y'], plot['marker'])
        for row in self.buffer:
            print(''.join(row))


    def _draw_axes(self):
        if self.xlim[0]==None:
            self.xlim[0] = min([min(plot['X']) for plot in self.plot_queue])
        if self.xlim[1]==None:
            self.xlim[1] = max([max(plot['X']) for plot in self.plot_queue])
        if self.ylim[0]==None:
            self.ylim[0] = min([min(plot['Y']) for plot in self.plot_queue])
        if self.ylim[1]==None:
            self.ylim[1] = max([max(plot['Y']) for plot in self.plot_queue])

        # get size of left margin to fit y-axis tick labels
        y_tick_min = '{:G}'.format(self.ylim[0])
        y_tick_max = '{:G}'.format(self.ylim[1])
        self.margin_left = max(len(y_tick_min), len(y_tick_max))

        # axes
        for y in range(self.height): # vertical
            self.buffer[y][self.margin_left] = '│'
        for x in range(self.margin_left, self.width):  # horizontal
            self.buffer[-self.margin_bottom-1][x] = '─'
        self.buffer[-self.margin_bottom-1][self.margin_left] = '┼'

        # ticks
        self.buffer[-self.margin_bottom-1][-1] = '┬'
        self.buffer[0][self.margin_left] = '┤'

        # tick labels
        for i, character in enumerate('{:G}'.format(self.xlim[0])): # min x
            self.buffer[-self.margin_bottom][self.margin_left+i] = character
        for i, character in enumerate(reversed('{:G}'.format(self.xlim[1]))): # max x
            self.buffer[-self.margin_bottom][-i-1] = character
        for i, character in enumerate(reversed(y_tick_min)): # min y
            self.buffer[-self.margin_bottom-1][self.margin_left-i-1] = character
        for i, character in enumerate(reversed(y_tick_max)): # max y`
            self.buffer[0][self.margin_left-i-1] = character

class Canvas(object):
    
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

    def scatter(self, X, Y, marker='.'):
        if not self.transform:
            self._find_transform(X, Y)
        for x,y in zip(X,Y):
            if self.xlim[1] >= x >= self.xlim[0] and self.ylim[1] >= y >= self.ylim[0]:
                x_buffer, y_buffer = self.transform(x,y)
                self.buffer[y_buffer][x_buffer] = marker
        

import numpy as np

X = np.arange(0,np.pi*4,.1)
Y = np.sin(X)

fig = Figure(xlim=[-15,15], ylim=[0,2])
fig.scatter(X,Y)
fig.scatter(X,Y*2,marker='*')
fig.show()
