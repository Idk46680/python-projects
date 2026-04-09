import cv2

image = cv2.imread('/Users/byzeedmollah_/python projects/8829c0e55f0522cea7b589fec420db88.jpg')

rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

resized_image_small = cv2.resize(rgb_image, (200,200))
resized_image_medium = cv2.resize(rgb_image, (400,400))
resized_image_large = cv2.resize(rgb_image, (600,600))




cv2.imshow('Small Image (200x200)', resized_image_small)
cv2.imshow('Medium Image (400x400)', resized_image_medium)
cv2.imshow('Large Image (600x600)', resized_image_large)

key = cv2.waitKey(0)

if key == ord('s'):

    cv2.imwrite('small_size_car_image.jpg', resized_image_small)
    cv2.imwrite('medium_size_car_image.jpg', resized_image_medium)
    cv2.imwrite('large_size_car_image.jpg', resized_image_large)

    print("Images saved")

else:

    print("Images not saved")


cv2.destroyAllWindows()

print(f"Small Image Dimensions: {resized_image_small.shape}")
print(f"Medium Image Dimensions: {resized_image_medium.shape}")
print(f"Large Image Dimensions: {resized_image_large.shape}")