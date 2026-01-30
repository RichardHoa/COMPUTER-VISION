import cv2

class LaplacianProcessor:
    def __init__(self):
        pass

    def process(self, img, ksize=3):
        if img is None:
            return None
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img
        laplacian = cv2.Laplacian(gray, cv2.CV_64F, ksize=ksize)
        return cv2.convertScaleAbs(laplacian)
