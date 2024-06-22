import os

class Config:
    # Minio
    MINIO_ROOT_USER = os.getenv("MINIO_ROOT_USER")
    MINIO_ROOT_PASSWORD = os.getenv("MINIO_ROOT_PASSWORD")
    ROOT_BUCKET_NAME =  os.getenv("MINIO_ROOT_BUCKET")
    MINIO_API_HOST = os.getenv("MINIO_ENDPOINT")
    MINIO_SERVER_PORT = os.getenv("MINIO_SERVER_PORT")