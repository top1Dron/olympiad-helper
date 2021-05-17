from config.celery import app
from typing import Any
from .services import send_email
import logging
import pickle

logger = logging.getLogger(__name__)


@app.task
def task_send_email(subject:str, message:str, to:list):
    send_email(subject, message, to)


@app.task(serializer='pickle')
def task_call_function(function: bytes, *args: list[Any], **kwargs: dict) -> Any:
    return function(*args, **kwargs)