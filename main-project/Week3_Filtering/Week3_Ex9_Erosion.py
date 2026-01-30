import cv2
import numpy as np

class ErosionProcessor:
    def __init__(self):
        pass

    def process(self, img, kernel_size=(5, 5), iterations=1):
        if img is None:
            return None
        kernel = np.ones(kernel_size, np.uint8)
        return cv2.erode(img, kernel, iterations=iterations)
