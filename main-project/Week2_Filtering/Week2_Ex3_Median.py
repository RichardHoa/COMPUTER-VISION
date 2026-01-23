import cv2
import os
class MedianProcessor:
    def __init__(self):
        pass

    def apply_median_filter(self, img_array, filename="output_median_custom.bmp"):
        try:
            if img_array is None:
                return None

            median_filtered = cv2.medianBlur(img_array, 5)

            save_dir = "CapturedImage"
            save_path = os.path.join(save_dir, filename)
            success = cv2.imwrite(save_path, median_filtered)

            if success:
                print(f"Successfully saved to {save_path}")
            
            return median_filtered

        except Exception as e:
            print("Error saving image:", e)
            return None