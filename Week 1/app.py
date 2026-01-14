from PIL import Image

# Load BMP (24-bit color)
image = Image.open('input.bmp')

image = image.convert('RGB')
pixels = image.load()           
width, height = image.size

# Create a new grayscale image
gray_image = Image.new('L', (width, height))  
gray_pixels = gray_image.load()

# Manual nested loops for pixel-wise processing
for y in range(height):
    for x in range(width):
        r, g, b = pixels[x, y]
        # Calculate grayscale by standard formula
        gray = int(0.299*r + 0.587*g + 0.114*b)
        gray_pixels[x, y] = gray

# Save the grayscale image as BMP
gray_image.save('output_grayscale.bmp')

print('Grayscale BMP image saved as output_grayscale.bmp')