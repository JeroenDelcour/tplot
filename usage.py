from gog3 import *

anscombeA = [
    sorted([10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5]),
    sorted([8.04, 6.95, 7.58, 8.81, 8.33, 9.96, 7.24, 4.26, 10.84, 4.82, 5.68])
]

fig = Figure(x=anscombeA[0], y=anscombeA[1])
fig.line(marker="*")
fig.scatter(marker="o")
fig.show()
