from aiogram import Dispatcher, types
from init_bot import bot
from keyboards import none_kb, keyboard_cl_edit_interests, keyboard_cl_settings, keyboard_cl_settings_age, keyboard_cl_settings_gender
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from backend import check_link, check_admin

from .core import start_command,DeleteChannels,DeleteTasks,stop,AddChannel,AddChannels,AddTask,AddTasks,AddToChannels,AppendState,ViewIncrementState,DeleteState

"""
#REGISTRATION
#funcs to import 
from .registration import start_register
#objects
from .registration import gender
from .registration import interests
from .registration import ClientRegistrationState, EditState
"""

#Basic func
async def start_bot(message : types.Message):
    user_id=message.from_user.id
    await bot.send_message(user_id, "Привет! Это бот для управления программой для накрутки просмотров!\n\n\n"+
    "Напиши /add_channels для добавления каналов, в которые нужно добавить бота\n\n"+
    "Напиши /delete_channels для очистки списка каналов, в которые нужно добавить бота\n\n"+
    "Напиши /add_tasks для добавления задач накрутки(После этой команды следует пересылать либо конкретное сообщение с канала, либо просто ссылку на канал, если надо просмотреть его весь)\n\n"+
    "Напиши /delete_tasks для очистки списка задач\n\n"+
    "Напиши /stop для того, чтобы закончить добавление задач/каналов\n\n"+
    "Напиши /join_chat для добавления всех пользовательских аккаунтов в созданный вами список каналов\n\n"+
    "Напиши /start_view для того, чтобы ВКЛЮЧИТЬ НАКРУТКУ\n\n")

async def start_viewing(message: types.Message, state: FSMContext):
    await start_command(message, state,"run")
async def join_to_chats(message: types.Message, state: FSMContext):
    await start_command(message, state, "")

def register_handlers(dp : Dispatcher):
    #basic commands
    #dp.register_message_handler(add_channel, lambda msg: check_admin(msg.from_user.id) and check_link(msg.text))
    #basic commands
    #dp.register_message_handler(cancel, lambda msg: msg.text.lower() in ["cancel","/cancel", "cancel 🚫"],state="*")
    dp.register_message_handler(start_bot, commands=["start", "help"],state=None)
    dp.register_message_handler(AddChannels, commands=["add_channels"],state=None)
    dp.register_message_handler(AddTasks, commands=["add_tasks"],state=None)
    dp.register_message_handler(AddChannel,lambda msg: "t.me/" in msg.text,state=AppendState.append_chats)
    dp.register_message_handler(AddTask,lambda msg: "t.me/" in msg.text,state=AppendState.append_tasks)
    dp.register_message_handler(DeleteChannels,commands=["delete_channels"],state=None)
    dp.register_message_handler(DeleteTasks, commands=["delete_tasks"],state=None)
    dp.register_message_handler(stop, commands=["stop"],state=[AppendState.append_chats,AppendState.append_tasks, ViewIncrementState.is_working])
    dp.register_message_handler(join_to_chats, commands=["join_chat"],state=None)
    dp.register_message_handler(start_viewing, commands=["start_view"],state=None)
    #dp.register_message_handler(edit_interests,,state=IsAuthorized.is_auth)
