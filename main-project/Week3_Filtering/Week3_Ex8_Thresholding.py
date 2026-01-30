import cv2

class ThresholdingProcessor:
    def __init__(self):
        pass

    def process(self, img, thresh=127, maxval=255, type=cv2.THRESH_BINARY):
        if img is None:
            return None
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img
        _, dst = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return dst
