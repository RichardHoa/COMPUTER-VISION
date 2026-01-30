import cv2

class MedianProcessor:
    def __init__(self):
        pass

    def process(self, img, ksize=5):
        if img is None:
            return None
        return cv2.medianBlur(img, ksize)
