import asyncio


@dp.message(Command("enableposting") & F.from_user.id.in_(admin_ids))
async def enable_posting(message: types.Message):
    chat_data = dp.chat_data.setdefault(message.chat.id, {})
    chat_data['posting_mode'] = True
    await message.reply("Режим постинга включен!")

#Пример команды для выключения режима posting (добавьте, если еще нет)
@dp.message(Command("disableposting") & F.from_user.id.in_(admin_ids))
async def disable_posting(message: types.Message):
    chat_data = dp.chat_data.setdefault(message.chat.id, {})
    chat_data['posting_mode'] = False
    await message.reply("Режим постинга выключен!")


# Пример обработчика для загрузки изображений (добавьте, если еще нет)
@dp.message(F.photo & F.from_user.id.in_(admin_ids))
async def handle_image_upload(message: types.Message):
    chat_data = dp.chat_data.setdefault(message.chat.id, {})

    file_id = message.photo[-1].file_id  # Берем самое большое разрешение фото
    file = await bot.get_file(file_id)
    file_path = file.file_path
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import KeyboardButton, FSInputFile, ReplyKeyboardMarkup
from api_token import TOKEN
from aiogram import F
import main
bot = Bot(TOKEN)
dp = Dispatcher()

@dp.message(F.text.strip().lower() == '🌱каталог')
async def exit_support(message: types.Message):
    # Если пользователь находится в режиме поддержки, удаляем его из списка

    # Возвращаем пользователя в главное меню
    kb = [
        [KeyboardButton(text='🔴 товар')],
        [KeyboardButton(text='🔵 товар')],
        [KeyboardButton(text='🟢 товар')],
        [KeyboardButton(text='🟡 товар')],
        [KeyboardButton(text='🟠 това')]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb,
                                         is_persistent=True,
                                         resize_keyboard=True,
                                         one_time_keyboard=False,
                                         input_field_placeholder='Вы в главном меню')
    await message.answer("Вы вышли из чата с поддержкой. Если нужно, вы можете вернуться заново.", reply_markup=keyboard)