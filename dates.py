import pandas as pd

# --- DECORATOR TO CONVERT DATE INSIDE FUNCTION TO DATETIME FORMAT --- #

def date_convert(func):
    """
    Function variable must me named "date" and be the first parameter.
    If not, this decorator does nothing.
    """
    def wrap(*args, **kwargs):
        try:
            if "date" not in kwargs:
                args = list(args)
                date = pd.to_datetime(args[0])
                args[0] = date
                args = tuple(args)
            else:
                kwargs["date"] = pd.to_datetime(kwargs["date"])
        except:
            None

        return func(*args, **kwargs)
    return wrap


# --- CHECK IF DATE IS A BUSINESS DAY --- #

@date_convert
def is_business_day(date, holidays=[]):
    """
    · date: date in Datetime format or YYYYMMDD
    · holidays: extra holidays to consider besides weekends
    """
    return date in pd.bdate_range(date, date, freq="C", holidays=holidays)


# --- DECORATOR TO BLOCK FUNCION EXCECUTION IN NON BUSINESS DAYS --- #

def valid_workday(date, holidays=[], output_message="Non-business day"):
    """
    · date: date in Datetime format or YYYYMMDD
    · holidays: extra holidays to consider besides weekends
    """
    def decorator(func):
        def wrap(*args, **kwargs):
            if not is_business_day(date, holidays):
                print(output_message)
                return
            func(*args, **kwargs)
        return wrap
    return decorator


# --- FINANCIAL BUSINESS DAY TREATMENT: FOLLOWING --- #

@date_convert
def following(date, holidays=[]):
    """
    · date: date in Datetime format or YYYYMMDD
    · holidays: extra holidays to consider besides weekends
    """
    if is_business_day(date):
        return date
    
    else:
        return pd.bdate_range(date, date + pd.Timedelta(days=100), holidays=holidays, freq="C")[0]
    

# --- FINANCIAL BUSINESS DAY TREATMENT: PRECEDING --- #

@date_convert
def preceding(date, holidays=[]):
    """
    · date: date in Datetime format or YYYYMMDD
    · holidays: extra holidays to consider besides weekends
    """
    if is_business_day(date):
        return date
    
    else:
        return pd.bdate_range(date - pd.Timedelta(days=100), date, holidays=holidays, freq="C")[-1]
    

# --- FINANCIAL BUSINESS DAY TREATMENT: MODIFIED FOLLOWING --- #

@date_convert
def modified_following(date, holidays=[]):
    """
    · date: date in Datetime format or YYYYMMDD
    · holidays: extra holidays to consider besides weekends
    """
    if following(date, holidays).month != date.month:
        return preceding(date, holidays)
    
    return following(date, holidays)


# --- DATE IN EXCEL NUMBER FORMAT --- #

@date_convert
def excel_date(date, time=True):
    date_0 = pd.to_datetime("18991230")
    delta = date - date_0
    days = (delta).days

    if time:
        return delta.days + delta.seconds / (24 * 60 * 60)
    
    return delta.days