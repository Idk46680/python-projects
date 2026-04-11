import cv2
import numpy as np
import matplotlib.pyplot as plt

image = cv2.imread("/Users/byzeedmollah_/python projects/earth_image.jpeg")
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

(h, w) = image.shape[:2]
center = (w//2, h//2)
M = cv2.getRotationMatrix2D(center, 25, 1.2)
rotated = cv2.warpAffine(image, M, (w, h))

brightness_matrix = np.ones(image.shape, dtype = "uint8") * 65
final_image = cv2.add(rotated, brightness_matrix)

final_rgb = cv2.cvtColor(final_image, cv2.COLOR_BGR2RGB)

plt.imshow(final_rgb)
plt.title("Rotated + Brighter Image")
plt.axis('off')
plt.show()