tplot
=====

`tplot` is a Python module for creating text-based graphs. Useful for visualizing data to the terminal or log files.

Features
--------

- Scatter, line, horizontal/vertical bar, and image plotting
- Supports numerical and categorical data
- Legend
- Automatic detection of unicode support with ascii fallback
- Colors using ANSI escape characters (Windows supported)
- Few dependencies
- Lightweight


Installation
------------

`tplot` is available on [PyPi](https://test.pypi.org/project/tplot/):
```bash
pip install tplot
```


Basic usage
-----------

```python
   import tplot
   fig = tplot.Figure()
   fig.scatter([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
   fig.show()
```

Prints:

```
   10┤                                                                            •
     │                                                                             
     │                                                                    •        
     │                                                                             
    8┤                                                             •               
     │                                                                             
     │                                                     •                       
     │                                                                             
    6┤                                              •                              
     │                                                                             
     │                                      •                                      
     │                                                                             
    4┤                              •                                              
     │                                                                             
     │                       •                                                     
     │                                                                             
    2┤               •                                                             
     │                                                                             
     │        •                                                                    
     │                                                                             
    0┤•                                                                            
      ┬───────┬──────┬───────┬──────┬───────┬───────┬──────┬───────┬──────┬───────┬
      0       1      2       3      4       5       6      7       8      9      10
```


Documentation
-------------

Full API reference is available on [readthedocs](https://tplot.readthedocs.io/en/latest/).