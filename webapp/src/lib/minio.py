from minio import Minio
from config import Config

# Initialize connection
client = Minio(Config.MINIO_API_HOST, Config.MINIO_ROOT_USER, Config.MINIO_ROOT_PASSWORD, secure=False)

def __upload_minio_object(foldername, filename, data, length):
    # Create bucket if it doesn't exist
    if client.bucket_exists(Config.ROOT_BUCKET_NAME):
        print(f"Bucket '{Config.ROOT_BUCKET_NAME}' found")
    else:
        print(f"Bucket '{Config.ROOT_BUCKET_NAME}' not found, creating")
        client.make_bucket(Config.ROOT_BUCKET_NAME, object_lock=True)

    # Upload the file
    client.put_object(Config.ROOT_BUCKET_NAME, f"{foldername}/{filename}", data, length)
    print(f"{foldername}/{filename} is successfully uploaded to bucket {Config.ROOT_BUCKET_NAME}")

def __allowed_file(filename):
    # Validate input against support file extensions
    return "."in filename and filename.rsplit(".", 1)[1].lower() in Config.ALLOWED_FILE_EXTENSIONS

def __get_presigned_url(file_path):
  presigned_url = client.presigned_get_object(Config.ROOT_BUCKET_NAME, file_path)
  return presigned_url