import cv2
import os
import numpy as np
class CaptureSaveImgProcessor:
    def __init__(self):
        pass
    
    def capture_and_save_image(self, bgr_img, filename):
 
        try:
            if bgr_img is None or not isinstance(bgr_img, np.ndarray):
                return False

            save_dir = "CapturedImage"
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)

            save_path = os.path.join(save_dir, filename)

            success = cv2.imwrite(save_path, bgr_img)

            return success

        except Exception as e:
            print("Error saving image:", e)
            return False
    