from filters import IsAdmin, IsUser
import os
import handlers
from aiogram import executor, types
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove
from data import config
from loader import dp, db, bot
import filters
import logging
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands

filters.setup(dp)

WEBAPP_HOST = "0.0.0.0"
WEBAPP_PORT = int(os.environ.get("PORT", 5000))
user_message = '🙎‍♂️ User'
admin_message = '👨‍🔧 admin'

catalog = '🛍️ mahsulot'
balance = '💰 Balans'
cart = '🛒 Savatcha'
delivery_status = '🚚 zakas holati'

settings = '⚙️ kategoria sozlash'
orders = '🚚 Zakaz'
questions = '❓ Savol'


@dp.message_handler(commands='start', user_id = config.ADMINS)
async def cmd_start(message: types.Message):

    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    markup.row(admin_message, user_message)

    await message.answer(f"👋 Assalomu alaykum {message.from_user.full_name}! 🤖 Men sizning botingizman\nMeni admin rejimida sozlashni unutmang!", reply_markup=markup)


@dp.message_handler(IsUser(), commands='start')
async def user_menu(message: types.Message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(catalog)
    markup.add(balance, cart)
    markup.add(delivery_status)

    await message.answer('''Assalomu alaykum! 👋

🤖 Men har qanday toifadagi tovarlarni etkazib beradigan bot-do'konman.
    
🛍️ Katalogga o'tish va o'zingizga yoqqan mahsulotlarni tanlash uchun buyruqdan foydalaning /menu.

❓ Savollaringiz bormi? Muammo emas! /sos buyrug'i sizga imkon qadar tezroq javob berishga harakat qiladigan administratorlar bilan bog'lanishga yordam beradi.

    ''', reply_markup=markup, disable_web_page_preview=True)


@dp.message_handler(IsAdmin(), text=user_message)
async def user_mode(message: types.Message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(catalog)
    markup.add(balance, cart)
    markup.add(delivery_status)
    
    cid = message.chat.id
    if cid in config.ADMINS:
        config.ADMINS.remove(cid)

    # await message.answer('Включен пользовательский режим.', reply_markup=ReplyKeyboardRemove())

    await message.answer('Foydalanuvchi rejimi yoqilgan.', reply_markup=markup)

@dp.message_handler(text=admin_message, user_id = config.ADMINS)
async def admin_mode(message: types.Message):

    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(settings)
    markup.add(questions, orders)
    markup.add(user_message)

    cid = message.chat.id
    if cid not in config.ADMINS:
        config.ADMINS.append(cid)

    # await message.answer('Включен админский режим.', reply_markup=ReplyKeyboardRemove())

    await message.answer('Admin rejimi yoqilgan.', reply_markup=markup)


async def on_startup(dp):
    # Birlamchi komandalar (/start va /help)
    await set_default_commands(dp)

    logging.basicConfig(level=logging.INFO)
    db.create_tables()

    # Bot ishga tushgani haqida adminga xabar berish
    await on_startup_notify(dp)

    await bot.delete_webhook()
    await bot.set_webhook(config.WEBHOOK_URL)


async def on_shutdown():
    logging.warning("Shutting down..")
    await bot.delete_webhook()
    await dp.storage.close()
    await dp.storage.wait_closed()
    logging.warning("Bot down")


if __name__ == '__main__':

    if "HEROKU" in list(os.environ.keys()):

        executor.start_webhook(
            dispatcher=dp,
            webhook_path=config.WEBHOOK_PATH,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            skip_updates=True,
            host=WEBAPP_HOST,
            port=WEBAPP_PORT,
        )

    else:

        executor.start_polling(dp, on_startup=on_startup, skip_updates=False)
