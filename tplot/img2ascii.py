from functools import lru_cache

import numpy as np

from .scales import LinearScale

COLORMAPS = {
    # "ascii": "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "[::-1],
    "ascii": np.array(tuple(" .:-=+*#%@")),
    "block": np.array(tuple(" ░▒▓█")),
}


@lru_cache(maxsize=1)
def _regular_meshgrid(xmin, ymin, xmax, ymax, **kwargs):
    return np.meshgrid(np.arange(xmin, xmax), np.arange(ymin, ymax), **kwargs)


def resize(image: np.ndarray, shape: tuple) -> np.ndarray:
    """Nearest neighbor image resizing"""
    x, y = _regular_meshgrid(0, 0, shape[0], shape[1])
    x = image.shape[0] * x / shape[0]
    y = image.shape[1] * y / shape[1]
    x = x.astype(int)
    y = y.astype(int)
    return image[x, y].T


def img2ascii(
    image: np.ndarray,
    width: int,
    height: int,
    vmin: float,
    vmax: float,
    cmap: str = "block",
) -> np.ndarray:
    if len(image.shape) != 2:
        raise ValueError("Invalid shape for grayscale image")
    image = resize(image, (height, width))
    scale = LinearScale()
    scale.fit([vmin, vmax], target_min=0, target_max=len(COLORMAPS[cmap]) - 1)
    cmap_idx = scale.transform(image.astype(float).clip(vmin, vmax)).round().astype(int)
    return COLORMAPS[cmap][cmap_idx]
