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

def saturdays():
    """Return list of saturdays 

    Returns:
        list(datetime): List of date time object
    """
    today = date.today()
    st_date = today
    
    # Finding next Saturday from today
    while st_date.weekday() != 5:  
        st_date += timedelta(days=1)
    
    saturdays_dates_list = []
    next_year_begin_date = dt.date(today.year + 1, 1, 1)
    
    # Add every Saturday 
    while st_date < next_year_begin_date:
        saturdays_dates_list.append(st_date)
        st_date += timedelta(days=7)
    
    return saturdays_dates_list

def first_or_fifteenth(date):
    """This function check the datate is between 1st day to 15th day or not and also saturday or sunday

    Args:
        date (datetime): A date 

    Returns:
        Boolean: True or False
    """
    if date.day in [1, 15] and date.weekday() not in [5, 6]:  
        return True
    return False
