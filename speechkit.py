import requests
import os
import math
from dotenv import load_dotenv
from database import tokens_add_stt, tokens_user_stt, tokens_user, tokens_add, message_add

load_dotenv()


# Функция генерация голосовых сообщений по тексту
async def speech_to_text(voice):
    params = "&".join([
        "topic=general",
        f"folderId={os.getenv('folder_id')}",
        "lang=ru-RU"
    ])

    headers = {
        'Authorization': f'Bearer {os.getenv('iam_token')}',
    }

    response = requests.post(f"{os.getenv('URL')}{params}",
                             headers=headers,
                             data=voice
                             )

    decoded_data = response.json()
    if decoded_data.get("error_code") is None:
        return decoded_data.get("result")
    else:
        return "При запросе в SpeechKit возникла ошибка"


# Функция для контроля аудио-блоков и длительности голосового сообщения
async def is_stt_block_limit(user_id, duration):
    audio_blocks = math.ceil(duration / 15)
    stt_user = tokens_user_stt()
    result_stt = await stt_user.stt_symbols_user(user_id)
    await stt_user.close()
    if duration >= 30:
        return "Превышено длительность голосового сообщения"
    if result_stt >= 6:
        return f"Превышен лимит для пользователя"
    all_blocks = result_stt + audio_blocks
    voice_control_add_user = tokens_add_stt()
    await voice_control_add_user.add_stt_symbols(all_blocks, user_id)
    await voice_control_add_user.close()


# Функция для подсчета символов и запись в базу данных, также запись текста
async def stt_symbols_db(user_id, text):
    info_db_tokens1 = tokens_user()
    tokens_db1 = await info_db_tokens1.tts_symbols_user(user_id)
    result = tokens_db1 + len(text)
    await info_db_tokens1.close()

    save_tokens = tokens_add()
    await save_tokens.add_tts_symbols(result, user_id)
    await save_tokens.close()

    save_text = message_add()
    await save_text.add_text(text, user_id)
    await save_text.close()
