import os
import sqlite3

class Database:
    def __init__(self):
        self.db_path = 'sqlite.db'

    def init_db(self):
        print(f"Database path: {self.db_path}")
        try:
            conn = sqlite3.connect(self.db_path)
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
            print(f"Database created: {os.path.exists(self.db_path)}")
        except Exception as e:
            print(f"Error when creating database: {e}")

    def save_to_db(self, user_input, chatgpt_response, expected_output, actual_output, similarity_score, iteration_number):
        conn = sqlite3.connect(self.db_path)
        conn.execute('''
        INSERT INTO interactions (user_input, chatgpt_response, expected_output, actual_output, similarity_score, iteration_number)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_input, chatgpt_response, expected_output, actual_output, similarity_score, iteration_number))
        conn.commit()
        conn.close()

    def get_last_interaction(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.execute('SELECT * FROM interactions ORDER BY id DESC LIMIT 1')
        result = cursor.fetchone()
        conn.close()
        return result

    def update_db(self, id, chatgpt_response, actual_output, similarity_score):
        conn = sqlite3.connect(self.db_path)
        conn.execute('''
        UPDATE interactions
        SET chatgpt_response = ?, actual_output = ?, similarity_score = ?
        WHERE id = ?
        ''', (chatgpt_response, actual_output, similarity_score, id))
        conn.commit()
        conn.close()
