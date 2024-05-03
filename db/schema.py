DB_NAME = 'data_base.db'

TABLE_NAME_USERS = 'users'
USERS_TABLE_CREATE = f"""CREATE TABLE IF NOT EXISTS {TABLE_NAME_USERS} (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            gpt_tokens INTEGER,
            tokens INTEGER,
            blocks INTEGER
        );"""

TABLE_NAME_MESSAGE = 'message'
MESSAGE_TABLE_CREATE = f"""CREATE TABLE IF NOT EXISTS {TABLE_NAME_MESSAGE} (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            role TEXT,
            message TEXT,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        );"""


TABLE_NAME_WORD_EXPLETIVES = 'word_expletives'
WORD_EXPLETIVES_TABLE_CREATE = f"""CREATE TABLE IF NOT EXISTS {TABLE_NAME_WORD_EXPLETIVES} (
            user_id INTEGER,
            word TEXT,
            count INTEGER,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        );"""
