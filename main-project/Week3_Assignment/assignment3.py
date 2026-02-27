import cv2
import numpy as np
import os
import glob

# Location of the image files
INPUT_DIR = "../../assignment3"
OUTPUT_DIR = "output"

def region_of_interest(img, vertices):
    """
    Applies an image mask. Only keeps the region of the image defined by the polygon
    formed from `vertices`. The rest of the image is set to black.
    """
    mask = np.zeros_like(img)
    if len(img.shape) > 2:
        channel_count = img.shape[2]
        ignore_mask_color = (255,) * channel_count
    else:
        ignore_mask_color = 255
        
    cv2.fillPoly(mask, vertices, ignore_mask_color)
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image

def process_image(image_path, output_path):
    # Load the image
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error loading image: {image_path}")
        return
        
    out_dir = os.path.dirname(output_path)
    base_name = os.path.basename(image_path)

    # 1. Convert to grayscale for edge detection
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(os.path.join(out_dir, f"01_gray_{base_name}"), gray)

    # 2. Apply Gaussian Blur (Optional but recommended to reduce noise)
    kernel_size = 3
    gray = cv2.GaussianBlur(gray, (kernel_size, kernel_size), 0)

    # 3. Apply Canny Edge Detector
    low_threshold = 100
    high_threshold = 300
    
    edges = cv2.Canny(gray, low_threshold, high_threshold)
    cv2.imwrite(os.path.join(out_dir, f"02_canny_{base_name}"), edges)

    # 4. Define Region of Interest (ROI)
    imshape = img.shape
    height, width = imshape[0], imshape[1]
    
    vertices = np.array([[
        (0, height),          
        (0, height * 0.8),         
        (width * 0.3, height * 0.5), 
        (width * 0.6, height * 0.5),      
        (width, height * 0.75)    ,
        (width, height)      
    ]], dtype=np.int32)
    
    masked_edges = region_of_interest(edges, vertices)
    cv2.imwrite(os.path.join(out_dir, f"03_masked_edges_{base_name}"), masked_edges)

    # 5. Apply Hough Transform
    rho = 1.5            # distance resolution in pixels
    theta = np.pi/180    # angular resolution in radians
    threshold = 60       # minimum number of votes
    min_line_length = 30 # minimum number of pixels making up a line
    max_line_gap = 40    # maximum gap in pixels between connectable line segments

    lines = cv2.HoughLinesP(masked_edges, rho, theta, threshold, np.array([]),
                            minLineLength=min_line_length, maxLineGap=max_line_gap)

    # 6. Draw the lines and center (Optional Extension)
    line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    
    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                if abs(y2 - y1) < 10:
                    continue
                print(f"x1: {x1}, y1: {y1}, x2: {x2}, y2: {y2}")
                cv2.line(line_img, (x1, y1), (x2, y2), [0, 0, 255], 5) 

    cv2.imwrite(os.path.join(out_dir, f"04_hough_lines_drawn_{base_name}"), line_img)

    # 7. Overlay lines onto original image
    result = cv2.addWeighted(img, 0.8, line_img, 1.0, 0)

    # Save the result
    cv2.imwrite(output_path, result)
    print(f"Processed and saved: {output_path}")

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # Use glob to find typical image formats
    image_files = glob.glob(os.path.join(INPUT_DIR, "*.jpg")) + \
                  glob.glob(os.path.join(INPUT_DIR, "*.png")) + \
                  glob.glob(os.path.join(INPUT_DIR, "*.jpeg"))
                  
    if not image_files:
        print(f"No images found in {INPUT_DIR}. Please check the path and try again.")
        return

    print(f"Found {len(image_files)} images. Processing only the first one for debugging...")

    if image_files:
        for img_path in image_files:
            filename = os.path.basename(img_path)
            out_path = os.path.join(OUTPUT_DIR, f"result_{filename}")
            process_image(img_path, out_path)
        # img_path = image_files[0]
        # filename = os.path.basename(img_path)
        # out_path = os.path.join(OUTPUT_DIR, f"result_{filename}")
        # process_image(img_path, out_path)

if __name__ == "__main__":
    main()
