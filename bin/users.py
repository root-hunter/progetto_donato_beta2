import sqlite3
import mysql.connector

conn = mysql.connector.connect(
  host="localhost",
  user="root",
  password="password",
  database="mydb"
)

db_name = "mydb.db"

def check_user(bot):
    cur = conn.cursor()
    account_id = bot['message']['chat']['id']

    cur.execute("SELECT count(*) FROM users WHERE telegram_id = '%s';", (account_id))
    result = cur.fetchone()

    if result[0] == None or result[0] == 0:
        return False
    elif result[0] >= 1:
        return True

def singup(bot, update):
    cur = conn.cursor()
    account_id = bot['message']['chat']['id']

    if check_user(bot):
        cur.execute("INSERT INTO users(telegram_id, last_update)"
                     " VALUES(%s,%s);", (account_id, datetime.datetime.now()))

        print("CREATO NUOVO UTENTE: "+account_id)

        conn.commit()
    else:
        cur.execute("UPDATE users SET last_update = %s WHERE telegram_id = %s;", (datetime.datetime.now(),account_id))
        print("LOGIN: "+str(account_id))
        conn.commit()


def check_user_state(bot = None, user_id = None):
    cur = conn.cursor(buffered=True)
    account_id = None

    if user_id == None:
        account_id = bot['message']['chat']['id']
    else:
        account_id = user_id

    cur.execute("SELECT state FROM users WHERE telegram_id = '%s';", (account_id))
    result = cur.fetchone()

    if result == None:
        return None
    else:
        return result[0]

def set_user_state(bot = None, update = None, state = 0, user_id = None):
    cur = conn.cursor(buffered=True)

    account_id = None

    if user_id == None:
        account_id = bot['message']['chat']['id']
    else:
        account_id = user_id
    cur.execute("UPDATE users SET state = %s WHERE telegram_id = %s", (state,account_id))
    conn.commit()

def set_name_surname(bot, update, name, surname):
    cur = conn.cursor(buffered=True)

    account_id = bot['message']['chat']['id']

    cur.execute("UPDATE users SET name = '%s', surname = '%s' WHERE telegram_id = '%s'", (name, surname, account_id))
    conn.commit()


def update_start_date(user_id, date):
    cur = conn.cursor(buffered=True)

    cur.execute("UPDATE users SET start = '%s' WHERE telegram_id = '%s'", (date, user_id))
    conn.commit()


def update_end_date(user_id, date):
    cur = conn.cursor(buffered=True)

    cur.execute("UPDATE users SET end = %s WHERE telegram_id = %s", (date, user_id))
    conn.commit()


def set_avaib(user_id, state):
    cur = conn.cursor(buffered=True)

    cur.execute("UPDATE users SET availability = '%s' WHERE telegram_id = %s", (state, user_id))
    conn.commit()


def get_avaib(user_id):
    cur = conn.cursor(buffered=True)

    cur.execute("SELECT availability FROM users WHERE telegram_id = %s", (user_id,))
    r = cur.fetchone()
    print(r)
    if r == None:
        return None
    else:
        return r[0]


def set_region(user_id, region):
    cur = conn.cursor(buffered=True)
    cur.execute("UPDATE users SET region = %s WHERE telegram_id = %s ;", (region, str(user_id)))
    conn.commit()



def set_province(user_id, province):
    cur = conn.cursor(buffered=True)

    cur.execute("UPDATE users SET province = %s WHERE telegram_id = %s ;", (province, user_id))
    conn.commit()

def reset_province(user_id):
    cur = conn.cursor(buffered=True)

    cur.execute("UPDATE users SET province = %s WHERE telegram_id = %s ;", (None,user_id))
    conn.commit()

def reset_region(user_id):
    cur = conn.cursor(buffered=True)

    cur.execute("UPDATE users SET region = %s WHERE telegram_id = %s ;", (None,user_id))
    conn.commit()



def reset_reg_pro(user_id):
    cur = conn.cursor(buffered=True)

    cur.execute("UPDATE users SET region = %s, province = %s WHERE telegram_id = %s", (None,None, user_id))
    conn.commit()


def check_master(user_id : str) ->bool:
    cur = conn.cursor(buffered=True)

    cur.execute("SELECT count(telegram_id) FROM managers WHERE telegram_id = %s;", (str(user_id),))

    r = cur.fetchone()

    print("BACCALALAL")
    print(r[0])
    conn.commit()

    if r[0] >= 1:
        return True
    elif r[0] == 0:
        return False


