import numpy as np
from .scales import LinearScale
from PIL import Image


def resize(im, shape):
    """Nearest neighbor image resizing"""
    nR, nC = shape
    nR0, nC0 = im.shape[:2]  # input shape
    return np.array([[im[int(nR0 * r / nR)][int(nC0 * c / nC)] for c in range(nC)] for r in range(nR)])


def img2ascii(image: np.ndarray, width: int, height: int, cmap: str = "ascii") -> np.ndarray:
    COLORMAPS = {
        "ascii": "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "[::-1],
        "ascii_short": " .:-=+*#%@",
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


def gaussian2D(shape, x_offset, y_offset, sigma_x=1, sigma_y=1, amplitude=1):
    X, Y = np.meshgrid(np.arange(0, shape[1]), np.arange(0, shape[0]))
    return amplitude * np.exp(
        -(
            (X - x_offset) ** 2 / (2 * (sigma_x ** 2))
            + (Y - y_offset) ** 2 / (2 * (sigma_y ** 2))
        )
    )


# # image = gaussian2D((40, 40), x_offset=20, y_offset=20, sigma_x=5, sigma_y=5)
# image = np.array(Image.open("cameraman.png").convert("L"))
# result = img2ascii(image, 80, 50, cmap="ascii_short")
# print("\n".join(["".join(row) for row in result]))
