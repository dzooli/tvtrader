import time
from datetime import datetime
from typing import Dict
from pytz import timezone
from sanic import Sanic
from sanic.log import logger


def add_timezone_info(jsondata: Dict, app: Sanic):
    """
    Fixing the JSON data

    Converts the timestamp string given in UTC string to
    a local timezone based timestamp given in seconds.
    Also converts the direction field to uppercase and appends
    the utc_offset into the JSON object.
    """
    try:
        local_time_zone = timezone(app.config.TIMEZONE)
        t = time.strptime(jsondata["timestamp"], "%Y-%m-%dT%H:%M:%SZ")
        dt = datetime(t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec)
        utc_offset = local_time_zone.utcoffset(dt).total_seconds()
        timestamp = dt.timestamp() + utc_offset
    except Exception as ex:
        logger.error(str(ex))
        raise ex
    jsondata["utcoffset"] = utc_offset
    jsondata["timestamp"] = int(timestamp)


def format_json_input(jsondata: Dict):
    """
    Data format processing

    - strategy direction conversion to uppercase
    """
    jsondata["direction"] = jsondata["direction"].upper()
