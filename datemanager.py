from datetime import date, timedelta

date_format = '%Y-%m-%d'
weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

def create_week():
    x = date.today()
    day_idx = (x.weekday())
    today = x - timedelta(days=day_idx)
    x = today
    x += timedelta(days=1)
    for n in range(7):
        yield x
        x += timedelta(days=1)

def get_week():
    week = [d.isoformat() for d in create_week()]
    return week

def inPast(dayx):
    day = date.strptime(dayx, date_format)
    if day < date.today():
        return True
    else:
        return False

def isDayException(chosen_day, exceptionsx):
    day = date.strptime(chosen_day, date_format)
    exceptions = exceptionsx[0].split()
    if weekdays[day.weekday()] in exceptions:
        return True
    else:
        return False
