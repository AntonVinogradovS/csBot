from aiogram import types, Dispatcher
from aiogram.types import CallbackQuery, MediaGroup, InputMediaDocument
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import dp, bot
from texts import *
from keyboards import * 
from database import *
import re
from config import CHANNEL_USERNAME
import random
from datetime import datetime, timedelta
import pytz 

async def cmdStart(message: types.Message):
    
    user_id = message.from_user.id
    print(user_id)

    # Проверяем, подписан ли пользователь на канал
    try:
        user_status = await bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        
        if user_status.status != 'member' and user_status.status != 'creator':
            await message.answer("Для продолжения необходимо подписаться на канал.", reply_markup=helpFollowerKeyboard)
            return
    except Exception as e:
        print(e)
        await message.answer("Не удалось проверить подписку на канал.")
        return
    #print(message.from_user.id)
    referral_token_str = message.get_args()
    if referral_token_str:
        referral_token = int(referral_token_str)
    else:
        referral_token = 0
    checkInDB = await get_user_by_id(message.from_user.id)
    if checkInDB == None:
        await add_user(user_id, referral_token, 1, 0, 0)
    # if referral_token:
    #     referred_by_user_id = get_user_id_by_referral_token(referral_token)  # Функция, которая находит пользователя, который пригласил
    #     if referred_by_user_id:
    #         # Свяжите текущего пользователя с пользователем, который пригласил
    #         link_referral_users(referred_by_user_id, message.from_user.id)
    await message.answer(text=welcomeMessage, reply_markup=firstKeyboard)

async def checkFollower(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    try:
        user_status = await bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        print(user_status.status)
        if user_status.status != 'member' and user_status.status != 'creator' :
            await callback_query.answer("Подписка не обнаружена.")
            return
    except Exception as e:
        print(e)
        await callback_query.answer("Не удалось проверить подписку на канал.")
        return
    await bot.delete_message(callback_query.message.chat.id,callback_query.message.message_id)

    with open("scken.jpg", "rb") as file:
        await bot.send_photo(chat_id=callback_query.from_user.id,photo=file, caption="✅ Отлично, отправь мне свою trade ссылку.  Узнать свою трейд ссылку можно нажав на кнопку ниже.", reply_markup=steamKeyboard)
    
    await FSMAdd.a0.set()
    

class FSMAdd(StatesGroup):
    a0 = State()

async def inputUrl(message: types.Message):
    user_id = message.from_user.id
    try:
        user_status = await bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        if user_status.status != 'member' and user_status.status != 'creator' :
            await message.answer("Для продолжения необходимо подписаться на канал.", reply_markup=helpFollowerKeyboard)
            return
    except Exception as e:
        print(e)
        await message.answer("Не удалось проверить подписку на канал.")
        return
    with open("scken.jpg", "rb") as file:
        await bot.send_photo(chat_id=message.from_user.id,photo=file, caption="✅ Отлично, отправь мне свою trade ссылку.  Узнать свою трейд ссылку можно нажав на кнопку ниже.", reply_markup=steamKeyboard)
    await FSMAdd.a0.set()

async def inputUrlCheck(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    text = message.text
    '''Вставить переадресацию в личку админу'''
    admin_id = user_id
    
    checkinfo = await get_user_by_id(user_id)
    if checkinfo[2] != 0:    
        if re.match(r'https?://', text):
            random_number = random.randint(1, 30)
            moscow_tz = pytz.timezone('Europe/Moscow')
            current_time = datetime.now(moscow_tz)
            future_time = current_time + timedelta(hours=3)
            formatted_future_time = future_time.strftime("%Y-%m-%d %H:%M:%S МСК")
            await bot.send_message(chat_id= admin_id, text= text)
            # Создание сообщения
            mess = f"✅ <b>Вы успешно заняли место в очереди\n\nВаше место: {random_number}\n⌛️ Трейд поступит приблизительно в: {formatted_future_time}. ожидайте</b>"
            await message.answer(mess, parse_mode=types.ParseMode.HTML)
            count = checkinfo[2] - 1
            ref = checkinfo[1]
            if ref != 0:
                infoRef = await get_user_by_id(ref)

                await update_friends_invited(ref, infoRef[2]+1, infoRef[4]+1)
            await update_skins_received(user_id, count, checkinfo[3]+1)
        else:
            await message.answer("Пожалуйста, отправьте действительную ссылку.")
    else:
        await message.answer("Ваша квота на получение скинов закончилась. Для получения скина, вы можете пригласить друга по реферальной ссылке.")
    await state.finish()

async def personalAccount(message: types.Message):
    id = message.from_user.id

    chekInfo = await get_user_by_id(id)
    countInvitations = chekInfo[-1]
    countScins = chekInfo[-2]
    limitScins = chekInfo[-3]
    with open("account.jpg", "rb") as file:
        await bot.send_photo(chat_id=message.from_user.id, photo=file, caption=personalAccountAnswer(countInvitations, countScins, limitScins, id), parse_mode=types.ParseMode.HTML)
    #await message.answer(text=personalAccountAnswer(countInvitations, countScins, limitScins, id), parse_mode=types.ParseMode.HTML)

async def help(message: types.Message):
    with open("help.jpg", "rb") as file:
        await bot.send_photo(chat_id= message.from_user.id, photo=file, caption=helpText, reply_markup=readmeKeyboard)
    #await message.answer(text = helpText, reply_markup=readmeKeyboard)

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(cmdStart, commands=['start'])
    dp.register_message_handler(inputUrl, text="🎁 Получить скин")
    dp.register_message_handler(inputUrlCheck, state=FSMAdd.a0, content_types=types.ContentTypes.TEXT)
    dp.register_message_handler(personalAccount, text="🤵‍♂️ Личный кабинет")
    dp.register_callback_query_handler(checkFollower, lambda c: c.data == "checkFollow")
    dp.register_message_handler(help, text = "🙋‍♂️Помощь")
