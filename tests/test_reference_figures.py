from pathlib import Path

import numpy as np
import pytest
from PIL import Image

import tplot

GENERATE = False


def equal_to_file(output, filename):
    with open(
        Path("tests") / "reference_figures" / filename, "w" if GENERATE else "r"
    ) as f:
        if GENERATE:
            f.write(output)
            return True
        else:
            return output == f.read()


def ascii_only(s):
    try:
        s.encode("ascii")  # this fails if the string contains non-ascii characters
        return True
    except UnicodeEncodeError:
        return False


datasets = {
    "anscombe": [
        (4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14),
        (4.26, 5.68, 7.24, 4.82, 6.95, 8.81, 8.04, 8.33, 10.84, 7.58, 9.96),
    ],
    "iris": [
        (5.1, 4.9, 4.7, 7, 6.4, 6.9, 6.3, 5.8, 7.1),
        (["I. setosa"] * 3 + ["I. versicolor"] * 3 + ["I. virginica"] * 3),
    ],
    "cheese_or_chocolate": [
        ("cheese", "chocolate", "cheese", "chocolate", "chocolate"),
        ("pasta", "ice cream", "rice", "waffles", "pancakes"),
    ],
}

gradient = np.linspace(np.zeros(24), np.ones(24), num=24)
gradient = (gradient + gradient.T) / 2

reference_figures_dir = Path("tests/reference_figures")


def test_ascii_fallback():
    fig = tplot.Figure(width=80, height=24, ascii=True)
    for dataset_name, data in datasets.items():
        fig.clear()
        fig.scatter(data[0], data[1])
        assert ascii_only(str(fig))

    fig.clear()
    fig.image(gradient)
    assert ascii_only(str(fig))


def test_figure_too_small_error():
    fig = tplot.Figure(width=1, height=1)
    for dataset_name, data in datasets.items():
        fig.clear()
        fig.scatter(data[0], data[1])
        with pytest.raises(IndexError):
            str(fig)

    fig.clear()
    fig.image(gradient)
    with pytest.raises(IndexError):
        str(fig)


def test_y_only():
    fig = tplot.Figure(width=80, height=24)
    fig.scatter(range(10))
    with open(reference_figures_dir / "y_only.txt", "w" if GENERATE else "r") as f:
        if GENERATE:
            f.write(str(fig))
        else:
            assert str(fig) == f.read()


def test_scatter():
    fig = tplot.Figure(width=80, height=24)
    for dataset_name, data in datasets.items():
        fig.clear()
        fig.scatter(data[0], data[1])
        assert equal_to_file(str(fig), f"scatter_{dataset_name}.txt")


def test_line():
    fig = tplot.Figure(width=80, height=24)
    for dataset_name, data in datasets.items():
        fig.clear()
        fig.line(data[0], data[1])
        assert equal_to_file(str(fig), f"line_{dataset_name}.txt")


def test_bar():
    fig = tplot.Figure(width=80, height=24)
    for dataset_name, data in datasets.items():
        fig.clear()
        fig.bar(data[0], data[1])
        assert equal_to_file(str(fig), f"bar_{dataset_name}.txt")


def test_hbar():
    fig = tplot.Figure(width=80, height=24)
    for dataset_name, data in datasets.items():
        fig.clear()
        fig.hbar(data[0], data[1])
        assert equal_to_file(str(fig), f"hbar_{dataset_name}.txt")


def test_image():
    fig = tplot.Figure(width=80, height=24)
    fig.image(gradient)
    assert equal_to_file(str(fig), "image.txt")

    fig.clear()
    fig.image((gradient * 128).astype(np.uint8))
    assert equal_to_file(str(fig), "image_big_values.txt")

    fig.clear()
    fig.image(gradient * -1e-3)
    assert equal_to_file(str(fig), "image_small_values.txt")

    fig.clear()
    fig.image(gradient, vmin=-1, vmax=1)
    assert equal_to_file(str(fig), "image_vmin_vmax.txt")

    fig.clear()
    fig.image(gradient, cmap="ascii")
    assert equal_to_file(str(fig), "image_ascii.txt")

    fig.clear()
    cameraman = np.array(Image.open("tests/cameraman.png"))
    fig.image(cameraman)
    assert equal_to_file(str(fig), "image_cameraman.txt")


def test_legend():
    for legendloc in ("topleft", "topright", "bottomright", "bottomleft"):
        fig = tplot.Figure(width=80, height=24, legendloc=legendloc)
        fig.scatter(range(5), label="First")
        fig.line(range(-5, 0), label="Second")
        fig.scatter(range(5, 10), marker="3", label="Third")
        assert equal_to_file(str(fig), f"legendloc_{legendloc}.txt")


def test_axis_labels():
    fig = tplot.Figure(
        xlabel="x axis label goes here",
        ylabel="y axis label goes here",
        title="Title goes here",
        width=80,
        height=40,
        legendloc="bottomright",
    )
    fig.scatter(range(10), label="Legend label goes here")
    assert equal_to_file(str(fig), "axis_labels.txt")


def test_colors():
    fig = tplot.Figure(width=80, height=24, legendloc="bottomright")
    for i, color in enumerate(
        ["red", "green", "blue", "yellow", "magenta", "cyan", "grey", "white"]
    ):
        fig.scatter([i], [i], color=color, label=color)
    assert equal_to_file(str(fig), "colors.txt")


def test_text():
    fig = tplot.Figure(width=80, height=24)
    fig.text(x=4, y=0, text="testing text")
    fig.text(x=4, y=-1, text="testing colored text", color="red")
    fig.text(x=9, y=8, text="testing text at right boundary")
    assert equal_to_file(str(fig), "text.txt")


def test_braille():
    fig = tplot.Figure(width=80, height=24)
    for dataset_name, data in datasets.items():
        fig.clear()
        fig.scatter(data[0], data[1], marker="braille", color="red")
        assert equal_to_file(str(fig), f"braille_scatter_{dataset_name}.txt")

        fig.clear()
        fig.line(data[0], data[1], marker="braille", color="green")
        assert equal_to_file(str(fig), f"braille_line_{dataset_name}.txt")

        fig.clear()
        fig.bar(data[0], data[1], marker="braille", color="blue")
        assert equal_to_file(str(fig), f"braille_bar_{dataset_name}.txt")

        fig.clear()
        fig.hbar(data[0], data[1], marker="braille")
        assert equal_to_file(str(fig), f"braille_hbar_{dataset_name}.txt")


def test_y_axis_direction():
    fig = tplot.Figure(width=80, height=24, y_axis_direction="down")
    for dataset_name, data in datasets.items():
        fig.clear()
        fig.scatter(data[0], data[1])
        assert equal_to_file(str(fig), f"y_axis_down_{dataset_name}.txt")

    fig = tplot.Figure(width=80, height=24, y_axis_direction="up")
    fig.image(gradient)
    assert equal_to_file(str(fig), "y_axis_up.txt")
