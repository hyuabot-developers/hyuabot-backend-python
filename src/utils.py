import datetime
import logging
import random
import string

logger = logging.getLogger(__name__)
ALPHA_NUM = string.ascii_letters + string.digits
KST = datetime.timezone(datetime.timedelta(hours=9))


def generate_random_alphanum(length: int = 20) -> str:
    return "".join(random.choices(ALPHA_NUM, k=length))


def time_to_str(td: datetime.time) -> str:
    return f"{td.hour:02d}:{td.minute:02d}:{td.second:02d}"


def remove_timezone(dt: datetime.time) -> datetime.time:
    return dt.replace(tzinfo=None)


def timestamp_tz_to_datetime(ts: datetime.time) -> str:
    return ts.strftime("%H:%M:%S")


def datetime_to_str(dt: datetime.datetime) -> str:
    return dt.strftime("%Y-%m-%d %H:%M:%S")
