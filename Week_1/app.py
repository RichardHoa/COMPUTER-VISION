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
        gray = int(0.8*r + 0.6*g + 0.3*b)
        gray_pixels[x, y] = gray

# Save the grayscale image as BMP
gray_image.save('2_output_grayscale.bmp')