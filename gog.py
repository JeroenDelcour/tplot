# Grammar of graphics: https://ucsb-bren.github.io/env-info/refs/lit/Wickham%20-%202010%20-%20A%20Layered%20Grammar%20of%20Graphics.pdf
# Geometric shapes unicode: https://en.wikipedia.org/wiki/Geometric_Shapes

import itertools
import pandas as pd

# To create a complete plot we need three things:
# - data
# - scales and coordinate system
# - plot annotations (title, background, etc.)

# Here's a basic dataset
dataset = pd.DataFrame({
    'A': [2, 1, 4, 9],
    'B': [3, 2, 5, 10],
    'C': [7, 1, 15, 20],
    'D': ['a', 'a', 'b', 'b']
})

# Let's say we want a scatter plot of column A vs column C.
# First we need to map this data into something we can plot:

plottable_dataset = pd.DataFrame({
    'x': [25, 0, 75, 200],
    'y': [11, 0, 53, 300],
    'shape': ['circle', 'circle', 'square', 'square']
})

# To do this, we need functions that map the data to aesthetics.
# I.e. map column A to x-coordinates, column C to y-coordinates,
# and column D to geometric shapes. Since A and C are continuous,
# we choose to map them using a linear scale to a Cartesian coordinate
# system. Let's write a function that creates these mappings.


def aes(x=None, y=None, color=None, shape=None, label=None):
    """ Aesthetic mapping. """
    mapping = {}
    if x is not None:
        x_min = min(x)
        x_range = max(x) - x_min
        mapping['x'] = (int((canvas_width-1)*(x_i-x_min)/x_range)
                        for x_i in x)
    if y is not None:
        y_min = min(y)
        y_range = max(y) - y_min
        mapping['y'] = (int(-(canvas_height-1)*(y_i-y_min)/y_range)-1
                        for y_i in y)
    shapes = ['●', '■', '▲']
    if shape is not None:
        shapemap = {v: g for v, g in zip(set(shape), itertools.cycle(shapes))}
        mapping['shape'] = (shapemap[shape_i] for shape_i in shape)
    else:
        mapping['shape'] = itertools.cycle(shapes[0])
    return mapping


# We're gonna need a canvas to draw on


canvas_width, canvas_height = 16, 9
canvas = [[' ' for w in range(canvas_width)] for h in range(canvas_height)]

# Let's draw our data, using our aesthetic mappings.

mapping = aes(x=dataset['A'], y=dataset['C'], shape=dataset['D'])
for idx, row in dataset.iterrows():
    for x, y, shape in zip(mapping['x'], mapping['y'], mapping['shape']):
        canvas[y][x] = shape

# Show the plot!

for row in canvas:
    print(''.join(row))
