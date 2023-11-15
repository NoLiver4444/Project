from datetime import datetime
from calendar import monthrange

def new_month(db, days):
    year_now = datetime.now().year
    month_now = datetime.now().month
    days = monthrange(year_now, month_now)[1]
    db.cursor().execute("""update checking set number = 0 where name = 'check_month'""")
    db.cursor().execute("update checking set number = " + str(year_now) + " where name = 'year'")
    db.cursor().execute("update checking set number = " + str(month_now) + " where name = 'month'")
    db.commit()
    return days

def days_maker(db, days):
    db.cursor().execute("""delete from days""")
    for i in range(1, days + 1):
        db.cursor().execute("INSERT INTO days(day, number, time) values('" + str(i) + "', '0', '0')")
    db.cursor().execute("""update checking set number = 1 where name = 'check_month'""")
    db.commit()

def make_time(timer):
    text = list(map(int, timer.text().split(":")))
    text[2] += 1
    if text[2] == 60:
        text[1] += 1
        text[2] = 0
    if text[1] == 60:
        text[0] += 1
        text[1] = 0
    for i in range(len(text)):
        if text[i] < 10:
            text[i] = "0" + str(text[i])
        else:
            text[i] = str(text[i])
    return text


def obn_db_time(db):
    text = \
        db.cursor().execute("select time from days where day = " + str(datetime.now().day)).fetchall()[0][
            0]
    db.cursor().execute(
        "update days set time = " + str(int(text) + 1) + " where day = " + str(datetime.now().day))
    db.commit()