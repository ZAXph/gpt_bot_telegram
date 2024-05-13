from config import MAX_USER_STT_BLOCKS, MAX_STT_DURATION, MAX_USER_TTS_SYMBOLS, MAX_TTS_SYMBOLS, \
     MAX_TOKENS_USER_GPT, MAX_TOKENS_USER_GPT_ALL
from math import ceil
from db.repository import DataBase
from yacloud.gpt import count_gpt_tokens
from db.schema import USERS_TABLE_CREATE, TABLE_NAME_USERS

table_users = DataBase(TABLE_NAME_USERS, USERS_TABLE_CREATE)


def is_stt_block_limit(message, duration):
    # Переводим секунды в аудиоблоки
    audio_blocks = ceil(duration / 15)
    # округляем в большую сторону
    # Функция из БД для подсчёта всех потраченных пользователем аудиоблоков
    all_blocks = table_users.get_data("blocks", message.from_user.id)[0][0] + audio_blocks

    # Проверяем, что аудио длится меньше 30 секунд
    if duration >= MAX_STT_DURATION:
        msg = "SpeechKit STT работает с голосовыми сообщениями меньше 30 секунд"
        return False, msg

    # Сравниваем all_blocks с количеством доступных пользователю аудиоблоков
    if all_blocks > MAX_USER_STT_BLOCKS:
        msg = f"Превышен общий лимит SpeechKit STT {MAX_USER_STT_BLOCKS}. Использовано {all_blocks} блоков. Доступно: {MAX_USER_STT_BLOCKS - all_blocks + audio_blocks}"
        return False, msg

    return True, audio_blocks


def is_tts_symbol_limit(message, text):
    text_symbols = len(text)

    # Функция из БД для подсчёта всех потраченных пользователем символов
    all_symbols = table_users.get_data("tokens", message.from_user.id)[0][0] + text_symbols

    # Сравниваем all_symbols с количеством доступных пользователю символов
    if all_symbols > MAX_USER_TTS_SYMBOLS:
        msg = f"Превышен общий лимит SpeechKit TTS {MAX_USER_TTS_SYMBOLS}. Использовано: {all_symbols - text_symbols} токенов. Доступно: {MAX_USER_TTS_SYMBOLS - all_symbols + text_symbols}"
        return False, msg

    # Сравниваем количество символов в тексте с максимальным количеством символов в тексте
    if text_symbols >= MAX_TTS_SYMBOLS:
        msg = f"Превышен лимит SpeechKit TTS на запрос {MAX_TTS_SYMBOLS}, в сообщении {text_symbols} токенов"
        return False, msg

    return True, text_symbols


def is_gpt_symbol_limit(message, text):
    text_symbols = count_gpt_tokens([{'role': 'user', 'text': text}])

    # Функция из БД для подсчёта всех потраченных пользователем символов
    all_symbols = table_users.get_data("gpt_tokens", message.from_user.id)[0][0] + text_symbols
    # Сравниваем all_symbols с количеством доступных пользователю символов
    if all_symbols >= MAX_TOKENS_USER_GPT_ALL:
        msg = f"Превышен общий лимит YaGPT {MAX_TOKENS_USER_GPT_ALL}. Использовано: {all_symbols - text_symbols} символов. Доступно: {MAX_TOKENS_USER_GPT_ALL - all_symbols + text_symbols}"
        return False, msg

    # Сравниваем количество символов в тексте с максимальным количеством символов в тексте
    if text_symbols >= MAX_TOKENS_USER_GPT:
        msg = f"Превышен лимит YaGPT на запрос {MAX_TOKENS_USER_GPT}, в сообщении {text_symbols} символов"
        return False, msg

    return True, text_symbols


def is_stt_block_limit_user(message):
    all_blocks = table_users.get_data("blocks", message.from_user.id)[0][0]
    if all_blocks == MAX_USER_STT_BLOCKS:
        msg = f"Превышен общий лимит SpeechKit TTS {MAX_USER_STT_BLOCKS}. Использовано: {all_blocks} блоков. Доступно: {MAX_USER_STT_BLOCKS - all_blocks}"
        return False, msg
    return True, None
