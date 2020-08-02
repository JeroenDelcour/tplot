import numpy as np
from .scales import LinearScale


def resize(im, shape):
    """Nearest neighbor image resizing"""
    nR, nC = shape
    nR0, nC0 = im.shape[:2]  # input shape
    return np.array([[im[int(nR0 * r / nR)][int(nC0 * c / nC)] for c in range(nC)] for r in range(nR)])


def img2ascii(image: np.ndarray, width: int, height: int, vmin: float, vmax: float, cmap: str = "block") -> np.ndarray:
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
    scale.fit([vmin, vmax], target_min=0, target_max=len(cmap) - 1)
    out = [[cmap[min(max(round(scale.transform(v)), 0), len(cmap) - 1)] for v in row] for row in image]
    return np.array(out)
