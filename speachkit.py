import requests
from config import VOICE, IAM_TOKEN, FOLDER_ID, URL_TTS


def speech_to_text(data):
    # Указываем параметры запроса
    params = "&".join([
        "topic=general",  # используем основную версию модели
        f"folderId={FOLDER_ID}",
        "lang=ru-RU"  # распознаём голосовое сообщение на русском языке
    ])

    # Аутентификация через IAM-токен
    headers = {
        'Authorization': f'Bearer {IAM_TOKEN}',
    }

     # Выполняем запрос
    response = requests.post(
    f"https://stt.api.cloud.yandex.net/speech/v1/stt:recognize?{params}",
        headers=headers,
        data=data
    )

    # Читаем json в словарь
    decoded_data = response.json()
    # Проверяем, не произошла ли ошибка при запросе
    if decoded_data.get("error_code") is None and decoded_data.get("result"):
        return True, decoded_data.get("result")  # Возвращаем статус и текст из аудио
    else:
        return False, "При запросе в SpeechKit возникла ошибка. Возможно вы отправили пустое сообщение"


def text_to_speech(text_user):
    headers = {'Authorization': f"Bearer {IAM_TOKEN}"}
    data = {'text': text_user,  # текст, который нужно преобразовать в голосовое сообщение
            'lang': 'ru-RU',  # язык текста - русский
            'voice': VOICE,  # мужской голос Филиппа
            'folderId': FOLDER_ID, }

    response_tts = requests.post(
        URL_TTS,
        headers=headers,
        data=data
    )
    if response_tts.status_code == 200:
        return True, response_tts.content
    return False, "При запросе в SpeechKit возникла ошибка"
