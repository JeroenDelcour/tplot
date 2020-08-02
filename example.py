import tplot
from PIL import Image
import cv2
import numpy as np
import sys
from time import time, sleep

anscombeA = [
    [10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5],
    [8.04, 6.95, 7.58, 8.81, 8.33, 9.96, 7.24, 4.26, 10.84, 4.82, 5.68]
]
anscombeB = [
    [10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5],
    [9.14, 8.14, 8.74, 8.77, 9.26, 8.10, 6.13, 3.10, 9.13, 7.26, 4.74]
]
# sort by X value
anscombeA = list(zip(*[(str(x), y) for x, y in sorted(zip(*anscombeA))]))
anscombeB = list(zip(*[(x-8, y) for x, y in sorted(zip(*anscombeB))]))


def gaussian2D(shape, x_offset, y_offset, sigma_x=1, sigma_y=1, amplitude=1):
    X, Y = np.meshgrid(np.arange(0, shape[1]), np.arange(0, shape[0]))
    return amplitude * np.exp(
        -(
            (X - x_offset) ** 2 / (2 * (sigma_x ** 2))
            + (Y - y_offset) ** 2 / (2 * (sigma_y ** 2))
        )
    )


# image = gaussian2D((40, 40), x_offset=20, y_offset=20, sigma_x=5, sigma_y=5)
# image = np.array(Image.open("cameraman.png").convert("L"))
# fig = tplot.Figure()
# fig.bar(*anscombeA)
# fig.show()

def main():
    cap = cv2.VideoCapture("rickroll.mp4")
    fig = tplot.Figure()
    while True:
        t0 = time()
        success, frame = cap.read()
        if not success:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        fig.clear()
        fig.image(gray, cmap="block")
        scrollup = 54
        sys.stdout.write(f"\x1b[{scrollup}A")
        fig.show()
        dt = (time() - t0) / 1000
        sleep(1/25 - dt)


main()
