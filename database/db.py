import os
import sqlite3
from flask import json

class Database:
    def __init__(self):
        self.db_path = 'sqlite.db'
        self.init_db()

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
                iteration_number INTEGER,
                created INTEGER,
                prompt_tokens INTEGER,  # Add this line
                completion_tokens INTEGER,  # Add this line
                total_tokens INTEGER,  # Add this line
                response_id TEXT,  # Add this line
                chatgpt_finish_reason TEXT,  # Add this line
                chatgpt_output TEXT,  # Add this line
                api_response TEXT  # Add this line
            )
            ''')
            conn.close()
            print(f"Database created: {os.path.exists(self.db_path)}")
        except Exception as e:
            print(f"Error when creating database: {e}")


    def save_to_db(
        self,
        user_input,
        expected_output,
        actual_output,
        similarity_score,
        prompt_tokens,
        completion_tokens,
        total_tokens,
        response_id,
        chatgpt_finish_reason,
        chatgpt_output,
        api_response
    ):
        conn = sqlite3.connect(self.db_path)
        conn.execute(
            '''
            INSERT INTO interactions (
                user_input,
                expected_output,
                actual_output,
                similarity_score,
                prompt_tokens,
                completion_tokens,
                total_tokens,
                response_id,
                chatgpt_finish_reason,
                chatgpt_output,
                api_response,
                created
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''',
            (
                user_input,
                expected_output,
                actual_output,
                similarity_score,
                prompt_tokens,
                completion_tokens,
                total_tokens,
                response_id,
                chatgpt_finish_reason,
                chatgpt_output,
                json.dumps(api_response),
                api_response['created']
            )
        )
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
