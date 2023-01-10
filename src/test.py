import datetime

from dateutil.rrule import rrule, DAILY


date1 = datetime.datetime(2023, 1, 10)
date2 = datetime.datetime(2023, 2, 1)


a = {
    date1: "Hola",
    date2: "Chau"
}

date1 = datetime.datetime(2023, 1, 10)
print(a[date1])