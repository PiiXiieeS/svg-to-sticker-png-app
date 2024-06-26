from flask import *
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms.validators import DataRequired
from .lib.minio import __allowed_file, __upload_minio_object
from .lib.redis import __sheduled_tasks_count, __formatted_finished_tasks, __finished_tasks, __add_task_to_queue
from uuid import uuid4
import os, io
import json

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(32) # Key for FormWTF CSRF

class FileUploadForm(FlaskForm):
    file = FileField()

@app.route("/", methods=["GET", "POST"])
def landing_page():
    form = FileUploadForm()

    if form.validate_on_submit():
        file = request.files["file"]
        if file.filename and file and __allowed_file(file.filename):
            size = os.fstat(file.fileno()).st_size
            image_folder_uuid = f"{uuid4()}"
            __upload_minio_object(image_folder_uuid, "source-logo.svg", file, size)
            __add_task_to_queue("tasks.process_image_task", json.dumps({ "image_folder_uuid": image_folder_uuid }))
            form = FileUploadForm()
            form.file = FileField() # reset the form
            
    data = { "form": form, "queue_count": __sheduled_tasks_count(),"jobs": __formatted_finished_tasks(), "completed": len(__finished_tasks()) }
    return render_template("index.html", data=data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=FLASK_PORT)
