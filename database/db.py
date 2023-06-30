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
                created INTEGER,
                api_created INTEGER,
                api_model TEXT
            )
            ''')
            conn.close()
            print(f"Database created: {os.path.exists(self.db_path)}")
        except Exception as e:
            print(f"Error when creating database: {e}")

    def save_to_db(self, user_input, expected_output, actual_output, similarity_score, prompt_tokens, completion_tokens,
                   total_tokens, response_id, chatgpt_finish_reason, chatgpt_output, extracted_code, api_response,
                   created):
        conn = sqlite3.connect(self.db_path)
        serialized_api_response = json.dumps(api_response)

        api_created = api_response['created']
        api_model = api_response['model']

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
                created,
                api_created,
                api_model
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
                created,
                api_created,
                api_model
            )
        )
        conn.commit()
        conn.close()



