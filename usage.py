from gog3 import *

anscombeA = [
    [10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5],
    [8.04, 6.95, 7.58, 8.81, 8.33, 9.96, 7.24, 4.26, 10.84, 4.82, 5.68]
]
# sort by X value
anscombeA = list(zip(*[(x, y) for x, y in sorted(zip(*anscombeA))]))

fig = Figure(x=anscombeA[0], y=anscombeA[1], xlabel="x label", ylabel="y label", title="Anscombe I")
fig.line(marker="*")
fig.scatter(marker="o")
fig.show()
