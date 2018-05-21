#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from plot import *

def test():
    from math import sin, cos
    from time import time

    small = (33,13)
    t0 = time()
    X = [0,1,2,3,4,5,6,7,8,9,10]
    Y = [0,1,2,3,4,5,6,7,8,9,10]
    print(plot(X, Y, size=small))
    print()
    X, Y = range(-5,1), range(-10,-4)
    print(plot(X, Y, marker='+', color='red', bgcolor='blue', size=small))
    print()
    X1 = (-5,-4,-3,-2,-1,0,1,2,3,4,5)
    X2 = (-5,-4,-3,-2,-1,0,1,2,3,4,5)
    Y1 = (-5,-4,-3,-2,-1,0,1,2,3,4,5)
    Y2 = (5,4,3,2,1,0,-1,-2,-3,-4,-5)
    print(plot((X1,X2), (Y1,Y2), marker='*', color=['red', 'white'],
               xlim=(-12,12), ylim=(-6,6), size=small))
    print()
    X = [x/10 for x in range(150)]
    Y = [cos(x) for x in X]
    print(plot(X, Y, bgcolor='white'))
    print()
    return 'All tests finished in {:G} seconds.'.format(time()-t0)

if __name__=="__main__":
    print(test())
