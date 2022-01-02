import tplot
import numpy as np
from pathlib import Path

generate = False


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

image = np.linspace(np.zeros(24), np.ones(24), num=24)
image = (image + image.T) / 2

refence_figures_dir = Path("tests/reference_figures")


def test_y_only():
    fig = tplot.Figure(width=80, height=24)
    fig.scatter(range(10))
    with open(refence_figures_dir / "y_only.txt", "w" if generate else "r") as f:
        if generate:
            f.write(str(fig))
        else:
            assert str(fig) == f.read()


def test_scatter():
    fig = tplot.Figure(width=80, height=24)
    for dataset_name, data in datasets.items():
        fig.clear()
        fig.scatter(data[0], data[1])
        with open(
            refence_figures_dir / f"scatter_{dataset_name}.txt",
            "w" if generate else "r",
        ) as f:
            if generate:
                f.write(str(fig))
            else:
                assert str(fig) == f.read()


def test_line():
    fig = tplot.Figure(width=80, height=24)
    for dataset_name, data in datasets.items():
        fig.clear()
        fig.line(data[0], data[1])
    with open(
        refence_figures_dir / f"line_{dataset_name}.txt", "w" if generate else "r"
    ) as f:
        if generate:
            f.write(str(fig))
        else:
            assert str(fig) == f.read()


def test_bar():
    fig = tplot.Figure(width=80, height=24)
    for dataset_name, data in datasets.items():
        fig.clear()
        fig.bar(data[0], data[1])
    with open(
        refence_figures_dir / f"bar_{dataset_name}.txt", "w" if generate else "r"
    ) as f:
        if generate:
            f.write(str(fig))
        else:
            assert str(fig) == f.read()


def test_hbar():
    fig = tplot.Figure(width=80, height=24)
    for dataset_name, data in datasets.items():
        fig.clear()
        fig.hbar(data[0], data[1])
    with open(
        refence_figures_dir / f"hbar_{dataset_name}.txt", "w" if generate else "r"
    ) as f:
        if generate:
            f.write(str(fig))
        else:
            assert str(fig) == f.read()


def test_image():
    fig = tplot.Figure(width=80, height=24)
    fig.image(image)
    with open(refence_figures_dir / "image.txt", "w" if generate else "r") as f:
        if generate:
            f.write(str(fig))
        else:
            assert str(fig) == f.read()

    fig.clear()
    fig.image((image * 128).astype(np.uint8))
    with open(
        refence_figures_dir / "image_big_values.txt", "w" if generate else "r"
    ) as f:
        if generate:
            f.write(str(fig))
        else:
            assert str(fig) == f.read()

    fig.clear()
    fig.image(image * -1e-3)
    with open(
        refence_figures_dir / "image_small_values.txt", "w" if generate else "r"
    ) as f:
        if generate:
            f.write(str(fig))
        else:
            assert str(fig) == f.read()

    fig.clear()
    fig.image(image, vmin=-1, vmax=1)
    with open(
        refence_figures_dir / "image_vmin_vmax.txt", "w" if generate else "r"
    ) as f:
        if generate:
            f.write(str(fig))
        else:
            assert str(fig) == f.read()

    fig.clear()
    fig.image(image, cmap="ascii")
    with open(refence_figures_dir / "image_ascii.txt", "w" if generate else "r") as f:
        if generate:
            f.write(str(fig))
        else:
            assert str(fig) == f.read()


# def test_ascii_fallback():
#     fig = tplot.Figure(width=80, height=24, ascii=True)
#         for dataset_name, data in datasets.items():
#         fig.clear()
#         fig.scatter(data[0], data[1])
#         fig.show()

#     fig.clear()
#     fig.image(image)
#     fig.show()


def test_legend():
    for legendloc in ("topleft", "topright", "bottomright", "bottomleft"):
        fig = tplot.Figure(width=80, height=24, legendloc=legendloc)
        fig.scatter(range(5), label="First")
        fig.line(range(-5, 0), label="Second")
        fig.scatter(range(5, 10), marker="3", label="Third")
        with open(
            refence_figures_dir / f"legendloc_{legendloc}.txt", "w" if generate else "r"
        ) as f:
            if generate:
                f.write(str(fig))
            else:
                assert str(fig) == f.read()


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
    with open(refence_figures_dir / "axis_labels.txt", "w" if generate else "r") as f:
        if generate:
            f.write(str(fig))
        else:
            assert str(fig) == f.read()


def test_colors():
    fig = tplot.Figure(width=80, height=24, legendloc="bottomright")
    for i, color in enumerate(
        ["red", "green", "blue", "yellow", "magenta", "cyan", "grey", "white"]
    ):
        fig.scatter([i], [i], color=color, label=color)
    with open(refence_figures_dir / "colors.txt", "w" if generate else "r") as f:
        if generate:
            f.write(str(fig))
        else:
            assert str(fig) == f.read()


def test_text():
    fig = tplot.Figure(width=80, height=24)
    fig.text(x=4, y=0, text="testing text")
    fig.text(x=4, y=-1, text="testing colored text", color="red")
    fig.text(x=9, y=8, text="testing text at right boundary")
    with open(refence_figures_dir / "text.txt", "w" if generate else "r") as f:
        if generate:
            f.write(str(fig))
        else:
            assert str(fig) == f.read()


def test_braille():
    fig = tplot.Figure(width=80, height=24)
    for dataset_name, data in datasets.items():
        fig.clear()
        fig.scatter(data[0], data[1], marker="braille", color="red")
        with open(
            refence_figures_dir / f"braille_scatter_{dataset_name}.txt",
            "w" if generate else "r",
        ) as f:
            if generate:
                f.write(str(fig))
            else:
                assert str(fig) == f.read()
        fig.clear()
        fig.line(data[0], data[1], marker="braille", color="green")
        with open(
            refence_figures_dir / f"braille_line_{dataset_name}.txt",
            "w" if generate else "r",
        ) as f:
            if generate:
                f.write(str(fig))
            else:
                assert str(fig) == f.read()
        fig.clear()
        fig.bar(data[0], data[1], marker="braille", color="blue")
        with open(
            refence_figures_dir / f"braille_bar_{dataset_name}.txt",
            "w" if generate else "r",
        ) as f:
            if generate:
                f.write(str(fig))
            else:
                assert str(fig) == f.read()
        fig.clear()
        fig.hbar(data[0], data[1], marker="braille")
        with open(
            refence_figures_dir / f"braille_hbar_{dataset_name}.txt",
            "w" if generate else "r",
        ) as f:
            if generate:
                f.write(str(fig))
            else:
                assert str(fig) == f.read()


def test_y_axis_direction():
    fig = tplot.Figure(width=80, height=24, y_axis_direction="down")
    for dataset_name, data in datasets.items():
        fig.clear()
        fig.scatter(data[0], data[1])
        with open(
            refence_figures_dir / f"y_axis_down_{dataset_name}.txt",
            "w" if generate else "r",
        ) as f:
            if generate:
                f.write(str(fig))
            else:
                assert str(fig) == f.read()
    fig = tplot.Figure(width=80, height=24, y_axis_direction="up")
    fig.image(image)
    with open(refence_figures_dir / "y_axis_up.txt", "w" if generate else "r") as f:
        if generate:
            f.write(str(fig))
        else:
            assert str(fig) == f.read()
