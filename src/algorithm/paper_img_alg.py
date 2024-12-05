import numpy as np
from PIL import Image

# 4D Cat Map for pseudorandom number generation
def cat_map_4d(size, a, b, c, d, initial_vector):
    A = np.array([[25, 4, 9, 7],
                  [66, 11, 24, 19],
                  [24, 4, 9, 7],
                  [14, 2, 5, 4]])
    current = initial_vector
    results = []
    for _ in range(size):
        current = np.mod(A @ current, 1)
        results.append(current)
    return np.array(results)

# Generate pseudorandom matrix
def generate_pr_matrix(size, initial_vector):
    sequence = cat_map_4d(size * size // 4, 2, 1, 2, 2, initial_vector)
    matrix = sequence[:, :4].reshape(size, size)
    return (matrix * 255).astype(np.uint8)

# 2D Cat Map for shuffling and unshuffling
def cat_map_2d(data, a, b, iterations, reverse=False):
    height, width = data.shape
    size = height * width
    A = np.array([[1, a],
                  [b, a * b + 1]])

    # If reverse is True, invert the map matrix
    if reverse:
        det = int(np.linalg.det(A))
        assert det == 1, "Matrix determinant must be 1 for reversibility."
        A = np.linalg.inv(A).astype(int) % height

    indices = np.arange(size)
    for _ in range(abs(iterations)):
        row, col = indices // width, indices % width
        new_row = (A[0, 0] * row + A[0, 1] * col) % height
        new_col = (A[1, 0] * row + A[1, 1] * col) % width
        indices = (new_row * width + new_col).astype(int)

    # Ensure indices are within bounds
    assert np.max(indices) < size, f"Index out of bounds: max index {np.max(indices)}, size {size}"
    return data.flatten()[indices].reshape((height, width))



# Encrypt an image with the corrected cat map
def encrypt_image(image_path, block_size, rounds, initial_key, output_path):
    image = Image.open(image_path).convert("L")  # Convert to grayscale
    image = np.array(image)
    height, width = image.shape
    
    assert height == width, "La imagen debe ser de proporción 1:1"
    assert height % block_size == 0, "Las dimensiones de la imagen deben ser divisibles por el tamaño del bloque"

    # Generate pseudorandom matrices X and W
    X = generate_pr_matrix(height, initial_key)
    W = generate_pr_matrix(height, initial_key + 0.1)

    for _ in range(rounds):
        # Shuffling Phase
        image = cat_map_2d(image, 1, 2, 1)
        X = cat_map_2d(X, 1, 2, 1)

        # Masking Phase
        image = np.bitwise_xor(image, X)
        image = np.bitwise_xor(image, W)
    Image.fromarray(image).save(output_path)
    return image

def decrypt_image(image_path, block_size, rounds, initial_key, output_path):
    encrypted_image = Image.open(image_path).convert("L")  # Convert to grayscale
    encrypted_image = np.array(encrypted_image)
    height, width = encrypted_image.shape
    assert height == width, "La imagen debe ser de proporción 1:1"
    assert height % block_size == 0, "Las dimensiones de la imagen deben ser divisibles por el tamaño del bloque"

    # Generate pseudorandom matrices X and W
    X = generate_pr_matrix(height, initial_key)
    W = generate_pr_matrix(height, initial_key + 0.1)

    for _ in range(rounds):
        # Reverse Masking Phase
        encrypted_image = np.bitwise_xor(encrypted_image, W)
        encrypted_image = np.bitwise_xor(encrypted_image, X)

        # Reverse Shuffling Phase
        encrypted_image = cat_map_2d(encrypted_image, 1, 2, 1, reverse=True)
        X = cat_map_2d(X, 1, 2, 1, reverse=True)
    
    Image.fromarray(encrypted_image).save(output_path)
    return encrypted_image


# Example Usage
key = np.array([0.1, 0.2, 0.3, 0.4])  # Example initial vector for the 4D cat map
block_size = 32  # Example block size
rounds = 4
input_image_path = "images/babuino.jpg"
encrypted_path = "encrypted-images/encrypted_babuino.png"
decrypted_path = "decrypted-images/decrypted_babuino.png"

#encrypted = encrypt_image(input_image_path, block_size, rounds, key, encrypted_path)

#decrypted = decrypt_image(encrypted, block_size, rounds, key, decrypted_path)
