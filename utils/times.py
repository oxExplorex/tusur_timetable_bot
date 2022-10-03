from datetime import datetime
from random import randint
from pytz import timezone

tz_nairobi = timezone("Asia/Novosibirsk")

def get_time_now() -> str:
    return datetime.now(tz_nairobi).strftime("%d_%m_%y")

def get_week_year() -> str:
    return datetime.now(tz_nairobi).strftime("%y_%W")

def get_time_update() -> str:
    return datetime.now(tz_nairobi).strftime(f"%X.{randint(10,99)}")

def check_week(date: str) -> bool:
    d, m, g = date.split("_")
    get_week = datetime.strptime(date, '%d_%m_%y').strftime("%W")
    now_g, now_week = get_week_year().split("_")
    if g != now_g:
        return False
    if get_week == now_week:
        return True
    else:
        return False



if __name__ == "__main__":
    print(check_week(get_time_now()))


