from numbers import Number
from functools import cached_property
from colorama import init
import numpy as np

from scales import *
from utils import *


class Figure:
    def __init__(self, x=None, y=None, xlabel=None, ylabel=None, title=None, width=64, height=21, xticklabel_length=7):
        self.x = x
        self.y = y
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.title = title
        self.width = width
        self.height = height
        self.xticklabel_length = xticklabel_length

        self.canvas = np.empty((height, width), dtype="U1")
        self.canvas[:] = " "
        self._draw_x_axis()
        self._draw_y_axis()
        if self.title:
            title = self.title[:self.width]  # make sure it fits
            self._center_draw(title, self.canvas[0, :])

    @cached_property
    def _yscale(self):
        if all([isinstance(value, Number) for value in self.y]):
            scale = LinearScale()
        else:
            scale = NominalScale()
        scale.fit(self.y, target_min=self._xax_height - bool(self.xlabel), target_max=self.height-1 - bool(self.title))
        return scale

    @cached_property
    def _xscale(self):
        if all([isinstance(value, Number) for value in self.x]):
            scale = LinearScale()
        else:
            scale = NominalScale()
        scale.fit(self.x, target_min=self._yax_width-1, target_max=self.width-1)
        return scale

    @property
    def _xax_height(self):
        return 2 + bool(self.xlabel)

    @cached_property
    def _yax_width(self):
        """
        Since y-axis tick labels are drawn horizontally, the width of the y axis
        depends on the length of the labels, which themselves depend on the data.
        """
        labels = (str(value) for value in self._ytick_values)
        width = max([len(label) for label in labels])
        width += 1  # for axis ticks
        width += bool(self.ylabel) * 2  # for y label
        return width

    def _center_draw(self, string, array, fillchar=" "):
        array[:] = np.array(list(string.center(len(array), fillchar)))

    def _ljust_draw(self, string, array, fillchar=" "):
        array[:] = np.array(list(string.ljust(len(array), fillchar)))

    def _rjust_draw(self, string, array, fillchar=" "):
        array[:] = np.array(list(string.rjust(len(array), fillchar)))

    @cached_property
    def _ytick_values(self):
        if isinstance(self._yscale, NominalScale):
            return set(self.y)  # note this may not fit depending on the height of the figure
        else:
            start = int(self._yscale.transform(min(self.y)))
            end = int(self._yscale.transform(max(self.y)))
            return best_ticks(min(self.y), max(self.y), most=(end-start) // 2)

    @cached_property
    def _xtick_values(self):
        if isinstance(self._xscale, NominalScale):
            return set(self.x)  # note this may not fit dependong on the width of the figure
        else:
            start = int(self._xscale.transform(min(self.x)))
            end = int(self._xscale.transform(max(self.x)))
            return best_ticks(min(self.x), max(self.x), most=(end-start) // self.xticklabel_length)

    def _draw_y_axis(self):
        start = int(self._yscale.transform(min(self.y)))
        end = int(self._yscale.transform(max(self.y)))
        self.canvas[-end-1:-start-1, self._yax_width-1] = "|"
        for value, pos in zip(self._ytick_values, self._yscale.transform(self._ytick_values)):
            pos = int(pos)
            label = str(value)
            self.canvas[end-pos, self._yax_width-1] = "+"
            self._rjust_draw(label, self.canvas[end-pos, bool(self.ylabel)*2:self._yax_width-1])

        if self.ylabel:
            ylabel = self.ylabel[:end-start]  # make sure it fits
            self._center_draw(ylabel, self.canvas[start:end, 0])

    def _draw_x_axis(self):
        start = int(self._xscale.transform(min(self.x)))
        end = int(self._xscale.transform(max(self.x)))
        self.canvas[-self._xax_height, start:end] = "-"
        before = self.xticklabel_length // 2
        after = self.xticklabel_length - before
        for value, pos in zip(self._xtick_values, self._xscale.transform(self._xtick_values)):
            pos = int(pos)
            label = str(value)
            self.canvas[-self._xax_height, pos] = "+"
            if pos == start:  # left-adjust first ticklabel
                self._ljust_draw(label[:after], self.canvas[-self._xax_height+1, pos:pos+after])
            elif pos == end:  # right-adjust last ticklabel
                self._rjust_draw(label[:before+1], self.canvas[-self._xax_height+1, pos-before:pos+1])
            else:  # center other ticklabels
                self._center_draw(label[:self.xticklabel_length],
                                  self.canvas[-self._xax_height+1, pos-before:pos+after])

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
