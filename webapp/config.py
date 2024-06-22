import os

class Config:
    FLASK_PORT= os.getenv("FLASK_PORT")
    ALLOWED_FILE_EXTENSIONS = {"svg"}
    
    # Minio
    MINIO_ROOT_USER = os.getenv("MINIO_ROOT_USER")
    MINIO_ROOT_PASSWORD = os.getenv("MINIO_ROOT_PASSWORD")
    ROOT_BUCKET_NAME =  os.getenv("MINIO_ROOT_BUCKET")
    MINIO_API_HOST = os.getenv("MINIO_ENDPOINT")

    # Redis
    REDIS_QUEUE_URL = os.getenv("REDIS_QUEUE_URL")
    REDIS_IMAGE_JOB_QUEUE = os.getenv("REDIS_IMAGE_JOB_QUEUE") or 'image-processing-queue'