import cv2
class GaussianProcessor:
    def __init__(self):
        pass
    
    def apply_gaussian_filter(self, img, kernel_size=(5, 5), sigma=1.0):

        if img is None:
            return None

        filtered_img = cv2.GaussianBlur(img, kernel_size, sigma)
        return filtered_img
