# Grammar of graphics: https://ucsb-bren.github.io/env-info/refs/lit/Wickham%20-%202010%20-%20A%20Layered%20Grammar%20of%20Graphics.pdf
# Geometric shapes unicode: https://en.wikipedia.org/wiki/Geometric_Shapes

import pandas as pd

dataset = pd.DataFrame({
    'A': [2, 1, 6, 4, 5],
    'B': [3, 2, 3, 5, 10],
    'C': [7, 1, 5, 15, -5],
    'D': ['a', 'a', 'a', 'b', 'b']
})


def aes(x=None, y=None, color=None, shape=None, label=None):
    return {'x': x, 'y': y, 'color': color, 'shape': shape, 'label': label}


def linear_scale(plot):
    X = plot.data[plot.mapping['x']]
    Y = plot.data[plot.mapping['y']]
    X_min = min(X)
    Y_min = min(Y)
    X_range = max(X) - X_min
    Y_range = max(Y) - Y_min

    def scale(x, y):
        x = (plot.width-1)*(x-X_min)/X_range
        y = (plot.height-1)*(y-Y_min)/Y_range
        return int(round(x)), -int(round(y))-1
    return scale


_scales = {'linear': linear_scale}


class Plot:
    def __init__(self, data=None, mapping=None, scale='linear', width=16, height=9):
        self.width = width
        self.height = height
        self.canvas = [['.' for w in range(width)] for h in range(height)]
        self.layers = []
        self.mapping = mapping

        self.data = data

        self.scale = _scales[scale](self)
        self.data_scaled = (self.scale(x, y) for x, y in zip(
            self.data[mapping['x']], self.data[mapping['y']]))

    def __add__(self, layer):
        assert(isinstance(layer, Layer))
        self.layers.append(layer)
        return self

    def draw(self):
        for layer in self.layers:
            layer.draw(plot)
        print('\n'.join((''.join(row) for row in self.canvas)))


class Layer:
    def __init__(self, data, mapping):
        self.data = data
        self.mapping = mapping
        self.plot = None


class geom_point(Layer):
    def __init__(self, data=None, mapping=None, shape='o'):
        super().__init__(data, mapping)
        self.shape = shape

    def draw(self, plot):
        for x, y in plot.data_scaled:
            plot.canvas[y][x] = self.shape


class geom_path(Layer):
    def __init__(self, data=None, mapping=None):
        super().__init__(data, mapping)

    def draw(self, plot):

        def plot_line(x0, y0, x1, y1):
            """ Plot line using Bresenham algorithm. Yields (x, y). """
            if x0 > x1:  # always draw left to right
                x0, x1 = x1, x0
                y0, y1 = y1, y0
            dx = x1 - x0
            dy = y1 - y0
            axes_swapped = False
            if abs(dy) > abs(dx):  # ensure slope is not >1
                axes_swapped = True
                x0, y0, x1, y1 = y0, x0, y1, x1
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

        x0, y0 = next(plot.data_scaled)
        for x1, y1 in plot.data_scaled:
            for x, y in plot_line(x0, y0, x1, y1):
                plot.canvas[y][x] = 'o'
            x0, y0 = x1, y1


plot = Plot(data=dataset, mapping=aes(
    x='A', y='C', shape='D'), width=64, height=32)
plot += geom_path()
plot += geom_point(shape='+')
plot.draw()
