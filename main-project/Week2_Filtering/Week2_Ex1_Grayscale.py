import cv2


class GrayscaleProcessor:
    def __init__(self):
        pass
    
    def convert_to_grayscale(self, bgr_img):

        if bgr_img is None:
            return None

        gray_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2GRAY)
        return gray_img
    
