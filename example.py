import tplot

anscombeA = [
    [10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5],
    [8.04, 6.95, 7.58, 8.81, 8.33, 9.96, 7.24, 4.26, 10.84, 4.82, 5.68]
]
anscombeB = [
    [10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5],
    [9.14, 8.14, 8.74, 8.77, 9.26, 8.10, 6.13, 3.10, 9.13, 7.26, 4.74]
]
# sort by X value
anscombeA = list(zip(*[(x, y) for x, y in sorted(zip(*anscombeA))]))
anscombeB = list(zip(*[(x, -y) for x, y in sorted(zip(*anscombeB))]))

fig = tplot.Figure(xlabel="x label", ylabel="y label", title="Anscombe", legendloc="bottomright")
fig.scatter(x=anscombeA[0], y=anscombeA[1], label="Anscombe I")
fig.scatter(*anscombeB, label="Anscombe II", marker="+")
fig.show()
