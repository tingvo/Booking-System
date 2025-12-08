from datetime import date, timedelta

one_day = timedelta(days=1)

def create_week():
    x = date.today()
    day_idx = (x.weekday())
    today = x - timedelta(days=day_idx)
    x = today
    x += one_day
    for n in range(7):
        yield x
        x += one_day

def get_week():
    week = [d.isoformat() for d in create_week()]
    return week

def inPast():
    #return True
    #return False
    pass

