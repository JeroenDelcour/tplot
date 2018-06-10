#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from plot import scatter

def test():
    from math import sin, cos
    from time import time
    import numpy as np
    import pandas as pd

    small = (32,12)
    t0 = time()

    X = [0,1,2,3,4,5,6,7,8,9]
    Y = [0,1,2,3,4,5,6,7,8,9]
    scatter(X, Y, size=small)
    print()
    X, Y = range(-5,1), range(-10,-4)
    scatter(X, Y, marker='+', color='red', bgcolor='blue', size=small)
    print()
    X1 = np.arange(-5,5,.1)
    Y1 = np.arange(-5,5,.1)
    X2 = X1
    Y2 = -Y1
    scatter((X1,X2), (Y1,Y2), color=['red', 'white'],
               xlim=(-6,6), ylim=(-6,6), size=small)
    print()
    X = np.arange(0,15,.01)
    df = pd.DataFrame({'X': X, 'cos': np.cos(X), 'sin': np.sin(X)})
    scatter([df['X'], df['X']], (df['sin'], df['cos']), color=['cyan', 'magenta'],
            marker=[None, '+'])
    print()
    values = np.arange(0, np.pi*2, np.pi/200)
    r = 3
    d = 3.2
    X, Y = [], []
    for i in range(3):
        X += [r * np.cos(values) + r + 2*d*i]
        Y += [r * np.sin(values) + r + d]
    X += [r * np.cos(values) + r + d]
    Y += [r * np.sin(values) + r]
    X += [r * np.cos(values) + 3 + 3*d]
    Y += [r * np.sin(values) + r]
    scatter(X, Y, color=['blue', 'black', 'red', 'yellow', 'green'], bgcolor='white')
    print()

    return 'All tests finished in {:G} seconds.'.format(time()-t0)

if __name__=="__main__":
    print(test())
