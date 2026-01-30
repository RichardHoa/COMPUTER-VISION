import cv2
import numpy as np

class DilationProcessor:
    def __init__(self):
        pass

    def process(self, img, kernel_size=(5, 5), iterations=1):
        if img is None:
            return None
        kernel = np.ones(kernel_size, np.uint8)
        return cv2.dilate(img, kernel, iterations=iterations)
