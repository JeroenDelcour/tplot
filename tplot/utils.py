from bisect import bisect
import math
from numbers import Number
from functools import lru_cache
import sys
from typing import Generator, Iterable


def unicode_supported(test_str="─│┤┬┌┐└┘█•·"):
    """ Tries to determine if unicode is supported by encoding a test string containing unicode characters. """
    try:
        test_str.encode(sys.stdout.encoding)
        return True
    except UnicodeEncodeError:
        return False


def _is_numerical(data: Iterable[Number]) -> bool:
    """ Returns True if all values in given iterable are numbers. """
    return all([isinstance(value, Number) for value in data])


def _plot_line_segment(x0: int, y0: int, x1: int, y1: int) -> Generator[Iterable[int], None, None]:
    """Plot line segment using Bresenham algorithm. Yields (x, y)."""
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


def _round_away_from_zero(value: float) -> int:
    return math.ceil(value) if value >= 0 else math.floor(value)


def _best_ticks(min_: float, max_: float, most: int) -> list:
    """ Returns a list of suitable tick values. """
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
    start = step * round(abs(min_) / step) * sign
    if start > min_:
        start -= step
    return [start+i*step for i in range(_round_away_from_zero((max_-start)/step)+1)]