def get_users_by_region(region):
    cur = conn.cursor(buffered=True)

    cur.execute("SELECT * FROM users WHERE region = %s", (region,))
    r = cur.fetchall()
    conn.commit()

    return r

def get_users_by_province(province):
    cur = conn.cursor(buffered=True)

    cur.execute("SELECT * FROM users WHERE province = %s", (province,))
    r = cur.fetchall()
    conn.commit()

    return r

def get_name_by_id(user_id):

    cur = conn.cursor(buffered=True)

    cur.execute("SELECT name FROM users WHERE id = '%s'", (user_id,))
    r = cur.fetchone()
    conn.commit()

    if r == None:
        return None
    else:
        return str(r[0])

def get_surname_by_id(user_id):
    cur = conn.cursor(buffered=True)

    cur.execute("SELECT surname FROM users WHERE id = '%s'", (user_id,))
    r = cur.fetchone()
    conn.commit()

    return str(r[0])

def get_dispo_by_id(user_id):
    cur = conn.cursor(buffered=True)

    cur.execute("SELECT availability FROM users WHERE id = '%s'", (user_id,))
    r = cur.fetchone()
    conn.commit()

    if r == None:
        return "NO"
    elif r[0] == 0:
        return "NO"
    elif r[0] == 1:
        return "SI"

def get_last_disp(user_id):

    cur = conn.cursor(buffered=True)

    cur.execute("SELECT availability_update FROM users WHERE id = '%s'", (user_id,))
    r = cur.fetchone()
    conn.commit()

    return str(r[0])
def get_regions():

    cur = conn.cursor(buffered=True)

    cur.execute("SELECT distinct u.region FROM users u order by u.region")
    r = cur.fetchall()
    conn.commit()

    if r == None:
        return None
    else:
        t = []

        for x in r:
            t.append(x[0])
        return t

def get_region_by_id(user_id):
    cur = conn.cursor(buffered=True)

    cur.execute("SELECT region FROM users WHERE id = '%s'", (user_id,))
    r = cur.fetchone()
    conn.commit()

    if r == None:
        return None
    else:
        return str(r[0])

def get_province_by_id(user_id):
    cur = conn.cursor(buffered=True)

    cur.execute("SELECT province FROM users WHERE id = '%s'", (user_id,))
    r = cur.fetchone()

    print("ALLALALA")
    print(r)

    conn.commit()

    if r == None:
        return None
    else:
        return str(r[0])

def get_provinces(user_id, region):

    cur = conn.cursor(buffered=True)
    cur.execute("SELECT distinct(province) FROM users WHERE region = %s order by province asc", (region,))
    r = cur.fetchall()
    print("DEBUT")
    print(r)
    cur.fetchall()
    conn.commit()

    if r == None:
        return None
    else:
        t = []
        for x in r:
            t.append(x[0])
        return list(t)
import datetime
def set_last_disponibility(user_id):
    cur = conn.cursor(buffered=True)

    cur.execute("UPDATE users SET availability_update = %s WHERE telegram_id = %s", (datetime.date.today(),user_id))
    conn.commit()


def get_user_session(user_id):
    cur = conn.cursor(buffered=True)

    cur.execute("SELECT * FROM users WHERE telegram_id = %s ", (user_id,))
    conn.commit()
    r = cur.fetchone()
    print("LALALALARRRJRJRJRJRJJRJRJRJ")
    print(r)
    if r[0] == None:
        return None
    else:
        return list(r)

def check_region(user_id):
    cur = conn.cursor(buffered=True)

    cur.execute("SELECT region FROM users WHERE telegram_id = %s ", (user_id,))
    conn.commit()
    r = cur.fetchone()
    print("LALALALARRRJRJRJRJRJJRJRJRJ")
    print(r)

    if r == None:
        return False
    else:
        return True


def check_province(user_id):
    cur = conn.cursor(buffered=True)

    cur.execute("SELECT province FROM users WHERE telegram_id = %s ", (user_id,))
    conn.commit()
    r = cur.fetchone()
    print("LALALALARRRJRJRJRJRJJRJRJRJ")
    print(r)

    if r[0] == None:
        return False
    else:
        return True

def get_users():
    cur = conn.cursor(buffered=True)

    cur.execute("SELECT * FROM users where region is not null order by surname, name")
    conn.commit()
    r = cur.fetchall()
    print("TUTTI GLI UTENTI")
    print(r)
    if r == None:
        return None
    else:
        return list(r)


#insert into users(name, surname, region, province, availability_update)
# values('Francesco', 'Cozza', 'PUGLIA', 'FOGGIA', date('2019-12-21'));