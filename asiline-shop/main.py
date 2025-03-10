import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import KeyboardButton, FSInputFile, ReplyKeyboardMarkup
from api_token import TOKEN
from aiogram import F

bot = Bot(TOKEN)
dp = Dispatcher()


images = [
    ("🔴 Красное изображение", '1 (1).jpg'),
    ("🟠 Оранжевое изображение", '1 (2).jpg'),
    ("🟡 Желтое изображение", '1 (3).jpg'),
    ("🟢 Зеленое изображение", '1 (4).jpg'),
    ("🔵 Синее изображение", '1 (5).jpg')
]

# Храним id пользователя, которому нужно пересылать сообщения
support_user_id = 7232723935  # Замените на ID пользователя @angry_mf

# Список пользователей, которые активировали поддержку
support_mode_users = set()

@dp.message(Command('zakaz'))
async def zakaz_command(message: types.Message, command: Command):
    if command.args is None:
        await message.answer('Пожалуйста сообщите: Адрес заказа, Время и дату, Номер заказчика')
        return
    try:
        name1, age, city = command.args.split(' ')
    except ValueError:
        await message.answer('Введены не все данные. Пример ввода:\n /zakaz Вишняковская2а 13:30 88005553535')
        return
    await message.answer(f'Адрес заказа: {name1}\n'
                         f'Время заказа: {age}\n'
                         f'Номер телефона: {city}\n')









@dp.message(Command('start'))
async def start_command(message: types.Message):
    kb = [
        [KeyboardButton(text='🚨Купить')],
        [KeyboardButton(text='🌱Каталог')],
        [KeyboardButton(text='📦История покупок')],
        [KeyboardButton(text='👥Связаться с поддержкой в чате')],
        [KeyboardButton(text='📱Контакты')]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb,
                                         is_persistent=True,
                                         resize_keyboard=True,
                                         one_time_keyboard=False,
                                         input_field_placeholder='Вы в главном меню')
    my_image = FSInputFile('torf.jpg')

    # Отправка текста с картинкой
    await message.answer_photo(my_image, caption=
        'Здравствуйте, это бот компании Asicilene для автоматических заказов',
        reply_markup=keyboard)


@dp.message(F.text.strip().lower() == '👥связаться с поддержкой в чате')
async def start_support(message: types.Message):
    # Добавляем пользователя в список тех, кто активировал поддержку
    support_mode_users.add(message.from_user.id)

    # Создаем клавиатуру с кнопкой выхода из чата
    kb = [
        [KeyboardButton(text='⚡ Выйти из чата')]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    # Отправляем сообщение с кнопкой выхода
    await message.answer("Ваши сообщения отправляются напрямую. Чтобы вернуться в главное меню нажмите кнопку ниже", reply_markup=keyboard)


@dp.message(F.text.strip().lower() == '⚡ выйти из чата')
async def exit_support(message: types.Message):
    # Если пользователь находится в режиме поддержки, удаляем его из списка
    if message.from_user.id in support_mode_users:
        support_mode_users.remove(message.from_user.id)

    # Возвращаем пользователя в главное меню
    kb = [
        [KeyboardButton(text='🚨Купить')],
        [KeyboardButton(text='🌱Каталог')],
        [KeyboardButton(text='📦История покупок')],
        [KeyboardButton(text='👥Связаться с поддержкой в чате')],
        [KeyboardButton(text='📱Контакты')]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb,
                                         is_persistent=True,
                                         resize_keyboard=True,
                                         one_time_keyboard=False,
                                         input_field_placeholder='Вы в главном меню')
    await message.answer("Вы вышли из чата с поддержкой. Если нужно, вы можете вернуться заново.", reply_markup=keyboard)


@dp.message(F.text.strip().lower() == '📱контакты')
async def with_puree(message: types.Message):
    phone_number = "+7 968 438-45-13"
    # Используем моноширинный шрифт с HTML
    await message.answer(f'Звонок поставщику:  <code>{phone_number}</code>', parse_mode='HTML')


@dp.message()
async def forward_to_support(message: types.Message):
    # Если пользователь в режиме поддержки, перенаправляем все его сообщения
    if message.from_user.id in support_mode_users:
        await bot.forward_message(chat_id=support_user_id, from_chat_id=message.chat.id, message_id=message.message_id)
    else:
        # Можно добавить логику для обычных сообщений
        pass



async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
