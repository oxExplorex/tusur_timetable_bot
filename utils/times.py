from datetime import datetime
from random import randint
from pytz import timezone

tz_nairobi = timezone("Asia/Novosibirsk")

def get_time_now():
    return datetime.now(tz_nairobi).strftime("%d_%m_%g")

def get_time_update():
    return datetime.now(tz_nairobi).strftime(f"%X.{randint(10,99)}")
