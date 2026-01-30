import cv2
import numpy as np

class SharpeningProcessor:
    def __init__(self):
        pass

    def process(self, img):
        if img is None:
            return None
        kernel = np.array([[0, -1, 0], 
                           [-1, 5,-1], 
                           [0, -1, 0]])
        return cv2.filter2D(img, -1, kernel)
