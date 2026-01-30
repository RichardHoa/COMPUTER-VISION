import cv2

class SobelXProcessor:
    def __init__(self):
        pass

    def process(self, img, ksize=3):
        if img is None:
            return None
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img
        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=ksize)
        return cv2.convertScaleAbs(sobelx)
