import sqlite3
def get_connection():
    con = sqlite3.connect('main.db')
    return con
def start_sheet():
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS users(
        userid INT PRIMARY KEY,
        question INT,
        coordinate STR
        );''')
def create_user(user_id):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(f"""SELECT * FROM users WHERE userid = {user_id};""")
        result = cur.fetchone()
        if result:
            return 1
        else:
            cur.execute(f"""INSERT INTO users VALUES(?,?,?);""", (user_id,0,'0 0'))
def db_start_quiz(user_id):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(f"""UPDATE users SET question = 0, coordinate = '0 0' WHERE userid = {user_id};""")
def get_current_position(id):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(f"""SELECT coordinate FROM users WHERE userid = {id};""")
        cord = cur.fetchone()
        return cord[0]
def get_current_question(id):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(f"""SELECT question FROM users WHERE userid = {id};""")
        question = cur.fetchone()
        return question[0]
def change_position(id,coordinates):
    cord = coordinates.split()
    x = int(cord[0])
    y = int(cord[1])
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(f"""SELECT coordinate FROM users WHERE userid = {id}""")
        cords = cur.fetchone()[0].split()
    x = int(cords[0])+x
    if x > 10:
        x = 10
    elif x < -10:
        x = -10
    y = int(cords[1])+y
    if y > 10:
        y = 10
    elif y < -10:
        y = -10
    cords = str(x) + ' ' + str(y)
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(f"""UPDATE users SET coordinate = '{cords}' WHERE userid = {id};""")
def go_to_next_question(id):
    q = get_current_question(id)
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(f"""UPDATE users SET question = {q+1} WHERE userid = {id};""")
def give_results(id):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(f"""SELECT * FROM users WHERE userid = {id};""")
        ans = cur.fetchone()
    return(ans)