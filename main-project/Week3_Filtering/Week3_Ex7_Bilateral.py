import cv2

class BilateralProcessor:
    def __init__(self):
        pass

    def process(self, img, d=9, sigmaColor=75, sigmaSpace=75):
        if img is None:
            return None
        return cv2.bilateralFilter(img, d, sigmaColor, sigmaSpace)
