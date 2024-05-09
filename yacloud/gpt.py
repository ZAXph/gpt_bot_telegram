import logging
import requests
from config import FOLDER_ID, LOGS, MAX_MODEL_TOKEN
from db.schema import TABLE_NAME_MESSAGE, MESSAGE_TABLE_CREATE
from db.repository import DataBase
from creds import get_creds


logging.basicConfig(filename=LOGS, level=logging.ERROR,
                    format="%(asctime)s FILE: %(filename)s IN: %(funcName)s MESSAGE: %(message)s", filemode="w")

table_message = DataBase(TABLE_NAME_MESSAGE, MESSAGE_TABLE_CREATE)


def prompt_create(user_id):
    message = table_message.last_message("role, message", user_id)
    promt = []
    for msg in message:
        promt.append({"role": msg[0], "text": msg[1]})
    return promt


# подсчитываем количество токенов в сообщениях
def count_gpt_tokens(messages):
    IAM_TOKEN = get_creds()
    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/tokenizeCompletion"
    headers = {
        'Authorization': f'Bearer {IAM_TOKEN}',
        'Content-Type': 'application/json'
    }
    data = {
        'modelUri': f"gpt://{FOLDER_ID}/yandexgpt-lite",
        "messages": messages
    }
    try:
        return len(requests.post(url=url, json=data, headers=headers).json()['tokens'])
    except Exception as e:
        logging.error(e)  # если ошибка - записываем её в логи
        return 0


# запрос к GPT
def ask_gpt(user_id):
    IAM_TOKEN = get_creds()
    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        'Authorization': f'Bearer {IAM_TOKEN}',
        'Content-Type': 'application/json'
    }
    data = {
        'modelUri': f"gpt://{FOLDER_ID}/yandexgpt-lite",
        "completionOptions": {
            "stream": False,
            "temperature": 0.7,
            "maxTokens": MAX_MODEL_TOKEN
        },
        "messages": prompt_create(user_id)
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        # проверяем статус код
        if response.status_code != 200:
            return False, f"Ошибка GPT. Статус-код: {response.status_code}", None
        # если всё успешно - считаем количество токенов, потраченных на ответ, возвращаем статус, ответ, и количество токенов в ответе
        answer = response.json()['result']['alternatives'][0]['message']['text']
        tokens_in_answer = count_gpt_tokens([{'role': 'assistant', 'text': answer}])
        return True, answer, tokens_in_answer
    except Exception as e:
        logging.error(e)  # если ошибка - записываем её в логи
        return False, "Ошибка при обращении к GPT",  None
