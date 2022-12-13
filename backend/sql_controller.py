import sqlite3
import config

conn = sqlite3.connect("config/tasks.db")
cur = conn.cursor()

def init_database():
    cur.execute("""CREATE TABLE IF NOT EXISTS tasks_t(
        taskid INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        type_inc TEXT,
        f_message INT);
        """)
    conn.commit()
    #cur.execute("""CREATE TABLE IF NOT EXISTS search(
   #userid INT PRIMARY KEY,
   #interest TEXT);
    #""")
    #conn.commit()
    #cur.execute(f"DELETE FROM search;")
    #conn.commit()
def update(id : str, data_to_append : str, data : str):
    cur.execute(f"UPDATE tasks_t SET {data} = '{data_to_append}' WHERE taskid={id};")
    conn.commit()
def add_task(data : tuple[str,int]):
    cur.execute("INSERT INTO tasks_t (type_inc,f_message) VALUES(?, ?);", data)
    conn.commit()
def check_task(id : str):
    cur.execute(f"SELECT * FROM tasks_t WHERE taskid={id}")
    #print(cur.fetchone())
    if cur.fetchone()==None:
        return False
    return True
def get_task(id : str):
    cur.execute(f"SELECT * FROM tasks_t WHERE taskid={id}")
    return cur.fetchone()

def check_link(link: str):
    if "t.me/" in link:
        return True
    return False
def check_admin(id: int):
    if id == config.user_id:
        return True
    return False
def del_task(id: int):
    cur.execute(f"DELETE FROM tasks_t WHERE userid='{id}';")
    conn.commit()
def get_tasks():
    cur.execute(f"SELECT * FROM tasks_t")
    return cur.fetchmany()
def del_tasks():
    cur.execute(f"DELETE FROM tasks_t")
    conn.commit()
def check_user_search(id : str):
    cur.execute(f"SELECT * FROM search WHERE userid={id}")
    #print(cur.fetchone())
    if cur.fetchone()==None:
        return False
    return True
def add_user_to_search(data : tuple[int,str]):
    cur.execute("INSERT INTO search VALUES(?, ?);", data)
    conn.commit()
