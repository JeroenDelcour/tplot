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


def linear_scale(V1, V2, W1, W2):
    """ Returns transform function from vector space V to vector space W. """
    V_range = V2 - V1
    W_range = W2 - W1

    def scale(x):
        return W_range*(x-V1)/V_range+W1
    return scale

# def linear_scale(plot):
#     X = plot.data[plot.mapping['x']]
#     Y = plot.data[plot.mapping['y']]
#     X_min = min(X)
#     Y_min = min(Y)
#     X_range = max(X) - X_min
#     Y_range = max(Y) - Y_min

#     def scale(x, y):
#         x = (plot.width-1)*(x-X_min)/X_range
#         y = (plot.height-1)*(y-Y_min)/Y_range
#         return int(round(x)), -int(round(y))-1
#     return scale

# continuous: float
# discrete: int
# nominal: str
# dichotomous: bool


scales = {'linear': linear_scale}


class Plot:
    def __init__(self, data=None, mapping=None, scale=scales['linear'], width=16, height=9):
        self.layers = []

        # 1. Data and mapping
        X, Y = data[mapping['x']], data[mapping['y']]
        X_min, X_max = min(X), max(X)
        Y_min, Y_max = min(Y), max(Y)

        # 2. Aesthetics and scales
        plot_w = width
        plot_h = height
        self.canvas = canvas = [
            ['.' for w in range(plot_w)] for h in range(plot_h)]

        x_margin = 1
        y_scale = scale(Y_min, Y_max, -x_margin-1, -height)
        y_labels = (Y_min, Y_max)
        y_ticks = [int(y_scale(y)) for y in y_labels]
        y_labels = [str(l) for l in y_labels]
        # max length of y_label strings
        y_margin = max((len(l) for l in y_labels))
        print(X_min, X_max, y_margin, width-1)
        x_scale = scale(X_min, X_max, y_margin, width-1)
        x_labels = (X_min, X_max)
        x_ticks = [int(x_scale(x)) for x in x_labels]
        x_labels = [str(l) for l in x_labels]

        for tick, label in zip(x_ticks, x_labels):
            for i, x in enumerate(range(tick, tick+len(label))):
                canvas[-1][x] = label[i]

        for tick, label in zip(y_ticks, y_labels):
            for i, x in enumerate(range(len(label))):
                canvas[tick][x] = label[i]

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
# plot += geom_path()
# plot += geom_point(shape='+')
plot.draw()
