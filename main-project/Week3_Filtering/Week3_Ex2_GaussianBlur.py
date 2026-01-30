import cv2

class GaussianProcessor:
    def __init__(self):
        pass

    def process(self, img, kernel_size=(5, 5), sigmaX=0):
        if img is None:
            return None
        return cv2.GaussianBlur(img, kernel_size, sigmaX)
