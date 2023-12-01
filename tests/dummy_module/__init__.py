import datetime
from uuid import uuid4, UUID
from tests import dummy_other_module

some_value = {"real_value": 1}


def get_current_time() -> datetime.datetime:
    return datetime.datetime.now()


def generate_uuid() -> UUID:
    return uuid4()


def something() -> str:
    return dummy_other_module.some_other_func()
