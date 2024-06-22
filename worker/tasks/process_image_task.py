from minio import Minio
from cairosvg import svg2png
import os
import json
from .image_editor.generate_logo_png import generate_logo_png
from .image_editor.generate_sticker_png import generate_sticker_png
from .image_editor.generate_thumbnail_jpg import generate_thumbnail_jpg
from config import Config

# Delete temp files generated from OpenCV (like grayscale.png)
def delete_file_gracefully(file_path):
  try:
    if os.path.isfile(file_path):
      os.remove(file_path)
  except FileNotFoundError:
    pass
  except PermissionError as e:
    pass

client = Minio(Config.MINIO_API_HOST, Config.MINIO_ROOT_USER, Config.MINIO_ROOT_PASSWORD, secure=False)

def __upload_minio_object(foldername, filename, data, length):
    client.put_object(Config.ROOT_BUCKET_NAME, f"{foldername}/{filename}", data, length)
    print(f"{foldername}/{filename} is successfully uploaded to bucket {Config.ROOT_BUCKET_NAME}")

def process_image_task(task_arg):
    payload = json.loads(task_arg)
    image_folder_uuid = payload["image_folder_uuid"]

    # download the "source-logo.png"
    client.fget_object(Config.ROOT_BUCKET_NAME,f"{image_folder_uuid}/source-logo.svg","source-logo.svg")
    
    # run svg2png logic generating 2000x2000 image
    SIZE=2000
    GENERATED_PNG_FILE="source-logo.png"
    svg2png(url="source-logo.svg", write_to=GENERATED_PNG_FILE, output_width=SIZE, output_height=SIZE)
    
    # upload the new "source-logo.png" to minio
    with open(GENERATED_PNG_FILE, 'rb') as f:
        file_size = os.path.getsize(GENERATED_PNG_FILE)
        __upload_minio_object(image_folder_uuid, "source-logo.png", f, file_size)
    delete_file_gracefully("source-logo.svg") # Cleanup

    # run image editor to generate logo.png
    generate_logo_png()
    # upload logo.png to minio
    with open("logo.png", 'rb') as f:
        minio_file_name="logo.png"
        file_size = os.path.getsize("logo.png")
        __upload_minio_object(image_folder_uuid, minio_file_name, f, file_size)
    delete_file_gracefully("source-logo.png") # Cleanup

    # run image editor to generate sticker.png
    generate_sticker_png()
    # upload sticker.png to minio
    with open("sticker.png", 'rb') as f:
        minio_file_name="sticker.png"
        file_size = os.path.getsize("sticker.png")
        __upload_minio_object(image_folder_uuid, minio_file_name, f, file_size)
    delete_file_gracefully("logo.png") # Cleanup

    # run image editor to generate thumbnail.jpg
    generate_thumbnail_jpg()
    # upload thumbnail.jpg to minio
    with open("thumbnail.jpg", 'rb') as f:
        minio_file_name="thumbnail.jpg"
        file_size = os.path.getsize("thumbnail.jpg")
        __upload_minio_object(image_folder_uuid, minio_file_name, f, file_size)
    delete_file_gracefully("sticker.png") # Cleanup
    delete_file_gracefully("thumbnail.jpg") # Cleanup

    job_payload = json.dumps({
        'image_folder_uuid': image_folder_uuid,
        'thumbnailJPGUrl': client.presigned_get_object(Config.ROOT_BUCKET_NAME, f"{image_folder_uuid}/thumbnail.jpg").replace("flask-localhost", Config.ROOT_BUCKET_NAME).replace("minio:9000", "127.0.0.1:9000").split('?')[0],
        'stickerPNGUrl': client.presigned_get_object(Config.ROOT_BUCKET_NAME, f"{image_folder_uuid}/sticker.png").replace("flask-localhost", Config.ROOT_BUCKET_NAME).replace("minio:9000", "127.0.0.1:9000").split('?')[0],
        'logoPNGUrl': client.presigned_get_object(Config.ROOT_BUCKET_NAME, f"{image_folder_uuid}/logo.png").replace("flask-localhost", Config.ROOT_BUCKET_NAME).replace("minio:9000", "127.0.0.1:9000").split('?')[0],
        'sourceLogoPNGUrl': client.presigned_get_object(Config.ROOT_BUCKET_NAME, f"{image_folder_uuid}/source-logo.png").replace("flask-localhost", Config.ROOT_BUCKET_NAME).replace("minio:9000", "127.0.0.1:9000").split('?')[0],
    })
    return job_payload



