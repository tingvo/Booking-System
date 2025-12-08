from datetime import date, timedelta

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

def inPast(day):
    if day < date.today():
        return True
    else:
        return False

