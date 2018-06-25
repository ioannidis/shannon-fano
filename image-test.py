import numpy as np
from PIL import Image

'''
https://github.com/DanonOfficial/Huffman-Shannon-Fano-Coding/blob/master/png.py
https://stackoverflow.com/questions/8863917/importerror-no-module-named-pil
https://stackoverflow.com/questions/25102461/python-rgb-matrix-of-an-image
https://stackoverflow.com/questions/13730468/from-nd-to-1d-arrays
'''

code_size = 0
noise = 0

# Load image from file
image = Image.open("image.jpg")
print("Format: {}, Size: {}, Mode: {}".format(image.format, image.size, image.mode))

width = image.size[0]
height = image.size[1]
pixel_array = image.load()

# Extract RGB values from all pixels
array_4d = np.array(image)

# Convert 4d array to 1d
array_1d = np.ravel(array_4d)

print(array_1d)

print(pixel_array[0, 0])