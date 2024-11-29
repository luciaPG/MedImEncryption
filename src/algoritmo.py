import cv2
import numpy as np
import matplotlib.pyplot as plt

def process_image(image_path, block_size, threshold):
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Image not found at path: {image_path}")
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert to RGB
    M, N, _ = image.shape

    # Adjust dimensions to be divisible by block size
    M_adjusted = M - (M % block_size)
    N_adjusted = N - (N % block_size)
    image = image[:M_adjusted, :N_adjusted]

    # Divide into blocks and process each
    roi_mask = np.zeros((M_adjusted, N_adjusted), dtype=np.uint8)
    for i in range(0, M_adjusted, block_size):
        for j in range(0, N_adjusted, block_size):
            # Extract the block
            block = image[i:i + block_size, j:j + block_size]

            # Calculate the mean and deviation
            block_mean = np.mean(block)
            e = np.mean(np.abs(block - block_mean))

            # Determine if it's ROI or ROB
            if e > threshold:
                roi_mask[i:i + block_size, j:j + block_size] = 255  # ROI

    return image, roi_mask


def main():
    for i in range(1, 4):
        image_path = f"imagenes\prueba{i}.jpg"
    # Parameters
        block_size = 16  # Block size (s)
        threshold = 30   # Statistical threshold (τ)

        # Process the image
        try:
            original_image, roi_result = process_image(image_path, block_size, threshold)

            # Visualize results
            plt.figure(figsize=(10, 5))
            plt.subplot(1, 2, 1)
            plt.title("Original Image")
            plt.imshow(original_image)
            plt.axis("off")

            plt.subplot(1, 2, 2)
            plt.title("Regions of Interest (ROI)")
            plt.imshow(roi_result, cmap="gray")
            plt.axis("off")

            plt.show()

        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()

