import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command,CommandObject
from aiohttp.web_routedef import delete

from api_token import TOKEN


bot= Bot(TOKEN)
dp = Dispatcher()

TEXT= '''
/start - запуск бота
/help - справочный текст
'''
@dp.message(Command('zakaz'))
async def start_command(message: types.Message, command: CommandObject):
    if command.args is None:
        await message.answer('Пожалуйста сообщите: Адрес заказа, Время и дату,Номер заказчика')
        return
    try:
        name1, age, city = command.args.split(' ')
    except ValueError:
        await message.answer('Введены не все данные. Пример ввода:\n /zakaz Вишняковская2а 13:30 88005553535')
    await message.answer(f'Адрес заказа: {name1}\n'
                         f'Время заказа: {age}\n'
                         f'Номер телефона: {city}\n')
@dp.message(Command('start'))
async def start_command(message: types.Message):
    await message.answer('ты опоздал')

@dp.message(Command('help'))
async def help_command(message: types.Message):
    await message.reply(TOKEN)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
