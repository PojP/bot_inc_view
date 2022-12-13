import asyncio
import config 
import os
import time
from pyrogram import Client
from rich.console import Console
from random import randint
console =Console()

reactions=["👍","❤️","🔥","🥰","👏"]

async def like(data, number):
    line=data[0]
    proxy=None
    if data[1]!=None:
        proxy=data[1].split(":")
        proxy = {
         "scheme": "socks5",  # "socks4", "socks5" and "http" are supported
         "hostname": proxy[0],
         "port": int(proxy[1]),
         "username": proxy[2],
         "password": proxy[3]
        }
    try:
        console.print(f"[blue] Попытка войти в аккаунт {line}\n Прокси: {proxy}")
        async with Client(f"{config.folder}my_acc", session_string=line, proxy=proxy) as app:
            console.print("[green] Попытка успешна!")
            history=app.get_chat_history(config.chat)
            last_id=0
            if os.path.isfile(f"id_{number}.txt"):
                with open(file=f"id_{number}.txt", mode="r") as file:
                    last_id =file.readline()
                    if last_id!="":
                        last_id=int(last_id)
                    else:
                        last_id=0
            with open(file=f"id_{number}.txt", mode="w+") as file:
                async for msg in history:
                    file.write(str(msg.id))
                    console.print(f"id последнего поста: {msg.id}")
                    break
            try:
                console.print("Просматриваем всю историю...")
                await app.read_chat_history(config.chat)
            except:
                console.print("Не получилось:(")
            
            async for message in app.get_chat_history(config.chat):
                msg_id=message.id
                if msg_id<=last_id:
                    console.print(f"[green] Посты кончились")
                    break
                if msg_id==1:
                    break
                try:
                    text=""
                    try:
                        text=message.text[0:30]
                    except:
                        text="Отсутствует"
                        console.print("Заголовок отсутсвует")
                    finally:
                        console.print(f"[blue]попытка лайкнуть {msg_id} пост сверху\n\n Заголовок: {text}...")
                        await app.send_reaction(config.chat,message.id, emoji=reactions[randint(0,4)])
                        console.print("[blue]Жмем на кнопку...")
                        try:
                            await message.click()
                        except:
                            console.print("[blue]Нет кнопки, чтобы лайкнуть")
                        finally:
                            continue

                except:
                    console.print_exception()
                    console.print(f"[red]Не удалось лайкнуть {msg_id} пост сверху:(")
                finally:
                    continue
    except:
        console.print_exception()
        console.print("[red]!!!ОШИБКА!!! Не получилось войти в аккаунт")
async def main():
    console.print("[bold green]Привет. Выбери нужный номер, чтобы я что-то сделала:")
    console.print("[blue]1 - добавить аккаунты")
    console.print("[blue]2-запустить программу с уже добавленными аккаунтами")
    try:
        a = int(console.input("[purple]Введи число: "))
    except:
        console.print("[red]!!!ОШИБКА!!! Нужно ввести число")
    if a ==2:
        proxies=[]
        with open("proxies.txt", mode="w+") as file:
            proxies=file.readlines()
        
        with open("sessions.txt", mode="r+") as file:
            session=file.readlines()
            if len(proxies)==0:
                count_acc=len(session)
            else:
                count_acc=len(session)%len(proxies)
            loop = asyncio.get_event_loop()
            tasks = []
            data_full=[]
            counter=0
            curr_proxy_id=0
            for i in session:
                if counter==count_acc:
                    curr_proxy_id+=1
                if curr_proxy_id==len(proxies)-1:
                    curr_proxy_id-=1
                data_full.append([i.rstrip(),None])
                counter+=1

            for line in data_full:
                tasks.append(loop.create_task(like(line,data_full.index(line))))
            START_TIME= time.time()
            await asyncio.wait(tasks)
            ALL_TIME=round(time.time()-START_TIME)
            minutes=ALL_TIME//60
            console.print(f"[bold green]ГОТОВО! Время исполнения {minutes} мин. {ALL_TIME-minutes*60} сек.")
    elif a==1:
        console.print("[bold green]Чтобы продолжать добавлять аккаунты, жмите Enter.\n Чтобы закончить - жмите или 'n' или 'н'")
        while True:
            async with Client(f"{config.folder}my_acc",config.api_id, config.api_hash, in_memory=True) as app:
                with open("sessions.txt", mode="a+") as file:
                    session=await app.export_session_string()
                    file.write(f"{session}\n")              
            en=console.input("[purple]Добавить еще?")
            if en == 'n' or en == "н":
                break
os.system("cls")
asyncio.run(main())
