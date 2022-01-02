import numpy as np
from tplot.img2ascii import *


def test_nearest_neighbor_resizing():
    image = np.array(
        [[0, 0, 1, 1], [0, 0, 1, 1], [1, 1, 0, 0], [1, 1, 0, 0]], dtype=np.uint8
    )
    out = resize(image, shape=(2, 2))
    assert out.shape == (2, 2)
    np.testing.assert_array_equal(out, np.array([[0, 1], [1, 0]], dtype=np.uint8))
