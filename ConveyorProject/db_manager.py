import sqlite3
from datetime import datetime, timedelta

def create_db():
    conn = sqlite3.connect('result.db')
    cursor = conn.cursor()

    # Create product table
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS product (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        datetime TEXT,
        uuid TEXT UNIQUE,
        is_defective INTEGER,
        defect_reason TEXT
    )
    '''
    cursor.execute(create_table_query)
    conn.commit()


def insert_data(datetime_value, uuid_value, is_defective, defect_reason=None):
    conn = sqlite3.connect('result.db')
    cursor = conn.cursor()
    insert_query = '''
    INSERT INTO product (datetime, uuid, is_defective, defect_reason)
    VALUES (?, ?, ?, ?)
    '''
    cursor.execute(insert_query, (datetime_value, uuid_value, is_defective, defect_reason))
    conn.commit()

def check_db():
    conn = sqlite3.connect('result.db')
    cursor = conn.cursor()

    now = datetime.now()
    twelve_hours_ago = now - timedelta(hours=240)

    twelve_hours_ago_str = twelve_hours_ago.strftime("%Y-%m-%d %H:%M:%S")

    query = '''
    SELECT * FROM product
    WHERE datetime >= ?
    '''

    cursor.execute(query, (twelve_hours_ago_str,))
    results = cursor.fetchall()

    for row in results:
        print(row)

    conn.close()

# check_db()