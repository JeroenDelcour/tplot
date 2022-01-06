# tplot

`tplot` is a Python module for creating text-based graphs. Useful for visualizing data to the terminal or log files.

## Features

- Scatter plots, line plots, horizontal/vertical bar plots, and image plots
- Supports numerical and categorical data
- Legend
- Unicode characters (with automatic ascii fallback if unicode is not supported)
- Colors (using ANSI escape characters, with Windows support)
- Few dependencies
- Fast and lightweight

## Installation

`tplot` is available on [PyPi](https://pypi.org/project/tplot/):

```bash
pip install tplot
```

## Examples

### Basic usage

```python
import tplot

fig = tplot.Figure()
fig.scatter([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
fig.show()
```

![Basic example](images/basic.png)

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

![Advanced example](images/advanced.png)

### Categorical data

`tplot` supports categorical data in the form of strings:

```python
import tplot

dish = ["Pasta", "Ice cream", "Rice", "Waffles", "Pancakes"]
topping = ["Cheese", "Chocolate", "Cheese", "Chocolate", "Chocolate"]

fig = tplot.Figure(height=7, title="Chocolate or cheese?")
fig.scatter(x=dish, y=topping, marker="X")
fig.show()
```
![Categorical data example](images/categorical.png)

Numerical and categorical data can be combined in the same plot:

```python
from collections import Counter
import tplot

counter = Counter(
    ["Spam", "sausage", "Spam", "Spam", "Spam", "bacon", "Spam", "tomato", "Spam"]
)

fig = tplot.Figure(ylabel="Count")
fig.bar(x=counter.keys(), y=counter.values())
fig.show()
```

![Spam, sausage, Spam, Spam, Spam, bacon, Spam, tomato and Spam](images/spamspamspamspam.png)

### Markers

`tplot` allows you to use any single character as a marker:

```python
import tplot

fig = tplot.Figure(title="Twinkle twinkle little ★")
notes = ["C", "C", "G", "G", "a", "a", "G", "F", "F", "E", "E", "D", "D", "C"]
fig.scatter(notes, marker="♩")
fig.show()
```

![Twinkle twinkle little star](images/twinkle_twinkle_little_star.png)

Be wary of using [fullwidth characters](https://en.wikipedia.org/wiki/Halfwidth_and_fullwidth_forms), because these will [mess up alignment](#character-alignment-issues).

### Images (2D arrays)

`tplot` can visualize 2D arrays using a few different "colormaps".

```python
import tplot
import numpy as np

mean = np.array([[0, 0]]).T
covariance = np.array([[0.7, 0.4], [0.4, 0.7]])
cov_inv = np.linalg.inv(covariance)
cov_det = np.linalg.det(covariance)

x = np.linspace(-2, 2)
y = np.linspace(-2, 2)
X, Y = np.meshgrid(x, y)
coe = 1.0 / ((2 * np.pi) ** 2 * cov_det) ** 0.5
z = coe * np.e ** (
    -0.5
    * (
        cov_inv[0, 0] * (X - mean[0]) ** 2
        + (cov_inv[0, 1] + cov_inv[1, 0]) * (X - mean[0]) * (Y - mean[1])
        + cov_inv[1, 1] * (Y - mean[1]) ** 2
    )
)

fig = tplot.Figure(title="Multivariate gaussian")
fig.image(z, cmap="block")
fig.show()
```

![Multivariate gaussian with "block" colormap](images/multivariate_gaussian_block.png)

```python
fig = tplot.Figure(title="Multivariate gaussian")
fig.image(z, cmap="ascii")
fig.show()
```
![Multivariate gaussian with "ascii" colormap](images/multivariate_gaussian_ascii.png)


Images can also be shown, if first converted to a Numpy array of type `uint8`:

![Original cameraman](images/cameraman.png)

```python
import tplot
from PIL import Image
import numpy as np

cameraman = Image.open("cameraman.png")
cameraman = np.array(cameraman, dtype=np.uint8)
fig = tplot.Figure()
fig.image(cameraman)
fig.show()
```

![Cameraman blocks](images/cameraman_blocks.png)

## Formatting issues

### Writing to a file and color support

You can get the figure as a string simply by converting to to the `str` type: `str(fig)`

However, if you have a figure with colors and you try to write it to a file (or copy and paste it from the terminal), you will find it looks all wrong:

```text
                  Trigonometric functions                   \n                                                            \nA    1┤\x1b[34m⠐\x1b[0m\x1b[34m⠢\x1b[0m\x1b[34m⠤\x1b[0m\x1b[34m⡀\x1b[0m  \x1b[31m⡠\x1b[0m\x1b[31m⠤\x1b[0m\x1b[31m⠒\x1b[0m\x1b[31m⠒\x1b[0m\x1b[31m⠢\x1b[0m\x1b[31m⡀\x1b[0m                   \x1b[34m⡠\x1b[0m\x1b[34m⠒\x1b[0m\x1b[34m⠒\x1b[0m\x1b[34m⠢\x1b[0m\x1b[34m⠤\x1b[0m\x1b[34m⡀\x1b[0m  \x1b[31m⡠\x1b[0m\x1b[31m⠒\x1b[0m\x1b[31m⠒\x1b[0m\x1b[31m⠢\x1b[0m\x1b[31m⠤\x1b[0m\x1b[31m⡀\x1b[0m        \nm     │   \x1b[34m⠈\x1b[0m\x1b[34m⣢\x1b[0m\x1b[34m⡜\x1b[0m     \x1b[31m⠈\x1b[0m\x1b[31m⠱\x1b[0m\x1b[31m⡀\x1b[0m               \x1b[34m⡔\x1b[0m\x1b[34m⠊\x1b[0m     \x1b[34m⠑\x1b[0m\x1b[34m⣴\x1b[0m\x1b[31m
⠊\x1b[0m     \x1b[31m⠘\x1b[0m\x1b[31m⠤\x1b[0m\x1b[31m⡀\x1b[0m      \np  0.5┤   \x1b[31m⡰\x1b[0m\x1b[31m⠁\x1b[0m\x1b[34m⠑
\x1b[0m\x1b[34m⡄\x1b[0m      \x1b[31m⠘\x1b[0m\x1b[31m⢄\x1b[0m            \x1b[34m⢀\x1b[0m\x1b[34m⠜\x1b[0m      \x1b[31m⢀
\x1b[0m\x1b[31m⠜\x1b[0m \x1b[34m⠱\x1b[0m\x1b[34m⡀\x1b[0m      \x1b[31m⠱\x1b[0m\x1b[31m⡀\x1b[0m     \nl     │ \x1b[31m⢀\x1b[0m\x1b[31m⠔\x1b[0m\x1b[31m⠁\x1b[0m  \x1b[34m⠈\x1b[0m\x1b[34m⢢\x1b[0m       \x1b[31m⢣\x1b[0m          \x1b[34m⢠\x1b[0m\x1b[34m⠃\x1b[0m      \x1b[31m⢠\x1b[0m\x1b[31m⠃\x1b[0m   \x1b[34m⠱\x1b[0m\x1b[34m⡀\x1b[0m      \x1b[31m⠑\x1b[0m\x1b[31m⢄
\x1b[0m    \ni     │\x1b[31m⢀\x1b[0m\x1b[31m⠎\x1b[0m      \x1b[34m⢇\x1b[0m       \x1b[31m⢣\x1b[0m        \x1b[34m⡠\x1b[0m\x1b[34m⠃\x1b[0m      \x1b[31m⢠\x1b[0m\x1b[31m⠃\x1b[0m     \x1b[34m⠈\x1b[0m\x1b[34m⢆\x1b[0m      \x1b[31m⠈\x1b[0m\x1b[31m⢆\x1b[0m   \nt    0┤        \x1b[34m⠈\x1b[0m\x1b[34m⠢\x1b[0m\x1b[34m⡀\x1b[0m      \x1b[31m⠱\x1b[0m\x1b[31m⡀\x1b[0m     \x1b[34m⡜\x1b[0m       \x1b[31m⡰\x1b[0m\x1b[31m⠁\x1b[0m       \x1b[34m⠈\x1b[0m\x1b[34m⢆\x1b[0m          \nu     │┌─Legend─┐\x1b[34m⠱\x1b[0m\x1b[34m⡀\x1b[0m      \x1b[31m⠱\x1b[0m\x1b[31m⡀\x1b[0m  \x1b[34m⢀\x1b[0m\x1b[34m⠜\x1b[0m       \x1b[31m⡰\x1b[0m\x1b[31m⠁\x1b[0m         \x1b[34m⠈\x1b[0m\x1b[34m⢢\x1b[0m         \nd -0.5┤│\x1b[31m⠄\x1b[0m sin(x)│ \x1b[34m
⠑\x1b[0m\x1b[34m⢄\x1b[0m      \x1b[31m⠑\x1b[0m\x1b[31m⢢\x1b[0m\x1b[34m⢠\x1b[0m\x1b[34m⠃\x1b[0m      \x1b[31m⢠\x1b[0m\x1b[31m⠔\x1b[0m\x1b[31m⠁\x1b[0m            \x1b[34m⠱\x1b[0m\x1b[34m⡀\x1b[0m       \ne     ││\x1b[34m⠄\x1b[0m cos(x)│   \x1b[34m⠱\x1b[0m\x1b[34m⣀\x1b[0m    \x1b[34m⡠\x1b[0m\x1b[34m⠔\x1b[0m\x1b[34m⠑\x1b[0m\x1b[31m⠤\x1b[0m\x1b[31m⡀\x1b[0m   \x1b[31m⣀\x1b[0m\x1b[31m⠔\x1b[0m\x1b[31m⠁\x1b[0m               \x1b[34m⠈\x1b[0m\x1b[34m⠢\x1b[0m\x1b[34m⡀\x1b[0m     \n    -1┤
└────────┘     \x1b[34m⠉\x1b[0m\x1b[34m⠒\x1b[0m\x1b[34m⠒\x1b[0m\x1b[34m⠊\x1b[0m    \x1b[31m⠈\x1b[0m\x1b[31m⠒\x1b[0m\x1b[31m⠒\x1b[0m\x1b[31m⠊\x1b[0m                    \x1b[34m⠈\x1b[0m\x1b[34m⠉\x1b[0m\x1b[34m⠒\x1b[0m   \n       ┬─────────┬──
────────┬─────────┬──────────┬─────────┬\n       0         2          4         6          8        10\n                              Phase                         
```

This is because `tplot` uses ANSI escape characters to display colors. ANSI escape characters allow terminals to display color, but don't work outside the terminal. Regular UTF-8 or unicode-encoded text files do not support colored text. If you want to write figures to a text file (e.g. for logging purposes), it is best to avoid the use of color.

### Converting to HTML

Alternatively, you can run the figure as a string through a tool such as [ansi2html](https://github.com/pycontribs/ansi2html) to format the figure using HTML:

```python
from ansi2html import Ansi2HTMLConverter

conv = Ansi2HTMLConverter(markup_lines=True)
html = conv.convert(str(fig))
with open("fig.html", "w") as f:
    f.write(html)
```

However, if you're using unicode characters (such as braille), you will probably run into character alignment issues.

### Character alignment issues

#### Fullwidth and halfwidth characters

`tplot` assumes all characters have a fixed width. Unless you're crazy, your terminal uses a monospace font. But even for monospaced fonts, the wondrous world of unicode has two character widths: halfwidth (so called because they are half as wide as they are tall) and fullwidth. Most characters you know are probably halfwidth. Many Asian languages such as Chinese, Korean, and Japanese use fullwidth characters. Emoji are usually also fullwidth.

Though fullwidth characters are exactly twice as wide as halfwidth characters, they still count as only one character. `tplot` will not stop you from using fullwidth characters, but it will mess up the alignment, potentially even causing lines to wrap around:

```
import tplot

fig = tplot.Figure(width=80, height=6)
x = [0, 1, 2, 3, 4, 5]
fig.scatter(x, y=[1, 1, 1, 1, 1, 1], marker="#")
fig.scatter(x, y=[0, 0, 0, 0, 0, 0], marker="💩")
fig.show()
```

![Example of misalignment due to fullwidth characters](images/misalignment.png)

#### Braille

`tplot` can use braille characters to subdivide each character into a 2x8 grid, increasing the resolution of the plot beyond what is possible with single characters. However, not all monospace fonts display braille characters the same. In Ubuntu's default terminal with the default Monospace Regular font, braille characters are rendered as halfwidth characters, so this will show a nice diagonal line:

```python
import tplot

fig = tplot.Figure()
fig.line([0,1], marker="braille")
fig.show()
```

![Correctly rendered braille](images/braille.png)

But many environments treat braille as somewhere in between halfwidth and fullwidth characters, leading to close-but-not-quite aligned plots:

```text
                                                                                
  1┤                                                                      ⣀⣀⠤⠤⠔⠒
   │                                                            ⢀⣀⣀⠤⠤⠒⠒⠊⠉⠉      
   │                                                   ⣀⣀⡠⠤⠤⠒⠒⠉⠉⠁               
   │                                          ⣀⣀⠤⠤⠔⠒⠒⠉⠉                         
0.5┤                                ⢀⣀⡠⠤⠤⠒⠒⠊⠉⠉                                  
   │                       ⣀⣀⡠⠤⠔⠒⠒⠉⠉⠁                                           
   │             ⢀⣀⣀⠤⠤⠔⠒⠊⠉⠉                                                     
   │    ⢀⣀⡠⠤⠤⠒⠒⠊⠉⠁                                                              
  0┤⠐⠒⠉⠉⠁                                                                       
    ┬───────┬──────┬───────┬──────┬───────┬──────┬───────┬──────┬───────┬──────┬
    0      0.1    0.2     0.3    0.4     0.5    0.6     0.7    0.8     0.9     1
```