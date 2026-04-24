import cv2
import numpy as np

def apply_color_filter(image,filter_type):
    """Apply the specified color filter to the image."""

    filtered_image = image.copy()
    if filter_type == "red_tint":
        filtered_image[:, :, 1] = 0 
        filtered_image[:, :, 0] = 0

    elif filter_type == "blue_tint":
        filtered_image[:, :, 1] = 0
        filtered_image[:, :, 2] = 0
    
    elif filter_type == "green_tint":
        filtered_image[:, :, 0] = 0
        filtered_image[:, :, 2] = 0

    elif filter_type == "increase_red":
        filtered_image[:, :, 2] = cv2.add(filtered_image[:, :, 2], 30)
    
    elif filter_type == "decrease_blue":
        filtered_image[:, :, 0] = cv2.subtract(filtered_image[:, :, 0], 30)

    elif filter_type == "increase_blue":
        filtered_image[:, :, 0] = cv2.add(filtered_image[:, :, 0], 30)

    elif filter_type == "decrease_red":
        filtered_image[:, :, 2] = cv2.subtract(filtered_image[:, :, 1], 30)

    elif filter_type == "increase green":
        filtered_image[:, :, 1] = cv2.add(filtered_image[:, :, 1], 30)

    elif filter_type == "decrease_green":
        filtered_image[:, :, 1] = cv2.subtract(filtered_image[:, :, 1], 30)


    return filtered_image

image_path = '/Users/byzeedmollah_/python projects/example (1).jpg'
image = cv2.imread(image_path)

if image is None:
    print("Error: Image not found!")
else:
    filter_type = "original"

    print("Press the following keys to apply filters:")
    print("r - Red Tint")
    print("b - Blue Tint")
    print("g - Green Tint")
    print("i - Increase Red Intensity")
    print("d - Decrease Blue Intensity")
    print("q - Quit")
    print("p - Increase Blue Intensity")
    print("l - Decrease Red Intensity")
    print("m - Increase Green Intensity")
    print("n - Decrease Green Intensity")

    while True:
        filtered_image = apply_color_filter(image, filter_type)
        cv2.imshow("Filtered Image", filtered_image)
        key = cv2.waitKey(0) & 0xFF

        if key == ord('r'):
            filter_type = "red_tint"
        elif key == ord('b'):
            filter_type = "blue_tint"
        elif key == ord('g'):
            filter_type = "green_tint"
        elif key == ord('i'):
            filter_type = "increase_red"
        elif key == ord('d'):
            filter_type = "decrease_blue"
        elif key == ord('p'):
            filter_type = "increase_blue"
        elif key == ord('l'):
            filter_type = "decrease_red"
        elif key == ord('m'):
            filter_type = "increase_green"
        elif key == ord('n'):
            filter_type = "decrease_green"
        elif key == ord('q'):
            print("Exiting...")
            break
        else:
            print("Invalid Key! Please use 'r', 'b', 'g', 'i', 'd', 'p', 'l', 'm', 'n' or 'q'. ")

cv2.destroyAllWindows()