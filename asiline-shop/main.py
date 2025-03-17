import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import KeyboardButton, FSInputFile, ReplyKeyboardMarkup
from aiogram import F
from api_token import TOKEN

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
    await message.answer_photo(my_image, caption='Здравствуйте, это бот компании ATLANTIS для автоматических заказов',
                               reply_markup=keyboard)

images = [
    ("🔴 Красное изображение", '1 (1).jpg'),
    ("🟠 Оранжевое изображение", '1 (2).jpg'),
    ("🟡 Желтое изображение", '1 (3).jpg'),
    ("🟢 Зеленое изображение", '1 (4).jpg'),
    ("🔵 Синее изображение", '1 (5).jpg')
]

@dp.message(F.text.strip().lower() == '🌱каталог')
async def show_catalog(message: types.Message):
    # Возвращаем пользователя в каталог
    kb = [
        [KeyboardButton(text='🔴 Красное изображение')],
        [KeyboardButton(text='🟠 Оранжевое изображение')],
        [KeyboardButton(text='🟡 Желтое изображение')],
        [KeyboardButton(text='🟢 Зеленое изображение')],
        [KeyboardButton(text='🔵 Синее изображение')]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb,
                                         is_persistent=True,
                                         resize_keyboard=True,
                                         one_time_keyboard=False,
                                         input_field_placeholder='Каталог')
    await message.answer("Выберите изображение из каталога:", reply_markup=keyboard)


@dp.message(F.text.strip().lower() == '🔴 красное изображение')
async def send_red_image(message: types.Message):
    with open('1 (1).jpg', 'rb') as img:
        await message.answer_photo(img, caption="🔴 Красное изображение")


@dp.message(F.text.strip().lower() == '🟠 оранжевое изображение')
async def send_orange_image(message: types.Message):
    with open('1 (2).jpg', 'rb') as img:
        await message.answer_photo(img, caption="🟠 Оранжевое изображение")


@dp.message(F.text.strip().lower() == '🟡 желтое изображение')
async def send_yellow_image(message: types.Message):
    with open('1 (3).jpg', 'rb') as img:
        await message.answer_photo(img, caption="🟡 Желтое изображение")


@dp.message(F.text.strip().lower() == '🟢 зеленое изображение')
async def send_green_image(message: types.Message):
    with open('1 (4).jpg', 'rb') as img:
        await message.answer_photo(img, caption="🟢 Зеленое изображение")


@dp.message(F.text.strip().lower() == '🔵 синее изображение')
async def send_blue_image(message: types.Message):
    with open('1 (5).jpg', 'rb') as img:
        await message.answer_photo(img, caption="🔵 Синее изображение")



@dp.message(F.text.strip().lower() == '📱контакты')
async def with_puree(message: types.Message):
     phone_number = "+7 968 438-45-13"
     # Используем моноширинный шрифт с HTML
     await message.answer(f'Звонок поставщику:  <code>{phone_number}</code>', parse_mode='HTML')
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
@from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import FSInputFile
import os

# Предполагается, что у вас уже есть bot, dp, admin_ids, subscribed_users

# Вместо global posting_mode и last_uploaded_image используем данные чата
@dp.message(lambda message: message.text and message.from_user.id in admin_ids)
async def handle_posting_message(message: types.Message, bot: Bot):
    chat_data = dp.chat_data.setdefault(message.chat.id, {}) # Получаем или создаем данные чата
    posting_mode = chat_data.get('posting_mode', False) # Получаем режим публикации (по умолчанию False)
    last_uploaded_image = chat_data.get('last_uploaded_image', None) # Получаем последнее загруженное фото (по умолчанию None)

    if not posting_mode:
        await message.reply("Режим публикации не активен.  Используйте команду /enableposting.")
        return #Прекращаем выполнение, если режим не активен

    text = message.text

    if last_uploaded_image:  # Если изображение было загружено
        # Отправляем фото с текстом всем пользователям
        for user_id in subscribed_users:
            try:
                await bot.send_photo(user_id, FSInputFile(last_uploaded_image), caption=text)
            except Exception as e:
                print(f"Ошибка при отправке сообщения пользователю {user_id}: {e}")

        # Удаляем изображение после отправки
        try:
            os.remove(last_uploaded_image)
        except Exception as e:
            print(f"Ошибка при удалении файла {last_uploaded_image}: {e}")

        # Очищаем last_uploaded_image в данных чата
        chat_data['last_uploaded_image'] = None

    else:
        # Если изображения нет, отправляем только текст
        for user_id in subscribed_users:
            try:
                await bot.send_message(user_id, text)
            except Exception as e:
                print(f"Ошибка при отправке сообщения пользователю {user_id}: {e}")


#Пример команды для включения режима posting (добавьте, если еще нет)
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
    destination_path = f"image_{message.message_id}.jpg"  # Уникальное имя

    await bot.download_file(file_path, destination_path)
    chat_data['last_uploaded_image'] = destination_path # Сохраняем путь к файлу

    await message.reply("Изображение загружено и готово к отправке.")ge.text)
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
