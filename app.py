import cv2
import numpy as np
import os
import openai
import requests
from dotenv import load_dotenv

load_dotenv()


openai.organization = "org-bEJ5GRQShzFzZJwuTmSp63x4"
openai.api_key = os.getenv("OPENAI_API_KEY")


IMAGE_FILE = "cat.png"
INVERT_MASK = True


def crop_image_to_square(image: str or np.ndarray, save_image_name: str = "cropped_image", save: bool = False):

    if isinstance(image, str):
        # if the passed variable is file name, we read the object:
        # Load the image
        image = cv2.imread(image)
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

    if save:
        # Save the resized image
        cv2.imwrite(save_image_name + ".jpg", image)
        return image, save_image_name + ".jpg"

    return image


def resize_image(image: str or np.ndarray, width: int = 600, height: int = 600, save_image_name: str = "resized_image", save: bool = False):

    if isinstance(image, str):
        # if the passed variable is file name, we read the object:
        # Load the image
        image = cv2.imread(image)

    # Resize the image
    image = cv2.resize(image, (width, height))

    if save:
        # Save the resized image
        cv2.imwrite(save_image_name + ".jpg", image)
        return image, save_image_name + ".jpg"

    return image


_, name = crop_image_to_square(IMAGE_FILE, save=True)
img, name = resize_image(name, save=True)


# Convert the image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply threshold to the grayscale image
_, thresholded = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)

thresholded = cv2.bitwise_not(thresholded)

# Create a 3-channel mask
mask = cv2.merge([thresholded, thresholded, thresholded])

# Convert the mask to RGBA
mask = cv2.cvtColor(mask, cv2.COLOR_BGR2RGBA)


# Create a transparent background
b, g, r, a = cv2.split(mask)
mask = np.zeros((img.shape[0], img.shape[1], 4), dtype=np.uint8)
mask[:, :, 0] = b
mask[:, :, 1] = g
mask[:, :, 2] = r
mask[:, :, 3] = (thresholded == 0) * 255

if INVERT_MASK:
    mask = cv2.bitwise_not(mask)

mask_file_name = "mask_"+name.replace(".jpg", ".png")
compressed_file_name = "compressed_"+name.replace(".jpg", ".png")
print(mask_file_name, compressed_file_name)

# Save the result
cv2.imwrite(mask_file_name, mask)
cv2.imwrite(compressed_file_name, img, [cv2.IMWRITE_PNG_COMPRESSION, 9])




prompt = input("give the prompt for the background: ")

response = openai.Image.create_edit(
  image=open(compressed_file_name, "rb"),
  mask=open(mask_file_name, "rb"),
  prompt=prompt,
  n=1,
  size="512x512"
)
image_url = response['data'][0]['url']
print(image_url)

result_image = requests.get(image_url)
open("generated_"+name, "wb").write(result_image.content)
