import os
from dotenv import load_dotenv


load_dotenv()

TOKEN = os.getenv('TOKEN')
FOLDER_ID = os.getenv('FOLDER_ID')
IAM_TOKEN_PATH = "iam_token.txt"

MAX_USER_STT_BLOCKS = 10
MAX_STT_DURATION = 30
MAX_USER_TTS_SYMBOLS = 2000
MAX_TTS_SYMBOLS = 500
MAX_MODEL_TOKEN = 50
MAX_USERS = 5
MAX_TOKENS_USER_GPT = 100
MAX_TOKENS_USER_GPT_ALL = 1000


URL_TTS = 'https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize'
VOICE = 'filipp'

LOGS = "log_file.txt"

expletives = ['типа', 'как бы', 'итак', 'короче', 'таки', 'ну', 'вот', 'честно', 'грубо', 'мягко', 'собственно говоря', 'на самом деле', 'в общем', 'прикинь', 'это самое', 'например', 'допустим', 'как говорится', 'в принципе', 'так сказать', 'прямо', 'да', 'э-э', 'кстати', 'слушай', 'понимаешь', 'так вот', 'ну-у', 'конкретно', 'а-а', 'м-м', 'и-и', 'то есть']
