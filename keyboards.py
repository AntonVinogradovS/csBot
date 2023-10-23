from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

firstKeyboard = ReplyKeyboardMarkup(resize_keyboard=True)\
    .add(KeyboardButton(text="🎁 Получить скин"))\
    .insert(KeyboardButton(text="🤵‍♂️ Личный кабинет"))\
    .add(KeyboardButton(text="🔪Скин от спонсора"))\
    .insert(KeyboardButton(text="🙋‍♂️Помощь"))\
#https://t.me/eatgamesleep
helpFollowerKeyboard = InlineKeyboardMarkup().add(InlineKeyboardButton(text="Ссылка на канал", url="https://t.me/eatgamesleep")).add(InlineKeyboardButton(text="✅Я подписался", callback_data="checkFollow"))
readmeKeyboard = InlineKeyboardMarkup().add(InlineKeyboardButton(text="👉 Инструкция", url="https://telegra.ph/OBYAZATELNO-K-PROCHTENIYU-10-12-3")).add(InlineKeyboardButton(text="🔧Техническая поддержка", callback_data="support"))
steamKeyboard = InlineKeyboardMarkup().add(InlineKeyboardButton(text="Узнать", url="https://steamcommunity.com/id/me/tradeoffers/privacy"))
def url(s, count):
    if count != 0:
        kb = InlineKeyboardMarkup().add(InlineKeyboardButton(text="Поделиться ссылкой", switch_inline_query=s))
        return kb



    
