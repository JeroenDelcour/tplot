import numpy as np
from .scales import LinearScale


def resize(im, shape):
    """Nearest neighbor image resizing"""
    nR, nC = shape
    nR0, nC0 = im.shape[:2]  # input shape
    return np.array([[im[int(nR0 * r / nR)][int(nC0 * c / nC)] for c in range(nC)] for r in range(nR)])


def img2ascii(image: np.ndarray, width: int, height: int, cmap: str = "ascii") -> np.ndarray:
    COLORMAPS = {
        "ascii": "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "[::-1],
        "ascii_simple": " .:-=+*#%@",
        "block": "█▓▒░ "[::-1]
    }
    cmap = COLORMAPS[cmap]
    if len(image.shape) != 2:
        raise ValueError("Invalid shape for grayscale image")
    image = resize(image, (height, width))
    scale = LinearScale()
    target_min, target_max = 0, len(cmap) - 1
    # guess correct value range
    if (image >= 0).all() and (image <= 1).all():  # between 0 and 1 inclusive
        scale.fit([0, 1], target_min, target_max)
    elif image.dtype == np.uint8:  # between 0 and 255 inclusive
        scale.fit([0, 255], target_min, target_max)
    else:
        scale.fit(image.flatten(), target_min, target_max)
    out = [[cmap[round(scale.transform(v))] for v in row] for row in image]
    return np.array(out)
