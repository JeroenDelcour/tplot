from termcolor import colored
from functools import lru_cache, partial
import numpy as np
from shutil import get_terminal_size
from typing import Optional
from warnings import warn
from colorama import init
init()

from .scales import *
from .utils import *
from .img2ascii import img2ascii

ASCII_FALLBACK = {
    "─": "-",
    "│": "|",
    "┤": "+",
    "┬": "+",
    "┌": "+",
    "┐": "+",
    "└": "+",
    "┘": "+",
    "█": "#",
    "•": "*",
    "·": "."
}


class Figure:
    """
    Figure used to draw graphs.

    Args:
        xlabel: Label for x axis
        ylabel: Label for y axis
        title: Title for figure
        width: Width of figure. Defaults to the terminal window width, or falls back to 80.
        height: Height of the figure. Defaults to the terminal window height, or falls back to 24.
        legendloc: Location of the legend. Accepted values: "topleft", "topright", "bottomleft", "bottomright".
        xticklabel_length: Length of the tick labels on the x axis. Determines how many x ticks are shown.
        ascii: Use only ascii characters. Defaults to trying to detect if unicode is supported in the terminal.
    """

    def __init__(self,
                 xlabel: Optional[str] = None,
                 ylabel: Optional[str] = None,
                 title: Optional[str] = None,
                 width: Optional[int] = None,
                 height: Optional[int] = None,
                 legendloc: str = "topright",
                 xticklabel_length: int = 7,
                 ascii: Optional[bool] = None):
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.title = title
        self.legendloc = legendloc
        self.xticklabel_length = xticklabel_length
        assert isinstance(self.xticklabel_length, int)
        assert self.xticklabel_length > 0

        self._y_origin = "lower"

        self.ascii_only = ascii
        if self.ascii_only is None:
            self.ascii_only = not unicode_supported()

        term_width, term_height = get_terminal_size(fallback=(80, 24))
        term_height -= 1  # room for prompt
        self.width = width if width else term_width
        self.height = height if height else term_height
        assert isinstance(self.width, int) and self.width > 0
        assert isinstance(self.height, int) and self.height > 0

        # gather stuff to plot before actually drawing it
        self._plots = []
        self._labels = []

    @property
    def x(self):
        return tuple([x for plot in self._plots for x in plot.keywords["x"]])

    @property
    def y(self):
        return tuple([y for plot in self._plots for y in plot.keywords["y"]])

    @lru_cache(maxsize=1)
    def _yscale(self):
        if is_numerical(self.y):
            scale = LinearScale()
        else:
            scale = CategoricalScale()
        target_min = -self._xax_height() - 1
        target_max = -self.height + 1 + bool(self.title)
        if self._y_origin == "upper":
            target_min, target_max = target_max, target_min
        scale.fit(self.y, target_min, target_max)
        if is_numerical(self.y):
            # refit scale to tick values, since those lay just outside the input data range
            scale.fit(self._ytick_values(), target_min, target_max)
        return scale

    @lru_cache(maxsize=1)
    def _xscale(self):
        if is_numerical(self.x):
            scale = LinearScale()
        else:
            scale = CategoricalScale()
        target_min = self._yax_width()
        target_max = self.width - 1
        scale.fit(self.x, target_min, target_max)
        if is_numerical(self.x):
            # refit scale to tick values, since those lay just outside the input data range
            scale.fit(self._xtick_values(), target_min, target_max)
        return scale

    def _xax_height(self):
        return 2 + bool(self.xlabel)

    def _fmt(self, value):
        if isinstance(value, Number):
            return f"{value:.3g}"
        else:
            return str(value)

    @lru_cache(maxsize=1)
    def _yax_width(self):
        """
        Since y-axis tick labels are drawn horizontally, the width of the y axis
        depends on the length of the labels, which themselves depend on the data.
        """
        labels = (self._fmt(value) for value in self._ytick_values())
        width = max([len(label) for label in labels])
        width += 1  # for axis ticks
        width += bool(self.ylabel) * 2  # for y label
        return width

    def _center_draw(self, string, array, fillchar=" "):
        array[:] = list(string.center(len(array), fillchar))

    def _ljust_draw(self, string, array, fillchar=" "):
        array[:] = list(string.ljust(len(array), fillchar))

    def _rjust_draw(self, string, array, fillchar=" "):
        array[:] = list(string.rjust(len(array), fillchar))

    @lru_cache(maxsize=1)
    def _ytick_values(self):
        if is_numerical(self.y):
            return best_ticks(min(self.y), max(self.y), most=self.height // 3)
        else:  # nominal
            values = sorted([str(v) for v in set(self.y)])
            y_axis_height = self.height - bool(self.title) - self._xax_height()
            if len(values) > y_axis_height:
                raise ValueError(
                    f"Too many ({len(values)}) unique y values to fit into y axis. Try making the graph taller.")
            return values

    @lru_cache(maxsize=1)
    def _xtick_values(self):
        if is_numerical(self.x):
            return best_ticks(min(self.x), max(self.x), most=self.width // self.xticklabel_length)
        else:  # categorical
            values = sorted([str(v) for v in set(self.x)])  # note this may not fit depending on the width of the figure
            x_axis_width = self.width - self._yax_width()
            if len(values)*self.xticklabel_length > x_axis_width:
                raise ValueError(
                    f"Too many ({len(values)}) unique x values to fit into x axis. Try making the graph wider or reducing `xtickvalue_length`.")
            return values

    def _draw_y_axis(self):
        start = round(self._yscale().transform(self._ytick_values()[-1]))
        end = round(self._yscale().transform(self._ytick_values()[0]))
        start, end = min(start, end), max(start, end)
        self._canvas[start:end, self._yax_width()-1] = "│"
        for value, pos in zip(self._ytick_values(), self._yscale().transform(self._ytick_values())):
            pos = round(pos)
            label = self._fmt(value)
            self._canvas[pos, self._yax_width()-1] = "┤"
            self._rjust_draw(label, self._canvas[pos, bool(self.ylabel)*2:self._yax_width()-1])

        if self.ylabel:
            ylabel = self.ylabel[:end-start]  # make sure it fits
            self._center_draw(ylabel, self._canvas[start:end, 0])

    def _draw_x_axis(self):
        start = round(self._xscale().transform(self._xtick_values()[0]))
        end = round(self._xscale().transform(self._xtick_values()[-1]))
        self._canvas[-self._xax_height(), start:end] = "─"
        before = self.xticklabel_length // 2
        after = self.xticklabel_length - before
        for value, pos in zip(self._xtick_values(), self._xscale().transform(self._xtick_values())):
            pos = round(pos)
            label = self._fmt(value)
            self._canvas[-self._xax_height(), pos] = "┬"
            if pos == start:  # left-adjust first ticklabel
                self._ljust_draw(label[:after], self._canvas[-self._xax_height()+1, pos:pos+after])
            elif pos == end:  # right-adjust last ticklabel
                self._rjust_draw(label[:before+1], self._canvas[-self._xax_height()+1, pos-before:pos+1])
            else:  # center other ticklabels
                self._center_draw(label[:self.xticklabel_length],
                                  self._canvas[-self._xax_height()+1, pos-before:pos+after])

        if self.xlabel:
            xlabel = self.xlabel[:end-start]  # make sure it fits
            self._center_draw(xlabel, self._canvas[-1, start:end])

    def _draw_legend(self):
        # labelstrings = [f"{marker} {label}" for marker, label in self._labels]
        width = max([len(label) for marker, label in self._labels]) + 4
        width = max(width, len("Legend") + 2)
        height = len(self._labels) + 2

        if self.legendloc.startswith("top"):
            top = int(self._yscale().transform(self._ytick_values()[-1]))
        elif self.legendloc.startswith("bottom"):
            top = int(self._yscale().transform(self._ytick_values()[0])) - height + 1
        if self.legendloc.endswith("right"):
            left = int(self._xscale().transform(self._xtick_values()[-1])) - width + 1
        elif self.legendloc.endswith("left"):
            left = int(self._xscale().transform(self._xtick_values()[0]))

        self._canvas[top, left:left+width] = list("┌" + "Legend".center(width-2, "─") + "┐")
        for i, (marker, label) in enumerate(self._labels):
            self._canvas[top+i+1, left:left+width] = list("│" + "  " + label.ljust(width-4) + "│")
            # the marker must be inserted separately in case of ANSI escape characters messing with the string length
            self._canvas[top+i+1, left+1] = marker
        self._canvas[top+len(self._labels)+1, left:left+width] = list("└" + "─"*(width-2) + "┘")

    def _prep(self, x, y, marker, color, label):
        if y is None:  # only y value provided
            x, y = range(len(x)), x
        assert(len(x) == len(y))
        marker = marker[0]
        if color and not self.ascii_only:
            marker = colored(text=marker, color=color)
        if label:
            self._labels.append((marker, label))
        self._clear_scale_cache()
        return x, y, marker, color, label

    def scatter(self, x, y=None, marker="•", color=None, label=None):
        x, y, marker, color, label = self._prep(x, y, marker, color, label)

        def draw_scatter(x, y, marker):
            for xi, yi in zip(self._xscale().transform(x), self._yscale().transform(y)):
                self._canvas[round(yi), round(xi)] = marker
        self._plots.append(partial(draw_scatter, x=x, y=y, marker=marker))

    def line(self, x, y=None, marker="·", color=None, label=None):
        x, y, marker, color, label = self._prep(x, y, marker, color, label)

        def draw_line(x, y, marker):
            xs = self._xscale().transform(x)
            ys = self._yscale().transform(y)
            for (x0, x1), (y0, y1) in zip(zip(xs[: -1], xs[1:]), zip(ys[: -1], ys[1:])):
                for x, y in plot_line_segment(round(x0), round(y0), round(x1), round(y1)):
                    self._canvas[y, x] = marker
        self._plots.append(partial(draw_line, x=x, y=y, marker=marker))

    def bar(self, x, y=None, marker="█", color=None, label=None):
        x, y, marker, color, label = self._prep(x, y, marker, color, label)

        def draw_bar(x, y, marker):
            if is_numerical(self.y):
                origin = self._yscale().transform(min(self._ytick_values(), key=abs))
            else:
                origin = self._yscale().transform(self._ytick_values()[0])
            for xi, yi in zip(self._xscale().transform(x), self._yscale().transform(y)):
                start, end = sorted([origin, yi])
                self._canvas[round(start):round(end)+1, round(xi)] = marker
        self._plots.append(partial(draw_bar, x=x, y=y, marker=marker))

    def hbar(self, x, y=None, marker="█", color=None, label=None):
        x, y, marker, color, label = self._prep(x, y, marker, color, label)

        def draw_hbar(x, y, marker):
            if is_numerical(self.x):
                origin = self._xscale().transform(min(self._xtick_values(), key=abs))
            else:
                origin = self._xscale().transform(self._xtick_values()[0])
            for xi, yi in zip(self._xscale().transform(x), self._yscale().transform(y)):
                start, end = sorted([origin, xi])
                self._canvas[round(yi), round(start):round(end)+1] = marker
        self._plots.append(partial(draw_hbar, x=x, y=y, marker=marker))

    def image(self, image, vmin=None, vmax=None, cmap="block", origin="upper"):
        cmap = "ascii" if self.ascii_only else cmap
        # guess correct value range
        # if (image >= 0).all() and (image <= 1).all():  # between 0 and 1 inclusive
        #     vmin = 0 if vmin is None else vmin
        #     vmax = 1 if vmax is None else vmax
        if image.dtype == np.uint8:  # probably a picture
            vmin = 0 if vmin is None else vmin
            vmax = 255 if vmax is None else vmax
        else:
            vmin = image.flatten().min() if vmin is None else vmin
            vmax = image.flatten().max() if vmax is None else vmax
        self._y_origin = origin

        def draw_image(x, y):
            xmin = round(self._xscale().transform(0))
            ymin = round(self._yscale().transform(0))
            xmax = round(self._xscale().transform(image.shape[1]))
            ymax = round(self._yscale().transform(image.shape[0]))
            ymin, ymax = min(ymin, ymax), max(ymin, ymax)
            drawn = img2ascii(image, width=xmax-xmin+1, height=ymax-ymin+1, vmin=vmin, vmax=vmax, cmap=cmap)
            if origin == "lower":
                drawn = np.flip(drawn, axis=0)
            self._canvas[ymin:ymax+1, xmin:xmax+1] = drawn

        self._plots.append(partial(draw_image, x=tuple(range(image.shape[1])), y=tuple(range(image.shape[0]))))
        self._clear_scale_cache()

    def draw(self):
        # 8 (ANSI escape char) + 1 (marker) + 8 (ANSI escape char) = 17
        self._canvas = np.empty((self.height, self.width), dtype="U17")
        self._canvas[:] = " "

        if self.title:
            title = self.title[:self.width]  # make sure it fits
            self._center_draw(title, self._canvas[0, :])

        self._draw_x_axis()
        self._draw_y_axis()

        for plot in self._plots:
            plot()
        if self._labels:
            self._draw_legend()

        if self.ascii_only:
            for old, new in ASCII_FALLBACK.items():
                self._canvas = np.char.replace(self._canvas, old, new)

    def clear(self):
        self._plots = []
        self._labels = []
        self._clear_scale_cache()

    def _clear_scale_cache(self):
        self._xscale.cache_clear()
        self._yscale.cache_clear()
        self._xtick_values.cache_clear()
        self._ytick_values.cache_clear()
        self._yax_width.cache_clear()

    def __repr__(self):
        self.draw()
        return "\n".join(["".join(row) for row in self._canvas.tolist()])

    def show(self):
        print(self)