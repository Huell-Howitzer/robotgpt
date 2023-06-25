# database.py
import os
import sqlite3

def init_db():
    db_path = 'sqlite.db'
    print(f"Database path: {db_path}")
    try:
        conn = sqlite3.connect(db_path)
        conn.execute('''
        CREATE TABLE IF NOT EXISTS interactions (
            id INTEGER PRIMARY KEY,
            user_input TEXT,
            chatgpt_response TEXT,
            expected_output TEXT,
            actual_output TEXT,
            similarity_score REAL,
            iteration_number INTEGER
        )
        ''')
        conn.close()
        print(f"Database created: {os.path.exists(db_path)}")
    except Exception as e:
        print(f"Error when creating database: {e}")
