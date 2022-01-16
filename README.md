# tplot

[![Documentation status](https://readthedocs.org/projects/tplot/badge/)](https://tplot.readthedocs.io/en/latest/)
[![Tests status](https://github.com/JeroenDelcour/tplot/actions/workflows/tests.yml/badge.svg)](https://github.com/JeroenDelcour/tplot/actions/workflows/tests.yml)
[![codecov](https://codecov.io/gh/JeroenDelcour/tplot/branch/master/graph/badge.svg?token=WXH7I3BGEO)](https://codecov.io/gh/JeroenDelcour/tplot)

[![Supported Python versions](https://img.shields.io/pypi/pyversions/tplot)](https://pypi.org/project/tplot/)
[![PyPI version](https://img.shields.io/pypi/v/tplot)](https://pypi.org/project/tplot/)
[![License](https://img.shields.io/github/license/jeroendelcour/tplot)](https://github.com/JeroenDelcour/tplot/blob/master/LICENSE)

`tplot` is a Python package for creating text-based graphs. Useful for visualizing data to the terminal or log files.

## Features

- Scatter plots, line plots, horizontal/vertical bar plots, and image plots
- Supports numerical and categorical data
- Legend
- Unicode characters (with automatic ascii fallback)
- Colors
- Few dependencies
- Fast and lightweight
- Doesn't take over your terminal (only prints strings)

## Installation

`tplot` is available on [PyPi](https://pypi.org/project/tplot/):

```bash
pip install tplot
```

## Documentation

Documentation is available on [readthedocs](https://tplot.readthedocs.io/en/latest/).

## Examples

### Basic usage

```python
import tplot

fig = tplot.Figure()
fig.scatter([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
fig.show()
```

![Basic example](docs/images/basic.png)

### A more advanced example

```python
import tplot
import numpy as np

x = np.linspace(start=0, stop=np.pi*3, num=80)

fig = tplot.Figure(
    xlabel="Phase",
    ylabel="Amplitude",
    title="Trigonometric functions",
    legendloc="bottomleft",
    width=60,
    height=15,
)
fig.line(x, y=np.sin(x), color="red", label="sin(x)")
fig.line(x, y=np.cos(x), color="blue", label="cos(x)")
fig.show()
```

![Advanced example](docs/images/advanced.png)

See more examples in the [documentation](https://tplot.readthedocs.io/en/latest/).

## Contributing

Contributions are welcome. Bug fixes, feature suggestions, documentation improvements etc. can be contributed via [issues](https://github.com/JeroenDelcour/tplot/issues) and/or [pull requests](https://github.com/JeroenDelcour/tplot/pulls).
