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
    height=14,
)
fig.line(x, y=np.sin(x), color="red", label="sin(x)")
fig.line(x, y=np.cos(x), color="blue", label="cos(x)")
fig.show()
```

```
                  Trigonometric functions                   
                                                            
A  1┤⠐⠒⠢⡀  ⢀⠤⠒⠒⠒⢄                   ⢀⡠⠔⠒⠒⠤⣀  ⢀⠔⠒⠒⠢⢄         
m   │   ⠈⢑⡎⠁     ⠑⠢⡀              ⢀⠤⠊      ⡱⣒⠁     ⠉⢆       
p   │  ⢀⠜⠁⠈⠱⡀      ⠑⢄            ⡠⠊      ⢀⠎  ⢣       ⠑⢄     
l   │ ⡠⠊    ⠱⡀      ⠈⢢          ⡜       ⡠⠊    ⠣⢄      ⠈⢆    
i  0┤⠐⠁      ⠈⢆       ⠑⡄      ⢠⠊       ⡜       ⠈⢆       ⠑   
t   │┌─Legend─┐⠑⡄      ⠘⢄   ⢀⡠⠃      ⢠⠊          ⠱⡀         
u   ││⠄ sin(x)│ ⠘⢄       ⠱⣀⢀⠎       ⡰⠁            ⠑⢄        
d   ││⠄ cos(x)│   ⠑⢄⡀    ⣀⠖⠣⡀     ⡠⠋                ⠑⠤⡀     
  -1┤└────────┘     ⠈⠑⠒⠒⠉   ⠈⠉⠒⠒⠊⠉                    ⠈⠒⠒   
     ┬──────────┬──────────┬─────────┬──────────┬──────────┬
     0          2          4         6          8         10
                             Phase                          
```

## Writing to a file and support for color

You can get the figure as a string simply by converting to to the `str` type: `str(fig)`

However, if you have a figure with colors and you try to write it to a file (or copy and paste it from the terminal), you will find it looks all wrong:

```
                  Trigonometric functions                   
                                                            
A  1┤[34m⠐[0m[34m⠒[0m[34m⠢[0m[34m⡀[0m  [31m⢀[0m[31m⠤[0m[31m⠒[0m[31m⠒[0m[31m⠒[0m[31m⢄[0m                   [34m⢀[0m[34m⡠[0m[34m⠔[0m[34m⠒[0m[34m⠒[0m[34m⠤[0m[34m⣀[0m  [31m⢀[0m[31m⠔[0m[31m⠒[0m[31m⠒[0m[31m⠢[0m[31m⢄[0m         
m   │   [34m⠈[0m[34m⢑[0m[34m⡎[0m[31m⠁[0m     [31m⠑[0m[31m⠢[0m[31m⡀[0m              [34m⢀[0m[34m⠤[0m[34m⠊[0m      [34m⡱[0m[34m⣒[0m[31m⠁[0m     [31m⠉[0m[31m⢆[0m       
p   │  [31m⢀[0m[31m⠜[0m[31m⠁[0m[34m⠈[0m[34m⠱[0m[34m⡀[0m      [31m⠑[0m[31m⢄[0m            [34m⡠[0m[34m⠊[0m      [31m⢀[0m[31m⠎[0m  [34m⢣[0m       [31m⠑[0m[31m⢄[0m     
l   │ [31m⡠[0m[31m⠊[0m    [34m⠱[0m[34m⡀[0m      [31m⠈[0m[31m⢢[0m          [34m⡜[0m       [31m⡠[0m[31m⠊[0m    [34m⠣[0m[34m⢄[0m      [31m⠈[0m[31m⢆[0m    
i  0┤[31m⠐[0m[31m⠁[0m      [34m⠈[0m[34m⢆[0m       [31m⠑[0m[31m⡄[0m      [34m⢠[0m[34m⠊[0m       [31m⡜[0m       [34m⠈[0m[34m⢆[0m       [31m⠑[0m   
t   │┌─Legend─┐[34m⠑[0m[34m⡄[0m      [31m⠘[0m[31m⢄[0m   [34m⢀[0m[34m⡠[0m[34m⠃[0m      [31m⢠[0m[31m⠊[0m          [34m⠱[0m[34m⡀[0m         
u   ││[31m⠄[0m sin(x)│ [34m⠘[0m[34m⢄[0m       [31m⠱[0m[31m⣀[0m[34m⢀[0m[34m⠎[0m       [31m⡰[0m[31m⠁[0m            [34m⠑[0m[34m⢄[0m        
d   ││[34m⠄[0m cos(x)│   [34m⠑[0m[34m⢄[0m[34m⡀[0m    [34m⣀[0m[34m⠖[0m[34m⠣[0m[31m⡀[0m     [31m⡠[0m[31m⠋[0m                [34m⠑[0m[34m⠤[0m[34m⡀[0m     
  -1┤└────────┘     [34m⠈[0m[34m⠑[0m[34m⠒[0m[34m⠒[0m[34m⠉[0m   [31m⠈[0m[31m⠉[0m[31m⠒[0m[31m⠒[0m[31m⠊[0m[31m⠉[0m                    [34m⠈[0m[34m⠒[0m[34m⠒[0m   
     ┬──────────┬──────────┬─────────┬──────────┬──────────┬
     0          2          4         6          8         10
                             Phase                          
```

This is because `tplot` uses ANSI escape characters to display colors. ANSI escape characters allow terminals to display color, but don't work outside the terminal.

## API refence

::: tplot.Figure