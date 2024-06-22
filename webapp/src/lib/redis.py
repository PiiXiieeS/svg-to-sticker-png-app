from redis import from_url
from rq import Queue
from rq.job import Job
import json
from config import Config

# Initialize connection
redis_url = Config.REDIS_QUEUE_URL
conn = from_url(redis_url)  

def __get_queue(queue_name=Config.REDIS_IMAGE_JOB_QUEUE):
    return Queue(name=queue_name,connection=conn)
    
def __sheduled_tasks_count(queue_name=Config.REDIS_IMAGE_JOB_QUEUE):
    queue = __get_queue()
    return queue.count
    
def __add_task_to_queue(task,*args,**kwargs):
    queue = __get_queue()
    queue.enqueue(task,*args,**kwargs)    

def __fetch_job(job_id):
    job_data = Job.fetch(job_id, connection=conn)
    return job_data

def __finished_tasks():
    queue = __get_queue()
    job_ids=queue.finished_job_registry.get_job_ids()
    _jobs=[Job.fetch(_job_id, connection=conn) for _job_id in job_ids]
    return _jobs

def __parsed_job_payload(job_data, job_id):
    payload = json.loads(job_data.result)
    thumbnailJPGUrl = payload["thumbnailJPGUrl"]
    stickerPNGUrl = payload["stickerPNGUrl"]
    logoPNGUrl = payload["logoPNGUrl"]
    sourceLogoPNGUrl = payload["sourceLogoPNGUrl"]
    data={'job_id': job_id, 'thumbnailJPGUrl': thumbnailJPGUrl, 'stickerPNGUrl': stickerPNGUrl, 'logoPNGUrl': logoPNGUrl, 'sourceLogoPNGUrl': sourceLogoPNGUrl }
    return data

def __formatted_finished_tasks():
    queue = __get_queue()
    job_ids=queue.finished_job_registry.get_job_ids()
    _formatted_jobs=[__parsed_job_payload(Job.fetch(_job_id, connection=conn), _job_id) for _job_id in job_ids]
    return _formatted_jobs