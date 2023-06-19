
from aiogram.types import Message, ReplyKeyboardMarkup
from loader import dp
from filters import IsUser

catalog = '🛍️ mahsulot'
balance = '💰 Balans'
cart = '🛒 Savatcha'
delivery_status = '🚚 zakas holati'

settings = '⚙️ kategoria sozlash'
orders = '🚚 Zakaz'
questions = '❓ Savol'



@dp.message_handler(IsUser(), commands="menu")
async def is_user_menu(message: Message):    
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(catalog)
    markup.add(balance, cart)
    markup.add(delivery_status)

    await message.answer('menu', reply_markup=markup)