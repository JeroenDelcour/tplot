import tplot
from tplot.utils import _optimize_xticklabel_anchors


def test_simple():
    anchors = _optimize_xticklabel_anchors(
        tick_positions=[0, 10, 20], labels=["0", "1", "2"], width=80
    )
    assert anchors == [[0, 1], [10, 11], [20, 21]]


def test_boundaries():
    anchors = _optimize_xticklabel_anchors(
        tick_positions=[0, 20], labels=["0.0", "2.0"], width=21
    )
    assert anchors == [[0, 2], [18, 21]]


def test_margin():
    anchors = _optimize_xticklabel_anchors(
        tick_positions=[5, 10], labels=["lorem", "ipsum"], width=80
    )
    assert anchors == [[2, 7], [9, 14]]


def test_pruning():
    """
    Tests that labels are shortened if they don't fit and they don't extend beyond the previous or next tick.
    """
    anchors = _optimize_xticklabel_anchors(
        tick_positions=[3, 5, 7],
        labels=[
            "your mother was a hamster",
            "and",
            "your father smelled of elderberries",
        ],
        width=10,
    )
    assert anchors == [[0, 5], [4, 6], [6, 10]]


def test_complex():
    anchors = _optimize_xticklabel_anchors(
        tick_positions=[10, 22, 34, 47, 59],
        labels=[
            "Delicious ice cream",
            "Pancakes with syrup",
            "Pasta",
            "Rice bowl",
            "Voluptuous waffles",
        ],
        width=60,
    )
    assert anchors == [[0, 16], [16, 34], [34, 39], [39, 48], [48, 60]]
