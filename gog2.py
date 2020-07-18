from colorama import init
from numbers import Number
from utils import *
from scales import *


class Figure:
    def __init__(self, x=None, y=None, width=64, height=32, xlabel=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.xlabel = xlabel
        assert len(self.x) == len(self.y)

        if all([isinstance(value, Number) for value in self.x]):
            self._xscale = LinearScale()
        else:
            self._xscale = NominalScale()
        if all([isinstance(value, Number) for value in self.y]):
            self._yscale = LinearScale()
        else:
            self._yscale = NominalScale()

        self._xscale.fit(self.x, 0, width-1)
        self._yscale.fit(self.y, 0, height-1)

        self.canvas = [[" " for j in range(width)] for i in range(height)]
        self._x_axis = self.draw_x_axis()

    def draw_x_axis(self):
        """Returns string which can be appended to the canvas."""
        # initialize lists of characters
        x_ticks = ["-"] * self.width
        x_tick_labels = [" "] * self.width
        # find best tick values and positions
        x_tick_values = best_ticks(min(self.x), max(self.x), most=self.width//6)
        x_tick_positions = self._xscale.transform(x_tick_values)
        # draw ticks and tick labels
        for value, position in zip(x_tick_values, x_tick_positions):
            label = str(value)
            pos = int(position)
            # tick mark
            x_ticks[pos] = "+"
            # tick label
            if pos == 0:  # left-align first tick label
                start = 0
            elif pos == self.width-1:  # right-align last tick label
                start = pos - len(label) + 1
            else:  # center-align the other tick labels
                start = pos - int(len(label)/2)
            x_tick_labels[start:start+len(label)] = list(label)
        # combine into one string
        x_ticks = "".join(x_ticks)
        x_tick_labels = "".join(x_tick_labels)
        x_axis = x_ticks + "\n" + x_tick_labels
        # add axis label if provided
        if self.xlabel is not None:
            x_axis_label = [" "] * self.width
            x_axis_label[int(self.width/2)] = "l"
            x_axis_label = "".join(x_axis_label)
            x_axis += "\n" + x_axis_label
        return x_axis

    def scatter(self, marker="o"):
        xs = self._xscale.transform(self.x)
        ys = self._yscale.transform(self.y)
        for x, y in zip(xs, ys):
            self.canvas[int(-y)-1][int(x)] = marker

    def line(self, marker="o"):
        xs = [int(x) for x in self._xscale.transform(self.x)]
        ys = [int(y) for y in self._yscale.transform(self.y)]
        for (x0, x1), (y0, y1) in zip(zip(xs[:-1], xs[1:]), zip(ys[:-1], ys[1:])):
            for x, y in plot_line_segment(x0, y0, x1, y1):
                self.canvas[-y-1][x] = marker

    def __repr__(self):
        canvas = "\n".join(["".join(row) for row in self.canvas])
        return "\n".join([canvas, self._x_axis])

    def show(self):
        print(self)
