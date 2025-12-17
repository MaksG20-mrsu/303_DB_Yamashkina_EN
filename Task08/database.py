import sqlite3
from sqlite3 import Error

def create_connection():
    """Создание подключения к базе данных SQLite"""
    conn = None
    try:
        conn = sqlite3.connect('exam_system.db')
        conn.row_factory = sqlite3.Row
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return conn

def execute_query(conn, query, params=()):
    """Выполнение SQL запроса"""
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        return cursor.lastrowid
    except Error as e:
        print(f"The error '{e}' occurred")
        return None

def execute_read_query(conn, query, params=()):
    """Выполнение SELECT запроса"""
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")
        return []