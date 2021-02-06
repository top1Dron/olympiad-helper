from config.celery import app
from .service import send_email


@app.task
def task_send_email(subject:str, message:str, to:list):
    send_email(subject, message, to)