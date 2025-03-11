import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import KeyboardButton, FSInputFile, ReplyKeyboardMarkup
from aiogram import F
from api_token import TOKEN

bot = Bot(TOKEN)
dp = Dispatcher()

# Список пользователей, которые взаимодействовали с ботом
subscribed_users = set()

# Список ID администраторов
admin_ids = {7232723935}  # Замените на ID администраторов

# Список пользователей, которые активировали поддержку
support_mode_users = set()

# Состояние поддержки для каждого пользователя
user_support_state = {}

# Словарь для хранения ID пользователей, которым администратор отвечает
user_reply_map = {}

# Состояние постинга
posting_mode = False
last_uploaded_image = None

# Папка для сохранения изображений
images_folder = "uploaded_images"
if not os.path.exists(images_folder):
    os.makedirs(images_folder)

# Состояние для админа
admin_state = {}


# Команда /start
@dp.message(Command('start'))
async def start_command(message: types.Message):
    print(f"Пользователь с ID {message.from_user.id} начал взаимодействие с ботом.")
    subscribed_users.add(message.from_user.id)

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
    await message.answer_photo(my_image, caption='Здравствуйте, это бот компании Asicilene для автоматических заказов',
                               reply_markup=keyboard)


# Команда для перехода в поддержку
@dp.message(F.text.strip().lower() == '👥связаться с поддержкой в чате')
async def start_support(message: types.Message):
    # Добавляем пользователя в список тех, кто активировал поддержку
    support_mode_users.add(message.from_user.id)
    user_support_state[message.from_user.id] = True  # Устанавливаем состояние поддержки как активное

    # Создаем клавиатуру с кнопкой выхода из чата
    kb = [
        [KeyboardButton(text='⚡ Выйти из чата')]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    # Отправляем сообщение с кнопкой выхода
    await message.answer("Ваши сообщения отправляются напрямую. Чтобы вернуться в главное меню нажмите кнопку ниже",
                         reply_markup=keyboard)


# Команда выхода из чата с поддержкой
@dp.message(F.text.strip().lower() == '⚡ выйти из чата')
async def exit_support(message: types.Message):
    # Если пользователь находится в режиме поддержки, удаляем его из списка
    if message.from_user.id in support_mode_users:
        support_mode_users.remove(message.from_user.id)
        user_support_state[message.from_user.id] = False  # Убираем состояние поддержки для этого пользователя

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
    await message.answer("Вы вышли из чата с поддержкой. Если нужно, вы можете вернуться заново.",
                         reply_markup=keyboard)


# Команда /admin для администратора
@dp.message(Command('admin'))
async def admin_command(message: types.Message):
    if message.from_user.id in admin_ids:
        kb = [
            [KeyboardButton(text='Изменить каталог')],
            [KeyboardButton(text='Перейти в поддержку')],
            [KeyboardButton(text='Режим постинга')]
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer("Вы в админском меню. Выберите нужное действие:", reply_markup=keyboard)
    else:
        await message.answer("У вас нет прав для использования админского меню.")


# Команда для перехода в поддержку
@dp.message(F.text.strip().lower() == 'перейти в поддержку')
async def transition_to_support(message: types.Message):
    if message.from_user.id in admin_ids:
        admin_state[message.from_user.id] = 'waiting_for_user_id'  # Переход в режим ожидания ID
        await message.answer("Пожалуйста, отправьте ID пользователя, которому вы хотите отправить сообщение:")


# Обработчик получения ID пользователя от администратора
@dp.message(lambda message: message.from_user.id in admin_ids and admin_state.get(message.from_user.id) == 'waiting_for_user_id')
async def handle_user_id(message: types.Message):
    if message.text.isdigit():
        user_id = int(message.text)
        admin_state[message.from_user.id] = {'state': 'waiting_for_message', 'user_id': user_id}  # Переход к ожиданию текста сообщения
        await message.answer(f"ID пользователя: {user_id}. Теперь напишите текст сообщения, который вы хотите отправить этому пользователю:")
    else:
        await message.answer("Пожалуйста, введите правильный ID пользователя.")


# Обработчик получения сообщения от администратора
@dp.message(lambda message: message.from_user.id in admin_ids and admin_state.get(message.from_user.id, {}).get(
    'state') == 'waiting_for_message')
async def handle_message_text(message: types.Message):
    user_id = admin_state[message.from_user.id].get('user_id')
    if user_id:
        text = message.text
        try:
            # Отправляем сообщение пользователю
            await bot.send_message(user_id, text)
            await message.answer("Сообщение было успешно отправлено пользователю.")
        except Exception as e:
            await message.answer(f"Не удалось отправить сообщение пользователю. Ошибка: {e}")

        # Завершаем режим
        del admin_state[message.from_user.id]
    else:
        await message.answer("Произошла ошибка. Попробуйте снова.")


# Режим постинга
@dp.message(F.text.strip().lower() == 'режим постинга')
async def posting_mode_command(message: types.Message):
    if message.from_user.id in admin_ids:
        global posting_mode
        posting_mode = True
        await message.answer(
            "Вы перешли в режим постинга. Напишите сообщение, которое хотите отправить всем пользователям. "
            "Вы можете также отправить изображение вместе с текстом.")


# Обработчик изображений в режиме постинга
@dp.message(lambda message: message.photo and posting_mode and message.from_user.id in admin_ids)
async def handle_image(message: types.Message):
    global last_uploaded_image

    # Сохраняем изображение локально с оригинальным именем
    file_id = message.photo[-1].file_id  # Получаем последний размер изображения (самый лучший)
    file = await bot.get_file(file_id)
    file_path = file.file_path

    # Получаем имя файла из пути
    file_name = file_path.split('/')[-1]
    image_path = os.path.join(images_folder, file_name)

    # Загружаем изображение
    await bot.download_file(file_path, image_path)

    last_uploaded_image = image_path  # Сохраняем путь к последнему загруженному изображению

    await message.answer(f"Изображение сохранено как {file_name}. Теперь отправьте текст для постинга.")


# Обработчик текстовых сообщений в режиме постинга
@dp.message(lambda message: message.text and posting_mode and message.from_user.id in admin_ids)
async def handle_posting_message(message: types.Message):
    global posting_mode
    global last_uploaded_image

    if posting_mode:
        text = message.text

        if last_uploaded_image:  # Если изображение было загружено
            # Отправляем фото с текстом всем пользователям
            for user_id in subscribed_users:
                try:
                    await bot.send_photo(user_id, FSInputFile(last_uploaded_image), caption=text)
                except Exception as e:
                    print(f"Ошибка при отправке сообщения пользователю {user_id}: {e}")

            # Удаляем изображение после отправки
            os.remove(last_uploaded_image)

        else:
            # Если изображения нет, отправляем только текст
            for user_id in subscribed_users:
                try:
                    await bot.send_message(user_id, text)
                except Exception as e:
                    print(f"Ошибка при отправке сообщения пользователю {user_id}: {e}")

        # Окончание режима постинга
        posting_mode = False
        last_uploaded_image = None  # Сбрасываем путь к изображению
        await message.answer("Сообщение было отправлено всем пользователям.")


# Обработчик сообщений, отправленных пользователями, когда они в чате поддержки
@dp.message(lambda message: user_support_state.get(message.from_user.id, False))
async def handle_support_message(message: types.Message):
    # Пересылаем все сообщения в поддержку администратору
    for admin_id in admin_ids:
        try:
            # Сохраняем информацию о пользователе, отправившем сообщение
            user_reply_map[message.message_id] = message.from_user.id
            await bot.forward_message(admin_id, message.from_user.id, message.message_id)
            # Отправляем администратору только ID пользователя в HTML формате
            await bot.send_message(admin_id, f"<code>{message.from_user.id}</code>", parse_mode='HTML')
        except Exception as e:
            print(f"Ошибка при пересылке сообщения администратору {admin_id}: {e}")


# Основная функция для запуска бота
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
