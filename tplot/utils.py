import math
import sys
from bisect import bisect
from numbers import Number
from typing import Generator, Iterable, List
from warnings import warn


def unicode_supported(test_str: str = "─│┤┬┌┐└┘█•·⣿") -> bool:
    """Tries to determine if unicode is supported by encoding a test string containing unicode characters."""
    try:
        test_str.encode(sys.stdout.encoding)
        return True
    except UnicodeEncodeError:
        return False


def _is_numerical(data: Iterable[Number]) -> bool:
    """Returns True if all values in given iterable are numbers."""
    return all([isinstance(value, Number) for value in data])


def _plot_line_segment(
    x0: int, y0: int, x1: int, y1: int
) -> Generator[Iterable[int], None, None]:
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
    D = 2 * dy - dx
    y = y0

    for x in range(x0, x1 + 1):
        yield (y, x) if axes_swapped else (x, y)
        if D > 0:
            y += yi
            D -= 2 * dx
        D += 2 * dy


def _round_away_from_zero(value: float) -> int:
    return math.ceil(value) if value >= 0 else math.floor(value)


def _round_half_away_from_zero(num: float) -> int:
    return ((num > 0) - (num < 0)) * int(abs(num) + 0.5)


def _best_ticks(min_: float, max_: float, most: int) -> list:
    """Returns a list of suitable tick values."""
    most = max(most, 1)
    # find step size
    range_ = max_ - min_
    if range_ == 0:
        return [min_]
    min_step = range_ / most
    magnitude = 10 ** math.floor(math.log(min_step, 10))
    residual = min_step / magnitude
    possible_steps = [1, 2, 5, 10]
    step = possible_steps[bisect(possible_steps, residual)] if residual < 10 else 10
    step *= magnitude
    # generate ticks
    sign = math.copysign(1, min_)
    start = step * round(abs(min_) / step) * sign
    if start > min_:
        start -= step
    return [
        start + i * step
        for i in range(_round_away_from_zero((max_ - start) / step) + 1)
    ]


def _optimize_xticklabel_anchors(
    tick_positions: List[int],
    labels: List[str],
    width: int,
    margin: int = 2,
    stepsize: float = 0.1,
    tolerance: float = 0.3,
    max_iterations: int = 1000,
) -> List[List[int]]:
    """
    Models the placement of tick labels as a 1-dimensional case of a force-directed graph.
    Spring forces between the labels are simulated iteratively until they stabilize.

    Args:
        tick_positions: Ordered positions of the ticks.
        labels: Tick labels.
        width: Width of plot.
        margin: Margin between labels.
        stepsize: Spring force simulation step size.
        tolerance: Tolerance for termination.
        max_iterations: Maximum number of iterations.
    Returns:
        List of [start, end] positions of labels.
    """
    anchors = []
    for tick_pos, label in zip(tick_positions, labels):
        left = tick_pos - len(label) // 2
        right = left + len(label)
        # if anchor is out of bounds, move it inside bounds
        d = right - width
        if d > 0:
            left -= d
            right -= d
        anchors.append([left, right])

    def calc_forces(anchors):
        forces = [0] * len(anchors)
        # forces between labels
        for i in range(len(anchors) - 1):
            f = max(0, anchors[i][1] + margin - anchors[i + 1][0])
            forces[i] -= f
            forces[i + 1] += f
        # figure boundary forces
        forces[0] -= min(0, anchors[0][0])
        forces[-1] -= max(0, anchors[-1][1] - width)
        return forces

    prev_total_forces = float("inf")
    forces = calc_forces(anchors)
    total_forces = sum([abs(f) for f in forces])

    if total_forces == 0:
        return anchors  # early return

    iterations = 0
    while abs(total_forces - prev_total_forces) > tolerance:
        for anchor, force, tick_pos in zip(anchors, forces, tick_positions):
            anchor[0] += force * stepsize
            anchor[1] += force * stepsize
            # don't move beyond tick position
            if round(anchor[0]) > tick_pos:
                d = round(anchor[0]) - tick_pos
                anchor[0] -= d
                anchor[1] -= d
            elif round(anchor[1]) - 1 < tick_pos:
                d = tick_pos - round(anchor[1]) + 1
                anchor[0] += d
                anchor[1] += d

        # recalculate forces
        prev_total_forces = sum([abs(f) for f in forces])
        forces = calc_forces(anchors)
        total_forces = sum([abs(f) for f in forces])

        iterations += 1
        # if iterations == 3:
        #     break
        if iterations >= max_iterations:
            warn(
                f"Max iterations (={max_iterations}) during X axis label placement reached."
            )
            break

    # round anchors
    anchors = [
        [round(anchor[0]), round(anchor[0]) + len(label)]
        for anchor, label in zip(anchors, labels)
    ]
    # limit to figure boundaries
    for anchor in anchors:
        anchor[0] = max(0, anchor[0])
        anchor[1] = min(width, anchor[1])
    # don't overwrite other labels
    for i in range(len(anchors)):
        if i > 0:
            anchors[i][0] = max(tick_positions[i - 1] + 1, anchors[i][0])
        if i < len(anchors) - 1:
            anchors[i][1] = min(tick_positions[i + 1], anchors[i][1])
    return anchors
