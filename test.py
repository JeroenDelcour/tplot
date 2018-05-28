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
    X = [0,1,2,3,4,5,6,7,8,9,10]
    Y = [0,1,2,3,4,5,6,7,8,9,10]
    scatter(X, Y, size=small)
    print()
    X, Y = range(-5,1), range(-10,-4)
    scatter(X, Y, marker='+', color='red', bgcolor='blue', size=small)
    print()
    values = np.arange(0, np.pi*2, np.pi/20)
    r = 4
    X = r * np.cos(values)
    Y = r * np.sin(values)
    scatter(X, Y, marker='o', color='yellow', size=small)
    print()
    X1 = np.arange(-5,6)
    X2 = X1
    Y1 = np.arange(-5,6)
    Y2 = -Y1
    scatter((X1,X2), (Y1,Y2), marker='*', color=['red', 'white'],
               xlim=(-12,12), ylim=(-6,6), size=small)
    print()
    X = np.arange(0,15,.1)
    Y = np.cos(X)
    df = pd.DataFrame({'X': X, 'Y': Y})
    scatter(df['X'], df['Y'], bgcolor='white')
    print()

    return 'All tests finished in {:G} seconds.'.format(time()-t0)

if __name__=="__main__":
    print(test())
