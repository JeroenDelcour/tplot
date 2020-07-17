from colorama import init
from numbers import Number
from bisect import bisect
import math


def plot_line_segment(x0, y0, x1, y1):
    """ Plot line segment using Bresenham algorithm. Yields (x, y). """
    dx = x1 - x0
    dy = y1 - y0
    axes_swapped = False
    if abs(dy) > abs(dx):  # ensure slope is not >1
        axes_swapped = True
        x0, y0, x1, y1 = y0, x0, y1, x1
    if x0 > x1:  # always draw left to right
        x0, x1 = x1, x0
        y0, y1 = y1, y0
    dx = x1 - x0
    dy = y1 - y0
    yi = 1
    if dy < 0:  # switch sign of slope
        yi = -1
        dy = -dy
    D = 2*dy - dx
    y = y0

    for x in range(x0, x1+1):
        yield (y, x) if axes_swapped else (x, y)
        if D > 0:
            y += yi
            D -= 2*dx
        D += 2*dy


def best_ticks(min_, max_, most):
    # find step size
    range_ = max_ - min_
    if range_ == 0:
        return [min_]
    min_step = range_ / most
    magnitude = 10 ** math.floor(math.log(min_step, 10))
    residual = min_step / magnitude
    possible_steps = [1, 2, 5, 10]
    step = possible_steps[bisect(
        possible_steps, residual)] if residual < 10 else 10
    step *= magnitude
    # generate ticks
    sign = math.copysign(1, min_)
    start = step * math.floor(abs(min_) / step) * sign
    return [start+i*step for i in range(int((max_-start)/step)+1)]


class Scale:
    def __init__(self):
        pass

    def transform(self, values):
        raise NotImplementedError


class LinearScale(Scale):
    """Transforms real values to real values linearly."""

    def __init__(self):
        super().__init__()

    def fit(self, values, target_min, target_max):
        original_min = min(values)
        original_max = max(values)
        original_range = original_max - original_min
        target_range = target_max - target_min

        def transform(values):
            return [target_range * (value - original_min) / original_range + target_min for value in values]
        self.transform = transform


class NominalScale(Scale):
    """Maps unique values to real values."""

    def __init__(self):
        super().__init__()

    def fit(self, values, target_min=0, target_max=None):
        idxmap = {value: i for i, value in enumerate(sorted(set(values)))}
        if target_max is not None and target_max > len(idxmap):
            scale = LinearScale()
            scale.fit(list(idxmap.values()), target_min, target_max)
            idxmap = {value: scale.transform([i])[0] for value, i in idxmap.items()}

        def transform(values):
            return [idxmap[value] for value in values]
        self.transform = transform


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
        if all([isinstance(value, Number) for value in self.x]):
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

    def scatterplot(self, marker="o"):
        xs = self._xscale.transform(self.x)
        ys = self._yscale.transform(self.y)
        for x, y in zip(xs, ys):
            self.canvas[int(-y)-1][int(x)] = marker

    def lineplot(self, marker="o"):
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
