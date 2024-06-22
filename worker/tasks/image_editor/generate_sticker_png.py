"""
Description: script to create sticker image from logo png using OpenCV
Author: @SpencerLepine
Date: April 2024
Usage: (pyenv) $ python3 generateStickerPNG.py -p logos/airtable -f logo.png -o thumbnail-output.png
"""

from .editor import ImageEditor

def generate_sticker_png():
  INPUT_FOLDER_PATH = '.'
  INPUT_FILE_NAME = 'logo.png'
  OUTPUT_FILE_NAME = 'sticker.png'

  # Initialize Editor
  editor = ImageEditor(
    INPUT_FOLDER_PATH,
    INPUT_FILE_NAME,
    OUTPUT_FILE_NAME,
    PADDING_PERCENTANGE=0.15,
    BORDER_PERCENTAGE=0.07
  )

  # Generate sticker.png with white border
  editor.ensure_square_crop()
  editor.auto_resize_for_padding() 
  editor.add_border_outline(should_fill_holes=True)
  editor.export_image()