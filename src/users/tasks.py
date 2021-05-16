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
    # function = pickle.loads(dumped_function)
    # args = [pickle.loads(arg) for arg in dumped_args]
    # kwargs = {key: pickle.loads(value) for key, value in dumped_kwargs.items()}
    # logger.info(args)
    # logger.info(kwargs)
    return function(*args, **kwargs)