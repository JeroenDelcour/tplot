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
# system. Let's write a function that does that.


def linear_transform(X, Y, canvas_width, canvas_height):
    x_min = min(X)
    y_min = min(Y)
    x_range = max(X) - x_min
    y_range = max(Y) - y_min

    def transform(x, y):
        x = int((canvas_width-1)*(x-x_min)/x_range)
        y = int(-(canvas_height-1)*(y-y_min)/y_range)-1  # inverted
        return x, y
    return transform

# Let's also write a function that maps values to geometric objects:


def geom_map(data, geoms=['●', '■', '▲']):
    geoms = ['o', 'x', '#', '*']
    map = {value: geom for value, geom in zip(
        set(data), itertools.cycle(geoms))}
    return lambda v: map[v]


# We're gonna need a canvas to draw on

canvas_width, canvas_height = 16, 9
canvas = [[' ' for w in range(canvas_width)] for h in range(canvas_height)]

# Let's draw our data, using our aesthetic mapping functions

geom = geom_map(dataset['D'])
transform = linear_transform(
    dataset['A'], dataset['C'], canvas_width, canvas_height)
for x, y, g in zip(dataset['A'], dataset['C'], dataset['D']):
    x, y = transform(x, y)
    canvas[y][x] = geom(g)

# Show the plot!

for row in canvas:
    print(''.join(row))
