import numpy as np

from imports import *
from constants import *


def crop_image_to_square(image: np.ndarray):

    # Get the height and width of the image
    height, width, _ = image.shape

    # Determine the length of the crop
    crop_length = min(height, width)

    # Compute the start and end row/column for the crop
    start_row = (height - crop_length) // 2
    end_row = start_row + crop_length
    start_col = (width - crop_length) // 2
    end_col = start_col + crop_length

    # Crop the image
    image = image[start_row:end_row, start_col:end_col]

    return image


def resize_image(image: np.ndarray, width: int = 600, height: int = 600):

    # Resize the image
    image = cv2.resize(image, (width, height))

    return image


def convert_to_grayscale(image: np.ndarray):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def get_mask(grayscale_image: np.ndarray, threshold: int = None):

    if threshold is None:
        return cv2.threshold(grayscale_image, 0, 255, cv2.THRESH_OTSU)

    return cv2.threshold(grayscale_image, threshold, 255, cv2.THRESH_BINARY)


def invert_bitwise(image: np.ndarray):
    return cv2.bitwise_not(image)


def create_transparent_mask_old(thresholded: np.ndarray):

    # Create a 3-channel mask
    mask = cv2.merge([thresholded, thresholded, thresholded])

    # Convert the mask to RGBA
    mask = cv2.cvtColor(mask, cv2.COLOR_BGR2RGBA)

    # Create a transparent background
    b, g, r, a = cv2.split(mask)
    mask = np.zeros((thresholded.shape[0], thresholded.shape[1], 4), dtype=np.uint8)
    mask[:, :, 0] = b
    mask[:, :, 1] = g
    mask[:, :, 2] = r
    mask[:, :, 3] = (thresholded == 0) * 255

    return mask


def create_transparent_mask(binary_img: np.ndarray):
    # Initialize an all-zero array in the shape of the input image but with 4 channels (RGBA)
    rgba = np.zeros((binary_img.shape[0], binary_img.shape[1], 4), dtype=np.uint8)

    # Set RGB channels equal to binary_img and A channel to the inverse of binary_img
    rgba[..., :3] = cv2.merge([binary_img] * 3)
    rgba[..., 3] = 255 - binary_img

    return rgba
