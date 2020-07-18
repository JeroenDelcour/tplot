from numbers import Number
from functools import cached_property
from colorama import init
import numpy as np

from scales import *
from utils import *


class Figure:
    def __init__(self, x=None, y=None, xlabel=None, ylabel=None, title=None, width=64, height=21):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.title = title

        if all([isinstance(value, Number) for value in self.x]):
            self._xscale = LinearScale()
        else:
            self._xscale = NominalScale()
        if all([isinstance(value, Number) for value in self.y]):
            self._yscale = LinearScale()
        else:
            self._yscale = NominalScale()

        self._yscale.fit(self.y, target_min=self._xax_height-1, target_max=self.height-1 - bool(self.title))
        self._xscale.fit(self.x, target_min=self._yax_width-1, target_max=self.width-1)

        self.canvas = np.empty((height, width), dtype="U1")
        self.canvas[:] = " "
        self._draw_x_axis()
        self._draw_y_axis()
        if self.title:
            title = self.title[:self.width]  # make sure it fits
            self._center_draw(title, self.canvas[0, :])

    @property
    def _xax_height(self):
        return 3

    @cached_property
    def _yax_width(self):
        """
        Since y-axis tick labels are drawn horizontally, the width of the y axis
        depends on the length of the labels, which themselves depend on the data.
        """
        labels = (str(value) for value in self._y_tick_values)
        return max([len(label) for label in labels]) + 2 + 1  # 2 for axis label, 1 for axis ticks

    def _center_draw(self, string, array, fillchar=" "):
        array[:] = np.array(list(string.center(len(array), fillchar)))

    def _ljust_draw(self, string, array, fillchar=" "):
        array[:] = np.array(list(string.ljust(len(array), fillchar)))

    def _rjust_draw(self, string, array, fillchar=" "):
        array[:] = np.array(list(string.rjust(len(array), fillchar)))

    @cached_property
    def _y_tick_values(self):
        start = int(self._yscale.transform(min(self.y)))
        end = int(self._yscale.transform(max(self.y)))
        return best_ticks(min(self.y), max(self.y), most=(end-start) // 2)

    def _draw_y_axis(self):
        start = int(self._yscale.transform(min(self.y)))
        end = int(self._yscale.transform(max(self.y)))
        self.canvas[-end-1:-start-1, self._yax_width-1] = "|"
        for value, pos in zip(self._y_tick_values, self._yscale.transform(self._y_tick_values)):
            pos = int(pos)
            label = str(value)
            self.canvas[end-pos-1, self._yax_width-1] = "+"
            self._rjust_draw(label, self.canvas[end-pos-1, 2:self._yax_width-1])

        if self.ylabel:
            ylabel = self.ylabel[:end-start]  # make sure it fits
            self._center_draw(ylabel, self.canvas[start:end, 0])

    def _draw_x_axis(self, ticklabel_length=7):
        start = int(self._xscale.transform(min(self.x)))
        end = int(self._xscale.transform(max(self.x)))
        self.canvas[-3, start:end] = "-"
        tick_values = best_ticks(min(self.x), max(self.x), most=(end-start) // ticklabel_length)
        before = ticklabel_length // 2
        after = ticklabel_length - before
        for value, pos in zip(tick_values, self._xscale.transform(tick_values)):
            pos = int(pos)
            label = str(value)
            self.canvas[-3, pos] = "+"
            if pos == start:  # left-adjust first ticklabel
                self._ljust_draw(label[:after], self.canvas[-2, pos:pos+after])
            elif pos == end:  # right-adjust last ticklabel
                self._rjust_draw(label[:before+1], self.canvas[-2, pos-before:pos+1])
            else:  # center other ticklabels
                self._center_draw(label[:ticklabel_length], self.canvas[-2, pos-before:pos+after])

        if self.xlabel:
            xlabel = self.xlabel[:end-start]  # make sure it fits
            self._center_draw(xlabel, self.canvas[-1, start:end])

    def scatter(self, marker="o"):
        for x, y in zip(self._xscale.transform(self.x), self._yscale.transform(self.y)):
            self.canvas[int(-y)-1, int(x)] = marker

    def line(self, marker="*"):
        xs = self._xscale.transform(self.x)
        ys = self._yscale.transform(self.y)
        for (x0, x1), (y0, y1) in zip(zip(xs[: -1], xs[1:]), zip(ys[: -1], ys[1:])):
            for x, y in plot_line_segment(int(x0), int(y0), int(x1), int(y1)):
                self.canvas[-y-1, x] = marker

    def __repr__(self):
        return "\n".join(["".join(row) for row in self.canvas.tolist()])

    def show(self):
        print(self)
