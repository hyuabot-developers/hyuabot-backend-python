import datetime
import logging
import random
import string

logger = logging.getLogger(__name__)
ALPHA_NUM = string.ascii_letters + string.digits


def generate_random_alphanum(length: int = 20) -> str:
    return "".join(random.choices(ALPHA_NUM, k=length))


def timedelta_to_str(td: datetime.timedelta) -> str:
    total_seconds = td.total_seconds()
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"


def remove_timezone(dt: datetime.datetime) -> datetime.datetime:
    return dt.replace(tzinfo=None)