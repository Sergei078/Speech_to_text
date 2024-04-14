from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile, ReplyKeyboardMarkup, ReplyKeyboardRemove
from dotenv import load_dotenv
import os
from FSM import FSMFillForm
from speechkit import is_stt_block_limit, stt_symbols_db, speech_to_text
from button import menu_kb
from database import tokens_user, Database, tokens_user_stt
import logging
from bot_token import bot

load_dotenv()

logging.basicConfig(filename=os.getenv('file_error'), level=logging.ERROR, filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')

router = Router()


@router.message(Command('log'))
async def logging_info(message: Message):
    file = FSInputFile(os.getenv('file_error'))
    await message.answer_document(file)


@router.message(CommandStart())
async def start(message: Message):
    keyboard = ReplyKeyboardMarkup(keyboard=menu_kb, resize_keyboard=True)
    db_user = Database()
    try:
        if not await db_user.check_user_exists(message.chat.id):
            await db_user.add_user(message.chat.id)
        await message.answer(f'<b>Привет, {message.chat.first_name}👋\n\n</b>'
                             '<i>🗣Я могу распознать гс\n'
                             'который ты мне запишешь.\n\n</i>',
                             parse_mode='html', reply_markup=keyboard)
    except Exception as e:
        logging.error(str(e))


@router.message(F.text == 'Распознать голосовое')
async def text_input(message: Message, state: FSMContext):
    await state.set_state(FSMFillForm.voice_message)
    await message.answer('Запиши голосовое', reply_markup=ReplyKeyboardRemove())


@router.message(FSMFillForm.voice_message)
async def voice_message_handler(message: Message, state: FSMContext):
    await state.update_data(voice=message.voice.file_id)
    data = await state.get_data()
    file_info = await bot.get_file(data['voice'])
    file = await bot.download_file(file_info.file_path)
    with open(os.getenv('file'), 'wb') as f:
        f.write(file.read())
    duration_user = message.voice.duration
    user_id = message.chat.id
    result_info = await is_stt_block_limit(user_id=user_id, duration=duration_user)
    keyboard = ReplyKeyboardMarkup(keyboard=menu_kb, resize_keyboard=True)
    if result_info == 'Превышено длительность голосового сообщения' or result_info == 'Превышен лимит для пользователя':
        await message.answer(result_info, reply_markup=keyboard)
    else:
        with open(os.getenv('file'), 'rb') as audio_file:
            audio_data = audio_file.read()
        voice_speechkit = await speech_to_text(audio_data)
        await stt_symbols_db(user_id, voice_speechkit)
        await message.answer(f'<i>*{voice_speechkit}.*</i>', parse_mode='html', reply_markup=keyboard)
    await state.clear()


@router.message(F.text == 'Баланс💳')
async def balance(message: Message):
    try:
        user_id = message.chat.id
        info_db_tokens = tokens_user()
        tokens_db = await info_db_tokens.tts_symbols_user(user_id)
        await info_db_tokens.close()
        stt_user = tokens_user_stt()
        result_stt = await stt_user.stt_symbols_user(user_id)
        await stt_user.close()
        await message.answer(f'<b>Количество потраченных символов:</b> {tokens_db}\n\n'
                             f'<b>Потрачено аудио-блоков:</b> {result_stt} из 6', parse_mode='html')
    except Exception as e:
        logging.error(str(e))
