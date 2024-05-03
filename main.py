from telebot import TeleBot
from validators import *
from yacloud.speachkit import *
from yacloud.gpt import ask_gpt
import logging
from config import TOKEN, LOGS, MAX_USERS
from word_expletives import count_word_expletives, top_user_words, text_create
from db.repository import DataBase
from db.schema import TABLE_NAME_USERS, USERS_TABLE_CREATE, TABLE_NAME_MESSAGE, MESSAGE_TABLE_CREATE, TABLE_NAME_WORD_EXPLETIVES, WORD_EXPLETIVES_TABLE_CREATE

bot = TeleBot(token=TOKEN)
table_users = DataBase(TABLE_NAME_USERS, USERS_TABLE_CREATE)
table_message = DataBase(TABLE_NAME_MESSAGE, MESSAGE_TABLE_CREATE)
table_word_expletives = DataBase(TABLE_NAME_WORD_EXPLETIVES, WORD_EXPLETIVES_TABLE_CREATE)
table_users.create_table()
table_message.create_table()
table_word_expletives.create_table()


logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename=LOGS,
    filemode="w",
)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.from_user.id, "Привет! Я могу сгенерировать пост для соцсетей по словестному описанию.")


@bot.message_handler(commands=['help'])
def start(message):
    bot.send_message(message.from_user.id, "Помогатор.")


@bot.message_handler(commands=['debug'])
def debug(message):
    with open("logs.txt", "rb") as f:
        bot.send_document(message.chat.id, f)


@bot.message_handler(commands=["get_top_for_me"])
def handler_top_me(message):
    result = table_word_expletives.get_data("*", message.from_user.id)
    if not result:
        bot.send_message(chat_id=message.chat.id, text="Вы молодец, ни разу не написали слово паразит!")
        return
    result = top_user_words(result)
    text = "TOP WORDS EXPLETIVES: "
    bot.send_message(chat_id=message.chat.id, text=text_create(text, result))


@bot.message_handler(commands=["get_top"])
def handler_top_me(message):
    result = table_word_expletives.get_data("*")
    result = top_user_words(result)
    text = "TOP WORDS EXPLETIVES ALL USERS: "
    bot.send_message(chat_id=message.chat.id, text=text_create(text, result))


@bot.message_handler(commands=["stt"])
def expectation_text(message):
    result = table_users.get_data("user_id", message.from_user.id)
    if not result:
        table_users.create_user(message.from_user.id, 0, 0, 0)
    elif not is_stt_block_limit_user(message):
        logging.warning("У пользователя закончились токены")
        return
    bot.send_message(chat_id=message.chat.id, text="Отправь своё голосовое сообщение")
    bot.register_next_step_handler(message, processing_voice)


def processing_voice(message):
    if not message.voice:
        bot.send_message(chat_id=message.chat.id,
                         text="Вы отправили не голосовое сообщение! Отправьте голосовое сообщение:")
        logging.warning("Пользователь отправил не голосовое сообщение")
        bot.register_next_step_handler(message, processing_voice)
    else:
        success, amount_blocks = is_stt_block_limit(message, message.voice.duration)
        if not success:
            logging.warning("Слишком длинное голосовое сообщение")
            msg = bot.send_message(chat_id=message.chat.id, text="Поменяйте голосовое сообщение:")
            bot.register_next_step_handler(msg, processing_voice)
        else:  # получаем id голосового сообщения
            file_info = bot.get_file(message.voice.file_id)  # получаем информацию о голосовом сообщении
            file = bot.download_file(file_info.file_path)  # скачиваем голосовое сообщение
            success, text = speech_to_text(file)
            if success:
                table_users.update_data(message.from_user.id, "blocks", amount_blocks)
                bot.reply_to(message, text=text)
                bot.send_message(chat_id=message.chat.id, text="Новый запрос: /stt")
            else:
                logging.error(text)
                bot.send_message(chat_id=message.chat.id, text=text)


@bot.message_handler(commands=["start"])
def start_bot(message):
    bot.send_message(chat_id=message.chat.id,
                     text="Привет! Доступна команда:\n/tts - После написания команды, отправь боту текст и он его озвучит.")


@bot.message_handler(commands=["tts"])
def expectation_text(message):
    result = table_users.get_data("user_id", message.from_user.id)
    if not result:
        table_users.create_user(message.from_user.id, 0, 0, 0)
    elif not is_tts_symbol_limit(message, ""):
        logging.warning("У пользователя закончились токены")
        print("У пользователя закончились токены")
        pass
    bot.send_message(chat_id=message.chat.id, text="Отправь свой текст")
    bot.register_next_step_handler(message, processing_text)


