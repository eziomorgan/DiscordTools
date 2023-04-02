import sqlite3
from sqlite3 import Error
import datetime

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    if conn:
        return conn

def create_table(conn):
    create_table_sql = """CREATE TABLE IF NOT EXISTS interactions (
                              id INTEGER PRIMARY KEY AUTOINCREMENT,
                              channel_id TEXT NOT NULL,
                              author TEXT NOT NULL,
                              command_type TEXT NOT NULL,
                              input TEXT NOT NULL,
                              output TEXT NOT NULL,
                              timestamp DATETIME NOT NULL
                          );"""
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

# Create database and table
db_file = "bot_interactions.db"
global_conn = create_connection(db_file)
if global_conn:
    create_table(global_conn)

def log_interaction(interaction):
    global global_conn
    sql = '''INSERT INTO interactions(channel_id, author, command_type, input, output, timestamp)
             VALUES(?,?,?,?,?,?)'''
    cur = global_conn.cursor()
    cur.execute(sql, interaction)
    global_conn.commit()
    return cur.lastrowid

def get_interaction(channel_id, author, command_type, input, output):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    interaction = (channel_id, author, command_type, input, output, timestamp)
    return interaction