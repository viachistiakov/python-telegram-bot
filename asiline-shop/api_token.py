TOKEN='8187659834:AAHf9PJd-Mbh7AWLiRWp3gCFTLYOXCfCrTM'





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