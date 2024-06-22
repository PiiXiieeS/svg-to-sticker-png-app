"""
Description: script to create sticker image from logo png using OpenCV
Author: @SpencerLepine
Date: April 2024
Usage: (pyenv) $ python3 generateThumbnailJPG.py -p logos/airtable -f sticker.png -o thumbnail.jpg
"""

import cv2
import numpy as np

# Config
WHITE_BACKGROUND=(247,247,247)
BLUR_PIXEL_SIZE=40

def __generate_transparent_background(img):
    if img.shape[2] == 4:
        return img

    alpha = np.sum(img, axis=-1) > 0
    alpha = np.uint8(alpha * 255)
    transparent_image = np.dstack((img, alpha))
    return transparent_image

def __generate_black_logo_shape(image):
  hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
  saturation = hsv_image[:, :, 1]
  value = hsv_image[:, :, 2]

  # Add off-white background
  transparent_pixels = (saturation == 0)
  colored_mask = (saturation > 0) | (value > 230)
  hsv_image[transparent_pixels, 0] = 0.114
  hsv_image[transparent_pixels, 1] = 0
  hsv_image[transparent_pixels, 2] = WHITE_BACKGROUND[2]

  ## Add dark shadow pixels
  hsv_image[colored_mask, 0] = 0.114
  hsv_image[colored_mask, 1] = 0
  DARK_COLOR=(3, 3, 3)
  hsv_image[colored_mask, 2] = DARK_COLOR[2]

  modified_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)
  blurred_img = cv2.blur(modified_image, (BLUR_PIXEL_SIZE, BLUR_PIXEL_SIZE))
  return blurred_img

def __merge_two_images(bg_img, img_to_overlay_t):
    b,g,r,a = cv2.split(img_to_overlay_t)
    overlay_color = cv2.merge((b,g,r))
    mask = cv2.medianBlur(a,5)
    img1_bg = cv2.bitwise_and(bg_img.copy(),bg_img.copy(),mask = cv2.bitwise_not(mask))
    img2_fg = cv2.bitwise_and(overlay_color,overlay_color,mask = mask)
    bg_img = cv2.add(img1_bg, img2_fg)

    return bg_img

def generate_thumbnail_jpg():
    INPUT_FOLDER_PATH = '.'
    INPUT_FILE_NAME = 'sticker.png'
    OUTPUT_FILE_NAME = 'thumbnail.jpg'
    INPUT_FILE_PATH=INPUT_FOLDER_PATH + '/' + INPUT_FILE_NAME
    OUTPUT_FILE_PATH=INPUT_FOLDER_PATH + '/' + OUTPUT_FILE_NAME

    source_image = cv2.imread(INPUT_FILE_PATH)
    source_image = __generate_transparent_background(source_image)
    shadow_image = __generate_black_logo_shape(source_image)
    merged_image = __merge_two_images(shadow_image, source_image)
    resized = cv2.resize(merged_image, (650, 650), interpolation = cv2.INTER_LINEAR)
    cv2.imwrite(OUTPUT_FILE_PATH, resized)

