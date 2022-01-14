import numpy as np

import tplot


def test_linear_scale():
    data = [-1, 3, -0.5, 4]
    scale = tplot.scales.LinearScale()
    scale.fit(data, target_min=-1, target_max=1)
    assert scale.transform(4) == 1
    assert scale.transform(-1) == -1
    assert scale.transform(1.5) == 0
    assert scale.transform([4, -1, 1.5]) == [1, -1, 0]
    np.testing.assert_array_equal(
        scale.transform(np.array([4, -1, 1.5])), np.array([1, -1, 0])
    )


def test_linear_inverted_scale():
    data = [-1, 3, -0.5, 4]
    scale = tplot.scales.LinearScale()
    scale.fit(data, target_min=1, target_max=-1)
    assert scale.transform(4) == -1
    assert scale.transform(-1) == 1


def test_linear_single_value():
    scale = tplot.scales.LinearScale()
    scale.fit([1], target_min=0, target_max=1)
    assert scale.transform(1) == 0.5


def test_categorical_scale():
    data = ["eggs", 42, "bacon", "spam", "spam", "spam", "bacon", "spam", "eggs"]
    scale = tplot.scales.CategoricalScale()
    scale.fit(data)
    # should return index of lexically sorted string representation of unique values
    scale.transform(42) == 0
    scale.transform("42") == 0
    scale.transform("bacon") == 1
    scale.transform("eggs") == 2
    scale.transform("spam") == 3
    scale.transform(["42", "bacon", "eggs", "spam"]) == [0, 1, 2, 3]
    np.testing.assert_array_equal(
        scale.transform(np.array(["42", "bacon", "eggs", "spam"])),
        np.array(([0, 1, 2, 3])),
    )
