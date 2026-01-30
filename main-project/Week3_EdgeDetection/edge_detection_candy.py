import cv2
import matplotlib.pyplot as plt

img = cv2.imread('../TestImage/test.jpg', cv2.IMREAD_GRAYSCALE)

# Canny edge detection, double threshold: 100 and 200
edges = cv2.Canny(img, 100, 300)

plt.imshow(edges, cmap='gray')
plt.title('Sobel Edge')
plt.axis('off')
plt.show()