def processing_text(message):
    success, len_text = is_tts_symbol_limit(message, message.text)
    if not success:
        logging.warning("Слишком длинное сообщение")
        msg = bot.send_message(chat_id=message.chat.id, text="Поменяйте текст:")
        bot.register_next_step_handler(msg, processing_text)
    else:
        success, response = text_to_speech(message.text)
        if success:
            table_users.update_data(message.from_user.id, "tokens",  len_text)
            bot.send_voice(chat_id=message.chat.id, voice=response)
            bot.send_message(chat_id=message.chat.id, text="Новый запрос: /tts")
        else:
            logging.error(response)
            bot.send_message(chat_id=message.chat.id, text="Что-то пошло не так!")


@bot.message_handler(content_types=['voice'])
def handler_voice(message):
    result_user = table_users.count_all_column("id")
    result = table_users.get_data("user_id", message.from_user.id)
    if result_user >= MAX_USERS and not result:
        logging.warning(f"Достигнут лимит пользователей {MAX_USERS}")
        bot.send_message(message.from_user.id, "Кол-во пользователей ограничено")
        return
    if not result:
        table_users.create_user(message.from_user.id, 0, 0, 0)
        print("Добавление в базу данных")
    success, amount_blocks = is_stt_block_limit(message, message.voice.duration)
    if not success:
        logging.warning("Кончились или превышены блоки")
        bot.send_message(chat_id=message.chat.id, text=amount_blocks)
    else:
        file_info = bot.get_file(message.voice.file_id)  # получаем информацию о голосовом сообщении
        file = bot.download_file(file_info.file_path)  # скачиваем голосовое сообщение
        success, text = speech_to_text(file)
        if success:
            processing_handler_voice(message, text, amount_blocks)


def processing_handler_voice(message, text, amount_blocks):
    table_users.update_data(message.from_user.id, "blocks", amount_blocks)
    table_message.add_data(message.from_user.id, "role", "message", "user", text)
    count_word_expletives(message.from_user.id, text)
    success, symbols = is_gpt_symbol_limit(message, text)
    if success:
        success, resp, tokens = ask_gpt(message.from_user.id)
        if not success:
            logging.error(resp)
            bot.send_message(chat_id=message.chat.id, text="YaGPT оффлайн")
            return
        table_message.add_data(message.from_user.id, "role", "message", "assistant", resp)
        table_users.update_data(message.from_user.id, "gpt_tokens", symbols + tokens)
        success, len_text = is_tts_symbol_limit(message, resp)
        if not success:
            logging.warning("Кончились или превышены токены")
            bot.send_message(chat_id=message.chat.id, text=len_text)
        else:
            success, response = text_to_speech(resp)
            if success:
                table_users.update_data(message.from_user.id, "tokens", len_text)
                bot.send_voice(chat_id=message.chat.id, voice=response)
            else:
                logging.error(response)
                bot.send_message(chat_id=message.chat.id, text=response)
    else:
        logging.warning("Кончились или превышены gpt-токены")
        bot.send_message(chat_id=message.chat.id, text=symbols)


@bot.message_handler(content_types=['text'])
def handler_text(message):
    result_user = table_users.count_all_column("id")
    result = table_users.get_data("user_id", message.from_user.id)
    if result_user >= MAX_USERS and not result:
        logging.warning(f"Достигнут лимит пользователей {MAX_USERS}")
        bot.send_message(message.from_user.id, "Кол-во пользователей ограничено")
        return
    if not result:
        table_users.create_user(message.from_user.id, 0, 0, 0)
    count_word_expletives(message.from_user.id, message.text)
    success, symbols = is_gpt_symbol_limit(message, message.text)
    if success:
        table_message.add_data(message.from_user.id, "role", "message", "user", message.text)
        success, resp, tokens = ask_gpt(message.from_user.id)
        if not success:
            logging.error(resp)
            bot.send_message(chat_id=message.chat.id, text="YaGPT оффлайн")
            return
        table_message.add_data(message.from_user.id, "role", "message", "assistant", resp)
        table_users.update_data(message.from_user.id, "gpt_tokens", symbols + tokens)
        bot.send_message(chat_id=message.chat.id, text=resp)
    else:
        logging.warning("Кончились или превышены gpt-токены")
        bot.send_message(chat_id=message.chat.id, text=symbols)
        bot.register_next_step_handler(message, handler_text)


@bot.message_handler(func=lambda: True)
def handler(message):
    bot.send_message(message.from_user.id, "Отправь мне голосовое или текстовое сообщение, и я тебе отвечу")


if __name__ == "__main__":
    bot.infinity_polling()
