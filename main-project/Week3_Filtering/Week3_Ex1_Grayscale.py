import cv2

class GrayscaleProcessor:
    def __init__(self):
        pass

    def process(self, img):
        if img is None:
            return None
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
