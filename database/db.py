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
                prompt_tokens INTEGER,
                completion_tokens INTEGER,
                total_tokens INTEGER,
                response_id TEXT,
                chatgpt_finish_reason TEXT,
                chatgpt_output TEXT,
                extracted_code TEXT,
                api_response TEXT,
                created INTEGER
            )
            ''')
            conn.close()
            print(f"Database created: {os.path.exists(self.db_path)}")
        except Exception as e:
            print(f"Error when creating database: {e}")

    def save_to_db(self, user_input, expected_output, actual_output, similarity_score, prompt_tokens, completion_tokens,
                   total_tokens, response_id, chatgpt_finish_reason, chatgpt_output, extracted_code, api_response,
                   created):
        # Your implementation of saving the data to the database

        conn = sqlite3.connect(self.db_path)
        serialized_api_response = json.dumps(api_response)
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
                extracted_code,
                api_response,
                created
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
                extracted_code,
                serialized_api_response,
                created
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


