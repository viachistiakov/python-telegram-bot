import asyncio
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