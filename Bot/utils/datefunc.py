from datetime import datetime

import pytz

from config import TIME_ZONE


local_tz = pytz.timezone(TIME_ZONE)


def datetime_local_now():
    local_dt = datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_tz.normalize(local_dt)  # return datetime instance
