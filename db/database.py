import sqlite3
import pandas as pd

def get_connection():
    return sqlite3.connect('db/investment_dashboard.db')

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS trading212_cash (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fetched_at TEXT,
            free REAL,
            total REAL,
            ppl REAL,
            result REAL,
            invested REAL,
            pieCash REAL,
            blocked REAL
        )
    """)
    conn.commit()
    conn.close()


def insert_account_cash(data):
    conn = get_connection()
    cursor = conn.cursor()
    cash_info = data.get('data', {})
    meta = data.get('meta', {})
    cursor.execute("""
        INSERT INTO trading212_cash (fetched_at, free, total, ppl, result, invested, pieCash, blocked)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        meta.get('fetched_at'),
        cash_info.get('free'),
        cash_info.get('total'),
        cash_info.get('ppl'),
        cash_info.get('result'),
        cash_info.get('invested'),
        cash_info.get('pieCash'),
        cash_info.get('blocked')
    ))
    conn.commit()
    conn.close()


def fetch_all_cash_records():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM trading212_cash")
    rows = cursor.fetchall()
    conn.close()
    return rows

def drop_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS trading212_cash")
    conn.commit()
    conn.close()
    print("Table dropped successfully.")

def fetch_data():
    conn = sqlite3.connect('db/investment_dashboard.db')
    query = "SELECT fetched_at, invested, total FROM trading212_cash"
    df = pd.read_sql_query(query, conn)
    df['fetched_at'] = pd.to_datetime(df['fetched_at'])
    conn.close()
    return df

if __name__ == "__main__":
    drop_table()
    create_tables()
    print("Tables created successfully.")
    
    print(fetch_all_cash_records())