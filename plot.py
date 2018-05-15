class Figure(object):

    def __init__(self, figsize=(96,24)):
        self.width = figsize[0]
        self.height = figsize[1]
        self.margin_left = None
        self.margin_bottom = 1
        self.canvas = None

        self.buffer = [[' '] * self.width for n in range(self.height)]

    def scatter(self, X, Y, marker='·'):
        if not self.canvas:
            self._draw_axes(X, Y)
            self.canvas = Canvas((self.width-self.margin_left, self.height-self.margin_bottom),
                                 (self.margin_left, self.margin_bottom),
                                 self.buffer)
        self.canvas.scatter(X, Y, marker)

    def _draw_axes(self, X, Y):
        y_tick_min = '{:G}'.format(min(Y))
        y_tick_max = '{:G}'.format(max(Y))
        self.margin_left = max(len(y_tick_min), len(y_tick_max))

        # axes
        for y in range(self.height): # vertical
            self.buffer[y][self.margin_left] = '│'
        for x in range(self.margin_left, self.width):  # horizontal
            self.buffer[-self.margin_bottom-1][x] = '─'
        self.buffer[-self.margin_bottom-1][self.margin_left] = '┼'

        # ticks
        self.buffer[-self.margin_bottom-1][-1] = '┬'
        self.buffer[0][self.margin_left-1] = '┤'

        # tick labels
        for i, character in enumerate('{:G}'.format(min(X))): # min x
            self.buffer[-self.margin_bottom][self.margin_left+i] = character
        for i, character in enumerate(reversed('{:G}'.format(max(X)))): # max x
            self.buffer[-self.margin_bottom][-i-1] = character
        for i, character in enumerate(reversed(y_tick_min)): # min y
            self.buffer[-self.margin_bottom-1][self.margin_left-i-1] = character
        for i, character in enumerate(reversed(y_tick_max)): # max y`
            self.buffer[0][self.margin_left-i-1] = character

    def show(self):
        for row in self.buffer:
            print(''.join(row))

class Canvas(object):
    
    def __init__(self, shape, offset, buffer_):
        self.width = shape[0]
        self.height = shape[1]
        self.offset_x = offset[0]
        self.offset_y = offset[1]
        self.buffer = buffer_
        self.transform = None

    def _find_transform(self, X, Y):
        """Find transform from data space to buffer space"""
        x_scaling = (self.width-1) / (max(X) - min(X))
        x_offset = min(X) * -x_scaling + self.offset_x
        y_scaling = -(self.height-1) / (max(Y) - min(Y))
        y_offset = min(Y) * -y_scaling - 1 - self.offset_y
        self.transform = lambda x,y: (int(round(x*x_scaling+x_offset)),
                                      int(round(y*y_scaling+y_offset)))

    def scatter(self, X, Y, marker='.'):
        if not self.transform:
            self._find_transform(X, Y)
        for x,y in zip(X,Y):
            x_buffer, y_buffer = self.transform(x,y)
#            if x_buffer >= 0 and x_buffer <= self.width+2 and y_buffer <= -1 and y_buffer >= -self.height-2:
            self.buffer[y_buffer][x_buffer] = marker
        

import numpy as np

X = np.arange(0,np.pi*4,.1)
Y = -np.sin(X)

fig = Figure()
fig.scatter(X,Y)
fig.show()
