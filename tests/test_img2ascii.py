import numpy as np

from tplot.img2ascii import resize


def test_nearest_neighbor_downscaling():
    image = np.array(
        [[0, 0, 1, 1], [0, 0, 1, 1], [1, 1, 0, 0], [1, 1, 0, 0]], dtype=np.uint8
    )
    out = resize(image, shape=(2, 2))
    assert out.shape == (2, 2)
    np.testing.assert_array_equal(out, np.array([[0, 1], [1, 0]], dtype=np.uint8))


def test_nearest_neighbor_upscaling():
    image = np.array([[0, 1], [1, 0]], dtype=np.uint8)
    out = resize(image, shape=(4, 4))
    assert out.shape == (4, 4)
    np.testing.assert_array_equal(
        out,
        np.array(
            [[0, 0, 1, 1], [0, 0, 1, 1], [1, 1, 0, 0], [1, 1, 0, 0]], dtype=np.uint8
        ),
    )
