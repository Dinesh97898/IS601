import datetime as dt
from datetime import datetime, date, timedelta

def my_datetime(dt):
    """This method coverts the date time to string

    Args:
        dt (datatime): datetime

    Returns:
        str: formatted datetime
    """
    return dt.strftime("%Y %m %d %H %M %S")
