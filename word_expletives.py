from config import expletives, LOGS
from db.schema import TABLE_NAME_WORD_EXPLETIVES, WORD_EXPLETIVES_TABLE_CREATE
from db.repository import DataBase
from string import punctuation
import logging

table_word_expletives = DataBase(TABLE_NAME_WORD_EXPLETIVES, WORD_EXPLETIVES_TABLE_CREATE)

logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename=LOGS,
    filemode="w",
)


def count_word_expletives(user_id, text):
    text = text.lower().translate(str.maketrans('', '', punctuation))
    for word in expletives:
        count = text.count(word)
        if count != 0:
            table_word_expletives.add_data(user_id, "word", "count", word, count)


def top_user_words(values):
    words = {}
    for i in values:
        if i[1] in words.values():
            words[i[1]] += i[2]
        else:
            words[i[1]] = i[2]
    result = {}
    try:
        for i in range(5):
            key = max(words, key=words.get)
            result[key] = words[key]
            del words[key]
        return result
    except ValueError:
        logging.warning("У пользователя нету 5 разных слов паразитов")
        return result


def text_create(text, result):
    for key in result:
        text += f"\n{key} - {result[key]}"
    return text
