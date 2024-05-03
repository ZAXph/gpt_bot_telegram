IAM_TOKEN = "t1.9euelZqXz5nPzc6Mj5Sdm86aj4-amu3rnpWamMyalJebnZOKxsyVypOajJTl9PdGDTJO-e9PUD-23fT3BjwvTvnvT1A_ts3n9euelZqLnpjGlZWVksmdz4vPyZHMi-_8xeuelZqLnpjGlZWVksmdz4vPyZHMi73rnpWayJXGlomOnMeazZGJyo-Riou13oac0ZyQko-Ki5rRi5nSnJCSj4qLmtKSmouem56LntKMng.JRKSxe6rHPaJdzoRjYcVbOZiQi1pASOu3G_IMtPtR1MGlnIKlgOAY4K4VTSGuVVahegATfrhAXkS0_hdgGfbBA"
FOLDER_ID = "b1gn1kghpq4rvsp4e2h1"

MAX_USER_STT_BLOCKS = 10
MAX_STT_DURATION = 30
MAX_USER_TTS_SYMBOLS = 2000
MAX_TTS_SYMBOLS = 500
MAX_MODEL_TOKEN = 50
MAX_USERS = 5
MAX_TOKENS_USER_GPT = 100
MAX_TOKENS_USER_GPT_ALL = 1000

TOKEN = "6815594086:AAFmwexlJBjfNt8xinJKVhUz2613ND2opX0"

URL_TTS = 'https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize'
VOICE = 'filipp'

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

LOGS = "log_file.txt"


expletives = ['типа', 'как бы', 'итак', 'короче', 'таки', 'ну', 'вот', 'честно', 'грубо', 'мягко', 'собственно говоря', 'на самом деле', 'в общем', 'прикинь', 'это самое', 'например', 'допустим', 'как говорится', 'в принципе', 'так сказать', 'прямо', 'да', 'э-э', 'кстати', 'слушай', 'понимаешь', 'так вот', 'ну-у', 'конкретно', 'а-а', 'м-м', 'и-и', 'то есть']
