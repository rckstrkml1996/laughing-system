import os

from datetime import datetime

import pytz

from .confparse import Config

path = os.path.normpath(os.path.join(os.getcwd(), "../config.cfg"))
config = Config("Settings", path, {"time_zone": "Europe/Moscow"})


local_tz = pytz.timezone(config("time_zone"))


def datetime_local_now():
    local_dt = datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_tz.normalize(local_dt).replace(tzinfo=None)  # return datetime instance
