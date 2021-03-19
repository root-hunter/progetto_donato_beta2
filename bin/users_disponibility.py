import sqlite3

import bin.users as u
import mysql.connector

conn = mysql.connector.connect(
  host="localhost",
  user="root",
  password="password",
  database="mydb"
)

def add_session(telegram_id):
    cur = conn.cursor(buffered=True)
    print(telegram_id)
    l = u.get_user_session(telegram_id)

    print(l)
    cur.execute("insert into users_disponibility(telegram_id, name, surname,availability, time_update, region, province) values(%s,%s,%s,%s,%s,%s,%s)", (l[1], l[2], l[3], l[4], l[6], l[7], l[8]))
    conn.commit()
    cur.close()

import matplotlib.pyplot as plt

def get_users_active():
    cur = conn.cursor(buffered=True)

    cur.execute("select * from users_active")
    r = cur.fetchall()

    if r == None:
        return None
    else:
        return list(r)

def get_users_inactive():
    cur = conn.cursor(buffered=True)

    cur.execute("select * from users_not_active")
    conn.commit()

    r = cur.fetchall()

    if r == None:
        return None
    else:
        return list(r)

def get_users_active_by_region(region):
    cur = conn.cursor(buffered=True)

    r = cur.execute("select * from users_active where region = %s",(region,))
    r = cur.fetchall()

    conn.commit()

    if r == None:
        return None
    else:
        return list(r)

def get_users_active_by_province(province):
    cur = conn.cursor(buffered=True)

    r = cur.execute("select * from users_active where province = %s",(province,))

    r = cur.fetchall()
    conn.commit()

    if r == None:
        return None
    else:
        return list(r)

def get_users_by_province(province):
    cur = conn.cursor(buffered=True)

    r = cur.execute("select * from users_for_search where province = %s",(province,))

    r = cur.fetchall()
    conn.commit()

    print("###################à")
    print(r)
    print("###################à")

    if r == None:
        return None
    else:
        return list(r)

def get_users_by_region(region):
    cur = conn.cursor(buffered=True)

    r = cur.execute("select * from users_for_search where region = %s",(region,))

    r = cur.fetchall()
    conn.commit()

    if r == None:
        return None
    else:
        return list(r)


def get_regions():
    cur = conn.cursor(buffered=True)
    cur.execute("SELECT distinct region FROM users_for_search")
    r = cur.fetchall()
    conn.commit()
    print(type(r))


    if r == None:
        return None
    else:
        t = []

        for x in r:
            t.append(x[0])
        return t

def get_provinces():
    cur = conn.cursor(buffered=True)
    r = cur.execute("SELECT distinct province FROM users_for_search")
    r = cur.fetchall()
    conn.commit()
    if r == None:
        return None
    else:
        t = []

        for x in r:
            t.append(x[0])
        return t

def count_active_users():
    cur = conn.cursor(buffered=True)

    cur.execute("SELECT count(id) FROM users_active")
    r = cur.fetchone()
    conn.commit()
    print(r)
    if r == None:
        return None
    else:
        return r[0]

def count_active_users_by_region(region):
    cur = conn.cursor(buffered=True)

    cur.execute("SELECT count(id) FROM users_active where region = %s", (region,))
    r = cur.fetchone()
    conn.commit()
    print(r)
    if r == None:
        return None
    else:
        return r[0]


def count_not_active_user():
    cur = conn.cursor(buffered=True)

    cur.execute("SELECT count(id) FROM users_not_active")
    r = cur.fetchone()
    conn.commit()
    print(r)
    if r == None:
        return None
    else:
        return r[0]


def count_not_active_users_by_region(region):
    cur = conn.cursor(buffered=True)

    cur.execute("SELECT count(id) FROM users_not_active where region = %s", (region,))
    r = cur.fetchone()
    conn.commit()
    print(r)
    if r == None:
        return None
    else:
        return r[0]

def count_users_by_region(region):
    cur = conn.cursor(buffered=True)

    cur.execute("SELECT count(id) FROM users where region = %s", (region,))
    r = cur.fetchone()
    conn.commit()
    print(r)
    if r == None:
        return None
    else:
        return r[0]


def get_percent_active():
    return float((count_active_users()/count_total_users())*100)

def get_percent_inactive():
    return float((count_not_active_user()/count_total_users())*100)

def count_total_users():
    cur = conn.cursor(buffered=True)

    cur.execute("SELECT count(p.id) FROM (select * from users_active union select * from users_not_active) as p")
    r = cur.fetchone()
    conn.commit()
    print(r)
    if r == None:
        return None
    else:
        return r[0]

if __name__ == '__main__':
    plotter("846989549")
