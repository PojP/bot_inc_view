from aiogram import types
from init_bot import bot
from keyboards import none_kb
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from backend import add_task, del_tasks, get_tasks, add_task
import asyncio
import aiofiles
#import time
#import rich
from pyrogram import Client, errors
import pyrogram.raw.functions as raw_f
import pyrogram.raw.types as raw_t
from config import config





async def show_all_tasks():
    pass
async def show_all_channels():
    pass
async def check_task():
    pass
async def check_channel(): 
    pass

async def start_viewing_hardware(data, u_message: types.Message):
    line=data[0]
    proxy=None
    if data[1]!=None:
        proxy=data[1].split(":")
        proxy = {
         "scheme": config.proxy_type,
         "hostname": proxy[0],
         "port": int(proxy[1]),
         "username": proxy[2],
         "password": proxy[3]
        }
    try:
        channels = get_tasks()        
        for ch in channels:
            print(f" Попытка войти в аккаунт {line}\n Прокси: {proxy}")
            async with Client(f"{config.folder}my_acc", session_string=line, proxy=proxy, ipv6=config.ipv6) as app:
                try: 
                    channel = await app.get_chat(ch[1])
                except Exception as e:
                    return print(e)
                print("успешно!")
                try:
                    if ch[2]==-1:
                        async for message in app.get_chat_history(channel.id):
                            views=await app.invoke(
                                raw_f.messages.GetMessagesViews(peer=await app.resolve_peer(channel.id),id=[message.id],increment=True)
                            )
                        print("VIEWS::    {}".format(views))
                    else:
                        message=app.get_messages(ch[1],ch[2])
                        views=await app.invoke(
                             raw_f.messages.GetMessagesViews(peer=await app.resolve_peer(channel.id),id=[message.id],increment=True)
                        )
                            #print("VIEWS::    {}".format(views))
                except:
                    await bot.send_message(u_message.from_user.id,"Аккаунт не смог просмотреть канал")
                    return 0
    except Exception as e:
        await bot.send_message(u_message.from_user.id," Не вышло войти в канал")
        print(e)

#States
class AppendState(StatesGroup):
    append_chats= State()
    append_tasks= State()
class DeleteState(StatesGroup):
    delete_chats= State()
    delete_tasks= State()
class ViewIncrementState(StatesGroup):
    is_working  = State()
    is_idle     = State()

g_tasks=[]
###MAIN FUNC###
async def start_command(message: types.Message,state: FSMContext, cmd: str):
    proxies=[]
    async with aiofiles.open("config/proxies.txt", mode="r+") as file:
        #print(file.readlines())
        #proxies==await file.readlines()
        async for i in file:
            proxies.append(i)
    print(proxies)
    async with aiofiles.open("config/sessions.txt", mode="r+") as file:
        session=[]
        async for sess in file:
            session.append(sess)
        print(session)
        proxy_id=(len(session))//10
        if len(proxies)<proxy_id:
            print("Недостаточно прокси: имеется {0} штуки, но должно быть минимум {1}".format(len(proxies),proxy_id))
        else:
            loop = asyncio.get_event_loop()
            tasks = []
            counter=0
            for i in session:
                counter+=1
                if cmd=="run":
                    tasks.append(loop.create_task(start_viewing_hardware([i.rstrip(),proxies[counter//10]], message)))
                    
                else:
                    tasks.append(loop.create_task(AddToChannels([i.rstrip(),proxies[counter//10]])))
            if cmd=="run":
                global g_tasks
                g_tasks=tasks
                await state.set_state(ViewIncrementState.is_working)
                runner(tasks, state)
            else:
                await asyncio.wait(tasks)
            await bot.send_message(message.from_user.id, "Готово, запустилось {} аккаунтов".format(counter))
async def runner(tasks, state):
    if await state.get_state()==ViewIncrementState.is_working:
        await asyncio.wait(tasks)
        await asyncio.sleep(12*60*60)
        await runner(tasks,state)
#
async def AddToChannels(data):
    line=data[0]
    proxy=None
    if data[1]!=None:
        proxy=data[1].split(":")
        proxy = {
         "scheme": config.proxy_type,
         "hostname": proxy[0],
         "port": int(proxy[1]),
         "username": proxy[2],
         "password": proxy[3]
        }
    try:
        while True:
            async with aiofiles.open("config/channels.txt","r", encoding="utf-8") as fileee:
                async for ch in fileee:
                    print(f" Попытка войти в аккаунт {line}\n Прокси: {proxy}")
                    async with Client(f"{config.folder}my_acc", session_string=line, proxy=proxy, ipv6=config.ipv6) as app:
                        try: 
                            print(ch)
                            channel = await app.join_chat(ch)
                            print(channel)  
                        except errors.exceptions.bad_request_400.UserAlreadyParticipant as e:
                                return print("user already added")
                        except errors.BadRequest as e:
                            print(e)
            await asyncio.sleep(12*60*60)
            
    except Exception as e:
        print(e)
async def AddChannels(message: types.Message,state : FSMContext):
    await state.set_state(AppendState.append_chats)
    await bot.send_message(message.from_user.id, "Отправляйте ссылки на каналы!")
async def AddChannel(message: types.Message):
    async with aiofiles.open("config/channels.txt", "a+", encoding="utf-8") as file:
        try:
            await file.write(message.text+"\n")
        except Exception as e:
            print(e)
    await bot.send_message(message.from_user.id, "Добавлено!")
    
async def AddTasks(message: types.Message,state : FSMContext):
    await state.set_state(AppendState.append_tasks)
    await bot.send_message(message.from_user.id, "Отправляйте ссылки на каналы или пересылайте посты оттуда для накрутки конктретного поста!")
async def AddTask(message: types.Message):
    if message.is_forward():
        add_task((message.forward_from, message.forward_from_message_id))
    else:
        if "t.me/" in message.text:
            add_task((message.text,-1))
    await bot.send_message(message.from_user.id, "Добавлено!")
async def DeleteTasks(message: types.Message,):
    del_tasks()
    await bot.send_message(message.from_user.id, "Удалено!")
async def DeleteChannels(message: types.Message,):
    async with aiofiles.open("config/channels.txt", "w",encoding="utf-8") as file:
        await file.write("")
    await bot.send_message(message.from_user.id, "Удалено!")
async def stop(message: types.Message,state: FSMContext):
    if await state.get_state()==ViewIncrementState.is_working:
        global g_tasks
        for i in g_tasks:
            i.cancel()
    await state.reset_state()
    await bot.send_message(message.from_user.id, "Завершено:)")
async def help_cmd(chat_id: str):
    await bot.send_message(chat_id,"")

