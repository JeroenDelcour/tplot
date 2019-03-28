# Grammar of graphics: https://ucsb-bren.github.io/env-info/refs/lit/Wickham%20-%202010%20-%20A%20Layered%20Grammar%20of%20Graphics.pdf
# Geometric shapes unicode: https://en.wikipedia.org/wiki/Geometric_Shapes
# Useful: https://towardsdatascience.com/a-comprehensive-guide-to-the-grammar-of-graphics-for-effective-visualization-of-multi-dimensional-1f92b4ed4149

import math
from bisect import bisect
from itertools import repeat


dataset = {
    'Aardvark': [2, 1, 6, 4, 5],
    'Betadine': [3, 2, 3, 5, 10],
    'Cylindrical': [7, 1, 5, 15, -5],
    'Dirk': ['aantonend', 'afstoten', 'aardig', 'bij', 'bezig']
}


def generate_scale(data, W1, W2):
    def linear(data, W1, W2):
        """ Returns transform function from vector space V to vector space W. """
        V1 = min(data)
        V2 = max(data)
        V_range = V2 - V1
        W_range = W2 - W1

        if V_range == 0:
            return lambda: W1

        def linear(v):
            try:
                return (W_range*(vi-V1)/V_range+W1 for vi in v)
            except:
                return W_range*(v-V1)/V_range+W1
        return linear

    def discrete(data, W1, W2):
        s = sorted(set(data))
        if W2-W1 <= len(s):
            sign = +1 if W2 >= W1 else -1
            d = {v: W1+i*sign for i, v in enumerate(s)}
        else:
            linear_scaler = linear(range(len(s)), W1, W2)
            d = {v: linear_scaler(i) for i, v in enumerate(s)}

        def discrete(v):
            return d[v]
        return discrete

    try:
        return linear(data, W1, W2)
    except TypeError:
        return discrete(data, W1, W2)


def geom_point(marker=None):
    def geom_point_fn(canvas, scaled_data, marker=marker):
        for x, y, m in zip(scaled_data['x'](), scaled_data['y'](), scaled_data['marker']()):
            canvas[int(y)][int(x)] = m if not marker else marker
        return canvas
    return geom_point_fn


def geom_path(marker=None):

    def plot_line(x0, y0, x1, y1):
        """ Plot line using Bresenham algorithm. Yields (x, y). """
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

    def geom_path_fn(canvas, scaled_data, marker=marker):
        X, Y = scaled_data['x'](), scaled_data['y']()
        x0, y0 = next(X), next(Y)
        for x1, y1, m in zip(X, Y, scaled_data['marker']()):
            for x, y in plot_line(int(x0), int(y0), int(x1), int(y1)):
                canvas[y][x] = m if not marker else marker
            x0, y0 = x1, y1

        return canvas
    return geom_path_fn


aes_defaults = {'x': 0,
                'y': 0,
                'marker': "\u2022"}


def aes(x=None,
        y=None,
        marker=None):
    if all([dim == None for dim in locals().values()]):
        raise ValueError('At least one aesthetic must be mapped to the data.')
    return locals()


