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

.. highlight:: bash

`tplot` is available on `PyPi <https://pypi.org/project/tplot/>`_::
   
   pip install tplot


Basic usage
-----------

.. highlight:: python

.. code-block::

   import tplot
   fig = tplot.Figure()
   fig.scatter([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
   fig.show()

.. highlight:: none

Prints::

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

To get a string representation of the figure instead of printing to `std`, simply use ``str(fig)``.


Advanced usage
--------------

.. highlight:: python

.. code-block::

   import tplot
   fig = tplot.Figure(title=""

API reference
-------------

.. automodule:: tplot.figure
   :members:
   :undoc-members:
   :show-inheritance:


.. toctree::
   :maxdepth: 2
   :caption: Contents:


Indices and tables
==================

* :ref:`genindex`
* :ref:`search`
