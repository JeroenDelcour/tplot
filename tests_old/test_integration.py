import unittest
import tplot
import numpy as np


def ascii_only(s):
    try:
        s.encode("ascii")  # this fails if the string contains non-ascii characters
        return True
    except UnicodeEncodeError:
        return False


datasets = []
anscombe = [
    (4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14),
    (4.26, 5.68, 7.24, 4.82, 6.95, 8.81, 8.04, 8.33, 10.84, 7.58, 9.96),
]
datasets.append(anscombe)
iris_sample = [
    (5.1, 4.9, 4.7, 7, 6.4, 6.9, 6.3, 5.8, 7.1),
    (["I. setosa"] * 3 + ["I. versicolor"] * 3 + ["I. virginica"] * 3),
]
datasets.append(iris_sample)
cheese_or_chocolate = [
    ("cheese", "chocolate", "cheese", "chocolate", "chocolate"),
    ("pasta", "ice cream", "rice", "waffles", "pancakes"),
]
datasets.append(cheese_or_chocolate)

image = np.linspace(np.zeros(24), np.ones(24), num=24)
image = (image + image.T) / 2


class TestIntegration(unittest.TestCase):
    def test_y_only(self):
        fig = tplot.Figure(width=80, height=24)
        fig.scatter(range(10))
        fig.show()

    def test_scatter(self):
        fig = tplot.Figure(width=80, height=24)
        for data in datasets:
            fig.clear()
            fig.scatter(data[0], data[1])
            fig.show()

    def test_line(self):
        fig = tplot.Figure(width=80, height=24)
        for data in datasets:
            fig.clear()
            fig.line(data[0], data[1])
            fig.show()

    def test_bar(self):
        fig = tplot.Figure(width=80, height=24)
        for data in datasets:
            fig.clear()
            fig.bar(data[0], data[1])
            fig.show()

    def test_hbar(self):
        fig = tplot.Figure(width=80, height=24)
        for data in datasets:
            fig.clear()
            fig.hbar(data[0], data[1])
            fig.show()

    def test_image(self):
        fig = tplot.Figure(width=80, height=24)
        fig.image(image)
        fig.show()

        fig.clear()
        fig.image((image * 128).astype(np.uint8))
        fig.show()

        fig.clear()
        fig.image(image * -1e-3)
        fig.show()

        fig.clear()
        fig.image(image, vmin=-1, vmax=1)
        fig.show()

        fig.clear()
        fig.image(image, cmap="ascii")
        fig.show()

    def test_ascii_fallback(self):
        fig = tplot.Figure(width=80, height=24, ascii=True)
        for data in datasets:
            fig.clear()
            fig.scatter(data[0], data[1])
            fig.show()
            self.assertTrue(ascii_only(str(fig)))

        fig.clear()
        fig.image(image)
        fig.show()
        self.assertTrue(ascii_only(str(fig)))

    def test_legend(self):
        for legendloc in ("topleft", "topright", "bottomright", "bottomleft"):
            fig = tplot.Figure(width=80, height=24, legendloc=legendloc)
            fig.scatter(range(5), label="First")
            fig.line(range(-5, 0), label="Second")
            fig.scatter(range(5, 10), marker="3", label="Third")
            fig.show()

    def test_axis_labels(self):
        fig = tplot.Figure(
            xlabel="x axis label goes here",
            ylabel="y axis label goes here",
            title="Title goes here",
            width=80,
            height=40,
            legendloc="bottomright",
        )
        fig.scatter(range(10), label="Legend label goes here")
        fig.show()

    def test_colors(self):
        fig = tplot.Figure(width=80, height=24, legendloc="bottomright")
        for i, color in enumerate(
            ["red", "green", "blue", "yellow", "magenta", "cyan", "grey", "white"]
        ):
            fig.scatter([i], [i], color=color, label=color)
        fig.show()

    def test_text(self):
        fig = tplot.Figure(width=80, height=24)
        fig.text(x=4, y=0, text="testing text")
        fig.text(x=4, y=-1, text="testing colored text", color="red")
        fig.text(x=9, y=8, text="testing text at right boundary")
        fig.show()

    def test_braille(self):
        fig = tplot.Figure(width=80, height=24)
        for data in datasets:
            fig.clear()
            fig.scatter(data[0], data[1], marker="braille", color="red")
            fig.show()
            fig.clear()
            fig.line(data[0], data[1], marker="braille", color="green")
            fig.show()
            fig.clear()
            fig.bar(data[0], data[1], marker="braille", color="blue")
            fig.show()
            fig.clear()
            fig.hbar(data[0], data[1], marker="braille")
            fig.show()

    def test_y_axis_direction(self):
        fig = tplot.Figure(width=80, height=24, y_axis_direction="down")
        for data in datasets:
            fig.clear()
            fig.scatter(data[0], data[1])
            fig.show()
        fig = tplot.Figure(width=80, height=24, y_axis_direction="up")
        fig.image(image)
        fig.show()
