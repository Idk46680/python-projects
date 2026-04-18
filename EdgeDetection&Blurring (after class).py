import cv2
import numpy as np
import matplotlib.pyplot as plt

def display_image(title, image):
    """Utility function to display an image."""
    plt.figure(figsize = (8, 8))
    if len(image.shape) == 2:
        plt.imshow(image, cmap = 'gray')
    else:
        plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title(title)
    plt.axis('off')
    plt.show()

def display_comparison(title, original, processed):
    """Display original and processed images side by side and allow saving."""
    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    if len(original.shape) == 2:
        plt.imshow(original, cmap='gray')
    else:
        plt.imshow(cv2.cvtColor(original, cv2.COLOR_BGR2RGB))
    plt.title("Original")
    plt.axis('off')

    plt.subplot(1, 2, 2)
    if len(processed.shape) == 2:
        plt.imshow(processed, cmap='gray')
    else:
        plt.imshow(cv2.cvtColor(processed, cv2.COLOR_BGR2RGB))
    plt.title(title)
    plt.axis('off')
    plt.tight_layout()
    plt.show()

    save_choice = input("Press 's' to save the processed image or any other key to continue: ").lower()
    if save_choice == 's':
        filename = input("Enter file name to save (e.g., output.jpg): ")
        cv2.imwrite(filename, processed)
        print(f"Image saved as {filename}")

def interactive_edge_detection(image_path):
    """Interactive activity for edge detection and filtering"""
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Image Not Found")
        return
    
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    display_image("Original Grayscale Image", gray_image)

    print("Select an option:")
    print("1. Sobel Edge Detection")
    print("2. Canny Edge Detection")
    print("3. Laplacian Edge Detection")
    print("4. Gaussian Smoothing")
    print("5. Median Filtering")
    print("6. Exit")

    while True:
        choice = input("Enter your choice (1-6): ")

        if choice == "1":
            sobel_x = cv2.Sobel(gray_image, cv2.CV_64F, 1, 0, ksize = 5)
            sobel_y = cv2.Sobel(gray_image, cv2.CV_64F, 0, 1, ksize = 5)
            combined_sobel = cv2.bitwise_or(sobel_x.astype(np.uint8), sobel_y.astype(np.uint8))
            display_comparison("Sobel Edge Detection", gray_image, combined_sobel)

        elif choice == "2":
            print("Adjust Thresholds for Canny (default: 100 and 200)")
            lower_thresh = int(input("Enter Lower threshold: "))
            upper_thresh = int(input("Enter Upper threshold: "))
            edges = cv2.Canny(gray_image, lower_thresh, upper_thresh)
            display_comparison("Canny Edge Detection",gray_image, edges)

        elif choice == "3":
            laplacian = cv2.Laplacian(gray_image, cv2.CV_64F)
            display_comparison("Laplacian Edge Detection", gray_image, np.abs(laplacian).astype(np.uint8))

        elif choice == "4":
            print("Adjust kernel size for Gaussian blur (must be odd, default: 5)")
            kernel_size = int(input("Enter kernel size (odd number): "))
            blurred = cv2.GaussianBlur(image, (kernel_size, kernel_size), 1)
            display_comparison("Gaussian Smoothed Image", gray_image, blurred)

        elif choice == "5":
            print("Adjust kernel size for Median Filtering (must be odd, default: 5)")
            kernel_size = int(input("Enter kernel size (odd number): "))
            median_filtered = cv2.medianBlur(image, kernel_size)
            display_image("Median Filtered Image", gray_image, median_filtered)

        elif choice == "6":
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please select a number between 1 and 6.")

interactive_edge_detection('/Users/byzeedmollah_/python projects/example (1).jpg')