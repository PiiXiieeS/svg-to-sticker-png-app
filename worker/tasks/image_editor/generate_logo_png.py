"""
Description: script to auto-adjust padding and make .png a square
Author: @SpencerLepine
Date: April 2024
Usage: (pyenv) $ python3 generateLogoPNG.py -p logos/airtable -f logo.png -o thumbnail-output.png
"""

from .editor import ImageEditor

def generate_logo_png():
  INPUT_FOLDER_PATH = '.'
  INPUT_FILE_NAME = 'source-logo.png'
  OUTPUT_FILE_NAME = 'logo.png'

  # Initialize Editor
  editor = ImageEditor(
    INPUT_FOLDER_PATH,
    INPUT_FILE_NAME,
    OUTPUT_FILE_NAME,
    PADDING_PERCENTANGE=0.03,
    BORDER_PERCENTAGE=0.07
  )

  # Generate re-sized logo.png
  editor.ensure_square_crop()
  editor.auto_resize_for_padding()
  editor.export_image()