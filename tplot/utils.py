from bisect import bisect
import math
from numbers import Number
from functools import lru_cache
import sys
from typing import Generator, Iterable


def unicode_supported(test_str="┌┬┐╔╦╗╒╤╕╓╥╖│║─═├┼┤╠╬╣╞╪╡╟╫╢└┴┘╚╩╝╘╧╛╙╨╜"):
    try:
        test_str.encode(sys.stdout.encoding)
        return True
    except UnicodeEncodeError:
        return False


def is_numerical(data: Iterable[Number]) -> bool:
    return all([isinstance(value, Number) for value in data])


def plot_line_segment(x0: int, y0: int, x1: int, y1: int) -> Generator[Iterable[int], None, None]:
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


def round_away_from_zero(value: float) -> int:
    return math.ceil(value) if value >= 0 else math.floor(value)


def best_ticks(min_: float, max_: float, most: int) -> list:
    """Returns a list of suitable tick values."""
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
    return [start+i*step for i in range(round_away_from_zero((max_-start)/step)+1)]


def get_braille(s):
    """
    `s` is a string of '1's and '0's specifying which dots in the desired braille character must be on ('1')
    and which must be off ('0').
    Dots in the 2x8 braille matrix are ordered top-down, left-to-right, i.e:

    a •• e
    b •• f
    c •• g
    d •• h

    Schematic example:

    •    10
     •   01
    •• = 11
     •   01

    ⢵ = '10100111'

    More examples:
    '10000000' = ⠁ (only top left dot)
    '00011110' = ⡸
    '11001111' = ⢻
    '11111111' = ⣿
    '00000000' = ⠀ (empty braille character)

    For more info on the interesting relationship between binary and unicode braille dot ordering, see: https://en.wikipedia.org/wiki/Braille_Patterns#Identifying,_naming_and_ordering
    """
    s = s[:3] + s[4:7] + s[3] + s[7]  # rearrange ISO/TR 11548-1 dot order to something more managable
    return chr(10240 + int(s[::-1], 2))


def test_braille():
    assert(get_braille('10000000') == '⠁')
    assert(get_braille('11001111') == '⢻')
    assert(get_braille('11001111') == '⢻')
    assert(get_braille('11111111') == '⣿')
    assert(get_braille('00011110') == '⡸')
    assert(get_braille('00000000') == '⠀')
    print('All tests completed succesfully.')
