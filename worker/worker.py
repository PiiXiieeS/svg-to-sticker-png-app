import os
from redis import from_url
from rq import Worker, Queue, Connection

REDIS_IMAGE_JOB_QUEUE = os.getenv('REDIS_IMAGE_JOB_QUEUE') or 'image-processing-queue'
REDIS_QUEUE_URL = os.getenv('REDIS_QUEUE_URL')

listen = [REDIS_IMAGE_JOB_QUEUE]
conn = from_url(REDIS_QUEUE_URL)

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(list(map(Queue, listen)))
        worker.work()