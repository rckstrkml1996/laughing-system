from datetime import datetime

import pytz

from .confparse import Config

config = Config("Settings", "../config.cfg", {"time_zone": "Europe/Moscow"})


local_tz = pytz.timezone(config("time_zone"))


def datetime_local_now():
    local_dt = datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_tz.normalize(local_dt)  # return datetime instance
