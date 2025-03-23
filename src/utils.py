import datetime
import logging
import random
import string

logger = logging.getLogger(__name__)
ALPHA_NUM = string.ascii_letters + string.digits
KST = datetime.timezone(datetime.timedelta(hours=9))


def generate_random_alphanum(length: int = 20) -> str:
    return "".join(random.choices(ALPHA_NUM, k=length))


def timedelta_to_str(td: datetime.timedelta) -> str:
    total_seconds = td.total_seconds()
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"


def second_to_timedelta(seconds: int) -> datetime.timedelta:
    return datetime.timedelta(seconds=seconds)


def timedelta_to_seconds(td: datetime.timedelta) -> float:
    return td.total_seconds()


def remove_timezone(dt: datetime.time) -> datetime.time:
    return dt.replace(tzinfo=None)


def timestamp_tz_to_datetime(ts: datetime.time) -> str:
    return ts.strftime("%H:%M:%S")


def datetime_to_str(dt: datetime.datetime) -> str:
    return dt.strftime("%Y-%m-%d %H:%M:%S")