class Plot:
    def __init__(self, data, mapping, width=64, height=32):

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

        def y_aesthetics(data, height):
            y_scale = generate_scale(data['y'], -3, -height)
            if y_scale.__name__ == "discrete":
                y_labels = set(data['y'])
            else:
                y_labels = best_ticks(min(data['y']), max(
                    data['y']), most=int((height-2)/2))
            y_ticks = [int(y_scale(y)) for y in y_labels]
            if y_scale.__name__ != "discrete":
                y_labels = ['{:.6g}'.format(l) for l in y_labels]
            # max length of y label strings
            margin_left = max((len(l) for l in y_labels)) + 2
            return y_scale, y_ticks, y_labels, margin_left

        def x_aesthetics(data, width, margin_left):
            x_scale = generate_scale(
                data['x'], margin_left, width-1)
            if x_scale.__name__ == "discrete":
                x_labels = set(data['x'])
            else:
                x_labels = best_ticks(
                    min(data['x']), max(data['x']), most=int((width-margin_left)/(6+1)))
            x_ticks = [int(x_scale(x)) for x in x_labels]
            if x_scale.__name__ != "discrete":
                x_labels = ['{:.6g}'.format(l) for l in x_labels]
            return x_scale, x_ticks, x_labels

        def draw_axes(canvas, margin_left):
            for y in range(0, len(canvas)-3):  # y axis
                canvas[y][margin_left] = "\u2502"
            for x in range(margin_left+1, len(canvas[0])):  # x axis
                canvas[-3][x] = "\u2500"
            canvas[-3][margin_left] = "\u253C"  # origin
            return canvas

        def draw_x_ticks(canvas, ticks, labels):
            for tick, label in zip(ticks, labels):
                canvas[-3][tick] = "\u252C"
                if tick == len(canvas[0])-1:  # right-align last tick
                    start = tick - len(label) + 1
                else:
                    start = tick-int(len(label)/2)
                canvas[-2][start:start+len(label)] = list(label)
            return canvas

        def draw_y_ticks(canvas, ticks, labels, margin_left):
            for tick, label in zip(ticks, labels):
                canvas[tick][margin_left-len(label):margin_left] = list(label)
                canvas[tick][margin_left] = "\u2524"
            return canvas

        def draw_y_axis_label(canvas, label):
            height = len(canvas)-1
            center = int(height/2)
            start = center - int(len(label)/2)
            for l, y in zip(label, range(start, start+len(label)+1)):
                canvas[y][0] = l
            return canvas

        def draw_x_axis_label(canvas, label, margin_left):
            width = len(canvas[0]) - margin_left
            center = int(width/2)
            start = center - int(len(label)/2)
            for l, x in zip(label, range(start, start+len(label)+1)):
                canvas[-1][margin_left+x] = l
            return canvas

        def map_aes(data, mapping, defaults):
            """ Indexes data by aesthetic, inserting default values. """
            for v in mapping.values():
                if v is not None and not v in data:
                    raise KeyError("'{}' not in data".format(v))
            dim_lengths = list(
                map(len, (v for k, v in data.items() if v is not None)))
            if not dim_lengths.count(dim_lengths[0]) == len(dim_lengths):
                raise ValueError('Data dimensions must all be same length.')
            return {dim: data[key] if key is not None else [defaults[dim]]*dim_lengths[0]
                    for dim, key in mapping.items()}

        data = map_aes(data, mapping, aes_defaults)
        scales = {dim: lambda v: v for dim in (
            'x', 'y', 'marker')}  # identity functions

        # aesthetics order:
        # 1. marker/color/etc. (anything that needs a legend)
        # 2. y (to determine margin_left, since margin_right is fixed)
        # 3. x

        margin_left = 0
        if mapping['y']:
            scales['y'], y_ticks, y_labels, margin_left = y_aesthetics(
                data, height)
            if scales['y'].__name__ == "discrete_scaler":
                # resize plot to fit
                min_scale_height = -scales['y'](max(data['y']))
                min_y_label_height = len(mapping['y'])+1
                height = max(min_scale_height, min_y_label_height)
        else:
            height = 4

        if mapping['x']:
            scales['x'], x_ticks, x_labels = x_aesthetics(
                data, width, margin_left)
        else:
            width = margin_left + 2
            scales['x'] = lambda x: margin_left + 1

        canvas = [
            [' ' for w in range(width)] for h in range(height)]

        canvas = draw_axes(canvas, margin_left)
        if mapping['x']:
            canvas = draw_x_ticks(canvas, x_ticks, x_labels)
        if mapping['y']:
            canvas = draw_y_ticks(canvas, y_ticks, y_labels, margin_left)
        if mapping['x'] and mapping['y']:
            canvas[-3][margin_left] = "\u253C"  # draw origin
        if mapping['y']:
            canvas = draw_y_axis_label(canvas, mapping['y'])
        if mapping['x']:
            canvas = draw_x_axis_label(canvas, mapping['x'], margin_left)

        self.scaled_data = {dim: lambda s=scales[dim], d=data: map(s, d)
                            for dim, data in data.items()}
        self.canvas = canvas

    def __add__(self, geom):
        self.canvas = geom(self.canvas, self.scaled_data)
        return self

    def __repr__(self):
        return '\n'.join((''.join(row) for row in self.canvas))


print(Plot(dataset, aes(y='Aardvark', x='Dirk')) +
      geom_point(marker='+'))
