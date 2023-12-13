from functools import cached_property, partial
from numbers import Number
from shutil import get_terminal_size
from typing import Callable, Iterable, List, Optional, Tuple

import numpy as np
from colorama import init
from termcolor import colored

from . import utils
from .braille import draw_braille, is_braille
from .img2ascii import img2ascii
from .scales import CategoricalScale, LinearScale

init()


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
    "·": ".",
}


class Figure:
    """
    Figure to draw plots onto.

    Args:
        xlabel: Label for the x axis.
        ylabel: Label for the y axis.
        title: Title of the figure.
        width: Width of the figure in number of characters. Defaults to the terminal window width, or falls back to 80.
        height: Height of the figure in number of characters. Defaults to the terminal window height, or falls back to 24.
        legendloc: Legend location. Supported values are `"topleft"`, `"topright"`, `"bottomleft"`, and `"bottomright"`.
        ascii: Set to `True` to only use ascii characters. Defaults to trying to detect if unicode is supported in the terminal.
        y_axis_direction: Set to `"up"` to have Y axis point up (conventional for graphs), `"down"` to have Y axis point down
                          (conventional for images). By default, this is automatically determined based on the drawn plots.
    """

    def __init__(
        self,
        xlabel: Optional[str] = None,
        ylabel: Optional[str] = None,
        title: Optional[str] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        legendloc: str = "topright",
        ascii: bool = False,
        y_axis_direction: str = "auto",
    ) -> None:
        if legendloc not in {"topleft", "topright", "bottomleft", "bottomright"}:
            raise ValueError("Unsupported legend location")
        if width is not None:
            assert isinstance(width, int) and width > 0
        if height is not None:
            assert isinstance(height, int) and height > 0

        self._xlabel = xlabel
        self._ylabel = ylabel
        self.title = title
        self.legendloc = legendloc

        self._y_axis_direction = y_axis_direction

        self.ascii_only = ascii
        if not self.ascii_only:
            self.ascii_only = not utils.unicode_supported()

        term_width, term_height = get_terminal_size(fallback=(80, 24))
        term_height -= 1  # room for prompt
        self.width = width if width else term_width
        self.height = height if height else term_height

        # gather stuff to plot before actually drawing it
        self._plots: List[Callable] = []
        self._labels: List[Tuple[str, str]] = []

    @property
    def _x(self):
        return tuple([x for plot in self._plots for x in plot.keywords["x"]])

    @property
    def _y(self):
        return tuple([y for plot in self._plots for y in plot.keywords["y"]])

    @cached_property
    def _yscale(self):
        if utils._is_numerical(self._y):
            scale = LinearScale()
        else:
            scale = CategoricalScale()
        target_min = -self._xax_height() - 1
        target_max = -self.height + 1 + bool(self.title)
        if self._y_axis_direction == "down":
            target_min, target_max = target_max, target_min
        scale.fit(self._y, target_min, target_max)
        if utils._is_numerical(self._y):
            # refit scale to tick values, since those lay just outside the input data range
            scale.fit(self._ytick_values, target_min, target_max)
        return scale

    @cached_property
    def _xscale(self):
        if utils._is_numerical(self._x):
            scale = LinearScale()
        else:
            scale = CategoricalScale()
        target_min = self._yax_width
        target_max = self.width - 1
        scale.fit(self._x, target_min, target_max)
        if utils._is_numerical(self._x):
            # refit scale to tick values, since those lay just outside the input data range
            scale.fit(self._xtick_values, target_min, target_max)
        return scale

    def _xax_height(self) -> int:
        return 2 + bool(self._xlabel)

    def _fmt(self, value) -> str:
        if isinstance(value, Number):
            return f"{value:.3g}"
        else:
            return str(value)

    @cached_property
    def _yax_width(self) -> int:
        """
        Since y-axis tick labels are drawn horizontally, the width of the y axis
        depends on the length of the labels, which themselves depend on the data.
        """
        labels = (self._fmt(value) for value in self._ytick_values)
        width = max([len(label) for label in labels])
        width += 1  # for axis ticks
        width += bool(self._ylabel) * 2  # for y label
        return width

    def _center_draw(self, string, array, fillchar=" "):
        array[:] = list(string.center(len(array), fillchar))

    def _ljust_draw(self, string, array, fillchar=" "):
        array[:] = list(string.ljust(len(array), fillchar))

    def _rjust_draw(self, string, array, fillchar=" "):
        array[:] = list(string.rjust(len(array), fillchar))

    @cached_property
    def _ytick_values(self):
        if utils._is_numerical(self._y):
            return utils._best_ticks(min(self._y), max(self._y), most=self.height // 3)
        else:  # nominal
            values = tuple(sorted([str(v) for v in set(self._y)]))
            y_axis_height = self.height - bool(self.title) - self._xax_height()
            if len(values) > y_axis_height:
                raise IndexError(
                    f"Too many ({len(values)}) unique y values to fit into y axis. Try making the figure taller."
                )
            return values

    @cached_property
    def _xtick_values(self):
        if utils._is_numerical(self._x):
            return utils._best_ticks(min(self._x), max(self._x), most=self.width // 5)
        else:  # categorical
            # note this may not fit depending on the width of the figure
            values = tuple(sorted([str(v) for v in set(self._x)]))
            return values

    def _draw_y_axis(self) -> None:
        start = round(self._yscale.transform(self._ytick_values[-1]))
        end = round(self._yscale.transform(self._ytick_values[0]))
        start, end = min(start, end), max(start, end)
        self._canvas[start:end, self._yax_width - 1] = "│"
        for value, pos in zip(
            self._ytick_values, self._yscale.transform(self._ytick_values)
        ):
            pos = round(pos)
            label = self._fmt(value)
            self._canvas[pos, self._yax_width - 1] = "┤"
            self._rjust_draw(
                label, self._canvas[pos, bool(self._ylabel) * 2 : self._yax_width - 1]
            )

        if self._ylabel:
            ylabel = self._ylabel[: end - start]  # make sure it fits
            self._center_draw(ylabel, self._canvas[start:end, 0])

    def _draw_x_axis(self) -> None:
        tick_positions = [round(v) for v in self._xscale.transform(self._xtick_values)]
        labels = [self._fmt(v) for v in self._xtick_values]
        # draw axis
        axis_start = round(self._xscale.transform(self._xtick_values[0]))
        axis_end = round(self._xscale.transform(self._xtick_values[-1]))
        self._canvas[-self._xax_height(), axis_start:axis_end] = "─"
        # draw ticks
        for tick_pos in tick_positions:
            self._canvas[-self._xax_height(), tick_pos] = "┬"
        # draw labels
        anchors = utils._optimize_xticklabel_anchors(
            tick_positions=tick_positions, labels=labels, width=self.width
        )
        for (start, end), label in zip(anchors, labels):
            label = label[: end - start]  # shorten label if needed
            self._canvas[-self._xax_height() + 1, start:end] = list(label)
        # draw axis label
        if self._xlabel:
            xlabel = self._xlabel[: axis_end - axis_start]  # make sure it fits
            self._center_draw(xlabel, self._canvas[-1, axis_start:axis_end])

    def _draw_legend(self) -> None:
        width = max([len(label) for marker, label in self._labels]) + 4
        width = max(width, len("Legend") + 2)
        height = len(self._labels) + 2

        if self.legendloc.startswith("top"):
            top = int(self._yscale.transform(self._ytick_values[-1]))
        elif self.legendloc.startswith("bottom"):
            top = int(self._yscale.transform(self._ytick_values[0])) - height + 1
        if self.legendloc.endswith("right"):
            left = int(self._xscale.transform(self._xtick_values[-1])) - width + 1
        elif self.legendloc.endswith("left"):
            left = int(self._xscale.transform(self._xtick_values[0]))

        self._canvas[top, left : left + width] = list(
            "┌" + "Legend".center(width - 2, "─") + "┐"
        )
        for i, (marker, label) in enumerate(self._labels):
            self._canvas[top + i + 1, left : left + width] = list(
                "│" + "  " + label.ljust(width - 4) + "│"
            )
            # the marker must be inserted separately in case of ANSI escape characters messing with the string length
            self._canvas[top + i + 1, left + 1] = marker
        self._canvas[top + len(self._labels) + 1, left : left + width] = list(
            "└" + "─" * (width - 2) + "┘"
        )

    def _prep(self, x, y, marker, color, label) -> tuple:
        """Data preparation stuff common to all plots."""
        x_is_valid = x is not None and len(x) > 0
        y_is_valid = y is not None and len(y) > 0
        if not x_is_valid and not y_is_valid:
            raise ValueError("`x` and/or `y` must be provided and not be empty")

        if not x_is_valid and y_is_valid:
            # only `y` is provided
            x = range(len(y))
        if x_is_valid and y is None:
            # only `x` is provided, assume `x` is `y`
            x, y = range(len(x)), x

        if not len(x) == len(y):
            raise ValueError("`x` and `y` must have the same length")

        if marker == "braille":
            marker = "⠄" if not self.ascii_only else "."
        else:
            marker = marker[0]
        if color and not self.ascii_only:
            marker = colored(text=marker, color=color)
        if label:
            self._labels.append((marker, label))
        self._clear_scale_cache()
        return x, y, marker, color, label

    def scatter(
        self,
        x: Optional[Iterable] = None,
        y: Optional[Iterable] = None,
        marker: str = "•",
        color: Optional[str] = None,
        label: Optional[str] = None,
    ) -> None:
        """
        Adds scatter plot.

        Args:
            x: x data. If `y` is not provided, `x` is assumed to be y data.
            y: y data.
            marker: Marker used to draw points. Set to `"braille"` to use braille characters.
            color: Color of marker. Supported values are `"grey"`, `"red"`, `"green"`, `"yellow"`, `"blue"`, `"magenta"`, `"cyan"`, and `"white"`.
            label: Label to use for legend.
        """
        x, y, marker, color, label = self._prep(x, y, marker, color, label)

        def draw_scatter(x, y, marker):
            for xi, yi in zip(self._xscale.transform(x), self._yscale.transform(y)):
                if not self.ascii_only and any((is_braille(char) for char in marker)):
                    xi = utils._round_half_away_from_zero(xi)
                    yi = utils._round_half_away_from_zero(yi)
                    marker = draw_braille(xi, yi, self._canvas[yi, xi])
                    if color:
                        marker = colored(marker, color)
                    self._canvas[yi, xi] = marker
                else:
                    self._canvas[round(yi), round(xi)] = marker

        self._plots.append(partial(draw_scatter, x=x, y=y, marker=marker))

    def line(
        self,
        x: Optional[Iterable] = None,
        y: Optional[Iterable] = None,
        marker: str = "braille",
        color: Optional[str] = None,
        label: Optional[str] = None,
    ) -> None:
        """
        Adds line plot.

        Args:
            x: x data. If `y` is not provided, `x` is assumed to be y data.
            y: y data.
            marker: Marker used to draw lines. Set to `"braille"` to use braille characters.
            color: Color of marker. Supported values are `"grey"`, `"red"`, `"green"`, `"yellow"`, `"blue"`, `"magenta"`, `"cyan"`, and `"white"`.
            label: Label to use for legend.
        """
        x, y, marker, color, label = self._prep(x, y, marker, color, label)

        def draw_line(x, y, marker):
            xs = self._xscale.transform(x)
            ys = self._yscale.transform(y)
            for (x0, x1), (y0, y1) in zip(zip(xs[:-1], xs[1:]), zip(ys[:-1], ys[1:])):
                if not self.ascii_only and any((is_braille(char) for char in marker)):
                    for x, y in utils._plot_line_segment(
                        round(x0 * 2), round(y0 * 4), round(x1 * 2), round(y1 * 4)
                    ):
                        x = x / 2
                        y = y / 4
                        x_canvas = utils._round_half_away_from_zero(x)
                        y_canvas = utils._round_half_away_from_zero(y)
                        marker = draw_braille(x, y, self._canvas[y_canvas, x_canvas])
                        if color:
                            marker = colored(marker, color)
                        self._canvas[y_canvas, x_canvas] = marker
                else:
                    for x, y in utils._plot_line_segment(
                        round(x0), round(y0), round(x1), round(y1)
                    ):
                        self._canvas[y, x] = marker

        self._plots.append(partial(draw_line, x=x, y=y, marker=marker))

    def bar(
        self,
        x: Optional[Iterable] = None,
        y: Optional[Iterable] = None,
        marker: str = "█",
        color: Optional[str] = None,
        label: Optional[str] = None,
    ) -> None:
        """
        Adds vertical bar plot.

        Args:
            x: x data. If `y` is not provided, `x` is assumed to be y data.
            y: y data.
            marker: Marker used to draw bars. Set to `"braille"` to use braille characters.
            color: Color of marker. Supported values are `"grey"`, `"red"`, `"green"`, `"yellow"`, `"blue"`, `"magenta"`, `"cyan"`, and `"white"`.
            label: Label to use for legend.
        """
        x, y, marker, color, label = self._prep(x, y, marker, color, label)

        def draw_bar(x, y, marker):
            marker = marker.replace("⠄", "⡇")  # in case of braille
            if utils._is_numerical(self._y):
                origin = self._yscale.transform(min(self._ytick_values, key=abs))
            else:
                origin = self._yscale.transform(self._ytick_values[0])
            for xi, yi in zip(self._xscale.transform(x), self._yscale.transform(y)):
                start, end = sorted([origin, yi])
                self._canvas[round(start) : round(end) + 1, round(xi)] = marker

        self._plots.append(partial(draw_bar, x=x, y=y, marker=marker))

    def hbar(
        self,
        x: Optional[Iterable] = None,
        y: Optional[Iterable] = None,
        marker: str = "█",
        color: Optional[str] = None,
        label: Optional[str] = None,
    ) -> None:
        """
        Adds horizontal bar plot.

        Args:
            x: x data. If `y` is not provided, `x` is assumed to be y data.
            y: y data.
            marker: Marker used to draw bars. Set to `"braille"` to use braille characters.
            color: Color of marker. Supported values are `"grey"`, `"red"`, `"green"`, `"yellow"`, `"blue"`, `"magenta"`, `"cyan"`, and `"white"`.
            label: Label to use for legend.
        """
        x, y, marker, color, label = self._prep(x, y, marker, color, label)

        def draw_hbar(x, y, marker):
            marker = marker.replace("⠄", "⠒")  # in case of braille
            if utils._is_numerical(self._x):
                origin = self._xscale.transform(min(self._xtick_values, key=abs))
            else:
                origin = self._xscale.transform(self._xtick_values[0])
            for xi, yi in zip(self._xscale.transform(x), self._yscale.transform(y)):
                start, end = sorted([origin, xi])
                self._canvas[round(yi), round(start) : round(end) + 1] = marker

        self._plots.append(partial(draw_hbar, x=x, y=y, marker=marker))

    def text(self, x, y, text: str, color: Optional[str] = None) -> None:
        """
        Adds text.

        Args:
            x: x location (text is left-aligned).
            y: y location.
            text: Text to draw.
            color: Color of text. Supported values are `"grey"`, `"red"`, `"green"`, `"yellow"`, `"blue"`, `"magenta"`, `"cyan"`, and `"white"`.
        """
        if color and not self.ascii_only:
            text = colored(text, color)

        def draw_text(x, y, text):
            x0 = round(self._xscale.transform(x[0]))
            y0 = round(self._yscale.transform(y[0]))
            for i, char in enumerate(text):
                if x0 + i >= self.width:
                    break
                self._canvas[y0, x0 + i] = char

        self._plots.append(partial(draw_text, x=[x], y=[y], text=text))

    def image(
        self,
        image: np.ndarray,
        vmin: Optional[float] = None,
        vmax: Optional[float] = None,
        cmap: str = "block",
    ) -> None:
        """
        Adds image.

        Note that this sets the Y axis direction to point down, unless `y_axis_direction` is set otherwise in Figure init.

        Args:
            image: 2D array.
            vmin: Minimum value covered by the colormap. Lower values are clipped.
                  If set to `None`, uses 0 if the `dtype` of image is `numpy.uint8` (usual for pictures), `min(image)` otherwise.
            vmax: Maximum value covered by the colormap. Higher values are clipped.
                  If set to `None`, uses 255 if the `dtype` of image is `numpy.uint8` (usual for pictures), `max(image)` otherwise.
            cmap: Colormap used to map image values to characters. Currently supported cmaps are `"ascii"` and `"block"`.
        """
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

        if self._y_axis_direction == "auto":
            self._y_axis_direction = "down"

        def draw_image(x, y):
            xmin = round(self._xscale.transform(0))
            ymin = round(self._yscale.transform(0))
            xmax = round(self._xscale.transform(image.shape[1]))
            ymax = round(self._yscale.transform(image.shape[0]))
            ymin, ymax = min(ymin, ymax), max(ymin, ymax)
            drawn = img2ascii(
                image,
                width=xmax - xmin + 1,
                height=ymax - ymin + 1,
                vmin=vmin,
                vmax=vmax,
                cmap=cmap,
            )
            if self._y_axis_direction != "down":
                drawn = np.flip(drawn, axis=0)
            self._canvas[ymin : ymax + 1, xmin : xmax + 1] = drawn

        self._plots.append(
            partial(
                draw_image,
                x=tuple(range(image.shape[1] + 1)),
                y=tuple(range(image.shape[0] + 1)),
            )
        )
        self._clear_scale_cache()

    def _draw(self) -> None:
        if not self._plots:
            raise ValueError("No plots to draw.")

        # 8 (ANSI escape char) + 1 (marker) + 8 (ANSI escape char) = 17
        self._canvas = np.empty((self.height, self.width), dtype="U17")
        self._canvas[:] = " "

        try:
            if self.title:
                title = self.title[: self.width]  # make sure it fits
                self._center_draw(title, self._canvas[0, :])

            self._draw_x_axis()
            self._draw_y_axis()

            for plot in self._plots:
                plot()
            if self._labels:
                self._draw_legend()
        except IndexError:
            raise IndexError("Drawing out of bounds. Try increasing the figure size.")

        if self.ascii_only:
            for old, new in ASCII_FALLBACK.items():
                self._canvas = np.char.replace(self._canvas, old, new)

    def clear(self) -> None:
        """Clears previously added plots."""
        self._plots = []
        self._labels = []
        self._clear_scale_cache()

    def _clear_scale_cache(self) -> None:
        # clear cached values if cached, otherwise do nothing
        self.__dict__.pop("_xscale", None)
        self.__dict__.pop("_yscale", None)
        self.__dict__.pop("_xtick_values", None)
        self.__dict__.pop("_ytick_values", None)
        self.__dict__.pop("_yax_width", None)

    def __str__(self) -> str:
        self._draw()
        return "\n".join(["".join(row) for row in self._canvas.tolist()])

    def show(self) -> None:
        """
        Prints the figure.

        Note that to get the figure as a string (to write to a file, for example), you can simply convert it to str type: `str(fig)`
        """
        print(str(self))
